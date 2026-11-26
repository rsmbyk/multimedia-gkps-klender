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
