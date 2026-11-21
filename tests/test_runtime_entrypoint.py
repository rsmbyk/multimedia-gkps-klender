"""The container starts from an entrypoint no mount can replace (spec 217, FR-001..FR-004).

Spec 216 stripped ``docker/entrypoint.sh`` inside the image, but the ``web`` service mounts the
checkout over ``/app`` (``docker-compose.yml``), so the file that runs is the host's — still CRLF on a
Windows machine, and still refused by ``/bin/sh`` at ``set -e``. Measured on the built image: without
the mount it exits 0, with the checkout mounted it exits 2.

The guards here are about *where* the runtime entrypoint lives: outside ``/app``, stripped there, and
the only path ``ENTRYPOINT`` names. The strip is exercised as the command the Dockerfile writes,
applied to a CRLF copy in a temporary root — the absolute target redirected into it, because what
matters is that ``/bin/sh`` runs the result.

``tests/test_entrypoint_line_endings.py`` keeps the checkout-side guards (the ``*.sh`` LF pin and the
context's own file); this module owns the runtime path.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCKERFILE = REPO_ROOT / 'Dockerfile'
ENTRYPOINT = REPO_ROOT / 'docker' / 'entrypoint.sh'

COPY_PATTERN = re.compile(r'^COPY\s+docker/entrypoint\.sh\s+(?P<target>/\S+)\s*$')
STRIP_PATTERN = re.compile(
    r'^RUN\s+sed\s+-i\s+\'s/\\r\$//\'\s+(?P<target>/\S+)\s+&&\s+chmod\s+\+x\s+(?P=target)\s*$')
ENTRYPOINT_PATTERN = re.compile(r'^ENTRYPOINT\s+\[(?P<parts>.*)\]\s*$')

# The directory the local stack mounts the checkout over. Nothing the container needs to start may
# live inside it.
MOUNTED_TREE = '/app/'


def dockerfile_lines():
    return DOCKERFILE.read_text().splitlines()


def single(pattern, description):
    matches = [pattern.match(line) for line in dockerfile_lines()]
    found = [(index, match) for index, match in enumerate(matches) if match]
    assert len(found) == 1, f'the Dockerfile must carry exactly one {description}'
    return found[0]


def runtime_path():
    """The path the image copies its entrypoint to, as the Dockerfile writes it."""
    return single(COPY_PATTERN, 'COPY of docker/entrypoint.sh to a runtime path')[1].group('target')


def strip_command():
    return single(STRIP_PATTERN, 'RUN that strips and marks executable the runtime entrypoint')[1].string[len('RUN '):]


class RuntimeEntrypointPathTests(unittest.TestCase):
    def test_the_runtime_entrypoint_lives_outside_the_mounted_tree(self):
        """`web` mounts the checkout over /app, so a path inside it is the host's file again."""
        path = runtime_path()
        self.assertFalse(path.startswith(MOUNTED_TREE),
                         f'{path} sits inside {MOUNTED_TREE}, which the web service mounts from the host')
        self.assertEqual(single(STRIP_PATTERN, 'strip of the runtime entrypoint')[1].group('target'), path,
                         'the strip must clean the copy the ENTRYPOINT runs')

    def test_the_image_starts_from_that_path_and_no_other(self):
        entrypoint = single(ENTRYPOINT_PATTERN, 'ENTRYPOINT line')[1].group('parts')
        named = re.findall(r'"([^"]+)"', entrypoint)
        self.assertIn(runtime_path(), named, 'the ENTRYPOINT does not name the copied entrypoint')
        self.assertEqual([part for part in named if part.startswith('/') and part != '/bin/sh'],
                         [runtime_path()], 'the ENTRYPOINT names another absolute path as well')


class RuntimeEntrypointStripTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / 'gkps-entrypoint.sh'
        self.target.write_bytes(ENTRYPOINT.read_bytes().replace(b'\n', b'\r\n'))

    def run_entrypoint(self):
        return subprocess.run(
            ['/bin/sh', str(self.target), 'sh', '-c', 'printf reached'],
            cwd=str(self.root), capture_output=True, text=True, timeout=60)

    def test_the_copied_entrypoint_fails_before_the_strip(self):
        result = self.run_entrypoint()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('set', result.stderr)

    def test_the_copied_entrypoint_runs_after_the_strip(self):
        command = strip_command().replace(runtime_path(), str(self.target))
        subprocess.run(['/bin/sh', '-c', command], cwd=str(self.root), check=True)
        self.assertNotIn(b'\r', self.target.read_bytes())
        result = self.run_entrypoint()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'reached')

    def test_the_strip_leaves_an_lf_entrypoint_untouched(self):
        self.target.write_bytes(ENTRYPOINT.read_bytes())
        before = self.target.read_bytes()
        command = strip_command().replace(runtime_path(), str(self.target))
        subprocess.run(['/bin/sh', '-c', command], cwd=str(self.root), check=True)
        self.assertEqual(self.target.read_bytes(), before)