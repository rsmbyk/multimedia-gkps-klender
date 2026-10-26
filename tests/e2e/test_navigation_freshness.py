"""Spec 136: every reading page is painted from its own server response.

The saved-copy generation is gone, so these tests pin what survives: a click through the
rail reaches the page in one in-page request, and what the page shows is what the server
holds at that moment — never a copy painted first and replaced later.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.test import override_settings, tag
from playwright.sync_api import expect, sync_playwright

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


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
        translation = bible.BookTranslation.objects.create(version=version, book=book,
                                                           translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=1, verse=1,
                                   text='Before verse')
        songbook = songs.Book.objects.create(name='Kidung Test', short_name='KT')
        song = songs.Song.objects.create(book=songbook, title='Before song')
        self.song = song
        songs.Verse.objects.create(song=song, number=1, lyric='Before lyric')
        self.service = tatib.TataIbadah.objects.create(
            name='Before service', date=date(2026, 10, 20), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=0, title='Before item', text='Before body',
            order_number=1)

    def test_a_reading_navigation_paints_the_servers_page(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(write_from_worker, tatib.TataIbadah.objects.create,
                            name='Added service', date=date(2026, 10, 20),
                            is_active=True).result()
                pool.submit(write_from_worker,
                            tatib.TataIbadah.objects.filter(pk=self.service.pk).update,
                            name='Current service').result()
            documents = []
            page.on('request', lambda request: documents.append(request.url)
                    if request.resource_type == 'document' else None)
            page.locator('.rail [data-panel="tatib"]').click()
            expect(page.locator('#panelBody .book__n')).to_contain_text(
                ['Added service', 'Current service'])
            page.locator(f'#panelBody .book[href="/tatib/{self.service.pk}/"]').click()
            expect(page.locator('#readName')).to_have_text('Current service')
            self.assertEqual(documents, [], 'the navigation reloaded the document')
            browser.close()

    def test_a_saved_change_reaches_the_page_without_a_reload(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.live_server_url + '/home/')
            with ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(write_from_worker,
                            songs.Song.objects.filter(pk=self.song.pk).update,
                            title='Current song').result()
            page.locator('#searchQuery').fill('Current song')
            page.locator('#globalSearch').evaluate('(form) => form.requestSubmit()')
            expect(page.locator('.result-group[data-kind="songs"] .result-row__title')
                   ).to_contain_text('Current song')
            browser.close()
