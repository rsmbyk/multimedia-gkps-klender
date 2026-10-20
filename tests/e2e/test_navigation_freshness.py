"""Accepted Spec 119: current online data settles over a saved reading generation."""
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.test import override_settings, tag
from playwright.sync_api import expect, sync_playwright

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from tests.e2e.test_offline_library import wait_for_offline_ready


def write_from_worker(operation, *args, **kwargs):
    try:
        return operation(*args, **kwargs)
    finally:
        connections.close_all()


@override_settings(DEBUG=True, STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
@tag('e2e')
class NavigationFreshnessTests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='TB', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=1)
        translation = bible.BookTranslation.objects.create(version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=1, verse=1, text='Before verse')
        songbook = songs.Book.objects.create(name='Kidung Test', short_name='KT')
        song = songs.Song.objects.create(book=songbook, title='Before song')
        self.song = song
        songs.Verse.objects.create(song=song, number=1, lyric='Before lyric')
        self.service = tatib.TataIbadah.objects.create(
            name='Before service', date=date(2026, 10, 20), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=0, title='Before item', text='Before body', order_number=1)

    def test_online_rail_and_service_sidebar_settle_on_current_server_rows(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            page.wait_for_function("async () => !!(await GKPSOfflineRender.render('/tatib/'))")
            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(write_from_worker, tatib.TataIbadah.objects.create,
                            name='Added service', date=date(2026, 10, 20), is_active=True).result()
                pool.submit(write_from_worker, tatib.TataIbadah.objects.filter(pk=self.service.pk).update,
                            name='Current service').result()
            page.locator('.rail [data-panel="tatib"]').click()
            expect(page.locator('#panelBody .book__n')).to_contain_text(['Added service', 'Current service'])
            page.locator(f'#panelBody .book[href="/tatib/{self.service.pk}/"]').click()
            expect(page.locator('#readName')).to_have_text('Current service')
            expect(page.locator(f'#panelBody .book[href="/tatib/{self.service.pk}/"] .book__n')).to_have_text('Current service')
            browser.close()

    def test_online_search_settles_on_new_song_title(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            page.wait_for_function("async () => !!(await GKPSOfflineRender.render('/search?q=Current%20song'))")
            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(write_from_worker, songs.Song.objects.filter(pk=self.song.pk).update,
                            title='Current song').result()
            page.locator('#searchQuery').fill('Current song')
            page.locator('#globalSearch').evaluate('(form) => form.requestSubmit()')
            expect(page.locator('.result-group[data-kind="songs"] .result-row__title')).to_contain_text('Current song')
            browser.close()

    def test_saved_same_day_services_follow_server_creation_order(self):
        second = tatib.TataIbadah.objects.create(
            name='Second ID', date=date(2026, 10, 20), is_active=True)
        tatib.TataIbadah.objects.filter(pk=self.service.pk).update(
            created_at=datetime(2026, 10, 20, 12, tzinfo=timezone.utc))
        tatib.TataIbadah.objects.filter(pk=second.pk).update(
            created_at=datetime(2026, 10, 20, 10, tzinfo=timezone.utc))
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/tatib/')
            wait_for_offline_ready(page)
            self.assertEqual(page.locator('#panelBody .book__n').all_inner_texts(),
                             ['Before service', 'Second ID'])
            saved_order = page.evaluate("""async () => Array.from(
              (await GKPSOfflineRender.render('/tatib/')).querySelectorAll(
                '#panelBody .book__n')).map(row => row.textContent.trim())""")
            self.assertEqual(saved_order, ['Before service', 'Second ID'])
            browser.close()
