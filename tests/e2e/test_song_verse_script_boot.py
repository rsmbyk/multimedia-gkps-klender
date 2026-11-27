"""A song reached through the reading shell can still edit its verses (spec 230).

The shell swaps pages with fetch + importNode; a script inside the swapped fragment is
inserted into the DOM but never executed. These tests walk the same clicks a person makes
from the home page, which a Django response test cannot observe.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongVerseScriptBootE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Sidebar verse book', short_name='SV', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=self.book, title='Sidebar verse song')
        for number in (1, 2):
            songs.Verse.objects.create(
                song=self.song, number=number, lyric=f'line {number}')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _reach_song_from_sidebar(self):
        self.page.goto(self.live_server_url + '/', wait_until='networkidle')
        self.page.locator('a[href="%s"]' % reverse('web-books')).first.click()
        self.page.locator('#panelBody a[href="%s"]'
                          % reverse('web-book', args=[self.book.pk])).first.click()
        self.page.locator('#chList a[href="%s"]'
                          % reverse('web-song', args=[self.song.pk])).first.click()
        self.page.wait_for_selector('[data-add-verse]')

    def _watch_editor_requests(self):
        seen = []
        self.page.on('request', lambda request: seen.append(request.url)
                     if '/editor/verse/new/?song=' in request.url else None)
        return seen

    def test_add_verse_opens_from_sidebar(self):
        self._reach_song_from_sidebar()
        requests = self._watch_editor_requests()
        self.page.locator('[data-add-verse]').first.click()
        expect(self.page.locator('#editorModal[open]')).to_be_visible()
        title = self.page.locator('#editorContent .editor__title')
        self.assertEqual(title.inner_text(), 'New verse')
        self.assertEqual(len(requests), 1)
        self.assertEqual(self.errors, [])

    def test_edit_verse_opens_from_sidebar(self):
        self._reach_song_from_sidebar()
        # The verse number overlays the pencil at rest; activate the control itself
        # so this checks the delegated handler rather than pointer hit-testing.
        self.page.locator('[data-verse-edit]').first.evaluate('el => el.click()')
        expect(self.page.locator('#editorModal[open]')).to_be_visible()
        title = self.page.locator('#editorContent .editor__title')
        self.assertEqual(title.inner_text(), 'Edit verse 1')
        self.assertEqual(self.errors, [])

    def test_script_boots_at_shell_load(self):
        self.page.goto(self.live_server_url + '/', wait_until='networkidle')
        at_home = self.page.evaluate(
            'document.querySelectorAll(\'script[src*=songs_verse]\').length')
        fetched_at_home = self.page.evaluate(
            'performance.getEntriesByType(\'resource\')'
            '.filter(e => e.name.indexOf(\'songs_verse.js\') !== -1).length')
        self._reach_song_from_sidebar()
        on_song = self.page.evaluate(
            'document.querySelectorAll(\'script[src*=songs_verse]\').length')
        self.assertEqual((at_home, fetched_at_home, on_song), (1, 1, 1))
        self.assertEqual(self.errors, [])

    def test_direct_load_still_opens_both_dialogs(self):
        self.page.goto(self.live_server_url
                       + reverse('web-song', args=[self.song.pk]), wait_until='networkidle')
        include = self.page.evaluate(
            '(() => { const s = document.querySelector(\'script[src*=songs_verse]\');'
            ' return s ? {count: document.querySelectorAll(\'script[src*=songs_verse]\').length,'
            ' inFragment: !!s.closest(\'#readBody\')} : null; })()')
        self.assertEqual(include, {'count': 1, 'inFragment': False})
        requests = self._watch_editor_requests()
        self.page.locator('[data-add-verse]').first.click()
        expect(self.page.locator('#editorModal[open]')).to_be_visible()
        self.assertEqual(
            self.page.locator('#editorContent .editor__title').inner_text(), 'New verse')
        self.assertEqual(len(requests), 1)
        self.page.evaluate('document.getElementById("editorModal").close()')
        self.page.locator('[data-verse-edit]').first.evaluate('el => el.click()')
        expect(self.page.locator('#editorModal[open]')).to_be_visible()
        self.assertEqual(
            self.page.locator('#editorContent .editor__title').inner_text(), 'Edit verse 1')
        self.assertEqual(self.errors, [])
