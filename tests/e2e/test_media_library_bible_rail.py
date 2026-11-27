"""Spec 246: Media Library must not inherit a reading section.

The shell reads `data-section` from the document root; the Media Library page supplies no
sidebar lists, so inheriting `alkitab` makes the first Alkitab rail click a toggle over an
empty panel instead of a fetch. These cases read the DOM after the click so the red half is
an assertion, not a timeout.
"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from playwright.sync_api import sync_playwright

from multimedia.bible import models as bible


@override_settings(DEBUG=True,
                   STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
@tag('e2e')
class MediaLibraryBibleRailTests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='TB', abbreviation='TB')
        book = bible.Book.objects.create(name='Kej', testament='old', number_of_chapters=2)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Kejadian')
        for chapter in (1, 2):
            bible.Verse.objects.create(book_translation=translation, chapter=chapter,
                                       verse=1, text='Verse ' + str(chapter))

    def open_media_library(self, playwright):
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        requests = []
        page.on('request', lambda request: requests.append(request.url))
        page.goto(self.live_server_url + '/')
        page.locator('#railMediaLibrary').click()
        page.wait_for_function(
            "() => (document.querySelector('#read') || {}).dataset?.kind === 'media-library'")
        return browser, page, requests

    def test_media_library_declares_its_own_section(self):
        """The library page is a destination, not an already-selected Alkitab section."""
        with sync_playwright() as playwright:
            browser, page, _ = self.open_media_library(playwright)
            try:
                section = page.evaluate('() => document.documentElement.dataset.section')
                self.assertEqual(section, 'media-library')
            finally:
                browser.close()

    def test_first_bible_rail_click_from_media_library_opens_books(self):
        """The first Alkitab click fetches the books instead of toggling an empty sidebar."""
        with sync_playwright() as playwright:
            browser, page, requests = self.open_media_library(playwright)
            try:
                page.locator('.rail [data-panel="alkitab"]').click()
                page.wait_for_timeout(500)
                bible_requests = [url for url in requests if url.endswith('/bible/')]
                books = page.locator('#panelBody .book').count()
                empty_hidden = page.locator('#panelEmpty').get_attribute('hidden') is not None
                self.assertEqual(len(bible_requests), 1,
                                 'first Alkitab click should fetch /bible/ once')
                self.assertGreater(books, 0, 'the sidebar should carry the real book rows')
                self.assertTrue(empty_hidden, 'the empty-list copy should be gone')
            finally:
                browser.close()
