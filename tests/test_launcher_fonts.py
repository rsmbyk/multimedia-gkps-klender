"""The launchers name the font directories they mount (spec 192, FR-007).

``up.sh`` is driven through a real shell with a stubbed ``docker`` on PATH: the
stub logs every invocation and answers ``docker info`` so the Docker Desktop
skip branch can be exercised on Linux too. ``up.ps1`` carries the same lines
and is verified by inspection (PowerShell is not installed here).
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOCKER_STUB = """#!/bin/sh
printf '%s\\n' "$@" >> "{log}"
if [ "${{1:-}}" = "info" ]; then printf '%s' "{info}"; fi
exit 0
"""


class LauncherFontListingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        (self.home / '.local' / 'share' / 'fonts').mkdir(parents=True)
        (self.home / '.local' / 'share' / 'gkps-fonts').mkdir(parents=True)
        self.stub_dir = Path(self.temp.name) / 'stub'
        self.stub_dir.mkdir()
        self.stub = self.stub_dir / 'docker'
        self.stub.write_text(DOCKER_STUB.format(log=self.temp.name + '/docker-calls.log', info=''))
        self.stub.chmod(0o755)
        self.log = Path(self.temp.name) / 'docker-calls.log'

    def run_launcher(self, docker_info=''):
        self.stub.write_text(DOCKER_STUB.format(log=self.log, info=docker_info))
        env = dict(os.environ)
        env['PATH'] = f'{self.stub_dir}:{env.get("PATH", "")}'
        env['HOME'] = str(self.home)
        process = subprocess.run(
            ['sh', str(REPO_ROOT / 'docker' / 'up.sh'), '--print'],
            capture_output=True, text=True, env=env, cwd=str(REPO_ROOT), timeout=60)
        args = self.log.read_text().splitlines()
        override = None
        for i, arg in enumerate(args[:-1]):
            if arg == '-f' and args[i + 1].endswith('gkps-host-fonts.yaml'):
                override = args[i + 1]
        self.assertIsNotNone(override, 'the launcher never invoked compose')
        return process, override

    def test_listing_names_mounted_directories_and_labels_reach_the_override(self):
        process, override = self.run_launcher()
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
        process, override = self.run_launcher(docker_info='Docker Desktop')
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn('skipped /usr/share/fonts', process.stderr)
        self.assertIn('font directories from this computer (2):', process.stderr)
        override_text = Path(override).read_text()
        self.assertNotIn("source: '/usr/share/fonts'", override_text)
        self.assertIn(f"source: '{self.home}/.local/share/fonts'", override_text)

    def test_no_font_directory_is_said_outright(self):
        self.stub.write_text(DOCKER_STUB.format(log=self.log, info='Docker Desktop'))
        empty_home = Path(self.temp.name) / 'empty-home'
        empty_home.mkdir()
        env = dict(os.environ)
        env['PATH'] = f'{self.stub_dir}:{os.environ.get("PATH", "")}'
        env['HOME'] = str(empty_home)
        process = subprocess.run(
            ['sh', str(REPO_ROOT / 'docker' / 'up.sh'), '--print'],
            capture_output=True, text=True, env=env, cwd=str(REPO_ROOT), timeout=60)
        self.assertIn('no font directory found on this computer', process.stderr)