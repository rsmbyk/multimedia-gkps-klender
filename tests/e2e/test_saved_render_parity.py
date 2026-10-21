"""Spec 122: saved reading pages match the same server route before refresh."""

from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from playwright.sync_api import sync_playwright

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from tests.e2e.test_offline_library import wait_for_offline_ready


@override_settings(DEBUG=True, STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
@tag('e2e')
class SavedRenderParityTests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='TB', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=1)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=1, verse=1, text='Verse')
        sim_language = bible.Language.objects.create(name='Simalungun')
        sim_version = bible.Version.objects.create(
            lang=sim_language, name='SIM', abbreviation='SIM')
        bible.BookTranslation.objects.create(
            version=sim_version, book=book, translation='Matius Simalungun')
        self.bible_id = book.pk
        hymn = songs.Book.objects.create(name='Hymn Test', short_name='HT', is_hymn_book=True)
        self.hymn_song = songs.Song.objects.create(
            book=hymn, number=7, title='Numbered song')
        self.hymn_id = hymn.pk
        ordinary = songs.Book.objects.create(name='Ordinary Test', short_name='OT')
        self.ordinary_id = ordinary.pk
        self.song = songs.Song.objects.create(book=ordinary, title='581. Ordinary song')
        self.service = tatib.TataIbadah.objects.create(
            name='Empty service', date=date(2026, 10, 21), is_active=True)
        self.filled_service = tatib.TataIbadah.objects.create(
            name='Filled service', date=date(2026, 10, 20), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.filled_service, item_type=0, title='Opening',
            text='Welcome', order_number=1)

    def test_saved_documents_use_route_specific_labels_and_markup(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            cases = [
                ('/songs/', 'placeholder', 'Filter songbooks...'),
                ('/tatib/', 'placeholder', 'Filter Tata Ibadah...'),
                (f'/bible/{self.bible_id}/', 'heading', 'Chapters — Matius (Matius Simalungun)'),
                (f'/bible/{self.bible_id}/1/', 'heading', 'Chapters — Matius (Matius Simalungun)'),
                (f'/songs/book/{self.hymn_id}/', 'heading', 'Song list — Hymn Test'),
                (f'/songs/book/{self.hymn_id}/', 'first_song', 'HT 7'),
                (f'/songs/{self.hymn_song.pk}/', 'first_song', 'HT 7'),
                (f'/songs/{self.hymn_song.pk}/', 'first_song_number_data', 'HT 7'),
                (f'/songs/{self.song.pk}/', 'first_song_sort', 'ordinary song'),
                ('/tatib/', 'heading', 'Chapters'),
                (f'/songs/{self.song.pk}/', 'eyebrow', 'Ordinary Test'),
                (f'/songs/{self.song.pk}/', 'heading', 'Song list — Ordinary Test'),
                (f'/tatib/{self.service.pk}/', 'icon_count', 4),
            ]
            for url, field, expected in cases:
                with self.subTest(url=url, field=field):
                    actual = page.evaluate("""async ([url, field]) => {
                      const doc = await GKPSOfflineRender.render(url);
                      if (!doc) throw new Error('Saved route unavailable: ' + url);
                      const values = {
                        placeholder: () => doc.querySelector('#bookFilter').placeholder,
                        heading: () => doc.querySelector('#chTitle').textContent.trim(),
                        first_song: () => doc.querySelector('#chList .songrow__c').textContent.trim(),
                        first_song_number_data: () => doc.querySelector('#chList .songrow').dataset.num,
                        first_song_sort: () => doc.querySelector('#chList .songrow').dataset.t,
                        eyebrow: () => doc.querySelector('#readEyebrow').textContent.trim(),
                        icon_count: () => doc.querySelectorAll('.entry__empty-btn svg').length,
                      };
                      return values[field]();
                    }""", [url, field])
                    self.assertEqual(actual, expected)
            browser.close()

    def test_offline_sidebar_open_has_server_labels_without_reload(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            page.context.set_offline(True)

            page.locator('.rail [data-panel="kidung"]').click()
            page.locator(f'#panelBody a.book[href="/songs/book/{self.ordinary_id}/"]').click()
            page.locator(f'#chList a.songrow[href="/songs/{self.song.pk}/"]').click()
            self.assertEqual(page.locator('#bookFilter').get_attribute('placeholder'),
                             'Filter songbooks...')
            self.assertEqual(page.locator('#readEyebrow').text_content(), 'Ordinary Test')
            self.assertEqual(page.locator('#chTitle').text_content(), 'Song list — Ordinary Test')

            page.locator('.rail [data-panel="tatib"]').click()
            page.locator(f'#panelBody a.book[href="/tatib/{self.service.pk}/"]').click()
            self.assertEqual(page.locator('#bookFilter').get_attribute('placeholder'),
                             'Filter Tata Ibadah...')
            self.assertEqual(page.locator('.entry__empty-btn').count(), 5)
            self.assertEqual(page.locator('.entry__empty-btn svg').count(), 4)
            saved_boxes = page.locator('.entry__empty-btn').evaluate_all(
                '(buttons) => buttons.map(button => { const r = button.getBoundingClientRect();'
                ' return [r.x, r.y, r.width, r.height]; })')
            page.context.set_offline(False)
            page.goto(self.live_server_url + f'/tatib/{self.service.pk}/')
            server_boxes = page.locator('.entry__empty-btn').evaluate_all(
                '(buttons) => buttons.map(button => { const r = button.getBoundingClientRect();'
                ' return [r.x, r.y, r.width, r.height]; })')
            self.assertEqual(len(saved_boxes), len(server_boxes))
            for saved, server in zip(saved_boxes, server_boxes):
                self.assertLessEqual(abs(saved[3] - server[3]), 1)
            for index in range(1, len(saved_boxes)):
                saved_gap = saved_boxes[index][1] - saved_boxes[index - 1][1]
                server_gap = server_boxes[index][1] - server_boxes[index - 1][1]
                self.assertLessEqual(abs(saved_gap - server_gap), 1)
            browser.close()

    def test_saved_reading_routes_match_server_fields(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            urls = [
                '/home/', '/bible/', f'/bible/{self.bible_id}/',
                f'/bible/{self.bible_id}/1/', f'/bible/{self.bible_id}/1/?ed=sim',
                '/songs/', f'/songs/book/{self.hymn_id}/',
                f'/songs/{self.hymn_song.pk}/',
                f'/songs/book/{self.ordinary_id}/', f'/songs/{self.song.pk}/',
                '/tatib/', '/tatib/?mode=template', f'/tatib/{self.service.pk}/',
                f'/tatib/{self.filled_service.pk}/',
                '/search?q=ordinary',
            ]
            for url in urls:
                with self.subTest(url=url):
                    result = page.evaluate("""async url => {
                      const saved = await GKPSOfflineRender.render(url);
                      const response = await fetch(url, {cache: 'no-store'});
                      const server = new DOMParser().parseFromString(await response.text(), 'text/html');
                      const one = (doc, selector, attribute) => {
                        const node = doc.querySelector(selector);
                        return node ? (attribute ? node.getAttribute(attribute) : node.textContent.trim()) : null;
                      };
                      const many = (doc, selector) => Array.from(doc.querySelectorAll(selector))
                        .map(node => node.textContent.trim());
                      const fields = doc => ({
                        section: doc.documentElement.dataset.section,
                        panelTitle: one(doc, '#panelTitle'),
                        panelLabel: one(doc, 'label[for="bookFilter"]'),
                        panelPlaceholder: one(doc, '#bookFilter', 'placeholder'),
                        panelRows: many(doc, '#panelBody .book__n'),
                        chTitle: one(doc, '#chTitle'),
                        chLabel: one(doc, 'label[for="songFilter"]'),
                        chPlaceholder: one(doc, '#songFilter', 'placeholder'),
                        songNumbers: many(doc, '#chList .songrow__c'),
                        eyebrow: one(doc, '#readEyebrow'),
                        readName: doc.documentElement.dataset.read === 'on'
                          ? one(doc, '#readName') : null,
                        emptyActions: doc.documentElement.dataset.read === 'on'
                          ? many(doc, '.entry__empty-btn') : [],
                        emptyIcons: doc.documentElement.dataset.read === 'on'
                          ? doc.querySelectorAll('.entry__empty-btn svg').length : 0,
                        entryTitles: many(doc, '#readBody .tatib__item .read__sec'),
                        entryActionCount: doc.querySelectorAll('#readBody .tatib__item .entry__actions button').length,
                      });
                      return {saved: fields(saved), server: fields(server)};
                    }""", url)
                    self.assertEqual(result['saved'], result['server'])
            browser.close()
