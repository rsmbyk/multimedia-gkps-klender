"""A checkout made on Windows holds LF shell scripts (spec 216, FR-002).

Git for Windows checks text files out with CRLF by default, so a Windows clone put a CRLF
``docker/entrypoint.sh`` into the build context. The repository now pins ``*.sh`` to LF, which is the
half of the fix that stops the file being written wrong in the first place; the half that makes the
container start regardless of what the checkout holds — the runtime entrypoint living outside the
mounted tree, and its strip — moved with the strip's target and is guarded by
``tests/test_runtime_entrypoint.py`` (spec 217).
"""

import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class CheckoutLineEndingTests(unittest.TestCase):
    def test_shell_scripts_are_pinned_to_lf_and_powershell_is_not(self):
        """`git check-attr` is the answer the checkout depends on — not the file's text."""
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