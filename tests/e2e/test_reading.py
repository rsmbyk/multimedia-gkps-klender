"""End-to-end tests for the public reading experience.

Runs under Django's test runner (``python manage.py test``) via
``StaticLiveServerTestCase``. Skips cleanly when Playwright or its browser
binary is unavailable, so the unit suite stays runnable everywhere.

One-time setup::

    pip install -r requirements-dev.txt
    playwright install chromium
"""

import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse

from multimedia.songs import models

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReadingE2ETests(StaticLiveServerTestCase):
    # LiveServerTestCase runs against a real server thread, so fixtures are
    # created per test (committed) rather than in setUpTestData, and Playwright
    # starts only after the ORM work — its event loop must not overlap Django's
    # database access (including the flush in teardown).

    def setUp(self):
        super().setUp()
        lang = models.Language.objects.create(name='Indonesian')
        self.book = models.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.song = models.Song.objects.create(book=self.book, number=12, title='Di Waktu Pagi', key='c')
        models.Verse.objects.create(song=self.song, number=1, lyric='Di waktu pagi aku bersyukur')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _open_page(self):
        return self.browser.new_page()

    def test_reader_can_browse_and_read_a_song(self):
        page = self._open_page()
        page.goto(self.live_server_url + reverse('web-home'))
        self.assertIn('Multimedia GKPS Klender', page.title())

        page.get_by_role('link', name='Nyanyikanlah Kidung Baru').first.click()
        page.get_by_role('link', name='NKB 12').first.click()

        self.assertTrue(page.get_by_text('Di waktu pagi aku bersyukur').is_visible())

    def test_search_finds_a_song(self):
        page = self._open_page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.get_by_label('Search songs').fill('waktu pagi')
        page.get_by_role('button', name='Search').click()

        self.assertTrue(page.get_by_role('link', name='NKB 12').first.is_visible())

    def test_maintenance_notice_at_root(self):
        with self.settings(MAINTENANCE_MODE=True):
            page = self._open_page()
            page.goto(self.live_server_url + '/')
            self.assertTrue(page.get_by_text('pemeliharaan').is_visible())
