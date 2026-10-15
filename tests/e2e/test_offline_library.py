"""Spec 092 browser checks for saved shells and tab-local search state."""

from concurrent.futures import ThreadPoolExecutor

from django.test import LiveServerTestCase, override_settings
from playwright.sync_api import sync_playwright

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


@override_settings(DEBUG=True)
class OfflineLibraryE2ETests(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=1)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=1, verse=1,
                                   text='Kasih Tuhan membuka Injil')
        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=12, title='Kasih')
        songs.Verse.objects.create(song=song, number=1, lyric='Kasih Tuhan kekal')
        service = tatib.TataIbadah.objects.create(name='Ibadah Minggu', is_active=True)
        tatib.TataIbadahItem.objects.create(tatib=service, item_type=0, title='Doa',
                                            text='Tuhan dengar kami', order_number=1)
        self.book_id = book.pk
        self.song_id = song.pk
        self.songbook_id = songbook.pk
        self.service_id = service.pk

    def test_saved_content_and_projector_survive_disconnection(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            self.assertGreater(page.locator('#offlineSyncTitle').count(), 0, page.content()[:1200])
            page.wait_for_function("document.querySelector('#offlineSyncTitle').textContent.includes('Ready')")
            context.set_offline(True)
            page.goto(self.live_server_url + '/bible/')
            page.get_by_role('link', name='Matius').first.wait_for()
            page.goto(self.live_server_url + f'/bible/{self.book_id}/')
            page.get_by_role('link', name='Matius chapter 1').wait_for()
            page.goto(self.live_server_url + f'/bible/{self.book_id}/1/')
            page.get_by_text('Kasih Tuhan membuka Injil').wait_for()
            page.goto(self.live_server_url + f'/songs/{self.song_id}/')
            page.get_by_text('Kasih Tuhan kekal').wait_for()
            page.goto(self.live_server_url + '/songs/')
            page.get_by_role('link', name='Kidung Jemaat').first.wait_for()
            page.goto(self.live_server_url + f'/songs/book/{self.songbook_id}/')
            page.get_by_role('link', name='Kasih').first.wait_for()
            page.goto(self.live_server_url + f'/tatib/{self.service_id}/')
            page.get_by_text('Tuhan dengar kami').wait_for()
            page.goto(self.live_server_url + f'/obs/service/{self.service_id}/')
            page.locator('#projectorScreens .screen').first.wait_for(state='attached')
            self.assertIn('Tuhan dengar kami', page.locator('#projectorScreens').text_content())
            browser.close()

    def test_search_history_and_new_tab_are_independent(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            page.wait_for_function("document.querySelector('#offlineSyncTitle').textContent.includes('Ready')")
            page.locator('#searchQuery').fill('Kasih')
            page.locator('#globalSearch').evaluate('(form) => form.requestSubmit()')
            page.locator('.result-row').first.wait_for()
            first_url = page.url
            page.locator('#searchQuery').fill('draft text')
            page.locator('.rail__logo').click()
            self.assertEqual(page.locator('#searchQuery').input_value(), '')
            page.locator('#railSearch').click()
            self.assertEqual(page.locator('#searchQuery').input_value(), 'draft text')
            with context.expect_page() as opened:
                page.evaluate("window.open('/home/', '_blank')")
            another = opened.value
            another.wait_for_load_state()
            another.locator('#railSearch').click()
            self.assertEqual(another.locator('#searchQuery').input_value(), '')
            self.assertNotIn('/search', another.url)
            page.locator('#searchQuery').fill('Kasih')
            page.locator('#globalSearch').evaluate('(form) => form.requestSubmit()')
            page.locator('.result-row').first.wait_for()
            self.assertEqual(page.url, first_url)
            self.assertGreater(page.evaluate('history.length'), 2)
            browser.close()

    def test_interrupted_update_keeps_previous_generation_until_retry(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            page.wait_for_function("document.querySelector('#offlineSyncTitle').textContent.includes('Ready')")
            initial = page.evaluate("GKPSOffline.get('songs', %d)" % self.songbook_id)
            self.assertEqual(initial['songs'][0]['verses'][0]['lyric'], 'Kasih Tuhan kekal')

            def update_verse():
                verse = songs.Verse.objects.get(song_id=self.song_id, number=1)
                verse.lyric = 'Kasih Tuhan diperbarui'
                verse.save()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(update_verse).result()
            page.route('**/offline/chunk/songs/*/', lambda route: route.abort())
            page.locator('#offlineSyncButton').click()
            page.locator('#offlineSyncNow').click()
            page.wait_for_function("document.querySelector('#offlineSyncTitle').textContent.includes('Update failed')")
            saved = page.evaluate("GKPSOffline.get('songs', %d)" % self.songbook_id)
            self.assertEqual(saved['songs'][0]['verses'][0]['lyric'], 'Kasih Tuhan kekal')

            page.unroute('**/offline/chunk/songs/*/')
            page.locator('#offlineSyncNow').click()
            page.wait_for_function("GKPSOffline.get('songs', %d).then(x => x.songs[0].verses[0].lyric === 'Kasih Tuhan diperbarui')" % self.songbook_id)
            browser.close()
