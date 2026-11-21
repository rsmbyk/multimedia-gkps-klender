"""The launchers name the font directories they mount (spec 192, FR-007) and report a companion they
cannot inspect without aborting the start (spec 216, FR-004..FR-007).

``up.sh`` is driven through a real shell with a stubbed ``docker`` on PATH: the stub logs every
invocation and answers ``docker info`` so the Docker Desktop skip branch can be exercised on Linux
too. ``up.ps1`` carries the same lines and is verified by inspection (PowerShell is not installed
here).
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOCKER_STUB = """#!/bin/sh
printf '%s\\n' "CALL $*" >> "{log}"
if [ "${{1:-}}" = "info" ]; then printf '%s' "{info}"; exit 0; fi
case " $* " in
  *" exec "*) printf '%s' "{exec_out}"; exit {exec_status} ;;
esac
exit {up_status}
"""


class LauncherTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        (self.home / '.local' / 'share' / 'fonts').mkdir(parents=True)
        (self.home / '.local' / 'share' / 'gkps-fonts').mkdir(parents=True)
        self.stub_dir = Path(self.temp.name) / 'stub'
        self.stub_dir.mkdir()
        self.stub = self.stub_dir / 'docker'
        self.log = Path(self.temp.name) / 'docker-calls.log'
        self.write_stub()

    def write_stub(self, info='', exec_out='0', exec_status=0, up_status=0):
        self.stub.write_text(DOCKER_STUB.format(
            log=self.log, info=info, exec_out=exec_out,
            exec_status=exec_status, up_status=up_status))
        self.stub.chmod(0o755)

    def run_launcher(self, *arguments, home=None):
        env = dict(os.environ)
        env['PATH'] = f'{self.stub_dir}:{env.get("PATH", "")}'
        env['HOME'] = str(home or self.home)
        return subprocess.run(
            ['sh', str(REPO_ROOT / 'docker' / 'up.sh'), *arguments],
            capture_output=True, text=True, env=env, cwd=str(REPO_ROOT), timeout=60)

    def calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []


class LauncherFontListingTests(LauncherTestCase):
    def run_print(self, docker_info=''):
        self.write_stub(info=docker_info)
        process = self.run_launcher('--print')
        override = None
        for call in self.calls():
            arguments = call.removeprefix('CALL ').split()
            for index, argument in enumerate(arguments[:-1]):
                if argument == '-f' and arguments[index + 1].endswith('gkps-host-fonts.yaml'):
                    override = arguments[index + 1]
        self.assertIsNotNone(override, 'the launcher never invoked compose')
        return process, override

    def test_listing_names_mounted_directories_and_labels_reach_the_override(self):
        process, override = self.run_print()
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn('font directories from this computer (3):', process.stderr)
        self.assertIn('  /usr/share/fonts', process.stderr)
        self.assertIn(f'  {self.home}/.local/share/fonts', process.stderr)
        self.assertIn(f'  {self.home}/.local/share/gkps-fonts', process.stderr)
        override_text = Path(override).read_text()
        self.assertIn('GKPS_MEDIA_FONT_LABELS', override_text)
        self.assertIn('1=/usr/share/fonts', override_text)
        self.assertIn(f'2={self.home}/.local/share/fonts', override_text)
        self.assertIn(f'3={self.home}/.local/share/gkps-fonts', override_text)

    def test_a_docker_desktop_daemon_skips_the_system_directory_and_says_so(self):
        process, override = self.run_print(docker_info='Docker Desktop')
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn('skipped /usr/share/fonts', process.stderr)
        self.assertIn('font directories from this computer (2):', process.stderr)
        override_text = Path(override).read_text()
        self.assertNotIn("source: '/usr/share/fonts'", override_text)
        self.assertIn(f"source: '{self.home}/.local/share/fonts'", override_text)

    def test_no_font_directory_is_said_outright(self):
        self.write_stub(info='Docker Desktop')
        empty_home = Path(self.temp.name) / 'empty-home'
        empty_home.mkdir()
        process = self.run_launcher('--print', home=empty_home)
        self.assertIn('no font directory found on this computer', process.stderr)


class LauncherPostStartCheckTests(LauncherTestCase):
    """The check after `up` (spec 216): it reports, and it never changes the start's status."""

    NOT_RUNNING = 'docker compose logs media'

    def test_a_companion_that_is_not_running_is_reported(self):
        self.write_stub(exec_status=125, exec_out='')
        process = self.run_launcher()
        self.assertIn(self.NOT_RUNNING, process.stderr)
        self.assertNotIn('File Sharing', process.stderr)

    def test_a_running_companion_with_no_mounted_font_keeps_the_file_sharing_message(self):
        self.write_stub(exec_status=0, exec_out='0')
        process = self.run_launcher()
        self.assertIn('File Sharing', process.stderr)
        self.assertNotIn(self.NOT_RUNNING, process.stderr)

    def test_a_companion_that_sees_a_mounted_font_says_nothing(self):
        self.write_stub(exec_status=0, exec_out='42')
        process = self.run_launcher()
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertNotIn('File Sharing', process.stderr)
        self.assertNotIn(self.NOT_RUNNING, process.stderr)

    def test_a_failed_check_keeps_the_start_status(self):
        self.write_stub(exec_status=125, exec_out='')
        process = self.run_launcher()
        self.assertEqual(process.returncode, 0, process.stderr)

    def test_a_failed_start_runs_no_check(self):
        self.write_stub(up_status=1)
        process = self.run_launcher()
        self.assertEqual(process.returncode, 1, process.stderr)
        self.assertFalse([call for call in self.calls() if ' exec ' in call],
                         'the check ran after a start that failed')
