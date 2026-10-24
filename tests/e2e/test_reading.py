"""End-to-end tests for the public reading experience (spec 004).

Runs under Django's test runner (``python manage.py test``) via
``StaticLiveServerTestCase``. Skips cleanly when Playwright or its browser
binary is unavailable, so the unit suite stays runnable everywhere.

One-time setup::

    pip install -r requirements-dev.txt
    playwright install chromium
"""

import unittest
from datetime import date, datetime, timedelta, timezone

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
class ReadingE2ETests(StaticLiveServerTestCase):
    # LiveServerTestCase runs against a real server thread, so fixtures are
    # created per test (committed) rather than in setUpTestData, and Playwright
    # starts only after the ORM work — its event loop must not overlap Django's
    # database access (including the flush in teardown).

    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.song = songs.Song.objects.create(book=self.book, number=12, title='Di Waktu Pagi', key='c')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Di waktu pagi aku bersyukur')
        self.harian = songs.Book.objects.create(
            name='Kidung Harian', short_name='KH', is_hymn_book=False)
        # bulk first, so the reveal tests have a list long enough to travel
        for n in range(1, 31):
            songs.Song.objects.create(book=self.harian, title='Lagu %02d' % n)
        # Created last, so it is the newest by `modified`: the default order and the
        # alphabetical one have to be observably different.
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
        if self._testMethodName in (
            'test_tatib_quicklink_flash_repeats_after_animation_ends',
            'test_tatib_quicklink_during_flash_is_ignored_not_queued',
            'test_tatib_quicklink_flash_releases_when_stage_is_replaced',
            'test_tatib_quicklink_keyboard_activation_starts_flash',
            'test_tatib_quicklink_respects_reduced_motion_without_locking',
        ):
            self.flash_first = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=2,
                title='First flash target', text='First flash body')
            self.flash_second = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=3,
                title='Second flash target', text='Second flash body')
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
        if self._testMethodName == 'test_tatib_mode_switch_keeps_open_service_and_reveals_its_row':
            for n in range(20):
                tatib.TataIbadah.objects.create(name='Template %02d' % n, is_active=True)
        if self._testMethodName == 'test_tatib_mode_switch_keeps_template_and_no_page_state':
            self.mode_template = tatib.TataIbadah.objects.create(
                name='A Template', is_active=True)

        if self._testMethodName in (
            'test_drag_defers_sidebar_idle_collapse_then_restarts',
        ):
            self.idle_drag_entry = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                order_number=2, text='Drag while the sidebar waits')

        if self._testMethodName in (
            'test_bible_sidebar_labels_follow_edition_and_reset_on_refresh',
            'test_bible_edition_survives_menu_switches_and_history',
            'test_bible_edition_preference_returns_after_unavailable_chapter',
            'test_bible_edition_is_local_to_tab_and_resets_on_reload',
            'test_sim_codes_titles_labels_and_fallback_follow_selected_edition',
            'test_bible_language_highlight_slides_without_reflow',
            'test_bible_language_highlight_static_and_reduced_motion',
            'test_bible_language_highlight_starts_in_place_without_travel',
            'test_bible_language_links_keep_keyboard_and_no_js_navigation',
            'test_the_translation_switch_fills_the_hovered_option',
        ):
            sim_lang = bible.Language.objects.create(name='Simalungun')
            sim_version = bible.Version.objects.create(lang=sim_lang, name='Simalungun', abbreviation='SIM')
            sim_book = bible.BookTranslation.objects.create(
                version=sim_version, book=self.mat, translation='Mateus', abbreviation='Mat')
            bible.Verse.objects.create(book_translation=sim_book, chapter=5, verse=13, text='Garam ni dunia.')
            if self._testMethodName == 'test_sim_codes_titles_labels_and_fallback_follow_selected_edition':
                self.kej = bible.Book.objects.create(
                    name='Kej', testament='old', number_of_chapters=2)
                kej_tb = bible.BookTranslation.objects.create(
                    version=version, book=self.kej, translation='Kejadian')
                kej_sim = bible.BookTranslation.objects.create(
                    version=sim_version, book=self.kej, translation='1 Musa', abbreviation='1Mu')
                bible.Verse.objects.create(
                    book_translation=kej_tb, chapter=1, verse=1, text='TB first chapter.')
                bible.Verse.objects.create(
                    book_translation=kej_sim, chapter=1, verse=1, text='SIM first chapter.')
                bible.Verse.objects.create(
                    book_translation=kej_tb, chapter=2, verse=1, text='TB-only chapter.')
            if self._testMethodName == 'test_bible_sidebar_labels_follow_edition_and_reset_on_refresh':
                bible.Verse.objects.create(
                    book_translation=sim_book, chapter=6, verse=1, text='Bapa nami SIM.')
                bible.Verse.objects.create(
                    book_translation=mat_tb, chapter=6, verse=1, text='Bapa kami TB.')
            elif self._testMethodName == 'test_bible_edition_survives_menu_switches_and_history':
                bible.Verse.objects.create(
                    book_translation=sim_book, chapter=6, verse=1, text='SIM-only chapter.')

        if self._testMethodName == 'test_hymn_song_order_is_visible_after_browsing_from_home':
            songs.Song.objects.create(book=self.book, number=10, title='Ten')
            songs.Song.objects.create(book=self.book, number=12, sub_number='B', title='Suffix B')
            songs.Song.objects.create(book=self.book, number=12, sub_number='a', title='Suffix a')
            songs.Song.objects.create(book=self.book, number=2, title='Two')
            songs.Song.objects.create(book=self.book, number=None, title='Legacy')

        if self._testMethodName == 'test_service_text_sidebar_shows_two_lines_and_centers_grip':
            self.preview_text_entry = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=2,
                text='First line\nSecond line\nThird line')
            self.titled_text_entry = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, default_screen_mode='single_screen',
                order_number=3, title='Kept sidebar title', text='Body should not replace title')
            self.blank_text_entry = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=4,
                text='Keep this\n\nSkip this')

        if self._testMethodName == 'test_tatib_stage_entry_links_follow_the_theme':
            theme_song = songs.Song.objects.create(
                book=self.book, number=99, title='Nyanyian Tema')
            songs.Verse.objects.create(song=theme_song, number=1, lyric='Nyanyian tema')
            self.theme_service = tatib.TataIbadah.objects.create(
                name='Ibadah Tema', date=date(2026, 9, 6), is_active=True)
            tatib.ServiceEntry.objects.create(
                tatib=self.theme_service, kind=tatib.ServiceEntryKind.SONG,
                order_number=1, song=theme_song)

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        # Public-page tests now start an asynchronous local-library sync. Let any
        # in-flight manifest/chunk reads finish before LiveServerTestCase flushes
        # SQLite between examples.
        for context in self.browser.contexts:
            for page in context.pages:
                try:
                    page.evaluate("""async () => {
                      if (!window.GKPSOffline) return;
                      await GKPSOffline.install().catch(() => {});
                      await new Promise(resolve => setTimeout(resolve, 80));
                      const deadline = Date.now() + 8000;
                      while (Date.now() < deadline) {
                        const state = await GKPSOffline.status();
                        if (!state.syncing) return;
                        await new Promise(resolve => setTimeout(resolve, 40));
                      }
                    }""")
                except Exception:
                    pass
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
        expect(page.locator('.search-home__hint')).to_have_count(0)
        expect(page.locator('#railSearch[aria-current="page"]')).to_have_count(1)

    def test_search_finds_a_song(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        expect(page.locator('.result-group__title').filter(has_text='Kidung')).to_be_visible()
        self.assertEqual(page.url, self.live_server_url + reverse('web-search') + '?q=waktu%20pagi')

    def test_search_page_reads_the_query_grammar(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))

        # A quoted phrase matches only consecutively, and the status line shows it.
        self._search(page, '"Kasih dan kasih"')
        expect(page.locator('#searchStatus')).to_have_text("Results for “'Kasih dan kasih'”")
        expect(page.locator('.result-group[data-kind="bible"] .result-row').first).to_be_visible()

        # A dash excludes: 'terang dunia' lists, 'garam dunia' does not.
        self._search(page, 'dunia -garam')
        expect(page.locator('#searchStatus')).to_have_text('Results for “dunia -garam”')
        expect(page.locator('.result-group[data-kind="bible"] .result-row__title',
                            has_text='Matius 5:14')).to_have_count(1)
        expect(page.locator('.result-group[data-kind="bible"] .result-row__title',
                            has_text='Matius 5:13')).to_have_count(0)

        # A lone exclusion lists nothing and says why.
        self._search(page, '-garam')
        expect(page.locator('#searchStatus')).to_have_text(
            'Nothing to search — an exclusion like “-Israel” needs at least one other word.')
        expect(page.locator('.result-group')).to_have_count(0)

    def test_search_lists_no_bible_reference(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'Matius 5:13')
        # Digits are tokens (spec 105), so other verses can match '5'; the point is
        # that the reference itself resolves to no row.
        expect(page.locator('.result-group[data-kind="bible"] .result-row__title',
                            has_text='Matius 5:13')).to_have_count(0)
        expect(page.locator('.result-row[href*="v=13"]')).to_have_count(0)
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_have_count(0)

    def test_short_query_searches_and_empty_submit_returns_to_index(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        expect(page.get_by_text('Di Waktu Pagi', exact=True)).to_be_visible()
        field = page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')
        field.fill('di')                       # two characters search now
        field.press('Enter')
        page.wait_for_function("document.getElementById('searchStatus')?.textContent.includes('di')")
        field.fill('')                         # an empty submit resolves to the index
        field.press('Enter')
        expect(page).to_have_url(self.live_server_url + '/')
        expect(field).to_have_value('')
        expect(page.locator('.search-home__hint')).to_have_count(0)
        page.locator('#railSearch').click()
        expect(page.get_by_text('Results for').first).to_be_visible()
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        expect(field).to_have_value('')

    def test_search_keeps_last_result_set(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.locator('.result-group[data-kind="songs"] .result-row').first.click()
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        page.locator('#railSearch').click()
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        # The brand returns to the empty index; the Search rail restores this tab's results.
        page.locator('.rail__logo').click()
        expect(page).to_have_url(self.live_server_url + '/')
        expect(page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')).to_have_value('')
        expect(page.locator('.search-home__hint')).to_have_count(0)
        page.locator('#railSearch').click()
        expect(page.get_by_role('link', name='NKB 12')).to_be_visible()
        expect(page.get_by_label('Search Alkitab, Kidung, and Tata Ibadah')).to_have_value(
            'waktu pagi')

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
        self.assertEqual(page.url, self.live_server_url + reverse('web-song', args=[self.song.id]))

    def test_matching_idle_bible_sidebar_collapses_to_mini(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.clock.run_for(59000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.clock.run_for(1000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()

    def test_idle_collapsed_bible_sidebar_reopens_without_navigating(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        current_url = page.url
        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

        page.locator('.rail [data-panel="alkitab"]').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        self.assertEqual(page.url, current_url)

    def test_rail_activity_restarts_sidebar_idle_timeout(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))

        page.clock.run_for(30000)
        page.mouse.move(16, 16)
        page.clock.run_for(30000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.clock.run_for(30000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

    def test_sidebar_timeout_waits_while_filter_has_focus(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))

        page.locator('#bookFilter').focus()
        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.evaluate('document.activeElement.blur()')
        page.clock.run_for(59000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.clock.run_for(1000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

    def test_sidebar_for_other_section_stays_open_when_stage_is_bible(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        page.locator('.rail [data-panel="kidung"]').click()
        expect(page.locator('html')).to_have_attribute('data-section', 'kidung')
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')

        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()

    def test_narrow_layout_keeps_matching_sidebar_open(self):
        page = self._page(width=390, height=844)
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))

        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')

    def test_matching_idle_tatib_sidebar_closes_without_navigating(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        current_url = page.url

        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        self.assertEqual(page.url, current_url)
        expect(page.locator('#read[data-kind="tatib"]')).to_be_visible()

    def test_dialog_defers_sidebar_idle_collapse_then_restarts(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')

        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        page.evaluate('document.activeElement.blur()')
        page.clock.run_for(1000)
        page.clock.run_for(58000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.clock.run_for(2000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')

    def test_drag_defers_sidebar_idle_collapse_then_restarts(self):
        page = self._page()
        page.clock.install(time=datetime(2026, 10, 13, 12, tzinfo=timezone.utc))
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        grip = page.locator(f'[data-move-grip="{self.idle_drag_entry.pk}"]')
        box = grip.bounding_box()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        page.mouse.down()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2 + 12)
        expect(page.locator('#chList.is-dragging')).to_have_count(1)

        page.clock.run_for(60000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.mouse.up()
        page.clock.run_for(1000)
        page.clock.run_for(59000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.clock.run_for(1000)
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')

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

    def test_system_theme_is_default_and_follows_os_changes(self):
        page = self._page()
        page.emulate_media(color_scheme='dark')
        page.goto(self.live_server_url + reverse('web-home'))
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'system')
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        expect(page.locator('.rail__foot button:visible')).to_have_count(2)
        expect(page.locator('#themeBtn')).to_have_attribute('aria-label', 'System mode')
        expect(page.locator('#themeBtn')).to_have_attribute('data-tip', 'System mode')
        expect(page.locator('#themeBtn .system')).to_have_css('opacity', '1')
        page.emulate_media(color_scheme='light')
        expect(page.locator('html')).to_have_attribute('data-theme', 'light')
        expect(page.locator('#themeBtn')).to_have_attribute('aria-label', 'System mode')

    def test_theme_button_cycles_modes_and_current_labels(self):
        page = self._page()
        page.emulate_media(color_scheme='light')
        page.goto(self.live_server_url + reverse('web-home'))
        for mode, icon in [('dark', 'moon'), ('light', 'sun'), ('system', 'system')]:
            page.locator('#themeBtn').click()
            expect(page.locator('html')).to_have_attribute('data-theme-mode', mode)
            expect(page.locator('#themeBtn')).to_have_attribute('aria-label', f'{mode.title()} mode')
            expect(page.locator('#themeBtn')).to_have_attribute('data-tip', f'{mode.title()} mode')
            expect(page.locator(f'#themeBtn .{icon}')).to_have_css('opacity', '1')

    def test_theme_button_keeps_original_rail_style(self):
        for width, expected_size in [(1280, 44), (500, 40)]:
            page = self._page(width=width)
            page.goto(self.live_server_url + reverse('web-home'))
            button = page.locator('#themeBtn')
            self.assertEqual(button.bounding_box()['width'], expected_size)
            self.assertEqual(button.bounding_box()['height'], expected_size)
            expect(button).to_have_css('background-color', 'rgba(0, 0, 0, 0)')
            page.close()

    def test_system_mode_can_be_restored_after_manual_override(self):
        page = self._page()
        page.emulate_media(color_scheme='light')
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'dark')
        page.emulate_media(color_scheme='dark')
        page.emulate_media(color_scheme='light')
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'light')
        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'system')
        expect(page.locator('html')).to_have_attribute('data-theme', 'light')
        page.reload()
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'system')
        page.emulate_media(color_scheme='dark')
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')

    def test_invalid_theme_storage_defaults_to_system(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.evaluate("localStorage.setItem('gkps-theme', 'unknown')")
        page.reload()
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'system')

    def test_unavailable_theme_storage_defaults_to_system(self):
        page = self._page()
        page.emulate_media(color_scheme='dark')
        page.add_init_script("Object.defineProperty(window, 'localStorage', {get: () => {throw new Error('blocked')}})")
        page.goto(self.live_server_url + reverse('web-home'))
        expect(page.locator('html')).to_have_attribute('data-theme-mode', 'system')
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        page.locator('#themeBtn').click()
        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme', 'light')

    def test_tatib_stage_entry_links_follow_the_theme(self):
        # Spec 056: the stage's entry-title links wear the theme's link colour
        # (forest green in light, lifted royal blue in dark), underline kept,
        # instead of the browser default blue.
        page = self._page()
        page.emulate_media(color_scheme='light')
        page.goto(self.live_server_url + reverse(
            'web-tatib-service', args=[self.theme_service.pk]))
        link = page.locator('#readBody .entry__jump').first
        expect(link).to_be_visible()
        expect(link).to_have_css('color', 'rgb(28, 92, 60)')          # --link, light
        self.assertEqual(
            link.evaluate('el => getComputedStyle(el).textDecorationLine'), 'underline')
        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        expect(link).to_have_css('color', 'rgb(124, 156, 240)')       # --link, dark

    def test_sidebar_selection_tint_matches_theme_for_all_current_rows(self):
        page = self._page()
        home_url = self.live_server_url + reverse('web-home')
        expected = {
            'light': {'background': 'rgb(185, 215, 201)', 'color': 'rgb(31, 31, 29)'},
            'dark': {'background': 'rgb(57, 63, 79)', 'color': 'rgb(245, 243, 238)'},
        }

        def assert_selected_row(selector, theme):
            selected = page.locator(selector)
            expect(selected).to_have_count(1)
            actual = selected.evaluate("""el => ({
                background: getComputedStyle(el).backgroundColor,
                color: getComputedStyle(el).color,
                className: el.className,
                connected: el.isConnected,
                citation: el.querySelector('.songrow__c')
                  ? getComputedStyle(el.querySelector('.songrow__c')).color : null,
                secondary: el.querySelector('.book__s') ? {
                  color: getComputedStyle(el.querySelector('.book__s')).color,
                  opacity: getComputedStyle(el.querySelector('.book__s')).opacity
                } : null
            })""")
            detail = '%s theme=%s actual=%r token=%s' % (
                selector, theme, actual,
                page.locator('html').evaluate("el => ({token: getComputedStyle(el).getPropertyValue('--sidebar-selected-bg'), sheets: Array.from(document.styleSheets).map(sheet => sheet.href), path: location.pathname})"))
            self.assertEqual(actual['background'], expected[theme]['background'], detail)
            self.assertEqual(actual['color'], expected[theme]['color'], detail)
            if '.songrow[' in selector:
                self.assertEqual(actual['citation'], expected[theme]['color'])
            if actual['secondary']:
                self.assertEqual(actual['secondary']['color'], expected[theme]['color'])
                self.assertEqual(actual['secondary']['opacity'], '1')

        def open_sidebar_tile(section, title, theme):
            page.goto(home_url)
            expect(page.locator('html')).to_have_attribute('data-theme', theme)
            page.locator('.rail [data-panel="%s"]' % section).click()
            expect(page.locator('html')).to_have_attribute('data-nav', 'open')
            tile = page.locator('#panelBody .book').filter(has_text=title).first
            expect(tile).to_be_visible()
            tile.click()
            expected_url = (self.live_server_url + reverse('web-tatib-service', args=[self.service.pk])
                            if section == 'tatib' else home_url)
            expect(page).to_have_url(expected_url)
            return tile

        page.emulate_media(color_scheme='light')
        page.goto(home_url)
        expect(page.locator('html')).to_have_attribute('data-theme', 'light')

        for theme in ('light', 'dark'):
            if theme == 'dark':
                page.locator('#themeBtn').click()
                expect(page.locator('html')).to_have_attribute('data-theme', 'dark')

            open_sidebar_tile('alkitab', 'Matius', theme)
            assert_selected_row('#panelBody .book[aria-current="true"]', theme)

            open_sidebar_tile('alkitab', 'Matius', theme)
            expect(page.locator('html')).to_have_attribute('data-ch', 'open')
            page.get_by_role('link', name='Matius chapter 5').click()
            expect(page).to_have_url(self.live_server_url
                                     + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
            assert_selected_row('#chList .ch-num[aria-current="true"]', theme)

            open_sidebar_tile('kidung', 'Nyanyikanlah Kidung Baru', theme)
            assert_selected_row('#panelBody .book[aria-current="true"]', theme)

            open_sidebar_tile('kidung', 'Nyanyikanlah Kidung Baru', theme)
            song = page.locator('#chList .songrow').filter(has_text='Di Waktu Pagi').first
            expect(song).to_be_visible()
            song.click()
            expect(page).to_have_url(self.live_server_url + reverse('web-song', args=[self.song.id]))
            assert_selected_row('#chList .songrow[aria-current="true"]', theme)

            open_sidebar_tile('tatib', 'Ibadah Minggu III', theme)
            assert_selected_row('#panelBody .book[aria-current="true"]', theme)

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
        self.assertEqual(page.url, self.live_server_url
                         + reverse('web-bible-chapter', args=[self.mat.pk, 5]))

    def test_empty_bible_header_row_does_not_reserve_space(self):
        for width in (1440, 390):
            with self.subTest(width=width):
                page = self._page(width=width)
                page.goto(self.live_server_url + reverse('web-home'))
                page.locator('.rail [data-panel="alkitab"]').click()
                page.locator('#panelBody .book').filter(has_text='Matius').first.click()
                page.locator('#chList .ch-num').nth(4).click()
                expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
                self.assertEqual(page.url, self.live_server_url
                                 + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
                geometry = page.evaluate('''() => {
                  const box = selector => document.querySelector(selector).getBoundingClientRect();
                  const stage = document.querySelector('.stage');
                  return {
                    rowHeight: box('.read__head-top').height,
                    titleTop: box('.read__title').top,
                    toggleTop: box('.read__lang').top,
                    stageTop: box('.stage').top,
                    paddingTop: parseFloat(getComputedStyle(stage).paddingTop),
                    titleVisible: box('.read__title').height > 0,
                    toggleVisible: box('.read__lang').height > 0
                  };
                }''')
                self.assertLessEqual(geometry['rowHeight'], 1, geometry)
                self.assertTrue(geometry['titleVisible'] and geometry['toggleVisible'], geometry)
                self.assertEqual(geometry['paddingTop'], 40, geometry)
                self.assertAlmostEqual(min(geometry['titleTop'], geometry['toggleTop']),
                                       geometry['stageTop'] + geometry['paddingTop'], delta=1)
                page.close()

    def test_bible_sidebar_labels_follow_edition_and_reset_on_refresh(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        row = page.locator(f'#panelBody .book[href="/bible/{self.mat.pk}/"]')
        expect(row.locator('.book__n')).to_have_text('Matius')
        expect(row.locator('.book__s')).to_have_text('Mateus')
        row.evaluate("el => { el.dataset.identityCheck = 'same-row'; }")

        page.locator('#langSim').click()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        expect(row.locator('.book__n')).to_have_text('Mateus')
        expect(row.locator('.book__s')).to_have_text('Matius')
        self.assertEqual(row.get_attribute('data-identity-check'), 'same-row')
        self.assertEqual(row.get_attribute('aria-label'), 'Mateus (Matius)')
        self.assertEqual(row.get_attribute('data-tip'), 'Mateus — Matius')
        for name in ('Mateus', 'Matius'):
            page.locator('#bookFilter').fill(name)
            self.assertTrue(row.is_visible())
        page.locator('#bookFilter').fill('')
        page.locator('#panelCollapse').click()
        page.wait_for_function("document.documentElement.dataset.nav === 'mini'")
        self.assertEqual(row.locator('.book__a').inner_text(), 'Mat')
        self.assertTrue(row.locator('.book__a').is_visible())

        page.locator('#chList .ch-num').nth(5).click()
        expect(page.get_by_text('Bapa nami SIM.')).to_be_visible()
        row = page.locator(f'#panelBody .book[href="/bible/{self.mat.pk}/"]')
        expect(row.locator('.book__n')).to_have_text('Mateus')
        self.assertEqual(row.locator('.book__a').inner_text(), 'Mat')
        page.reload()
        expect(page.get_by_text('Bapa kami TB.')).to_be_visible()
        row = page.locator(f'#panelBody .book[href="/bible/{self.mat.pk}/"]')
        expect(row.locator('.book__n')).to_have_text('Matius')
        expect(row.locator('.book__s')).to_have_text('Mateus')
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        page.close()

    def test_sim_codes_titles_labels_and_fallback_follow_selected_edition(self):
        no_js_context = self.browser.new_context(java_script_enabled=False)
        no_js_page = no_js_context.new_page()
        no_js_page.goto(self.live_server_url + reverse(
            'web-bible-chapter', args=[self.kej.pk, 1]) + '?ed=sim')
        expect(no_js_page.locator('#readName')).to_have_text('1 Musa')
        self.assertEqual(no_js_page.title(), '1 Musa 1 — GKPS Klender')
        self.assertEqual(
            no_js_page.locator(f'#panelBody .book[href="/bible/{self.kej.pk}/"] .book__a').inner_text(),
            '1Mu')
        self.assertEqual(no_js_page.locator('html').get_attribute('data-bible-edition'), 'sim')
        self.assertEqual(no_js_page.locator('.rail [data-panel="alkitab"]').get_attribute('data-tip'), 'Bibel')
        no_js_context.close()

        page = self._page()
        page.goto(self.live_server_url + reverse(
            'web-bible-chapter', args=[self.kej.pk, 1]) + '?ed=sim')
        expect(page.locator('#readName')).to_have_text('1 Musa')
        self.assertEqual(page.title(), '1 Musa 1 — GKPS Klender')
        self.assertEqual(page.locator('html').get_attribute('data-bible-edition'), 'sim')
        expect(page.get_by_text('SIM first chapter.')).to_be_visible()

        row = page.locator(f'#panelBody .book[href="/bible/{self.kej.pk}/"]')
        expect(row.locator('.book__n')).to_have_text('1 Musa')
        expect(row.locator('.book__s')).to_have_text('Kejadian')
        page.locator('#bookFilter').fill('Kej')
        expect(row).to_be_visible()
        page.locator('#bookFilter').fill('1Mu')
        expect(row).to_be_visible()
        page.locator('#bookFilter').fill('')

        page.locator('#langTb').click()
        expect(page.locator('#readName')).to_have_text('Kejadian')
        self.assertEqual(page.title(), 'Kejadian 1 — GKPS Klender')
        for section, label in (('alkitab', 'Alkitab'), ('kidung', 'Kidung'),
                               ('tatib', 'Tata Ibadah')):
            button = page.locator(f'.rail [data-panel="{section}"]')
            self.assertEqual(button.get_attribute('data-tip'), label)
            self.assertEqual(button.get_attribute('aria-label'), label)
        for code in ('Kej', '1Mu'):
            page.locator('#bookFilter').fill(code)
            expect(row).to_be_visible()
        page.locator('#bookFilter').fill('')
        page.locator('#langSim').click()
        expect(page.locator('#readName')).to_have_text('1 Musa')
        self.assertEqual(page.title(), '1 Musa 1 — GKPS Klender')

        expected_sim_labels = {
            'alkitab': ('Bibel', 'Bibel'),
            'kidung': ('Doding', 'Doding'),
            'tatib': ('Agenda', 'Agenda'),
        }
        for section, (tip, accessible_name) in expected_sim_labels.items():
            button = page.locator(f'.rail [data-panel="{section}"]')
            self.assertEqual(button.get_attribute('data-tip'), tip)
            self.assertEqual(button.get_attribute('aria-label'), accessible_name)
            button.hover()
            page.wait_for_timeout(650)
            self.assertEqual(button.get_attribute('data-tip-open'), 'true')
            self.assertEqual(
                button.evaluate("el => getComputedStyle(el, '::after').content"),
                f'"{tip}"')

        page.locator('#panelCollapse').click()
        page.wait_for_function("document.documentElement.dataset.nav === 'mini'")
        expect(row.locator('.book__a')).to_have_text('1Mu')

        page.locator('.rail [data-panel="kidung"]').click()
        self.assertEqual(page.locator('html').get_attribute('data-bible-edition'), 'sim')
        self.assertEqual(page.locator('.rail [data-panel="kidung"]').get_attribute('data-tip'), 'Doding')
        self.assertEqual(page.locator('.rail [data-panel="kidung"]').get_attribute('aria-label'), 'Doding')
        page.goto(self.live_server_url + reverse(
            'web-bible-chapter', args=[self.kej.pk, 2]) + '?ed=sim')
        row = page.locator(f'#panelBody .book[href="/bible/{self.kej.pk}/"]')
        expect(page.get_by_text('TB-only chapter.')).to_be_visible()
        expect(page.locator('#readName')).to_have_text('Kejadian')
        self.assertEqual(page.title(), 'Kejadian 2 — GKPS Klender')
        self.assertEqual(page.locator('html').get_attribute('data-bible-edition'), 'sim')
        expect(row.locator('.book__a')).to_have_text('1Mu')
        expect(page.locator('#panelBody [data-testament="old"] .group__head')).to_have_text(
            'Padan na Basaia')
        page.close()

    def test_bible_edition_survives_menu_switches_and_history(self):
        """Keep sidebar choice and chapter availability while the stage is non-Bible."""
        page = self._page()
        chapter_url = reverse('web-bible-chapter', args=[self.mat.pk, 5])
        songbook_url = reverse('web-book', args=[self.book.pk])
        song_url = reverse('web-song', args=[self.song.pk])
        book_url = reverse('web-bible-book', args=[self.mat.pk])

        def open_song_page_and_return_to_bible(edition):
            page.locator('.rail [data-panel="kidung"]').click()
            page.locator(f'#panelBody .book[href="{songbook_url}"]').click()
            page.locator(f'#chList .songrow[href="{song_url}"]').click()
            expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="{book_url}"]').click()
            row = page.locator(f'#panelBody .book[href="{book_url}"]')
            if edition == 'sim':
                expect(row.locator('.book__n')).to_have_text('Mateus')
                expect(row.locator('.book__s')).to_have_text('Matius')
                self.assertNotEqual(
                    page.locator('#chList .ch-num').nth(5).get_attribute('aria-disabled'),
                    'true', 'SIM-only chapter should stay available while Bible is open in the sidebar')
            else:
                expect(row.locator('.book__n')).to_have_text('Matius')
                expect(row.locator('.book__s')).to_have_text('Mateus')
            page.locator(f'#chList .ch-num[href="{chapter_url}"]').click()

        def open_service_page_and_return_to_bible():
            page.locator('#railSearch').click()
            self._search(page, 'Ibadah Minggu III')
            page.locator('.result-group[data-kind="tatib"] .result-row').first.click()
            expect(page.locator('#read[data-kind="tatib"]')).to_be_visible()
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="{book_url}"]').click()
            row = page.locator(f'#panelBody .book[href="{book_url}"]')
            expect(row.locator('.book__n')).to_have_text('Matius')
            expect(row.locator('.book__s')).to_have_text('Mateus')
            page.locator(f'#chList .ch-num[href="{chapter_url}"]').click()

        page.goto(self.live_server_url + chapter_url)
        page.locator('#langSim').click()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()

        open_song_page_and_return_to_bible('sim')
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        expect(page.locator('#langSim')).to_have_attribute('aria-pressed', 'true')
        row = page.locator(f'#panelBody .book[href="{book_url}"]')
        expect(row.locator('.book__n')).to_have_text('Mateus')
        expect(row.locator('.book__s')).to_have_text('Matius')

        page.go_back()
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        page.go_forward()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        expect(page.locator('#langSim')).to_have_attribute('aria-pressed', 'true')

        page.locator('#langTb').click()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        open_song_page_and_return_to_bible('tb')
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        open_service_page_and_return_to_bible()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        expect(row.locator('.book__n')).to_have_text('Matius')
        expect(row.locator('.book__s')).to_have_text('Mateus')

    def test_bible_edition_is_local_to_tab_and_resets_on_reload(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 900})
        page = context.new_page()
        chapter_url = reverse('web-bible-chapter', args=[self.mat.pk, 5])
        page.goto(self.live_server_url + chapter_url)
        page.locator('#langSim').click()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()

        other_tab = page.context.new_page()
        other_tab.goto(self.live_server_url + chapter_url)
        expect(other_tab.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        expect(other_tab.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()

        page.reload()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        other_tab.close()
        context.close()

    def test_bible_edition_preference_returns_after_unavailable_chapter(self):
        page = self._page()
        chapter_five = reverse('web-bible-chapter', args=[self.mat.pk, 5])
        page.goto(self.live_server_url + chapter_five)
        page.locator('#langSim').click()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()

        page.locator('#railSearch').click()
        self._search(page, 'kuatir')
        page.locator('.result-group[data-kind="bible"] .result-row').first.click()
        expect(page.get_by_text('Janganlah kamu kuatir akan hidupmu.')).to_be_visible()
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        expect(page.locator('#langSim')).to_have_attribute('aria-disabled', 'true')

        page.locator('#railSearch').click()
        self._search(page, 'garam dunia')
        page.locator('.result-group[data-kind="bible"] .result-row').first.click()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        expect(page.locator('#langSim')).to_have_attribute('aria-pressed', 'true')
        page.close()

    def test_bible_language_highlight_slides_without_reflow(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('.rail [data-panel="alkitab"]').click()
        page.locator('#panelBody .book').filter(has_text='Matius').first.click()
        page.locator('#chList .ch-num').nth(4).click()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        switch = page.locator('.read__lang')
        expect(switch.locator('.read__lang-thumb')).to_have_count(1)
        geometry = switch.bounding_box()
        header = page.locator('.read__head').bounding_box()
        # stretch the travel to a known long duration so it can be paused and
        # sampled deterministically; the move stays transform-only
        switch.locator('.read__lang-thumb').evaluate('el => el.style.transitionDuration = "3000ms"')
        for label, text, pressed in [('SIM', 'Garam ni dunia.', '#langSim'),
                                      ('TB', 'Kamu adalah garam dunia.', '#langTb')]:
            switch.get_by_text(label, exact=True).click()
            expect(page.get_by_text(text)).to_be_visible()
            expect(page.locator(pressed)).to_have_attribute('aria-pressed', 'true')
            state = switch.evaluate('''el => {
              const thumb = el.querySelector('.read__lang-thumb');
              const animation = thumb.getAnimations().find(a => a.transitionProperty === 'transform');
              if (animation) { animation.pause(); animation.currentTime = animation.effect.getTiming().duration / 2; }
              return { animation: !!animation,
                       middle: thumb.getBoundingClientRect().left,
                       start: el.querySelector('#langTb').getBoundingClientRect().left,
                       end: el.querySelector('#langSim').getBoundingClientRect().left };
            }''')
            self.assertTrue(state['animation'], state)
            self.assertGreater(state['middle'], state['start'] + 3, state)
            self.assertLess(state['middle'], state['end'] - 3, state)
            self.assertEqual(switch.bounding_box(), geometry)
            self.assertEqual(page.locator('.read__head').bounding_box(), header)
            switch.locator('.read__lang-thumb').evaluate('el => el.getAnimations().forEach(a => a.finish())')
            end = switch.locator('.read__lang-thumb').bounding_box()
            target = page.locator(pressed).bounding_box()
            self.assertAlmostEqual(end['x'], target['x'], delta=1)
            self.assertAlmostEqual(end['width'], target['width'], delta=1)
        switch.locator('.read__lang-thumb').evaluate('el => el.style.transitionDuration = ""')
        page.close()

    def test_bible_language_highlight_static_and_reduced_motion(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('.rail [data-panel="alkitab"]').click()
        page.locator('#panelBody .book').filter(has_text='Matius').first.click()
        page.locator('#chList .ch-num').nth(19).click()  # TB-only chapter
        switch = page.locator('.read__lang')
        expect(switch.locator('.read__lang-thumb')).to_have_count(1)
        expect(page.locator('#langSim')).to_have_attribute('aria-disabled', 'true')
        before = switch.locator('.read__lang-thumb').bounding_box()
        address = page.url
        page.locator('#langSim').dispatch_event('click')  # real click is disabled by aria-disabled
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        self.assertEqual(switch.get_attribute('data-edition'), 'tb')
        self.assertEqual(switch.locator('.read__lang-thumb').bounding_box(), before)
        self.assertEqual(page.url, address)
        page.close()

        page = self._page()
        page.emulate_media(reduced_motion='reduce')
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('.rail [data-panel="alkitab"]').click()
        page.locator('#panelBody .book').filter(has_text='Matius').first.click()
        page.locator('#chList .ch-num').nth(4).click()
        switch = page.locator('.read__lang')
        expect(switch.locator('.read__lang-thumb')).to_have_count(1)
        page.locator('#langSim').click()
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        expect(page.locator('#langSim')).to_have_attribute('aria-pressed', 'true')
        self.assertAlmostEqual(switch.locator('.read__lang-thumb').bounding_box()['x'],
                               page.locator('#langSim').bounding_box()['x'], delta=1)
        self.assertEqual(switch.locator('.read__lang-thumb').evaluate('el => el.getAnimations().length'), 0)
        self.assertEqual(switch.locator('.read__lang-thumb')
                         .evaluate('el => getComputedStyle(el).transitionDuration'), '0s')
        page.close()

    def test_the_translation_switch_fills_the_hovered_option(self):
        """The reading header's TB/SIM switch answers the pointer like the screen-mode one
        (spec 083)."""
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        switch = page.locator('.read__lang')
        expect(switch.locator('.read__lang-thumb')).to_have_count(1)
        unselected = switch.locator('a[aria-pressed="false"]')
        selected = switch.locator('a[aria-pressed="true"]')

        resting = unselected.evaluate('el => getComputedStyle(el).backgroundColor')
        unselected.hover()
        page.wait_for_timeout(260)             # the fill fades in over --ease
        hovered = unselected.evaluate('el => getComputedStyle(el).backgroundColor')

        self.assertNotEqual(hovered, resting, 'the unselected option took no fill on hover')
        self.assertEqual(hovered, 'rgba(31, 31, 29, 0.08)')     # --icon-hover-bg, light theme

        selected.hover()
        page.wait_for_timeout(260)
        self.assertEqual(selected.evaluate('el => getComputedStyle(el).backgroundColor'),
                         'rgba(0, 0, 0, 0)', 'the selected option filled over its thumb')

    def test_bible_language_highlight_starts_in_place_without_travel(self):
        page = self._page()
        page.goto(self.live_server_url
                  + reverse('web-bible-chapter', args=[self.mat.pk, 5]) + '?ed=sim')
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        self.assertEqual(page.url, self.live_server_url
                         + reverse('web-bible-chapter', args=[self.mat.pk, 5]) + '?ed=sim')
        switch = page.locator('.read__lang')
        expect(switch.locator('.read__lang-thumb')).to_have_count(1)
        expect(page.locator('#langSim')).to_have_attribute('aria-pressed', 'true')
        self.assertEqual(switch.get_attribute('data-edition'), 'sim')
        thumb = switch.locator('.read__lang-thumb')
        self.assertAlmostEqual(thumb.bounding_box()['x'],
                               page.locator('#langSim').bounding_box()['x'], delta=1)
        self.assertEqual(thumb.evaluate('el => el.getAnimations().length'), 0)
        # the highlight must not carry the old state or slide in.
        page.locator('#langTb').click()
        page.locator('.read__lang-thumb').evaluate(
            'el => Promise.all(el.getAnimations().map(animation => animation.finished))')
        page.locator('#chList .ch-num').nth(19).click()  # chapter 20, TB only
        expect(page.get_by_text('Janganlah kamu kuatir')).to_be_visible()
        switch = page.locator('.read__lang')
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        expect(page.locator('#langSim')).to_have_attribute('aria-disabled', 'true')
        self.assertEqual(switch.get_attribute('data-edition'), 'tb')
        thumb = switch.locator('.read__lang-thumb')
        self.assertAlmostEqual(thumb.bounding_box()['x'],
                               page.locator('#langTb').bounding_box()['x'], delta=1)
        self.assertEqual(thumb.evaluate('el => el.getAnimations().length'), 0)
        page.close()

    def test_bible_language_links_keep_keyboard_and_no_js_navigation(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('.rail [data-panel="alkitab"]').click()
        page.locator('#panelBody .book').filter(has_text='Matius').first.click()
        page.locator('#chList .ch-num').nth(4).click()
        sim = page.locator('#langSim')
        sim.focus()
        sim.press('Enter')
        expect(sim).to_have_attribute('aria-pressed', 'true')
        self.assertEqual(page.evaluate('document.activeElement.id'), 'langSim')
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        page.locator('#langTb').press('Enter')
        expect(page.locator('#langTb')).to_have_attribute('aria-pressed', 'true')
        self.assertEqual(page.evaluate('document.activeElement.id'), 'langTb')
        page.close()

        context = self.browser.new_context(java_script_enabled=False, viewport={'width': 1280, 'height': 900})
        page = context.new_page()
        chapter_url = self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5])
        page.goto(chapter_url + '?ed=sim')
        expect(page.get_by_text('Garam ni dunia.')).to_be_visible()
        self.assertNotIn('is-enhanced', page.locator('.read__lang').get_attribute('class') or '')
        page.locator('#langTb').click()
        expect(page.get_by_text('Kamu adalah garam dunia.')).to_be_visible()
        self.assertIn('ed=tb', page.url)
        context.close()

    def test_populated_reading_headers_keep_their_space(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.locator('.result-group[data-kind="songs"] .result-row').first.click()
        expect(page.get_by_text('Di waktu pagi aku bersyukur')).to_be_visible()
        expect(page.locator('#readEyebrow')).to_be_visible()
        self.assertEqual(page.locator('#readEyebrow').evaluate(
            "el => getComputedStyle(el).marginBottom"), '10px')
        self.assertGreaterEqual(page.locator('.read__head-top').bounding_box()['height'], 34)

        page.locator('.rail [data-panel="tatib"]').click()
        page.locator('#panelBody').get_by_text('Ibadah Minggu III').first.click()
        expect(page.locator('#readEyebrow')).to_have_text('23 Agustus 2026')
        expect(page.locator('.read__project-btn[data-project-open]')).to_be_visible()
        self.assertGreaterEqual(page.locator('.read__head-top').bounding_box()['height'], 34)

    def test_tatib_date_and_project_button_are_vertically_centered(self):
        for width in (1440, 390):
            with self.subTest(width=width):
                page = self._page(width=width)
                page.goto(self.live_server_url + reverse('web-home'))
                page.locator('.rail [data-panel="tatib"]').click()
                page.locator('#panelBody').get_by_text('Ibadah Minggu III').first.click()
                expect(page.locator('#readEyebrow')).to_have_text('23 Agustus 2026')
                expect(page.locator('.read__project-btn[data-project-open]')).to_be_visible()
                self.assertEqual(page.locator('#readEyebrow').evaluate(
                    "el => getComputedStyle(el).marginBottom"), '0px')

                geometry = page.evaluate('''() => {
                  const box = selector => document.querySelector(selector).getBoundingClientRect();
                  const date = box('#readEyebrow');
                  const button = box('.read__project-btn[data-project-open]');
                  const row = box('.read__head-top');
                  const title = box('.read__title');
                  return {
                    centerDelta: (date.top + date.height / 2) - (button.top + button.height / 2),
                    dateRight: date.right,
                    buttonLeft: button.left,
                    rowBottom: row.bottom,
                    titleTop: title.top
                  };
                }''')
                self.assertLessEqual(abs(geometry['centerDelta']), 1, geometry)
                self.assertLessEqual(geometry['dateRight'], geometry['buttonLeft'], geometry)
                self.assertGreaterEqual(geometry['titleTop'], geometry['rowBottom'], geometry)
                page.close()

    def _eyebrow_style(self, page):
        """The header element's computed look, so two pages can be compared as rendered."""
        return page.locator('#readEyebrow').evaluate('''el => {
          const cs = getComputedStyle(el);
          return {text: el.textContent.trim(), size: cs.fontSize, tracking: cs.letterSpacing,
                  leading: cs.lineHeight, weight: cs.fontWeight, colour: cs.color,
                  opacity: cs.opacity};
        }''')

    def test_tatib_date_header_matches_songbook_header(self):
        """The service date and the songbook header are the same element and must read the same."""
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'waktu pagi')
        page.locator('.result-group[data-kind="songs"] .result-row').first.click()
        expect(page.locator('#readEyebrow')).to_be_visible()
        songbook = self._eyebrow_style(page)
        self.assertEqual(songbook['text'], 'Nyanyikanlah Kidung Baru 12')

        page.locator('.rail [data-panel="tatib"]').click()
        page.locator('#panelBody').get_by_text('Ibadah Minggu III').first.click()
        expect(page.locator('#readEyebrow')).to_have_text('23 Agustus 2026')
        service_date = self._eyebrow_style(page)
        page.close()

        for key in ('size', 'tracking', 'leading', 'weight', 'colour', 'opacity'):
            self.assertEqual(service_date[key], songbook[key],
                             '%s differs: date %s vs songbook %s' % (key, service_date, songbook))
        self.assertEqual(service_date['size'], '16.5px', service_date)
        self.assertEqual(service_date['weight'], '600', service_date)
        self.assertEqual(service_date['opacity'], '0.78', service_date)
        self.assertAlmostEqual(float(service_date['tracking'].replace('px', '')), 16.5 * 0.12,
                               delta=0.01, msg=service_date)
        self.assertAlmostEqual(float(service_date['leading'].replace('px', '')), 16.5 * 1.65,
                               delta=0.01, msg=service_date)

    def test_tatib_date_header_reflows_at_a_narrow_stage(self):
        """A stage too narrow for the date and Project keeps the date whole and the page still."""
        for width in (1440, 1280, 390):
            with self.subTest(width=width):
                page = self._page(width=width)
                try:
                    page.goto(self.live_server_url + reverse('web-home'))
                    page.locator('.rail [data-panel="tatib"]').click()
                    page.locator('#panelBody').get_by_text('Ibadah Minggu III').first.click()
                    expect(page.locator('#readEyebrow')).to_have_text('23 Agustus 2026')
                    geometry = page.evaluate('''() => {
                      const eyebrow = document.querySelector('#readEyebrow');
                      const box = eyebrow.getBoundingClientRect();
                      const button = document.querySelector('.read__project-btn').getBoundingClientRect();
                      const row = document.querySelector('.read__head-top').getBoundingClientRect();
                      const range = document.createRange();
                      range.selectNodeContents(eyebrow);
                      return {
                        size: getComputedStyle(eyebrow).fontSize,
                        boxWidth: box.width,
                        inkWidth: range.getBoundingClientRect().width,
                        clipped: eyebrow.scrollWidth - eyebrow.clientWidth,
                        docOverflow: document.documentElement.scrollWidth - window.innerWidth,
                        rowWidth: row.width,
                        pairWidth: box.width + 12 + button.width,
                        buttonOnItsOwnLine: button.top >= box.bottom + 4
                      };
                    }''')
                    self.assertEqual(geometry['size'], '16.5px', geometry)
                    self.assertGreaterEqual(geometry['boxWidth'] + 1, geometry['inkWidth'], geometry)
                    self.assertLessEqual(geometry['clipped'], 0, geometry)
                    self.assertLessEqual(geometry['docOverflow'], 0, geometry)
                    # the rule: both on one row while they fit, the Project action beneath the date when not
                    cannot_fit = geometry['pairWidth'] - 12 > geometry['rowWidth']
                    self.assertEqual(geometry['buttonOnItsOwnLine'], cannot_fit, geometry)
                finally:
                    page.close()

    def test_service_text_sidebar_shows_two_lines_and_centers_grip(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('.rail [data-panel="tatib"]').click()
        page.locator('#panelBody').get_by_text('Ibadah Minggu III').first.click()

        row = page.locator(f'#chList .songrow[data-i="e{self.preview_text_entry.pk}"]')
        label = row.locator('.songrow__t')
        expect(row).to_be_visible()
        self.assertEqual(label.locator('.songrow__line').all_inner_texts(),
                         ['First line', 'Second line'])
        self.assertGreater(row.bounding_box()['height'], 38)

        grip = row.locator('xpath=..').locator('.toc__grip')
        row.hover()
        expect(grip).to_be_visible()
        centers = row.evaluate("""row => {
          const grip = row.parentElement.querySelector('.toc__grip');
          const rowBox = row.getBoundingClientRect();
          const gripBox = grip.getBoundingClientRect();
          return {rowHeight: rowBox.height,
                  delta: (gripBox.top + gripBox.height / 2) - (rowBox.top + rowBox.height / 2)};
        }""")
        self.assertLessEqual(abs(centers['delta']), 1, f'grip is not centered: {centers}')

        blank_row = page.locator(f'#chList .songrow[data-i="e{self.blank_text_entry.pk}"]')
        blank_label = blank_row.locator('.songrow__t')
        blank_lines = blank_label.locator('.songrow__line')
        self.assertEqual(blank_lines.count(), 2)
        self.assertEqual(blank_lines.nth(0).inner_text(), 'Keep this')
        self.assertEqual(blank_lines.nth(1).get_attribute('class'),
                         'songrow__line songrow__line--blank')
        self.assertGreater(blank_row.evaluate("el => el.getBoundingClientRect().height"), 38)

        titled_row = page.locator(f'#chList .songrow[data-i="e{self.titled_text_entry.pk}"]')
        titled_label = titled_row.locator('.songrow__t')
        expect(titled_label).to_have_text('Kept sidebar title')
        self.assertFalse(titled_label.evaluate("el => el.classList.contains('songrow__t--lines')"))

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

    def test_clear_controls_in_search_and_filter_fields(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-book', args=[self.harian.id]))
        clear = page.locator('.ch__search .field-clear')
        expect(clear).to_be_hidden()                              # nothing typed yet
        expect(clear).to_have_attribute('aria-label', 'Clear songs')
        total = page.locator('#chList .songrow').count()
        page.fill('#songFilter', 'Lagu 1')
        expect(clear).to_be_visible()
        filtered = page.evaluate(
            "Array.from(document.querySelectorAll('#chList .songrow'))"
            ".filter(r => !r.closest('.is-hidden')).length")
        self.assertLess(filtered, total, 'the filter did not filter')
        clear.click()
        expect(page.locator('#songFilter')).to_have_value('')
        expect(clear).to_be_hidden()
        self.assertEqual(page.evaluate(
            "Array.from(document.querySelectorAll('#chList .songrow'))"
            ".filter(r => !r.closest('.is-hidden')).length"), total)
        self.assertTrue(page.evaluate(
            "document.activeElement === document.getElementById('songFilter')"),
            'focus did not return to the field')

        # the panel filter names what it clears
        page.goto(self.live_server_url + reverse('web-tatib'))
        panel_clear = page.locator('.panel__filter .field-clear')
        expect(panel_clear).to_be_hidden()
        expect(panel_clear).to_have_attribute('aria-label', 'Clear Tata Ibadah')
        page.fill('#bookFilter', 'Ibadah')
        expect(panel_clear).to_be_visible()
        panel_clear.focus()
        page.keyboard.press('Enter')
        expect(page.locator('#bookFilter')).to_have_value('')
        expect(panel_clear).to_be_hidden()
        self.assertTrue(page.evaluate(
            "document.activeElement === document.getElementById('bookFilter')"))

        # the search field
        page.goto(self.live_server_url + reverse('web-home'))
        search_clear = page.locator('.search-home .field-clear')
        expect(search_clear).to_be_hidden()
        expect(search_clear).to_have_attribute('aria-label', 'Clear search')
        self._search(page, 'waktu pagi')
        page.wait_for_selector('#searchStatus')
        expect(search_clear).to_be_visible()
        search_clear.click()
        expect(page.locator('#searchQuery')).to_have_value('')
        expect(search_clear).to_be_hidden()
        expect(page.get_by_text('Di Waktu Pagi', exact=True)).to_be_visible()   # results stay

    def test_tatib_mode_switch_keeps_open_service_and_reveals_its_row(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.big.pk]))
        original_stage = page.locator('#read').inner_text()
        page.fill('#songFilter', 'Bagian')
        page.evaluate("document.getElementById('chBody').scrollTop = 120")
        second_scroll = page.evaluate("document.getElementById('chBody').scrollTop")
        self.assertGreater(second_scroll, 0)
        page.fill('#bookFilter', 'no matching service')

        page.locator('#tatibMode').click()
        expect(page.locator('#tatibMode')).to_have_attribute('aria-pressed', 'true')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        expect(page.locator('#songFilter')).to_have_value('Bagian')
        self.assertEqual(page.locator('#read').inner_text(), original_stage)
        self.assertAlmostEqual(page.evaluate("document.getElementById('chBody').scrollTop"),
                               second_scroll, delta=2)
        # template mode does not hold this dated order: it is not listed, nothing is selected,
        # and no row is invented for it (spec 082)
        expect(page.locator('#panelBody .book[aria-current="true"]')).to_have_count(0)
        expect(page.locator('#panelBody')).not_to_contain_text('Currently open')

        # back in its own mode its own row is selected again, filtered back into view
        page.locator('#tatibMode').click()
        expect(page.locator('#tatibMode')).to_have_attribute('aria-pressed', 'false')
        expect(page.locator('#bookFilter')).to_have_value('')
        expect(page.locator('#songFilter')).to_have_value('Bagian')
        selected = page.locator('#panelBody .book[aria-current="true"]')
        expect(selected).to_have_count(1)
        expect(selected).to_have_attribute('data-name', str(self.big.pk))
        page.wait_for_function("document.documentElement.dataset.scrollAnim !== 'on'")
        visible = selected.evaluate("""row => {
            const r = row.getBoundingClientRect();
            const b = document.getElementById('panelBody').getBoundingClientRect();
            return r.top >= b.top + 7 && r.bottom <= b.bottom - 7;
        }""")
        self.assertTrue(visible, 'the selected row was not revealed')

        page.locator('#chCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-ch', 'closed')
        page.locator('#tatibMode').click()
        expect(page.locator('html')).to_have_attribute('data-ch', 'closed')

    def test_tatib_mode_switch_keeps_template_and_no_page_state(self):
        template = self.mode_template
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[template.pk]))
        page.set_viewport_size({'width': 390, 'height': 844})
        page.emulate_media(reduced_motion='reduce')
        # The first pane sits behind the open second pane at this width; its
        # state must still survive the mode action when that level is surfaced.
        page.locator('#tatibMode').evaluate('el => el.click()')
        # this template is not in the dated list: nothing is selected, and no row is invented
        expect(page.locator('#panelBody .book[aria-current="true"]')).to_have_count(0)
        expect(page.locator('#panelBody')).not_to_contain_text('Currently open')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')

        page.goto(self.live_server_url + reverse('web-tatib'))
        page.locator('#tatibMode').click()
        expect(page.locator('#panelBody .book[aria-current="true"]')).to_have_count(0)
        expect(page.locator('html')).to_have_attribute('data-ch', 'closed')

    def test_clear_controls_have_matching_hit_areas_and_centered_icons(self):
        page = self._page()
        for url, field, wrapper in (
            (reverse('web-book', args=[self.harian.id]), '#songFilter', '.ch__search .filter-box'),
            (reverse('web-tatib'), '#bookFilter', '.panel__filter .filter-box'),
            (reverse('web-home'), '#searchQuery', '.search-home__form'),
        ):
            page.goto(self.live_server_url + url)
            page.fill(field, 'test')
            geometry = page.locator(wrapper).evaluate("""box => {
                const button = box.querySelector('.field-clear');
                const input = box.querySelector('input');
                const svg = button.querySelector('svg');
                const b = button.getBoundingClientRect();
                const i = input.getBoundingClientRect();
                const s = svg.getBoundingClientRect();
                const w = box.getBoundingClientRect();
                return {
                    button: [b.width, b.height], icon: [s.width, s.height],
                    centered: [Math.abs((b.left + b.right - s.left - s.right) / 2),
                               Math.abs((b.top + b.bottom - s.top - s.bottom) / 2)],
                    right: w.right - b.right,
                    clearance: b.left - (i.right - parseFloat(getComputedStyle(input).paddingRight)),
                };
            }""")
            self.assertEqual(geometry['button'], [26, 26], field)
            self.assertEqual(geometry['icon'], [14, 14], field)
            self.assertLessEqual(max(geometry['centered']), 1, field)
            self.assertAlmostEqual(geometry['right'], 58 if field == '#searchQuery' else 8,
                                   delta=1, msg=field)
            self.assertGreaterEqual(geometry['clearance'], 4, field)
            button = page.locator(wrapper + ' .field-clear')
            button.hover()
            page.wait_for_timeout(250)  # let the existing color transition finish
            self.assertNotEqual(button.evaluate(
                "el => getComputedStyle(el).backgroundColor"), 'rgba(0, 0, 0, 0)')
            page.locator(field).focus()
            page.keyboard.press('Tab')
            self.assertEqual(button.evaluate(
                "el => getComputedStyle(el).outlineStyle"), 'solid')
            page.set_viewport_size({'width': 390, 'height': 844})
            page.evaluate("document.documentElement.dataset.theme = 'dark'")
            self.assertEqual(button.evaluate(
                "el => [el.getBoundingClientRect().width, el.getBoundingClientRect().height]"),
                [26, 26])
            page.set_viewport_size({'width': 1280, 'height': 900})

    def test_sidebar_filters_reset_only_on_main_menu_switch(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-book', args=[self.harian.id]))
        page.fill('#bookFilter', 'not a songbook')
        page.fill('#songFilter', 'Lagu 1')
        expect(page.locator('.panel__filter .field-clear')).to_be_visible()
        expect(page.locator('.ch__search .field-clear')).to_be_visible()

        # Closing and reopening the active menu keeps both filters.
        page.locator('.rail [data-panel="kidung"]').click()
        page.locator('.rail [data-panel="kidung"]').click()
        expect(page.locator('#bookFilter')).to_have_value('not a songbook')
        expect(page.locator('#songFilter')).to_have_value('Lagu 1')

        page.locator('.rail [data-panel="tatib"]').click()
        expect(page.locator('html')).to_have_attribute('data-section', 'tatib')
        expect(page.locator('#bookFilter')).to_have_value('')
        expect(page.locator('#songFilter')).to_have_value('')
        expect(page.locator('.panel__filter .field-clear')).to_be_hidden()
        expect(page.locator('.ch__search .field-clear')).to_be_hidden()
        self.assertGreater(page.locator('#panelBody .book:not(.is-hidden)').count(), 0)

        page.locator('.rail [data-panel="kidung"]').click()
        expect(page.locator('html')).to_have_attribute('data-section', 'kidung')
        self.assertGreater(page.locator('#panelBody .book:not(.is-hidden)').count(), 0)
        expect(page.locator('#bookFilter')).to_have_value('')

        page.set_viewport_size({'width': 390, 'height': 844})
        page.fill('#bookFilter', 'songbook')
        page.locator('.rail [data-panel="alkitab"]').click()
        expect(page.locator('html')).to_have_attribute('data-section', 'alkitab')
        expect(page.locator('#bookFilter')).to_have_value('')

    def test_search_menu_resets_sidebar_filters_without_erasing_query(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        self._search(page, 'kasih')
        page.wait_for_selector('#searchStatus')
        page.locator('.rail [data-panel="tatib"]').click()
        page.fill('#bookFilter', 'Ibadah')
        page.locator('#railSearch').click()
        expect(page.get_by_text('Results for').first).to_be_visible()
        expect(page.locator('#bookFilter')).to_have_value('')
        expect(page.locator('.panel__filter .field-clear')).to_be_hidden()
        expect(page.locator('#searchQuery')).to_have_value('kasih')

    def test_hymn_song_order_is_visible_after_browsing_from_home(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.locator('.rail [data-panel="kidung"]').click()
        page.locator('#panelBody .book').filter(has_text=self.book.name).first.click()

        rows = page.locator('#chList .songrow')
        expect(rows).to_have_count(6)
        self.assertEqual(
            rows.evaluate_all("els => els.map(el => el.dataset.num || "
                              "el.querySelector('.songrow__t').textContent.trim())"),
            ['NKB 2', 'NKB 10', 'NKB 12', 'NKB 12A', 'NKB 12B', 'Legacy'],
        )
        expect(page.locator('#songSort')).to_be_hidden()

    def test_song_sort_toggles_between_last_modified_and_alphabetical(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-book', args=[self.harian.id]))
        sort = page.locator('#songSort')
        expect(sort).to_be_visible()
        rows = page.locator('#chList .songrow')
        expect(sort).to_have_attribute('data-order', 'm')
        expect(rows.first).to_contain_text('Zebra')      # last modified: Zebra is newest
        sort.click()
        expect(sort).to_have_attribute('data-order', 'title')
        expect(rows.first).to_contain_text('Alpha')      # alphabetical
        sort.click()
        expect(sort).to_have_attribute('data-order', 'm')
        expect(rows.first).to_contain_text('Zebra')      # and back again

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

    def _wait_for_stage_flash(self, page, anchor, active=True):
        page.wait_for_function(
            "([anchor, active]) => {"
            "const row = document.getElementById('ti-' + anchor);"
            "return !!row && row.classList.contains('tatib__flash') === active;"
            "}", arg=[anchor, active], timeout=3500)

    def test_tatib_quicklink_flash_repeats_after_animation_ends(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        anchor = 'e%d' % self.flash_first.pk
        row = page.locator('#chList .songrow[data-i="%s"]' % anchor)

        row.click()
        self._wait_for_stage_flash(page, anchor)
        self._wait_for_stage_flash(page, anchor, active=False)

        row.click()
        self._wait_for_stage_flash(page, anchor)

    def test_tatib_quicklink_during_flash_is_ignored_not_queued(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        first_anchor = 'e%d' % self.flash_first.pk
        second_anchor = 'e%d' % self.flash_second.pk
        first = page.locator('#chList .songrow[data-i="%s"]' % first_anchor)
        second = page.locator('#chList .songrow[data-i="%s"]' % second_anchor)

        first.click()
        self._wait_for_stage_flash(page, first_anchor)
        page.wait_for_timeout(150)
        first.click()
        second.click()
        self.assertTrue(page.locator('#ti-' + first_anchor).evaluate(
            "el => el.classList.contains('tatib__flash')"))
        self.assertFalse(page.locator('#ti-' + second_anchor).evaluate(
            "el => el.classList.contains('tatib__flash')"))

        self._wait_for_stage_flash(page, first_anchor, active=False)
        self.assertFalse(page.locator('#ti-' + second_anchor).evaluate(
            "el => el.classList.contains('tatib__flash')"))
        second.click()
        self._wait_for_stage_flash(page, second_anchor)

    def test_tatib_quicklink_flash_releases_when_stage_is_replaced(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        first_anchor = 'e%d' % self.flash_first.pk
        page.locator('#chList .songrow[data-i="%s"]' % first_anchor).click()
        self._wait_for_stage_flash(page, first_anchor)

        page.locator('#panelBody').get_by_text('Ibadah 01').click()
        expect(page.get_by_text('Isi ibadah 01')).to_be_visible()
        row = page.locator('#chList a.songrow[href^="#ti-"]').first
        anchor = row.get_attribute('href').split('#ti-')[-1]
        row.click()
        self._wait_for_stage_flash(page, anchor)

    def test_tatib_quicklink_keyboard_activation_starts_flash(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        anchor = 'e%d' % self.flash_first.pk
        row = page.locator('#chList .songrow[data-i="%s"]' % anchor)

        row.focus()
        page.keyboard.press('Enter')
        self._wait_for_stage_flash(page, anchor)

    def test_tatib_quicklink_respects_reduced_motion_without_locking(self):
        page = self._page()
        page.emulate_media(reduced_motion='reduce')
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        anchor = 'e%d' % self.flash_first.pk
        row = page.locator('#chList .songrow[data-i="%s"]' % anchor)

        row.click()
        self.assertFalse(page.locator('#ti-' + anchor).evaluate(
            "el => el.classList.contains('tatib__flash')"))
        page.emulate_media(reduced_motion='no-preference')
        row.click()
        self._wait_for_stage_flash(page, anchor)

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
        expect(page.locator('#railSearch')).to_have_attribute('href', '/')
        page.locator('#railSearch').click()
        page.wait_for_function("document.documentElement.dataset.home === 'landing'")
        expect(page).to_have_url(self.live_server_url + '/')
        expect(page.locator('html')).to_have_attribute('data-section', 'alkitab')
        expect(page.locator('.search-home__hint')).to_have_count(0)
        self.assertEqual(page.evaluate("localStorage.getItem('gkps-search')"), '/tatib/1/')
        # The logo opens a blank index; legacy shared state stays present but ignored.
        page.locator('.rail__logo').click()
        page.wait_for_function("document.documentElement.dataset.home === 'landing'")
        expect(page).to_have_url(self.live_server_url + '/')
        expect(page.locator('.search-home__hint')).to_have_count(0)

    def test_index_is_empty_but_search_restores_tab_local_state(self):
        page = self._page()
        page.goto(self.live_server_url + '/')
        self._search(page, 'kasih')
        page.wait_for_selector('#searchStatus')
        page.locator('#searchQuery').fill('unsent text')
        page.locator('.rail__logo').click()
        expect(page).to_have_url(self.live_server_url + '/')
        expect(page.locator('#searchQuery')).to_have_value('')
        page.locator('#railSearch').click()
        expect(page.get_by_text('Results for').first).to_be_visible()
        expect(page.locator('#searchQuery')).to_have_value('unsent text')

        # A pasted search URL replaces this tab's latest search snapshot.
        direct_url = self.live_server_url + reverse('web-search') + '?q=Di%20Waktu%20Pagi'
        page.goto(direct_url)
        page.wait_for_selector('#searchStatus')
        expect(page.locator('#searchQuery')).to_have_value('Di Waktu Pagi')
        expect(page.locator('#railSearch')).to_have_attribute(
            'href', reverse('web-search') + '?q=Di%20Waktu%20Pagi')
        page.locator('#railSearch').click()
        expect(page.locator('#searchQuery')).to_have_value('Di Waktu Pagi')
        expect(page.get_by_text('Results for').first).to_be_visible()

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
        stored_id = page.evaluate("sessionStorage.getItem('gkps-search-last-tab')")
        self.assertTrue(stored_id)
        snapshot = page.evaluate(
            "id => sessionStorage.getItem('gkps-search-entry:' + id)", stored_id)
        self.assertIn('/search?q=kasih', snapshot)
        self.assertIn('kasih', snapshot)
        page.locator('#railSearch').click()
        page.wait_for_selector('#searchStatus')
        expect(page.get_by_text('Results for').first).to_be_visible()
        # The remembered offset is restored with an animation: wait for the scroll to
        # settle before reading it, rather than racing a fixed pause.
        page.wait_for_function('''() => {
          const y = window.scrollY;
          if (window.__lastY === y) { window.__stable = (window.__stable || 0) + 1; }
          else { window.__stable = 0; }
          window.__lastY = y;
          return window.__stable >= 5 && y > 100;
        }''', timeout=5000)
        resumed = page.evaluate('window.scrollY')
        self.assertGreater(resumed, 100, f'the result set was not resumed at an offset: {resumed}')
        self.assertLessEqual(resumed, offset)
        self.assertGreaterEqual(resumed, offset - 60, f'resumed far from the remembered offset: {resumed} vs {offset}')


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SidebarStateOnItemOpenTests(StaticLiveServerTestCase):
    """Opening a page from a second-level list keeps the first sidebar as it was (spec 080).

    Every reading page is rendered with `data-nav="open"`, so copying the arriving page's
    value over the live one is what sprang a collapsed (or mini) first panel open.
    """

    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=language, name='Terjemahan Baru', abbreviation='TB')
        self.mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        translation = bible.BookTranslation.objects.create(
            version=version, book=self.mat, translation='Matius')
        for chapter in (5, 20):
            bible.Verse.objects.create(book_translation=translation, chapter=chapter, verse=1,
                                       text='Isi pasal %d' % chapter)
        self.mar = bible.Book.objects.create(name='Mar', testament='new', number_of_chapters=16)
        bible.BookTranslation.objects.create(
            version=version, book=self.mar, translation='Markus')
        self.songbook = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        for number in (1, 2):
            song = songs.Song.objects.create(
                book=self.songbook, number=number, title='Nyanyian %d' % number)
            songs.Verse.objects.create(song=song, number=1, lyric='Bait pertama')
        # An empty service, so its pane offers the empty state's Add Text
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 8, 23), is_active=True)

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
        return self.browser.new_page(viewport={'width': width, 'height': height})

    def _add_text_entry(self, page):
        page.locator('.entry__empty-btn', has_text='Add Text').click()
        expect(page.locator('#id_text')).to_be_visible()
        page.fill('#id_text', 'L : Marilah kita bangun berdiri.')
        page.click('.editor__save')
        page.wait_for_function(
            "() => document.getElementById('readBody').innerText.indexOf('Marilah kita bangun berdiri') !== -1")

    def test_a_collapsed_tata_ibadah_panel_survives_adding_an_entry(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.locator('#panelCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')

        self._add_text_entry(page)

        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        expect(page.locator('#read')).to_contain_text('Marilah kita bangun berdiri')

    def test_a_collapsed_songbook_panel_survives_opening_a_song(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-book', args=[self.songbook.pk]))
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        page.locator('#panelCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')

        page.locator('#chList a.songrow').first.click()

        expect(page.locator('#read')).to_contain_text('Nyanyian 1')
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        expect(page.locator('#chList a.songrow[aria-current="true"]')).to_have_count(1)

    def test_a_mini_bible_panel_survives_opening_a_chapter(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        page.locator('#panelCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

        page.locator('#chList a.ch-num', has_text='20').first.click()

        expect(page.locator('#read')).to_contain_text('Isi pasal 20')
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

    def test_selecting_a_bible_book_preserves_the_mini_panel(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-bible-chapter', args=[self.mat.pk, 5]))
        page.locator('#panelCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

        mar = page.locator('#panelBody a.book[href="%s"]' % reverse('web-bible-book', args=[self.mar.pk]))
        mar.click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        expect(page.locator('#panelBody a.book[aria-current="true"]')).to_have_attribute(
            'href', reverse('web-bible-book', args=[self.mar.pk]))
        expect(page.locator('#chTitle')).to_contain_text('Markus')
        expect(page.locator('#chList a.ch-num')).to_have_count(16)

        mar.click()
        expect(page.locator('html')).to_have_attribute('data-ch', 'closed')
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')
        mar.click()
        expect(page.locator('html')).to_have_attribute('data-ch', 'open')
        expect(page.locator('html')).to_have_attribute('data-nav', 'mini')

        page.locator('#panelExpand').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        page.locator('#panelBody a.book[href="%s"]' % reverse('web-bible-book', args=[self.mat.pk])).click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.locator('#chTitle')).to_contain_text('Matius')
        expect(page.locator('#chList a.ch-num')).to_have_count(28)

    def test_a_main_menu_switch_still_opens_the_arriving_panel(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('#panelCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')

        page.locator('a.rail__btn[data-panel="kidung"]').click()

        expect(page.locator('html')).to_have_attribute('data-nav', 'open')
        expect(page.locator('#panelBody')).to_contain_text('Kidung Jemaat')
        expect(page.locator('html')).to_have_attribute('data-ch', 'closed')

    def test_a_collapsed_panel_survives_opening_a_song_at_a_narrow_width(self):
        # At this width the first panel covers the song list, so collapsing it is the
        # only way to reach a song — and the song must not push it back open.
        page = self._page(width=390, height=844)
        page.goto(self.live_server_url + reverse('web-book', args=[self.songbook.pk]))
        page.locator('#panelCollapse').click()
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')

        page.locator('#chList a.songrow').first.click()

        expect(page.locator('#read')).to_contain_text('Nyanyian 1')
        expect(page.locator('html')).to_have_attribute('data-nav', 'closed')




@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ScrollbarE2ETests(StaticLiveServerTestCase):
    """The reading UI's scrollbars (spec 087): 5px, custom path, bare ends.

    The mechanism is the point. Chromium takes the custom ``::-webkit-scrollbar``
    path only while the standard properties are absent; set them and the native
    thin bar is painted instead -- 10px, with a stepper glyph at each end. So the
    occupied width and the computed ``scrollbar-width`` together say which bar the
    app is actually getting.
    """

    def setUp(self):
        super().setUp()
        # enough songbooks that the panel's list overflows its pane
        for number in range(1, 41):
            songs.Book.objects.create(name='Kidung %02d' % number, is_hymn_book=False)
        self._playwright = sync_playwright().start()
        try:
            # Playwright hides the scrollbars by default (`--hide-scrollbars`), which
            # would make every bar measure 0px and this module prove nothing.
            self.browser = self._playwright.chromium.launch(
                ignore_default_args=['--hide-scrollbars'])
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 720})
        page.goto(self.live_server_url + reverse('web-home'))
        page.wait_for_load_state('networkidle')
        page.click('.rail__btn[aria-label="Kidung"]')
        page.wait_for_selector('#panelBody li')
        page.wait_for_function(
            "() => { const b = document.getElementById('panelBody');"
            " return b.scrollHeight > b.clientHeight; }")
        return page

    def _metrics(self, page):
        return page.evaluate("""() => {
          const body = document.getElementById('panelBody');
          const style = getComputedStyle(body);
          const borders = parseFloat(style.borderLeftWidth) + parseFloat(style.borderRightWidth);
          return {
            occupied: body.offsetWidth - body.clientWidth - borders,
            scrollbarWidth: style.scrollbarWidth,
            overflows: body.scrollHeight > body.clientHeight,
          };
        }""")

    def test_the_panel_scrollbar_takes_five_pixels_and_the_custom_path(self):
        page = self._page()
        metrics = self._metrics(page)
        self.assertTrue(metrics['overflows'], 'the fixture list did not overflow')
        self.assertEqual(metrics['occupied'], 5, 'the bar is not the custom 5px one')
        self.assertEqual(metrics['scrollbarWidth'], 'auto',
                         'the standard properties are in play: this is the native bar')

        page.evaluate("() => { document.documentElement.dataset.theme = 'dark'; }")
        dark = self._metrics(page)
        self.assertEqual(dark['occupied'], 5, 'the bar changes width with the theme')
        self.assertEqual(dark['scrollbarWidth'], 'auto')

        # the control: with the standard properties put back, the engine takes the
        # native bar -- 10px here -- so the two measures above do tell them apart
        page.add_style_tag(content='#panelBody { scrollbar-width: thin; }')
        native = self._metrics(page)
        self.assertEqual(native['occupied'], 10, 'the control did not reach the native bar')
        self.assertEqual(native['scrollbarWidth'], 'thin')

    def test_the_bar_has_no_stepper_glyph_at_its_ends(self):
        """Scrolled mid-list the bar's top end paints nothing but its transparent
        track, so it matches the surface beside it -- a stepper button would not."""
        page = self._page()
        bar_top, beside = self._ends(page)
        self.assertEqual(bar_top, beside,
                         "something is painted over the track at the bar's top end")

        # the control: on the native path the same two strips differ, since that bar
        # paints its stepper button at the end
        page.add_style_tag(content='#panelBody { scrollbar-width: thin; }')
        native_bar_top, native_beside = self._ends(page)
        self.assertNotEqual(native_bar_top, native_beside,
                            'the strips cannot tell the two bars apart')

    def _ends(self, page):
        """The bar's top 5px column, and the 5px of surface just inside it."""
        box = page.evaluate("""() => {
          const body = document.getElementById('panelBody');
          body.scrollTop = (body.scrollHeight - body.clientHeight) / 2;
          const r = body.getBoundingClientRect();
          return {right: Math.round(r.right), top: Math.round(r.top)};
        }""")
        clip = {'y': box['top'] + 4, 'width': 5, 'height': 12}
        return (page.screenshot(clip=dict(clip, x=box['right'] - 5)),
                page.screenshot(clip=dict(clip, x=box['right'] - 10)))
