"""End-to-end tests for the public reading experience (spec 004).

Runs under Django's test runner (``python manage.py test``) via
``StaticLiveServerTestCase``. Skips cleanly when Playwright or its browser
binary is unavailable, so the unit suite stays runnable everywhere.

One-time setup::

    pip install -r requirements-dev.txt
    playwright install chromium
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

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
        lang = songs.Language.objects.create(name='Indonesian')
        self.book = songs.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.song = songs.Song.objects.create(book=self.book, number=12, title='Di Waktu Pagi', key='c')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Di waktu pagi aku bersyukur')

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru', abbreviation='TB')
        self.mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        mat_tb = bible.BookTranslation.objects.create(version=version, book=self.mat, translation='Matius')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=13, text='Kamu adalah garam dunia.')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=14, text='Kamu adalah terang dunia.')

        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Nyanyian Pembukaan', text='KJ 120', order_number=1)

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

    def _page(self, width=1280, height=900):
        page = self.browser.new_page(viewport={'width': width, 'height': height})
        return page

    def _search(self, page, query):
        field = page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')
        field.fill(query)
        field.press('Enter')

    # --- shell ---

    def test_search_first_home_renders(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        expect(page.locator('#homeLogo')).to_be_visible()
        expect(page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')).to_be_visible()
        expect(page.get_by_text('Try Matius 5:13, KJ 152, or pengampunan dosa')).to_be_visible()
        expect(page.locator('#railSearch[aria-current="page"]')).to_have_count(1)

    def test_search_finds_a_song(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.wait_for_url('**/search/**')
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        expect(page.locator('.result-group__title').filter(has_text='Kidung')).to_be_visible()

    def test_search_resolves_bible_reference(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'Matius 5:13')
        page.wait_for_url('**/search/**')
        first = page.locator('.result-group[data-kind="bible"] .result-row').first
        expect(first).to_contain_text('Matius 5:13')
        first.click()
        page.wait_for_url(f'**/bible/{self.mat.id}/5/**')
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        expect(page.locator('[data-search-target="true"]')).to_have_count(1)

    def test_search_minimum_length_never_clears_results(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.wait_for_url('**/search/**')
        expect(page.get_by_text('Di Waktu Pagi', exact=True)).to_be_visible()
        field = page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')
        field.fill('ab')
        field.press('Enter')
        expect(page.get_by_text('Enter at least 3 letters or numbers.')).to_be_visible()
        self.assertIn('q=waktu+pagi', page.url)
        expect(page.get_by_text('Di Waktu Pagi', exact=True)).to_be_visible()

    def test_search_keeps_last_result_set(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.wait_for_url('**/search/**')
        page.locator('.result-group[data-kind="songs"] .result-row').first.click()
        page.wait_for_url(f'**/songs/{self.song.id}/**')
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        page.locator('#railSearch').click()
        page.wait_for_url('**/search/**')
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        page.locator('.rail__logo').click()
        page.wait_for_url('**/home/**')
        expect(page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')).to_have_value('')

    def test_search_icon_exclusive_to_closed_sidebars(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        expect(page.locator('#railSearch[aria-current="page"]')).to_have_count(1)
        page.locator('.rail [data-panel="alkitab"]').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.locator('#railSearch[aria-current="page"]')).to_have_count(0)
        page.keyboard.press('Escape')
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        expect(page.locator('#railSearch[aria-current="page"]')).to_have_count(1)

    def test_reader_can_browse_and_read_a_song(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-books'))
        self.assertIn('GKPS Klender', page.title())
        page.get_by_role('link', name='Nyanyikanlah Kidung Baru').first.click()
        page.wait_for_url('**/songs/book/**')
        page.get_by_role('link', name='NKB 12').first.click()
        page.wait_for_url(f'**/songs/{self.song.id}/**')
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()

    def test_sidebar_restore_from_stage_content(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-song', args=[self.song.id]))
        expect(page.locator(f'.songrow[data-i="{self.song.id}"][aria-current="true"]')).to_have_count(1)
        page.locator('#chCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-ch', 'closed')
        page.locator('.rail [data-panel="kidung"]').click()      # closes the open panel
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        page.locator('.rail [data-panel="kidung"]').click()      # reopens from stage content
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        expect(page.locator(f'.songrow[data-i="{self.song.id}"][aria-current="true"]')).to_have_count(1)

    def test_dark_mode_toggles_and_persists(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        page.reload()
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')

    def test_print_shows_reading_content_only(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-song', args=[self.song.id]))
        page.emulate_media(media='print')
        expect(page.locator('.rail')).to_be_hidden()
        expect(page.locator('.chapters')).to_be_hidden()
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        page.emulate_media(media='screen')

    def test_no_horizontal_scroll(self):
        page = self._page()
        urls = [reverse('web-home'), reverse('web-search') + '?q=waktu pagi',
                reverse('web-song', args=[self.song.id])]
        for width in (320, 1440):
            page.set_viewport_size({'width': width, 'height': 900})
            for url in urls:
                page.goto(self.live_server_url + url)
                overflow = page.evaluate(
                    'document.documentElement.scrollWidth - window.innerWidth')
                self.assertLessEqual(overflow, 0, f'{url} overflows at {width}px')

    def test_maintenance_notice_at_root(self):
        with self.settings(MAINTENANCE_MODE=True):
            page = self._page()
            page.goto(self.live_server_url + '/')
            expect(page.get_by_text('pemeliharaan')).to_be_visible()
