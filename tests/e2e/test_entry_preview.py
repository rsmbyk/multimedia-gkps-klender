"""The entry preview (spec 032; the entry names itself in the header, spec 085).

A read-only modal: the entry's identity in a pinned header, a scrolling body, and a
sticky Close. Esc and the overlay dismiss it, and focus returns to the trigger.
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
        song_entry = tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.SONG,
            song=song, verses=[1, 2])
        if self._testMethodName == 'test_a_song_preview_verse_tabs_keep_equal_circles_and_scroll':
            for number in range(4, 13):
                songs.Verse.objects.create(song=song, number=number, lyric=f'bait {number}')
            song_entry.verses = list(range(1, 13))
            song_entry.save(update_fields=['verses'])
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=3, kind=tatib.ServiceEntryKind.TEXT,
            title='Long prayer', text='\n'.join(f'Line {number}' for number in range(1, 70)))

        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=4, kind=tatib.ServiceEntryKind.TEXT,
            text='L : Marilah kita bangun berdiri.')

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
        expect(page.locator('.preview__head')).to_be_visible()
        self.assertEqual(page.locator('#previewTitle').inner_text(), 'Matius 5:2-3')
        body = page.locator('#previewContent').inner_text()
        self.assertNotIn('Matius 5:2-3', body)          # named once, up in the header
        self.assertIn('ayat 2', body)
        self.assertIn('ayat 3', body)
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('#previewModal[open]')")

    def test_a_titled_text_preview_names_it_in_the_header(self):
        page = self._page()
        self._open_preview(page, 2)                     # the titled, long text
        expect(page.locator('.preview__head')).to_be_visible()
        self.assertEqual(page.locator('#previewTitle').inner_text(), 'Long prayer')
        self.assertNotIn('Long prayer', page.locator('#previewContent').inner_text())
        self.assertEqual(page.locator('#previewModal').get_attribute('aria-labelledby'),
                         'previewTitle')

    def test_an_untitled_text_preview_has_no_header(self):
        page = self._page()
        self._open_preview(page, 3)                     # a text with no title
        expect(page.locator('.preview__head')).to_be_hidden()
        expect(page.locator('#previewContent')).to_contain_text('Marilah kita bangun berdiri')
        self.assertEqual(page.locator('#previewModal').get_attribute('aria-label'), 'Preview')
        self.assertIsNone(page.locator('#previewModal').get_attribute('aria-labelledby'))

    def test_the_preview_header_stays_put_while_the_body_scrolls(self):
        page = self._page()
        page.set_viewport_size({'width': 900, 'height': 380})
        self._open_preview(page, 2)
        head = page.locator('.preview__head')
        head_top = head.bounding_box()['y']
        page.locator('#previewContent').evaluate('el => { el.scrollTop = 120; }')
        page.wait_for_function("document.querySelector('#previewContent').scrollTop > 100")
        self.assertEqual(head.bounding_box()['y'], head_top)
        self.assertGreater(page.locator('#previewContent').evaluate('el => el.scrollTop'), 100)

    def test_short_preview_arrow_keys_do_not_scroll_the_page(self):
        page = self._page()
        page.set_viewport_size({'width': 900, 'height': 380})
        self._open_preview(page, 0)
        body = page.locator('#previewContent')
        self.assertLessEqual(body.evaluate('el => el.scrollHeight'),
                             body.evaluate('el => el.clientHeight'))
        body.locator('.preview__line').first.click()
        page.wait_for_timeout(400)  # let the pane's opener scroll settle
        page_scroll = page.evaluate('window.scrollY')
        page.keyboard.press('ArrowDown')
        page.keyboard.press('ArrowUp')
        page.wait_for_timeout(150)
        self.assertEqual(body.evaluate('el => el.scrollTop'), 0)
        self.assertEqual(page.evaluate('window.scrollY'), page_scroll)

    def test_a_song_preview_tabs_between_its_verses(self):
        page = self._page()
        self._open_preview(page, 1)
        tabs = page.locator('.preview__head .preview__tab')      # the header carries them (spec 085)
        self.assertEqual(tabs.count(), 2)
        self.assertIn('bait 1', page.locator('#previewContent .preview__panel').first.inner_text())
        tabs.nth(1).click()
        self.assertIn('bait 2', page.locator('#previewContent .preview__panel').nth(1).inner_text())
        self.assertTrue(page.evaluate(
            'document.activeElement === document.querySelectorAll(".preview__head .preview__tab")[1]'))

    def test_a_song_preview_verse_tabs_keep_equal_circles_and_scroll(self):
        page = self._page()
        self._open_preview(page, 1)
        page.set_viewport_size({'width': 390, 'height': 844})
        tabs = page.locator('.preview__head .preview__tab')
        self.assertEqual(tabs.count(), 12)
        self.assertEqual(tabs.evaluate_all('''els => els.map(el => {
          const box = el.getBoundingClientRect();
          return [box.width, box.height, getComputedStyle(el).borderRadius];
        })'''), [[30, 30, '50%']] * 12)
        tablist = page.locator('.preview__head .preview__tabs')
        self.assertGreater(tablist.evaluate('el => el.scrollWidth'),
                           tablist.evaluate('el => el.clientWidth'))
        self.assertTrue(tabs.first.evaluate('''el => {
          const box = el.getBoundingClientRect();
          const viewport = el.closest('.preview__tabs').getBoundingClientRect();
          return box.left >= viewport.left && box.right <= viewport.right;
        }'''))
        tabs.nth(11).click()
        self.assertIn('bait 12', page.locator('#previewContent .preview__panel').nth(11).inner_text())
        self.assertEqual(tabs.nth(11).evaluate('el => el.getBoundingClientRect().width'), 30)
        tablist.evaluate('el => { el.scrollLeft = el.scrollWidth; }')
        self.assertTrue(tabs.nth(11).evaluate('''el => {
          const box = el.getBoundingClientRect();
          const viewport = el.closest('.preview__tabs').getBoundingClientRect();
          return box.left >= viewport.left && box.right <= viewport.right;
        }'''))

    def test_clicking_long_preview_text_allows_arrow_key_scrolling(self):
        page = self._page()
        page.set_viewport_size({'width': 900, 'height': 380})
        self._open_preview(page, 2)
        body = page.locator('#previewContent')
        self.assertGreater(body.evaluate('el => el.scrollHeight'),
                           body.evaluate('el => el.clientHeight'))
        body.locator('.preview__line').first.click()
        self.assertEqual(page.evaluate('document.activeElement.id'), 'previewContent')
        page.wait_for_timeout(400)  # let the pane's opener scroll settle before measuring it
        page_scroll = page.evaluate('window.scrollY')
        page.keyboard.press('ArrowDown')
        page.wait_for_function("document.querySelector('#previewContent').scrollTop >= 30")
        moved = body.evaluate('el => el.scrollTop')
        page.keyboard.press('ArrowUp')
        page.wait_for_function("document.querySelector('#previewContent').scrollTop < %d" % moved)
        page.wait_for_function("document.querySelector('#previewContent').scrollTop === 0")
        page.keyboard.press('ArrowUp')
        page.wait_for_timeout(150)
        self.assertEqual(page.evaluate('window.scrollY'), page_scroll)
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('#previewModal[open]')")

    def test_a_song_preview_header_reads_the_short_reference(self):
        page = self._page()
        self._open_preview(page, 1)
        self.assertEqual(page.locator('#previewTitle').inner_text(), 'KJ 152 — Ada Kuasa')
        self.assertFalse(page.locator('#previewContent').inner_text().startswith('KJ 152'))

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
