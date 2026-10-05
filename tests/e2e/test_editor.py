"""End-to-end tests for the sidebar editors (spec 005).

Same runner and skip behaviour as the reading suite: Django's test runner via
``StaticLiveServerTestCase``, skipped when Playwright or its browser is missing.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditorE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.lang = songs.Language.objects.create(name='Indonesian')
        self.hymn = songs.Book.objects.create(
            lang=self.lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.hymn_song = songs.Song.objects.create(
            book=self.hymn, number=12, title='Di Waktu Pagi', key='c')
        self.book = songs.Book.objects.create(
            lang=self.lang, name='Kidung Harian', short_name='KH', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=self.book, title='Alpha')
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembukaan', text='KJ 120', order_number=1)
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self._close_browser()
        super().tearDown()

    def _close_browser(self):
        """Playwright's loop must not overlap Django's database access, so any test
        that asserts against the database closes the browser first."""
        if self._playwright is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _fill(self, page, name, value):
        widget = page.locator(f'[name="{name}"]')
        if widget.evaluate('el => el.tagName') == 'SELECT':
            page.select_option(f'[name="{name}"]', value)
        else:
            page.fill(f'[name="{name}"]', value)

    def _save(self, page, **fields):
        for name, value in fields.items():
            self._fill(page, name, value)
        page.click('.editor__save')
        # a <dialog> is never detached; it just loses its open attribute
        page.wait_for_function("!document.querySelector('dialog[open]')")

    # --- the add buttons ---

    def test_add_songbook_through_the_modal(self):
        page = self._page(reverse('web-books'))
        expect(page.locator('dialog[open]')).to_have_count(0)
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New songbook')
        self._save(page, name='Kidung Sekolah', short_name='KS',
                   lang=str(self.lang.pk))
        expect(page.locator('dialog[open]')).to_have_count(0)
        expect(page.locator('#panelBody .book').filter(has_text='Kidung Sekolah')).to_be_visible()
        self._close_browser()
        self.assertTrue(songs.Book.objects.filter(name='Kidung Sekolah').exists())

    def test_add_song_to_the_open_songbook(self):
        page = self._page(reverse('web-book', args=[self.book.pk]))
        expect(page.locator('#songAdd')).to_be_enabled()
        page.click('#songAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New song')
        self._save(page, title='Lagu Baru', number='', sub_number='', key='')
        expect(page.locator('#chList .songrow').filter(has_text='Lagu Baru')).to_be_visible()
        self._close_browser()
        self.assertTrue(songs.Song.objects.filter(book=self.book, title='Lagu Baru').exists())

    def test_the_add_buttons_exist_on_the_home_to_section_path(self):
        """The path the owner actually uses: land on the home, click through in-page.

        The sidebars are swapped in by reading.js and the add buttons sit outside
        those swapped regions, so a page that never had one has to have it inserted
        -- updating in place left them missing on exactly this path (spec 005).
        """
        page = self._page(reverse('web-home'))
        expect(page.locator('.editor-add')).to_have_count(0)
        page.click('.rail__btn[aria-label="Kidung"]')
        panel_add = page.locator('#panelAdd')
        expect(panel_add).to_be_visible()
        expect(panel_add).to_contain_text('Add songbook')
        panel_add.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New songbook')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        # and it sits inside the sidebar's padding on both sides (review report:
        # a doubled inset pushed it past the edge)
        page.get_by_text(self.book.name, exact=True).first.click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        page.wait_for_timeout(700)                      # let its travel finish
        insets = page.evaluate('''() => {
            const b = document.getElementById('songAdd');
            const s = document.querySelector('.chapters');
            const br = b.getBoundingClientRect(), sr = s.getBoundingClientRect();
            return {left: br.left - sr.left, right: sr.right - br.right}; }''')
        self.assertGreater(insets['left'], 0, 'the add button overflows the left edge')
        self.assertGreater(insets['right'], 0, 'the add button overflows the right edge')
        page.click('.rail__btn[aria-label="Alkitab"]')
        expect(page.locator('#panelAdd')).to_have_count(0)          # and gone again
        self._close_browser()

    def test_escape_inside_the_modal_does_not_also_close_the_sidebar(self):
        """The modal is the innermost layer: Esc must stop there (review report)."""
        page = self._page(reverse('web-home'))
        page.click('.rail__btn[aria-label="Kidung"]')
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        self.assertEqual(page.evaluate("document.documentElement.dataset.nav"), 'open')
        expect(page.locator('#panelAdd')).to_be_visible()
        self._close_browser()

    def test_the_tata_ibadah_mode_toggle_exists_after_clicking_through(self):
        """It is part of the Tata Ibadah toolbar only, and the home path swaps that in."""
        page = self._page(reverse('web-home'))
        page.click('.rail__btn[aria-label="Kidung"]')
        expect(page.locator('#tatibMode')).to_have_count(0)
        page.click('.rail__btn[aria-label="Tata Ibadah"]')
        mode = page.locator('#tatibMode')
        expect(mode).to_be_visible()
        expect(mode).to_have_attribute('aria-label', 'Show Tata Ibadah templates')
        # and it sits where the mockup puts it: between the field and the collapse
        order = page.evaluate("""() => [...document.querySelectorAll('.panel__filter > *')]
            .map(e => e.id || e.className.split(' ')[0])""")
        self.assertEqual(order[-2:], ['tatibMode', 'panelCollapse'])
        self._close_browser()

    def test_closing_a_sidebar_reveals_no_row_control_and_no_rail_label(self):
        """Closing the song list left the row's control lit and a tile's label hanging."""
        page = self._page(reverse('web-home'))
        page.click('.rail__btn[aria-label="Kidung"]')
        page.get_by_text(self.book.name, exact=True).first.click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        page.wait_for_timeout(700)
        # close the song list with its own control, then look for anything revealed
        page.click('#chCollapse')
        page.wait_for_function("document.documentElement.dataset.ch === 'closed'")
        page.wait_for_timeout(500)
        lit = page.evaluate("""() => [...document.querySelectorAll('#panelBody .row-edit, #chList .row-edit')]
            .filter(b => getComputedStyle(b).opacity !== '0').length""")
        self.assertEqual(lit, 0, 'a row control was left revealed')
        # The label is painted by ::after, so read that -- an attribute or a missing
        # element proves nothing. First a positive control: hovering must raise it.
        lift = ("Number(getComputedStyle(document.querySelector("
                "'.rail__btn[aria-label=\"Kidung\"]'), '::after').opacity)")
        page.hover('.rail__btn[aria-label="Kidung"]')
        page.wait_for_timeout(900)
        self.assertGreater(page.evaluate(lift), 0.05, 'the label did not appear on hover')
        # closing the panel with its own control puts focus back on the tile, and that
        # must not raise the label again (review report: it did)
        page.click('#panelCollapse')
        page.wait_for_function("document.documentElement.dataset.nav === 'closed'")
        page.wait_for_timeout(700)
        self.assertEqual(page.evaluate(lift), 0, 'the rail label stayed up after closing')
        rails = page.evaluate("""() => [...document.querySelectorAll('.rail__btn[data-tip]')]
            .filter(b => Number(getComputedStyle(b, '::after').opacity) > 0.05).map(b => b.dataset.tip)""")
        self.assertEqual(rails, [], 'a rail label was left up')
        self._close_browser()

    def test_add_tatib_with_its_first_section(self):
        page = self._page(reverse('web-tatib'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New Tata Ibadah')
        self._save(page, name='Ibadah Baru', date='2026-11-01', first_title='Pembukaan',
                   first_text='KJ 1')
        expect(page.locator('#panelBody .book').filter(has_text='Ibadah Baru')).to_be_visible()
        self._close_browser()
        service = tatib.TataIbadah.objects.get(name='Ibadah Baru')
        self.assertEqual(service.tataibadahitem_set.count(), 1)

    # --- editing ---

    def test_edit_a_song_row_from_its_hover_control(self):
        page = self._page(reverse('web-book', args=[self.book.pk]))
        row = page.locator(f'li:has(.songrow[data-i="{self.song.pk}"])')
        control = row.locator('.row-edit')
        expect(control).to_have_css('opacity', '0')          # out of the way when idle
        self.assertEqual(control.evaluate('el => getComputedStyle(el).pointerEvents'), 'none')
        row.hover()
        expect(control).to_have_css('opacity', '1')
        control.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit song')
        expect(page.locator('[name="title"]')).to_have_value('Alpha')
        self._save(page, title='Alpha Baru')
        expect(page.locator('#chList .songrow').filter(has_text='Alpha Baru')).to_be_visible()
        self._close_browser()
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, 'Alpha Baru')

    def test_edit_a_tatib_row(self):
        page = self._page(reverse('web-tatib'))
        row = page.locator(f'li:has(.book[data-name="{self.service.pk}"])')
        row.hover()
        row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit Tata Ibadah')
        expect(page.locator('[name="name"]')).to_have_value('Ibadah Minggu III')
        self._save(page, name='Ibadah Minggu IV')
        expect(page.locator('#panelBody .book').filter(has_text='Ibadah Minggu IV')).to_be_visible()
        self._close_browser()
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Ibadah Minggu IV')

    def test_hymn_songbooks_and_their_songs_offer_no_control(self):
        page = self._page(reverse('web-book', args=[self.hymn.pk]))
        self.assertEqual(page.locator('#chList .row-edit').count(), 0)   # its songs
        hymn_panel = self._page(reverse('web-books'))
        hymn_row = hymn_panel.locator(f'li:has(.book[data-name="{self.hymn.pk}"])')
        self.assertEqual(hymn_row.locator('.row-edit').count(), 0)
        free_row = hymn_panel.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        self.assertEqual(free_row.locator('.row-edit').count(), 1)

    def test_validation_error_stays_in_the_modal(self):
        page = self._page(reverse('web-books'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        self._fill(page, 'name', 'Bentrok')
        self._fill(page, 'short_name', 'KH')                 # already used
        self._fill(page, 'lang', str(self.lang.pk))
        page.click('.editor__save')
        expect(page.locator('dialog[open]')).to_have_count(1)  # still open
        expect(page.locator('.editor__error')).to_contain_text('already been used')
        expect(page.locator('[name="name"]')).to_have_value('Bentrok')
        self._close_browser()
        self.assertFalse(songs.Book.objects.filter(name='Bentrok').exists())

    def test_the_shell_survives_a_save(self):
        page = self._page(reverse('web-song', args=[self.song.pk]))
        start = page.url
        page.click('#songAdd')
        page.wait_for_selector('dialog[open]')
        self._save(page, title='Lagu Kedua', number='', sub_number='', key='')
        expect(page.locator('dialog[open]')).to_have_count(0)
        self.assertEqual(page.url, start)                      # one page, no reload
        expect(page.locator('.read__title')).to_contain_text('Alpha')   # the stage kept reading
        self._close_browser()
        self.assertTrue(songs.Song.objects.filter(title='Lagu Kedua').exists())
