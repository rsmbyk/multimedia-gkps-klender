"""The companion's configuration page, driven through a real browser (spec 192).

The companion is spawned as its own process on a scratch port (``GKPS_MEDIA_PORT``)
with a scratch library root; Playwright then drives the served page — the same
surface the operator opens at ``http://127.0.0.1:63174/``.
"""

import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


class CompanionPageE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.port = free_port()
        env = dict(os.environ)
        env['GKPS_MEDIA_PORT'] = str(cls.port)
        env['GKPS_MEDIA_LIBRARY_ROOT'] = str(Path(cls.temp.name) / 'library')
        env['GKPS_MEDIA_ALLOWED_ORIGINS'] = 'http://localhost:63404'
        env['PYTHONPATH'] = str(REPO_ROOT) + os.pathsep + env.get('PYTHONPATH', '')
        cls.child_log = open(os.path.join(cls.temp.name, 'companion.log'), 'w+b')
        cls.process = subprocess.Popen(
            [sys.executable, '-m', 'multimedia.local_media'], cwd=str(REPO_ROOT), env=env,
            stdout=cls.child_log, stderr=subprocess.STDOUT)
        cls.addClassCleanup(cls.process.wait)
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                with socket.create_connection(('127.0.0.1', cls.port), timeout=1):
                    break
            except OSError:
                if cls.process.poll() is not None:
                    cls.child_log.seek(0)
                    raise AssertionError('the companion process exited before serving: '
                                         + cls.child_log.read().decode(errors='replace')[:400])
                time.sleep(0.2)
        else:
            raise AssertionError('the companion did not start within 15 seconds')
        cls.base = f'http://127.0.0.1:{cls.port}'

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        try:
            cls.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            cls.process.kill()

    def test_the_page_manages_the_recorded_origins(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.goto(f'{self.base}/')
            expect(page.locator('#empty')).to_be_visible()
            # a broken rule is named under the form and nothing is recorded
            page.fill('#origin', 'https://multimedia.example.org/')
            page.click('#addform button')
            expect(page.locator('#err')).to_contain_text('trailing slash')
            # a valid origin is recorded and survives a reload
            page.fill('#origin', 'https://multimedia.example.org')
            page.click('#addform button')
            expect(page.locator('#list .row__origin')).to_have_count(1)
            page.reload()
            expect(page.locator('#list .row__origin')).to_have_count(1)
            # the inline edit rewrites the row; Discard and the outside press discard
            page.locator('#list button').first.click()
            page.fill('.row__field', 'https://staging.multimedia.example.org')
            page.click('.btn-discard')
            expect(page.locator('#list .row__origin').first).to_contain_text(
                'multimedia.example.org')
            page.locator('#list button').first.click()
            page.fill('.row__field', 'https://staging.multimedia.example.org')
            page.click('.btn-confirm')
            expect(page.locator('#list .row__origin').first).to_contain_text('staging')
            # delete returns to the empty state
            page.locator('.row__act--danger').first.click()
            expect(page.locator('#list .row__origin')).to_have_count(0)
            expect(page.locator('#empty')).to_be_visible()
            browser.close()
