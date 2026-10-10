"""The entry preview (spec 032).

A read-only modal: no header, a scrolling body, and a sticky Close. Esc and the
overlay dismiss it, and focus returns to the trigger.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EntryPreviewE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        matius = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        for number in (2, 3):
            bible.Verse.objects.create(book_translation=matius, chapter=5, verse=number,
                                       text=f'ayat {number}')

        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=152, title='Ada Kuasa')
        for number in (1, 2, 3):
            songs.Verse.objects.create(song=song, number=number, lyric=f'bait {number}')

        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=matius, chapter=5, verse_start=2, verse_end=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.SONG,
            song=song, verses=[1, 2])

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

    def _page(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def _open_preview(self, page, index):
        item = page.locator('.tatib__item').nth(index)
        item.scroll_into_view_if_needed()
        item.hover()
        item.locator('[data-preview-open]').click()
        page.wait_for_selector('#previewModal[open]')

    def test_a_passage_preview_shows_its_reference_and_full_text(self):
        page = self._page()
        self._open_preview(page, 0)
        body = page.locator('#previewContent').inner_text()
        self.assertIn('Matius 5:2-3', body)
        self.assertIn('ayat 2', body)
        self.assertIn('ayat 3', body)
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('#previewModal[open]')")

    def test_a_song_preview_tabs_between_its_verses(self):
        page = self._page()
        self._open_preview(page, 1)
        tabs = page.locator('#previewContent .preview__tab')
        self.assertEqual(tabs.count(), 2)
        self.assertIn('bait 1', page.locator('#previewContent .preview__panel').first.inner_text())
        tabs.nth(1).click()
        self.assertIn('bait 2', page.locator('#previewContent .preview__panel').nth(1).inner_text())

    def test_a_song_preview_header_reads_the_short_reference(self):
        page = self._page()
        self._open_preview(page, 1)
        header = page.locator('#previewContent .preview__song').inner_text()
        self.assertEqual(header, 'KJ 152 — Ada Kuasa')

    def test_a_song_entry_reads_its_short_reference_and_verse_line(self):
        page = self._page()
        item = page.locator('.tatib__item').nth(1)           # the song entry
        self.assertEqual(item.locator('.read__sec').inner_text(), 'KJ 152 — Ada Kuasa')
        self.assertEqual(item.locator('.read__sub').inner_text(), 'Bait 1, 2')

    def test_the_overlay_closes_the_preview(self):
        page = self._page()
        self._open_preview(page, 0)
        page.mouse.click(20, 20)                       # the backdrop
        page.wait_for_function("!document.querySelector('#previewModal[open]')")
