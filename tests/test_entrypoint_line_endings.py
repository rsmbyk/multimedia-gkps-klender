"""The image starts from a checkout made on any platform (spec 216, FR-001..FR-003).

Git for Windows checks text files out with CRLF by default and the repository pinned nothing, so a
Windows clone put a CRLF ``docker/entrypoint.sh`` into the build context. Measured inside the real
``media`` container, that file exits 2 at ``set -e`` (``set: Illegal option -``), and the restart
policy turns the crash into a loop. Two guards: the image strips ``\\r`` before it makes the file
executable, and the repository pins ``*.sh`` to LF so the CRLF copy is not produced in the first
place.

The strip is exercised as the command the Dockerfile writes, applied to a CRLF copy laid out at the
same path inside a temporary directory — not as a line in a file: what matters is that ``/bin/sh``
runs the result.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCKERFILE = REPO_ROOT / 'Dockerfile'
ENTRYPOINT = REPO_ROOT / 'docker' / 'entrypoint.sh'

STRIP_PATTERN = re.compile(r'^RUN\s+sed\s+-i\s+\'s/\\r\$//\'\s+docker/entrypoint\.sh\s*$')


def dockerfile_lines():
    return DOCKERFILE.read_text().splitlines()


def strip_command():
    """The strip as the Dockerfile writes it, so the test cannot pass on a different command."""
    for line in dockerfile_lines():
        if STRIP_PATTERN.match(line):
            return line[len('RUN '):].strip()
    raise AssertionError('the Dockerfile carries no CR strip for docker/entrypoint.sh')


class EntrypointLineEndingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.copy = self.root / 'docker' / 'entrypoint.sh'
        self.copy.parent.mkdir()
        self.copy.write_bytes(ENTRYPOINT.read_bytes().replace(b'\n', b'\r\n'))

    def run_entrypoint(self):
        return subprocess.run(
            ['/bin/sh', 'docker/entrypoint.sh', 'sh', '-c', 'printf reached'],
            cwd=str(self.root), capture_output=True, text=True, timeout=60)

    def run_strip(self):
        subprocess.run(['/bin/sh', '-c', strip_command()], cwd=str(self.root), check=True)

    def test_a_crlf_entrypoint_fails_before_the_strip(self):
        """The fixture reproduces the report, so the next test proves the strip and not something else.

        The message is the shell's own and differs between ``dash`` (``Illegal option -``, which the
        image prints) and ``bash`` (``invalid option``, which a Linux host's ``/bin/sh`` prints), so
        the assertion is the behaviour: it stops on ``set`` before reaching the command.
        """
        result = self.run_entrypoint()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertIn('set', result.stderr)

    def test_a_crlf_entrypoint_runs_after_the_build_strip(self):
        self.run_strip()
        self.assertNotIn(b'\r', self.copy.read_bytes())
        result = self.run_entrypoint()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, 'reached')

    def test_the_strip_leaves_a_lf_entrypoint_untouched(self):
        self.copy.write_bytes(ENTRYPOINT.read_bytes())
        before = self.copy.read_bytes()
        self.run_strip()
        self.assertEqual(self.copy.read_bytes(), before)

    def test_the_strip_sits_between_the_copy_and_the_chmod(self):
        lines = dockerfile_lines()
        copied = [index for index, line in enumerate(lines) if line.strip() == 'COPY . .']
        stripped = [index for index, line in enumerate(lines) if STRIP_PATTERN.match(line)]
        chmod = [index for index, line in enumerate(lines)
                 if line.strip() == 'RUN chmod +x docker/entrypoint.sh']
        self.assertEqual(len(copied), 1, 'the Dockerfile no longer copies the build context once')
        self.assertEqual(len(stripped), 1, 'the Dockerfile carries no CR strip')
        self.assertEqual(len(chmod), 1, 'the Dockerfile no longer makes the entrypoint executable')
        self.assertLess(copied[0], stripped[0], 'the strip runs before the context is copied')
        self.assertLess(stripped[0], chmod[0], 'the strip runs after the file is made executable')


class CheckoutLineEndingTests(unittest.TestCase):
    def test_shell_scripts_are_pinned_to_lf_and_powershell_is_not(self):
        result = subprocess.run(
            ['git', 'check-attr', 'eol', '--',
             'docker/entrypoint.sh', 'docker/up.sh', 'docker/up.ps1'],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60, check=True)
        attributes = {}
        for line in result.stdout.splitlines():
            path, _attribute, value = line.split(': ')
            attributes[path] = value
        self.assertEqual(attributes['docker/entrypoint.sh'], 'lf')
        self.assertEqual(attributes['docker/up.sh'], 'lf')
        self.assertEqual(attributes['docker/up.ps1'], 'unspecified')
