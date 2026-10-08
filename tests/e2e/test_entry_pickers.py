"""The entry modal's picker menus (spec 040).

The book and song menus are capped to the VIEWPORT, not the dialog: they may
overlap the dialog's edge, they never leave the window, and they stay anchored to
their trigger while the dialog's content scrolls.
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
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EntryPickerE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        bible.BookTranslation.objects.create(version=version, book=book, translation='Matius')

        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=152, title='Ada Kuasa')
        for number in (1, 2):
            songs.Verse.objects.create(song=song, number=number, lyric=f'bait {number}')

        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')
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

    def _page(self, height=900):
        context = self.browser.new_context(viewport={'width': 1200, 'height': height})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def _open_modal(self, page, kind):
        item = page.locator('.tatib__item').first
        item.hover()
        page.locator(f'[data-entry-open="{kind}"]').first.click()
        page.wait_for_selector('dialog[open]')

    def _menu_geometry(self, page, picker):
        return page.evaluate("""pickerName => {
          const menu = document.querySelector(`[data-entry-picker="${pickerName}"] .editor__picker-menu`);
          const trigger = document.querySelector(`[data-entry-picker="${pickerName}"] [data-picker-trigger], [data-entry-picker="${pickerName}"] [data-verses-trigger]`);
          const m = menu.getBoundingClientRect(), t = trigger.getBoundingClientRect();
          const content = document.getElementById('editorContent').getBoundingClientRect();
          return {position: getComputedStyle(menu).position, gap: m.top - t.bottom,
                  top: m.top, bottom: m.bottom, left: m.left, right: m.right,
                  contentBottom: content.bottom,
                  windowWidth: window.innerWidth, windowHeight: window.innerHeight};
        }""", picker)

    def test_the_book_menu_is_capped_to_the_viewport_not_the_dialog(self):
        page = self._page()
        self._open_modal(page, 'scripture')
        page.locator('[data-entry-picker="book"] [data-picker-trigger]').click()
        expect(page.locator('[data-entry-picker="book"] .editor__picker-menu')).to_be_visible()
        geometry = self._menu_geometry(page, 'book')
        self.assertEqual(geometry['position'], 'fixed')
        self.assertAlmostEqual(geometry['gap'], 6, delta=2)          # anchored to its trigger
        self.assertGreaterEqual(geometry['left'], -1)
        self.assertLessEqual(geometry['right'], geometry['windowWidth'] + 1)
        self.assertGreaterEqual(geometry['top'], -1)
        self.assertLessEqual(geometry['bottom'], geometry['windowHeight'] + 1)

    def test_the_song_menu_is_capped_to_the_viewport_not_the_dialog(self):
        page = self._page()
        self._open_modal(page, 'song')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()
        expect(page.locator('[data-entry-picker="song"] .editor__picker-menu')).to_be_visible()
        geometry = self._menu_geometry(page, 'song')
        self.assertEqual(geometry['position'], 'fixed')
        self.assertLessEqual(geometry['bottom'], geometry['windowHeight'] + 1)

    def test_the_menu_follows_the_dialog_content_scroll(self):
        page = self._page(height=420)
        self._open_modal(page, 'scripture')
        page.add_style_tag(content='''#editorContent { height: 120px !important;
            max-height: 120px !important; flex: 0 0 120px !important; }''')
        page.locator('[data-entry-picker="book"] [data-picker-trigger]').click()
        menu = page.locator('[data-entry-picker="book"] .editor__picker-menu')
        expect(menu).to_be_visible()
        before = self._menu_geometry(page, 'book')
        page.locator('#editorContent').evaluate('el => { el.scrollTop = el.scrollHeight; }')
        page.wait_for_timeout(200)
        after = self._menu_geometry(page, 'book')
        self.assertAlmostEqual(after['gap'], 6, delta=3)             # still anchored
        self.assertNotAlmostEqual(before['top'], after['top'], places=0)   # it followed
        self.assertLessEqual(after['bottom'], after['windowHeight'] + 1)
