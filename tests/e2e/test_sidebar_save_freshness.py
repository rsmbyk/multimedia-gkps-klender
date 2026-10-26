"""Keep every visible reading-shell representation in sync after sidebar edits."""

import unittest
from datetime import date

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
class SidebarSaveFreshnessE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Preview Songbook', short_name='PV', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=self.book, title='Preview Song One')
        self.other_song = songs.Song.objects.create(book=self.book, title='Preview Song Two')
        self.service = tatib.TataIbadah.objects.create(
            name='Preview Tata Ibadah', date=date(2026, 10, 25), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembukaan', text='KJ 120', order_number=1)
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='TB', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=1)
        self.bible_book_translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(
            book_translation=self.bible_book_translation, chapter=1, verse=1,
            text='Preview Bible verse')

        self._start_browser()

    def _start_browser(self):
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            self._playwright = None
            raise unittest.SkipTest(f'Playwright browser unavailable: {error}')

    def tearDown(self):
        self._close_browser()
        super().tearDown()

    def _close_browser(self):
        if self._playwright is None:
            return
        self.browser.close()
        self._playwright.stop()
        self._playwright = None

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _edit(self, page, selector):
        control = page.locator(selector)
        control.scroll_into_view_if_needed()
        control.locator('xpath=ancestor::li[1]').hover()
        control.click()
        expect(page.locator('dialog[open]')).to_be_visible()

    def _save(self, page, **fields):
        for name, value in fields.items():
            page.locator(f'#editorContent [name="{name}"]').fill(value)
        page.locator('.editor__save').click()
        expect(page.locator('dialog[open]')).to_have_count(0, timeout=10000)

    def _time_origin(self, page):
        return page.evaluate('() => performance.timeOrigin')

    def test_tatib_sidebar_save_refreshes_row_and_active_stage(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        before = self._time_origin(page)
        route = page.url

        self._edit(page, f'#panelBody [data-editor-open="tatib"][data-editor-id="{self.service.pk}"]')
        self._save(page, name='Preview Tata Ibadah Updated')

        expect(page.locator(f'#panelBody .book[data-name="{self.service.pk}"] .book__n')) \
            .to_have_text('Preview Tata Ibadah Updated')
        expect(page.locator('#readName')).to_have_text('Preview Tata Ibadah Updated')
        self.assertIn('Preview Tata Ibadah Updated', page.title())
        self.assertEqual(page.url, route)
        self.assertEqual(self._time_origin(page), before, 'the save must not reload the document')
        page.close()

    def test_song_sidebar_save_refreshes_row_and_active_stage(self):
        page = self._page(reverse('web-song', args=[self.song.pk]))
        before = self._time_origin(page)
        route = page.url

        self._edit(page, f'#chList [data-editor-open="song"][data-editor-id="{self.song.pk}"]')
        self._save(page, title='Preview Song One Updated')

        expect(page.locator(f'#chList .songrow[data-i="{self.song.pk}"] .songrow__t')) \
            .to_have_text('Preview Song One Updated')
        expect(page.locator('#readName')).to_have_text('Preview Song One Updated')
        self.assertEqual(page.title(), 'Preview Songbook — Multimedia GKPS Klender',
                         'the tab keeps the header-derived title (reading R1)')
        self.assertEqual(page.url, route)
        self.assertEqual(self._time_origin(page), before, 'the save must not reload the document')
        page.close()

    def test_songbook_sidebar_save_refreshes_row_heading_and_title(self):
        page = self._page(reverse('web-song', args=[self.song.pk]))
        before = self._time_origin(page)
        route = page.url

        self._edit(page, f'#panelBody [data-editor-open="songbook"][data-editor-id="{self.book.pk}"]')
        self._save(page, name='Preview Songbook Updated')

        expect(page.locator(f'#panelBody .book[data-name="{self.book.pk}"] .book__n')) \
            .to_have_text('Preview Songbook Updated')
        expect(page.locator('#chTitle')).to_have_text('Song list — Preview Songbook Updated')
        self.assertIn('Preview Songbook Updated', page.title())
        expect(page.locator('#readName')).to_have_text('Preview Song One')
        self.assertEqual(page.url, route)
        self.assertEqual(self._time_origin(page), before, 'the save must not reload the document')
        page.close()

    def test_sidebar_save_preserves_filter_pane_scroll_and_focus(self):
        self._close_browser()
        for index in range(16):
            songs.Book.objects.create(name=f'Preview Extra Book {index:02d}')
            songs.Song.objects.create(book=self.book, title=f'Preview Extra Song {index:02d}')
        self._start_browser()

        page = self._page(reverse('web-song', args=[self.song.pk]))
        page.locator('#bookFilter').fill('Preview')
        page.locator('#songFilter').fill('Preview')
        page.locator('#panelBody').evaluate('(el) => { el.scrollTop = 80; }')
        page.locator('#chBody').evaluate('(el) => { el.scrollTop = el.scrollHeight; }')
        page.locator('#panelCollapse').click()
        page.wait_for_function("document.documentElement.dataset.nav === 'closed'")
        expect(page.locator('#chList .songrow').filter(has_text='Preview Song One')) \
            .to_be_visible()

        self._edit(page, f'#chList [data-editor-open="song"][data-editor-id="{self.song.pk}"]')
        page.evaluate('''() => {
          document.getElementById('panelBody').scrollTop = 80;
          const body = document.getElementById('chBody');
          body.scrollTop = body.scrollHeight;
        }''')
        panel_scroll = page.locator('#panelBody').evaluate('(el) => el.scrollTop')
        song_scroll = page.locator('#chBody').evaluate('(el) => el.scrollTop')
        self._save(page, title='Preview Song One Updated')

        expect(page.locator('#bookFilter')).to_have_value('Preview')
        expect(page.locator('#songFilter')).to_have_value('Preview')
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        expect(page.locator(f'#chList .songrow[data-i="{self.song.pk}"] .songrow__t')) \
            .to_have_text('Preview Song One Updated')
        expect(page.locator(f'#chList .songrow[data-i="{self.song.pk}"]')) \
            .to_be_focused()
        self.assertEqual(page.locator('#panelBody').evaluate('(el) => el.scrollTop'), panel_scroll)
        self.assertEqual(page.locator('#chBody').evaluate('(el) => el.scrollTop'), song_scroll)
        page.close()

    def _search_and_open_song_editor(self, page):
        page.locator('.rail__btn[aria-label="Kidung"]').click()
        page.locator(f'#panelBody .book[data-name="{self.book.pk}"]').click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        self._edit(page, f'#chList [data-editor-open="song"][data-editor-id="{self.song.pk}"]')

    def test_search_result_edit_keeps_matching_song_and_updates_counts(self):
        page = self._page('/search?q=Preview')
        before = self._time_origin(page)
        route = page.url

        expect(page.locator('.result-group[data-kind="songs"] .result-row')) \
            .to_have_count(2)
        self._search_and_open_song_editor(page)
        self._save(page, title='Preview Song One Updated')

        expect(page.locator('#searchQuery')).to_have_value('Preview')
        expect(page.locator('.result-group[data-kind="songs"] .result-row__title')) \
            .to_contain_text(['Preview Song One Updated', 'Preview Song Two'])
        expect(page.locator('.result-group[data-kind="songs"] .result-group__count')) \
            .to_have_text('2 results')
        self.assertEqual(page.url, route)
        self.assertEqual(self._time_origin(page), before, 'the save must not reload the document')

        page.locator('.result-group[data-kind="songs"] .result-row').nth(1).click()
        expect(page.locator('#readName')).to_have_text('Preview Song Two')
        page.go_back()
        expect(page.locator('#searchQuery')).to_have_value('Preview')
        expect(page.locator('.result-group[data-kind="songs"] .result-row__title').first) \
            .to_contain_text('Preview Song One Updated')
        page.close()

    def test_search_result_edit_removes_nonmatching_song_and_updates_counts(self):
        page = self._page('/search?q=Preview')
        before = self._time_origin(page)

        expect(page.locator('.result-group[data-kind="songs"] .result-row')) \
            .to_have_count(2)
        self._search_and_open_song_editor(page)
        self._save(page, title='Renamed Away')

        expect(page.locator('#searchQuery')).to_have_value('Preview')
        expect(page.locator('.result-group[data-kind="songs"] .result-row__title')) \
            .to_have_text(['Preview Song Two'])
        expect(page.locator('.result-group[data-kind="songs"] .result-group__count')) \
            .to_have_text('1 result')
        self.assertEqual(page.url, self.live_server_url + '/search?q=Preview')
        self.assertEqual(self._time_origin(page), before, 'the save must not reload the document')
        page.close()

    def test_kidung_sidebar_save_keeps_an_unrelated_bible_stage(self):
        page = self._page(f'/bible/{self.bible_book_translation.book_id}/1/')
        route = page.url

        page.locator('.rail__btn[aria-label="Kidung"]').click()
        page.locator(f'#panelBody .book[data-name="{self.book.pk}"]').click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        self._edit(page, f'#panelBody [data-editor-open="songbook"][data-editor-id="{self.book.pk}"]')
        self._save(page, name='Preview Songbook Updated')

        expect(page.locator(f'#panelBody .book[data-name="{self.book.pk}"] .book__n')) \
            .to_have_text('Preview Songbook Updated')
        expect(page.locator('#readName')).to_have_text('Matius')
        expect(page.locator('#readBody')).to_contain_text('Preview Bible verse')
        self.assertEqual(page.url, route)
        page.close()
