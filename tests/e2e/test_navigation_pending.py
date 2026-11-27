"""Spec 243: pending state for rail and sidebar fetches.

Each case uses CDP latency so the in-flight state can be observed before the
fetched page paints. No production code is referenced by name here; the tests
assert what the operator can see and the accessibility state of the shell.
"""
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from playwright.sync_api import expect, sync_playwright

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


def slow_network(page, latency=1800):
    """Delay every subsequent request without blocking the Python client."""
    cdp = page.context.new_cdp_session(page)
    cdp.send('Network.enable')
    cdp.send('Network.emulateNetworkConditions', {
        'offline': False,
        'latency': latency,
        'downloadThroughput': 10 * 1024 * 1024,
        'uploadThroughput': 10 * 1024 * 1024,
    })


@override_settings(DEBUG=True,
                   STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
@tag('e2e')
class NavigationPendingTests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='TB', abbreviation='TB')
        self.book = bible.Book.objects.create(name='Kej', testament='old',
                                              number_of_chapters=2)
        translation = bible.BookTranslation.objects.create(
            version=version, book=self.book, translation='Kejadian')
        for chapter in (1, 2):
            bible.Verse.objects.create(book_translation=translation, chapter=chapter,
                                       verse=1, text='Verse ' + str(chapter))
        self.songbook = songs.Book.objects.create(name='Pelengkap Kidung Jemaat',
                                                   short_name='PKJ', is_hymn_book=True)
        self.song = songs.Song.objects.create(book=self.songbook, title='Mulia, Mulia NamaNya',
                                              number=2)
        songs.Verse.objects.create(song=self.song, number=1, lyric='Lyric one')
        self.plain_book = songs.Book.objects.create(name='Lagu', short_name='LG')
        self.plain_song = songs.Song.objects.create(book=self.plain_book,
                                                    title='Boras Tenger')
        songs.Verse.objects.create(song=self.plain_song, number=1, lyric='Plain lyric')
        self.service = tatib.TataIbadah.objects.create(
            name='Service test', date=date(2026, 11, 25), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=0, title='Opening', text='Body',
            order_number=1)

    def open_home(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + '/')
        return playwright, browser, page

    def test_a_rail_click_locks_the_item_and_bars_both_lists(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            # The bar belongs to an open sidebar; open both columns first.
            page.evaluate("document.documentElement.dataset.nav='open';"
                          "document.documentElement.dataset.ch='open'")
            rail = page.locator('.rail [data-panel="kidung"]')
            rail.click()
            expect(rail).to_have_attribute('aria-disabled', 'true')
            opacity = rail.locator('svg').evaluate('(e) => getComputedStyle(e).opacity')
            self.assertEqual(opacity, '0.45')
            expect(page.locator('#panel > .pv-section-bar')).to_be_visible(timeout=1000)
            expect(page.locator('#chapters > .pv-section-bar')).to_be_visible(timeout=1000)
            self.assertIsNone(page.locator('.stage').get_attribute('aria-busy'))
            self.assertFalse(page.locator('.pv-placeholder').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_a_list_only_fetch_leaves_the_stage_untouched(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            slow_network(page)
            before = page.locator('#readName').inner_text()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            self.assertEqual(page.locator('#readName').inner_text(), before)
            self.assertIsNone(page.locator('.stage').get_attribute('aria-busy'))
            self.assertFalse(page.locator('#chapters > .pv-section-bar').is_visible())
            self.assertFalse(page.locator('.pv-placeholder').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_a_verse_write_seeds_the_bible_placeholder(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            slow_network(page)
            page.locator('#chList .ch-num').first.click()
            expect(page.locator('.stage')).to_have_attribute('aria-busy', 'true')
            ph = page.locator('#pvPh-bible')
            self.assertTrue(ph.is_visible())
            self.assertEqual(ph.locator('.pv-ph-name').inner_text(), 'Kejadian')
            self.assertEqual(ph.locator('.pv-ph-no').inner_text(), '1')
            self.assertEqual(ph.locator('p.v').count(), 5)
            self.assertTrue(page.locator('.stage > .pv-stagebar').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_placeholder_origin_matches_the_real_read(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            page.locator('#chList .ch-num').first.click()
            expect(page.locator('#read')).to_be_visible(timeout=5000)
            real = page.locator('#read').bounding_box()
            slow_network(page)
            page.locator('#chList .ch-num').nth(1).click()
            expect(page.locator('#pvPh-bible')).to_be_visible(timeout=1000)
            expect(page.locator('#pvPh-bible .read')).to_be_visible(timeout=1000)
            ph = page.locator('#pvPh-bible .read').bounding_box()
            self.assertEqual(round(ph['x']), round(real['x']))
            self.assertEqual(round(ph['y']), round(real['y']))
        finally:
            browser.close()
            playwright.stop()

    def test_settlement_clears_the_busy_state(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            slow_network(page, latency=900)
            page.locator('#chList .ch-num').first.click()
            expect(page.locator('#read')).to_have_attribute('data-kind', 'bible')
            page.wait_for_timeout(1200)
            self.assertIsNone(page.locator('.stage').get_attribute('aria-busy'))
            self.assertFalse(page.locator('#pvPh-bible').is_visible())
            self.assertFalse(page.locator('.stage > .pv-stagebar').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_write_then_write_cancels_the_first(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            slow_network(page)
            first = page.locator('#chList .ch-num').first
            first.click()
            page.locator('#chList .ch-num').nth(1).click()
            self.assertIsNone(first.get_attribute('aria-disabled'))
            self.assertEqual(page.locator('#pvPh-bible .pv-ph-no').inner_text(), '2')
            self.assertTrue(page.locator('.stage > .pv-stagebar').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_write_then_list_keeps_the_first_and_adds_a_list_bar(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            slow_network(page)
            page.locator('#chList .ch-num').first.click()
            page.locator('.rail [data-panel="kidung"]').click()
            self.assertEqual(page.locator('.stage').get_attribute('aria-busy'), 'true')
            self.assertTrue(page.locator('#panel > .pv-section-bar').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_list_then_write_cancels_the_list(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            slow_network(page)
            rail = page.locator('.rail [data-panel="kidung"]')
            rail.click()
            page.locator('#chList .ch-num').first.click()
            self.assertIsNone(rail.get_attribute('aria-disabled'))
            self.assertEqual(page.locator('.stage').get_attribute('aria-busy'), 'true')
            self.assertFalse(page.locator('#panel > .pv-section-bar').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_a_cancelled_item_can_be_clicked_again(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            rail = page.locator('.rail [data-panel="kidung"]')
            rail.click()
            page.locator('.rail [data-panel="alkitab"]').click()
            rail.click()
            self.assertEqual(rail.get_attribute('aria-disabled'), 'true')
        finally:
            browser.close()
            playwright.stop()

    def test_a_song_write_matches_the_real_song_header(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="kidung"]').click()
            page.locator(f'#panelBody .book[href="/songs/book/{self.songbook.pk}/"]').click()
            expect(page.locator('#chList .songrow')).to_be_visible(timeout=5000)
            slow_network(page)
            row = page.locator('#chList .songrow').first
            shown = row.locator('.songrow__t').inner_text()
            number = row.locator('.songrow__c').inner_text()
            row.click()
            expect(page.locator('#pvPh-song')).to_be_visible(timeout=1000)
            ph = page.locator('#pvPh-song')
            self.assertEqual(ph.locator('.pv-ph-eyebrow').inner_text(), number)
            self.assertEqual(ph.locator('.pv-ph-name').inner_text(), shown)
            self.assertFalse(ph.locator('.pv-ph-no').is_visible())
            self.assertEqual(ph.locator('.read__sec').count(), 0)
            self.assertEqual(ph.locator('p.v').count(), 3)
            self.assertTrue(ph.locator('p.v').first.locator('.v__n').inner_text(), '1')
        finally:
            browser.close()
            playwright.stop()

    def test_a_service_write_seeds_the_service_header(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="tatib"]').click()
            row = page.locator(f'#panelBody .book[href="/tatib/{self.service.pk}/"]')
            expect(row).to_be_visible(timeout=5000)
            slow_network(page)
            name = row.locator('.book__n').inner_text()
            row.click()
            expect(page.locator('#pvPh-tatib')).to_be_visible(timeout=1000)
            ph = page.locator('#pvPh-tatib')
            self.assertEqual(ph.locator('.pv-ph-eyebrow').text_content(), 'Tata Ibadah')
            self.assertEqual(ph.locator('.pv-ph-name').inner_text(), name)
            self.assertEqual(ph.locator('.tatib__item').count(), 3)
        finally:
            browser.close()
            playwright.stop()

    def test_a_non_hymn_song_placeholder_names_its_songbook(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="kidung"]').click()
            page.locator(f'#panelBody .book[href="/songs/book/{self.plain_book.pk}/"]').click()
            expect(page.locator('#chList .songrow')).to_be_visible(timeout=5000)
            slow_network(page)
            page.locator('#chList .songrow').first.click()
            expect(page.locator('#pvPh-song')).to_be_visible(timeout=1000)
            ph = page.locator('#pvPh-song')
            self.assertEqual(ph.locator('.pv-ph-eyebrow').text_content(), 'Lagu')
            self.assertEqual(ph.locator('.pv-ph-name').inner_text(), 'Boras Tenger')
            self.assertFalse(ph.locator('.pv-ph-no').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_destination_placeholder_hides_the_previous_search_home(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            page.locator('#railMediaLibrary').click()
            expect(page.locator('#pvPh-media-library')).to_be_visible(timeout=1000)
            for sel in ('#searchHome', '#homeLogo', '#searchQuery'):
                self.assertFalse(page.locator(sel).is_visible(), sel)
        finally:
            browser.close()
            playwright.stop()

    def test_media_library_direct_load_shows_a_loading_state(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        try:
            slow_network(page, latency=1500)
            page.goto(self.live_server_url + '/media-library/', wait_until='commit')
            expect(page.locator('#mediaResultCount')).to_have_text('Loading files…', timeout=8000)
            expect(page.locator('#mediaEmpty')).to_contain_text(
                'Loading files on this computer…', timeout=8000)
            spinner = page.locator('#mediaEmpty .media-library__loading-spinner')
            expect(spinner).to_be_visible(timeout=8000)
            self.assertEqual(spinner.evaluate('(e) => getComputedStyle(e).animationDuration'), '0.8s')
            self.assertEqual(spinner.evaluate('(e) => getComputedStyle(e).display'), 'block')
            above = page.evaluate("""() => {
              const spinner = document.querySelector('#mediaEmpty .media-library__loading-spinner');
              const range = document.createRange();
              range.selectNodeContents(document.getElementById('mediaEmpty'));
              const nodes = Array.from(document.getElementById('mediaEmpty').childNodes)
                .filter(n => n.nodeType === Node.TEXT_NODE);
              if (!nodes.length) return false;
              range.selectNode(nodes[0]);
              return spinner.getBoundingClientRect().bottom <= range.getBoundingClientRect().top;
            }""")
            self.assertTrue(above, 'spinner must sit above the loading text')
            expect(page.locator('#mediaResultCount')).to_contain_text('files shown', timeout=8000)
            self.assertEqual(page.locator('#mediaEmpty .media-library__loading-spinner').count(), 0)
        finally:
            browser.close()
            playwright.stop()

    def test_search_rail_locks_the_tile(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            tile = page.locator('#railSearch')
            tile.click()
            expect(tile).to_have_attribute('aria-disabled', 'true')
            opacity = tile.locator('svg').evaluate('(e) => getComputedStyle(e).opacity')
            self.assertEqual(opacity, '0.45')
            self.assertEqual(page.locator('.stage').get_attribute('aria-busy'), 'true')
        finally:
            browser.close()
            playwright.stop()

    def test_search_rail_shows_the_stage_bar(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            page.locator('#railSearch').click()
            bar = page.locator('.stage > .pv-stagebar')
            expect(bar).to_be_visible(timeout=1000)
            self.assertEqual(bar.evaluate('(e) => getComputedStyle(e).height'), '3px')
            offset = bar.evaluate('(e) => e.getBoundingClientRect().top '
                                  '- e.parentElement.getBoundingClientRect().top')
            self.assertEqual(round(offset), 0)
        finally:
            browser.close()
            playwright.stop()

    def test_search_results_placeholder_matches_real_groups(self):
        playwright, browser, page = self.open_home()
        try:
            page.evaluate("""() => {
              sessionStorage.setItem('gkps-search-last-tab', 'x');
              sessionStorage.setItem('gkps-search-entry:x', JSON.stringify({
                url: '/search/?q=Yoh+3%3A16', query: 'Yoh 3:16'}));
            }""")
            page.reload()
            slow_network(page)
            page.locator('#railSearch').click()
            ph = page.locator('#pvPh-results')
            expect(ph).to_be_visible(timeout=1000)
            self.assertEqual(ph.locator('.result-group').count(), 2)
            self.assertEqual(ph.locator('.result-group__head').count(), 2)
            self.assertEqual(ph.locator('.result-row').count(), 5)
            self.assertEqual(ph.locator('.result-row__excerpt').count(), 3)
            expect(ph.locator('.result-more')).to_be_visible()
        finally:
            browser.close()
            playwright.stop()

    def test_search_home_placeholder_matches_the_landing(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            page.locator('#railSearch').click()
            ph = page.locator('#pvPh-search-home')
            expect(ph).to_be_visible(timeout=1000)
            logo = ph.locator('.search-home__logo')
            self.assertEqual(logo.evaluate('(e) => getComputedStyle(e).width'), '96px')
            expect(ph.locator('.search-home__form')).to_be_visible()
            expect(ph.locator('.search-home__input')).to_be_visible()
            expect(ph.locator('.search-home__submit')).to_be_visible()
            expect(ph.locator('.pv-ph-bar--input')).to_be_visible()
            self.assertEqual(ph.locator('.search-home__input').get_attribute('placeholder'), '')
            pending_y = ph.locator('.search-home__input').bounding_box()['y']
            expect(page.locator('#searchHome')).to_be_visible(timeout=8000)
            real_y = page.locator('#searchHome .search-home__input').bounding_box()['y']
            self.assertLess(abs(pending_y - real_y), 2, (pending_y, real_y))
        finally:
            browser.close()
            playwright.stop()

    def test_media_library_rail_fetches_in_place(self):
        playwright, browser, page = self.open_home()
        try:
            origin = page.evaluate('performance.timeOrigin')
            slow_network(page)
            page.locator('#railMediaLibrary').click()
            expect(page.locator('#mediaLibrary')).to_be_visible(timeout=8000)
            self.assertEqual(page.evaluate('performance.timeOrigin'), origin)
            self.assertEqual(page.url.endswith('/media-library/'), True)
            expect(page.locator('#railMediaLibrary')).to_have_attribute('aria-current', 'page')
        finally:
            browser.close()
            playwright.stop()

    def test_media_library_placeholder_matches_real_rows(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            page.locator('#railMediaLibrary').click()
            ph = page.locator('#pvPh-media-library')
            expect(ph).to_be_visible(timeout=1000)
            expect(ph.locator('.media-library__intro')).to_be_visible()
            self.assertEqual(ph.locator('.media-library__chips button').count(), 6)
            self.assertEqual(ph.locator('.media-library__file').count(), 3)
            for cls in ('.media-library__file-icon', '.media-library__filename',
                        '.media-library__meta', '.media-library__unused',
                        '.media-library__cloud'):
                self.assertGreater(ph.locator(cls).count(), 0, cls)
            self.assertEqual(ph.locator('.media-library__group').count(), 0)
            self.assertEqual(ph.locator('.media-library__cloud-button, '
                                        '.media-library__remove').count(), 0)
            self.assertEqual(ph.locator('.pv-ph-bar--button').count(), 6)
            self.assertEqual(ph.locator('.media-library__filename').first.text_content().strip(), '')
            self.assertFalse(ph.locator('.media-library__icon-btn').first.is_visible())
            for sel in ('.media-library__intro', '.media-library__chips button',
                        '.pv-media-count', '.media-library__sort button span'):
                self.assertEqual(ph.locator(sel).first.evaluate(
                    '(e) => getComputedStyle(e).color'), 'rgba(0, 0, 0, 0)', sel)
            self.assertNotEqual(ph.locator('.media-library__chips button').first.evaluate(
                '(e) => getComputedStyle(e, "::after").content'), 'none')
            pending = ph.locator('.read').bounding_box()
            expect(page.locator('#mediaLibrary')).to_be_visible(timeout=8000)
            real = page.locator('#read').bounding_box()
            for key in ('x', 'y', 'width'):
                self.assertLess(abs(pending[key] - real[key]), 2, (key, pending, real))
        finally:
            browser.close()
            playwright.stop()

    def test_media_library_settlement_clears_state(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page, latency=900)
            tile = page.locator('#railMediaLibrary')
            tile.click()
            expect(page.locator('#mediaLibrary')).to_be_visible(timeout=8000)
            page.wait_for_timeout(900)
            self.assertIsNone(tile.get_attribute('aria-disabled'))
            self.assertIsNone(page.locator('.stage').get_attribute('aria-busy'))
            self.assertFalse(page.locator('.stage > .pv-stagebar').is_visible())
            self.assertFalse(page.locator('.pv-placeholder').is_visible())
        finally:
            browser.close()
            playwright.stop()

    def test_search_then_media_library_cancels_the_first(self):
        playwright, browser, page = self.open_home()
        try:
            slow_network(page)
            search_tile = page.locator('#railSearch')
            search_tile.click()
            expect(page.locator('#pvPh-search-home')).to_be_visible(timeout=1000)
            media_tile = page.locator('#railMediaLibrary')
            media_tile.click()
            expect(page.locator('#pvPh-media-library')).to_be_visible(timeout=1000)
            self.assertIsNone(search_tile.get_attribute('aria-disabled'))
            self.assertEqual(media_tile.get_attribute('aria-disabled'), 'true')
        finally:
            browser.close()
            playwright.stop()

    def test_destination_placeholder_origin_matches_the_reading_page(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator(f'#panelBody .book[href="/bible/{self.book.pk}/"]').click()
            page.locator('#chList .ch-num').first.click()
            expect(page.locator('#read')).to_be_visible(timeout=5000)
            real = page.locator('#read').bounding_box()
            slow_network(page)
            page.locator('#railMediaLibrary').click()
            ph = page.locator('#pvPh-media-library .read')
            expect(ph).to_be_visible(timeout=1000)
            box = ph.bounding_box()
            self.assertEqual(round(box['x']), round(real['x']))
            self.assertEqual(round(box['y']), round(real['y']))
        finally:
            browser.close()
            playwright.stop()

    def test_row_controls_are_disabled_while_its_fetch_is_pending(self):
        playwright, browser, page = self.open_home()
        try:
            page.locator('.rail [data-panel="kidung"]').click()
            li = page.locator('#panelBody li:has(.row-edit)').first
            expect(li.locator('.book')).to_be_visible(timeout=5000)
            row = li.locator('.book')
            slow_network(page)
            row.click()
            expect(row).to_have_attribute('aria-disabled', 'true')
            for control in ('.row-edit', '.row-delete'):
                button = li.locator(control)
                self.assertEqual(button.get_attribute('disabled'), '')
                self.assertEqual(button.get_attribute('aria-disabled'), 'true')
            page.wait_for_timeout(2200)
            for control in ('.row-edit', '.row-delete'):
                self.assertIsNone(li.locator(control).get_attribute('disabled'))
        finally:
            browser.close()
            playwright.stop()
