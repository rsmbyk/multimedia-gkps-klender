"""End-to-end tests for the public reading experience (spec 004).

Runs under Django's test runner (``python manage.py test``) via
``StaticLiveServerTestCase``. Skips cleanly when Playwright or its browser
binary is unavailable, so the unit suite stays runnable everywhere.

One-time setup::

    pip install -r requirements-dev.txt
    playwright install chromium
"""

import unittest
from datetime import date, timedelta

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
        self.harian = songs.Book.objects.create(
            lang=lang, name='Kidung Harian', short_name='KH', is_hymn_book=False)
        # bulk first, so the reveal tests have a list long enough to travel
        for n in range(1, 31):
            songs.Song.objects.create(book=self.harian, title='Lagu %02d' % n)
        songs.Song.objects.create(book=self.harian, title='Alpha')
        songs.Song.objects.create(book=self.harian, title='Zebra')

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru', abbreviation='TB')
        self.mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        mat_tb = bible.BookTranslation.objects.create(version=version, book=self.mat, translation='Matius')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=13, text='Kamu adalah garam dunia.')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=14, text='Kamu adalah terang dunia.')
        for verse in list(range(1, 13)) + list(range(15, 28)):   # a results page long enough to scroll
            bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=verse,
                                       text='Kasih dan kasih %d' % verse)
        # a chapter deep in the list, so a reveal has somewhere to travel
        bible.Verse.objects.create(book_translation=mat_tb, chapter=20, verse=1,
                                   text='Janganlah kamu kuatir akan hidupmu.')

        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Nyanyian Pembukaan', text='KJ 120', order_number=1)
        for n in range(1, 21):
            extra = tatib.TataIbadah.objects.create(
                name='Ibadah %02d' % n, date=date(2026, 1, 1) + timedelta(days=n), is_active=True)
            # a service is listed and searchable only while it has a public section
            tatib.TataIbadahItem.objects.create(
                tatib=extra, item_type=tatib.TataIbadahItemType.TEXT,
                title='Bagian %02d' % n, text='Isi ibadah %02d' % n, order_number=1)
        self.big = tatib.TataIbadah.objects.create(
            name='Susunan Panjang', date=date(2026, 6, 7), is_active=True)
        for n in range(1, 41):
            tatib.TataIbadahItem.objects.create(
                tatib=self.big, item_type=tatib.TataIbadahItemType.TEXT,
                title='Bagian %02d' % n, text='Isi bagian %02d' % n, order_number=n)

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
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        expect(page.locator('.result-group__title').filter(has_text='Kidung')).to_be_visible()
        self.assertEqual(page.url, self.live_server_url + reverse('web-home'))

    def test_search_resolves_bible_reference(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'Matius 5:13')
        first = page.locator('.result-group[data-kind="bible"] .result-row').first
        expect(first).to_contain_text('Matius 5:13')
        first.click()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        expect(page.locator('[data-search-target="true"]')).to_have_count(1)
        expect(page.locator('html')).to_have_attribute('data-read', 'on')
        self.assertEqual(page.url, self.live_server_url + reverse('web-home'))

    def test_short_query_searches_and_empty_submit_changes_nothing(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        expect(page.get_by_text('Di Waktu Pagi', exact=True)).to_be_visible()
        field = page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')
        field.fill('di')                       # two characters search now
        field.press('Enter')
        expect(page.get_by_text('Results for').first).to_be_visible()
        field.fill('')                         # an empty submit keeps the results
        field.press('Enter')
        expect(page.get_by_text('Di Waktu Pagi', exact=True)).to_be_visible()

    def test_search_keeps_last_result_set(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.locator('.result-group[data-kind="songs"] .result-row').first.click()
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        page.locator('#railSearch').click()
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        # the brand logo is the same route as the search icon (owner request)
        page.locator('.rail__logo').click()
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        expect(page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')).to_have_value('waktu pagi')
        self.assertEqual(page.url, self.live_server_url + reverse('web-home'))

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
        expect(page.get_by_role('link', name='NKB 12').first).to_be_visible()
        page.get_by_role('link', name='NKB 12').first.click()
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        self.assertEqual(page.url, self.live_server_url + reverse('web-books'))

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

    # --- one-page shell (spec 004 review round) ---

    def test_shell_navigates_in_place(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        start = page.url
        page.locator('.rail [data-panel="alkitab"]').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.locator('#panelBody .book').first).to_be_visible()
        page.locator('#panelBody .book').filter(has_text='Matius').first.click()
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        page.locator('#chList .ch-num').nth(4).click()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        self.assertEqual(page.url, start)        # one page, no address changes

    def test_sidebar_click_never_scrolls_the_list(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.id, 5]))
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        body = "document.getElementById('chBody')"

        page.evaluate(body + '.scrollTop = 0')
        page.evaluate("document.querySelectorAll('#chList .ch-num')[4].click()")
        page.wait_for_timeout(300)
        self.assertEqual(page.evaluate(body + '.scrollTop'), 0)   # visible row: no move

        # a row clipped at the top edge is nudged just enough to be fully visible
        page.evaluate(
            "(() => { const b = document.getElementById('chBody');"
            " const t = document.querySelector('#chList .ch-num:not(.no-data)');"
            " b.scrollTop += t.getBoundingClientRect().top - b.getBoundingClientRect().top + 30; })()")
        before = page.evaluate(body + '.scrollTop')
        self.assertGreater(before, 0, 'fixture list did not scroll')
        page.evaluate("document.querySelector('#chList .ch-num:not(.no-data)').click()")
        page.wait_for_timeout(300)
        after = page.evaluate(body + '.scrollTop')
        self.assertLessEqual(after, before)
        self.assertLess(before - after, 45)      # nudged, never centred

    def test_song_sort_toggle_on_non_hymn_books(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-book', args=[self.harian.id]))
        sort = page.locator('#songSort')
        expect(sort).to_be_visible()
        rows = page.locator('#chList .songrow')
        expect(rows.first).to_have_attribute('data-t', 'Zebra')   # newest first
        sort.click()
        expect(rows.first).to_have_attribute('data-t', 'Alpha')   # alphabetical
        expect(sort).to_have_attribute('data-order', 'title')
        sort.click()
        expect(rows.first).to_have_attribute('data-t', 'Zebra')

    # --- sidebar reveals (owner review round 2) ---

    def _settle_reveal(self, page):
        """Wait for the reveal to start and its travel (plus the settle pass) to end."""
        try:
            page.wait_for_function(
                "document.documentElement.dataset.scrollAnim === 'on'", timeout=2500)
        except Exception:
            pass
        page.wait_for_function(
            "document.documentElement.dataset.scrollAnim !== 'on'", timeout=8000)

    def _at_edge(self, page, body_sel):
        return page.evaluate(
            """(sel) => {
              const b = document.querySelector(sel);
              return b.scrollTop <= 2 || b.scrollTop >= b.scrollHeight - b.clientHeight - 2;
            }""", body_sel)

    def _row_state(self, page, body_sel, row_sel, match=None):
        """Centre offset (px), visibility and flash state of a list row."""
        return page.evaluate(
            """([bodySel, rowSel, match]) => {
              const body = document.querySelector(bodySel);
              const b = body.getBoundingClientRect();
              const rows = Array.from(document.querySelectorAll(rowSel));
              const row = match
                ? rows.find(r => r.dataset.i === match || r.dataset.name === match)
                : rows.find(r => r.getAttribute('aria-current') === 'true');
              if (!row) return null;
              const rr = row.getBoundingClientRect();
              return {delta: Math.round((rr.top + rr.height / 2) - (b.top + b.height / 2)),
                      visible: rr.top >= b.top - 1 && rr.bottom <= b.bottom + 1,
                      flashed: row.classList.contains('tatib__flash')};
            }""", [body_sel, row_sel, match])

    def test_song_result_centres_the_sidebar_row(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'Lagu 17')
        row = page.locator('.result-group[data-kind="songs"] .result-row').first
        expect(row).to_contain_text('Lagu 17')
        row.click()
        expect(page.locator('html')).to_have_attribute('data-read', 'on')
        self._settle_reveal(page)
        state = self._row_state(page, '#chBody', '#chList .songrow')
        self.assertIsNotNone(state, 'no current song row')
        self.assertTrue(state['visible'], f'row not visible: {state}')
        if not self._at_edge(page, '#chBody'):
            self.assertLessEqual(abs(state['delta']), 30, f'row not centred: {state}')

    def test_tata_ibadah_service_result_centres_the_service_row(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'Ibadah 07')
        page.locator('.result-group[data-kind="tatib"] .result-row').first.click()
        expect(page.locator('html')).to_have_attribute('data-read', 'on')
        self._settle_reveal(page)
        state = self._row_state(page, '#panelBody', '#panelBody .book')
        self.assertIsNotNone(state, 'no current service row')
        self.assertTrue(state['visible'], f'service row not visible: {state}')
        if not self._at_edge(page, '#panelBody'):
            self.assertLessEqual(abs(state['delta']), 40, f'service row not centred: {state}')

    def test_tata_ibadah_item_result_centres_and_flashes_the_contents_row(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'Bagian 25')
        page.wait_for_function(
            "document.getElementById('searchStatus') && "
            "document.getElementById('searchStatus').textContent.includes('Bagian 25')")
        rows = page.locator('.result-group[data-kind="tatib"] .result-row')
        expect(rows.first).to_be_visible()
        target, anchor = None, None
        for index in range(rows.count()):
            href = rows.nth(index).get_attribute('href') or ''
            if '#ti-' in href:
                target, anchor = rows.nth(index), href.split('#ti-')[-1]
                break
        self.assertIsNotNone(target, 'no item-level Tata Ibadah result')
        target.click()
        expect(page.locator('html')).to_have_attribute('data-read', 'on')
        self._settle_reveal(page)
        state = self._row_state(page, '#chBody', '#chList .songrow', anchor)
        self.assertIsNotNone(state, f'contents row {anchor} not found')
        self.assertTrue(state['flashed'], 'the contents quicklink was not flashed')
        self.assertTrue(state['visible'], f'contents row not visible: {state}')
        if not self._at_edge(page, '#chBody'):
            self.assertLessEqual(abs(state['delta']), 30, f'contents row not centred: {state}')
        service = self._row_state(page, '#panelBody', '#panelBody .book')
        self.assertTrue(service['visible'], 'the service row was not revealed')

    def test_sidebar_open_centres_the_row_shown_on_stage(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.id, 20]))
        expect(page.locator('#chList .ch-num[data-n="20"]')).to_have_attribute('aria-current', 'true')
        page.locator('#chCollapse').click()
        page.locator('.rail [data-panel="alkitab"]').click()      # close both levels
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        page.locator('.rail [data-panel="alkitab"]').click()      # reopen -> restore + reveal
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        self._settle_reveal(page)
        state = self._row_state(page, '#chBody', '#chList .ch-num')
        self.assertIsNotNone(state, 'no current chapter row')
        self.assertTrue(state['visible'], f'chapter row not visible: {state}')
        self.assertLessEqual(abs(state['delta']), 30, f'chapter row not centred: {state}')

    def test_reveal_travel_is_animated(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.id, 20]))
        page.locator('#chCollapse').click()
        page.locator('.rail [data-panel="alkitab"]').click()      # close both levels
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        out = page.evaluate("""() => new Promise(resolve => {
          const body = document.getElementById('chBody');
          body.scrollTop = 0;
          const seen = [];
          let flag = false;
          document.querySelector('.rail [data-panel="alkitab"]').click();
          const t0 = performance.now();
          function tick() {
            seen.push(body.scrollTop);
            if (document.documentElement.dataset.scrollAnim === 'on') flag = true;
            if (performance.now() - t0 < 1200) requestAnimationFrame(tick);
            else resolve({distinct: new Set(seen).size, flag: flag, last: seen[seen.length - 1]});
          }
          requestAnimationFrame(tick);
        })""")
        self.assertTrue(out['flag'], 'the reveal never marked itself as animating')
        self.assertGreater(out['distinct'], 4, f'the reveal jumped instead of travelling: {out}')

    def test_search_icon_never_opens_a_stale_stored_url(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.evaluate("localStorage.setItem('gkps-search', '/tatib/1/')")   # what an older build wrote
        page.reload()
        expect(page.locator('#railSearch')).to_have_attribute('href', reverse('web-home'))
        page.locator('#railSearch').click()
        page.wait_for_function("document.documentElement.dataset.home === 'landing'")
        expect(page.locator('html')).to_have_attribute('data-section', 'alkitab')
        expect(page.get_by_text('Try Matius 5:13, KJ 152, or pengampunan dosa')).to_be_visible()
        self.assertIsNone(page.evaluate("localStorage.getItem('gkps-search')"))
        # the logo takes the same route, not a restart
        page.locator('.rail__logo').click()
        page.wait_for_function("document.documentElement.dataset.home === 'landing'")
        expect(page.get_by_text('Try Matius 5:13, KJ 152, or pengampunan dosa')).to_be_visible()

    def test_search_state_survives_sidebar_browsing(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'kasih')
        page.wait_for_selector('#searchStatus')
        for _ in range(3):                       # make the result page tall enough to scroll
            more = page.locator('.result-more')
            if not more.count():
                break
            more.first.click()
            page.wait_for_timeout(250)
        page.evaluate('window.scrollTo(0, 400)')
        page.wait_for_timeout(150)
        offset = page.evaluate('window.scrollY')
        self.assertGreater(offset, 0, 'the result page did not scroll')
        # leave through the sidebars, never through a result
        page.locator('.rail [data-panel="alkitab"]').click()
        page.locator('#panelBody .book').filter(has_text='Matius').first.click()
        page.locator('#chList .ch-num').nth(4).click()
        page.wait_for_function("document.documentElement.dataset.read === 'on'")
        stored = page.evaluate("localStorage.getItem('gkps-search')")
        self.assertTrue(stored.startswith(reverse('web-search') + '?q=kasih'), stored)
        page.locator('#railSearch').click()
        page.wait_for_selector('#searchStatus')
        page.wait_for_timeout(250)
        expect(page.get_by_text('Results for').first).to_be_visible()
        resumed = page.evaluate('window.scrollY')
        self.assertGreater(resumed, 100, f'the result set was not resumed at an offset: {resumed}')
        self.assertLessEqual(resumed, offset)
        self.assertGreaterEqual(resumed, offset - 60, f'resumed far from the remembered offset: {resumed} vs {offset}')
