"""An empty song's invitation sits at the same height as an empty Tata Ibadah's (spec 224).

The two pages put the same `.entry__empty` block in different columns with different headers.
These cases assert the observable relationship — the titles share a vertical band — rather than
a hardcoded coordinate, at the two viewports where the two pages are meant to agree.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


TITLE_TOP = """() => {
  const el = document.querySelector('.entry__empty-title');
  return el ? el.getBoundingClientRect().top : null;
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongEmptyPlacementE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        book = songs.Book.objects.create(name='Lagu Place', short_name='LP', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=book, title='Lang Margogoh Au')
        self.service = tatib.TataIbadah.objects.create(name='Empty service', date='2026-11-23')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def title_top(self, path, width, height):
        page = self.browser.new_page(
            viewport={'width': width, 'height': height}, color_scheme='dark', device_scale_factor=1)
        try:
            page.goto(self.live_server_url + path, wait_until='networkidle')
            page.wait_for_selector('.entry__empty-title')
            return page.evaluate(TITLE_TOP)
        finally:
            page.close()

    def assert_titles_align(self, width, height):
        song_top = self.title_top(reverse('web-song', args=[self.song.pk]), width, height)
        tatib_top = self.title_top(
            reverse('web-tatib-service', args=[self.service.pk]), width, height)
        self.assertIsNotNone(song_top)
        self.assertIsNotNone(tatib_top)
        self.assertLessEqual(
            abs(song_top - tatib_top), 1.0,
            f'song title at {song_top:.1f}px and Tata Ibadah title at {tatib_top:.1f}px '
            f'at {width}x{height} differ by more than 1px')

    def test_empty_song_title_matches_the_tata_ibadah_title(self):
        self.assert_titles_align(1440, 900)

    def test_empty_song_title_matches_the_tata_ibadah_title_at_900x700(self):
        self.assert_titles_align(900, 700)
