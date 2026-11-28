"""Enter accepts a delete confirmation even when focus is not on its button (spec 256)."""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

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
class EnterDeleteConfirmE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Keyboard service', date=date(2026, 12, 6), is_active=True)
        for order, title in enumerate(('Opening', 'Survivor'), 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=order,
                kind=tatib.ServiceEntryKind.TEXT, title=title, text=title)
        book = songs.Book.objects.create(name='Lagu Lain', short_name='LL',
                                         is_hymn_book=False)
        self.song = songs.Song.objects.create(book=book, title='Editable song')
        songs.Verse.objects.create(song=self.song, number=1, lyric='First')
        songs.Verse.objects.create(song=self.song, number=2, lyric='Second')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self._close_browser()
        super().tearDown()

    def _close_browser(self):
        if self._playwright is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    def _page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900},
                                     color_scheme='dark', device_scale_factor=1)
        page.goto(self.live_server_url + path)
        page.wait_for_load_state('networkidle')
        return page

    @staticmethod
    def _enter_away_from_control(page):
        """Enter belongs to the confirmation, not to whichever button has focus."""
        page.evaluate('() => { if (document.activeElement) document.activeElement.blur(); }')
        page.keyboard.press('Enter')

    def test_enter_deletes_an_entry_with_focus_away_from_the_button(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('.tatib__item').first.hover()
        page.locator('[data-entry-delete]').first.click()
        page.wait_for_selector('#editorModal [data-confirm-delete]')
        self._enter_away_from_control(page)
        page.wait_for_function("!document.querySelector('#editorModal').open")
        self._close_browser()
        self.assertEqual(tatib.ServiceEntry.objects.count(), 1)
        self.assertEqual(tatib.ServiceEntry.objects.first().title, 'Survivor')

    def test_enter_deletes_a_sidebar_record_with_focus_away_from_the_button(self):
        page = self._page(reverse('web-index'))
        page.locator('[data-panel="tatib"]').click()
        page.locator('.book[href*="/tatib/"]').first.hover()
        page.locator('[data-editor-delete="tatib"]').first.click()
        page.wait_for_selector('#editorModal [data-editor-delete-form]')
        self._enter_away_from_control(page)
        page.wait_for_function("!document.querySelector('#editorModal').open")
        self._close_browser()
        self.assertFalse(tatib.TataIbadah.objects.get(pk=self.service.pk).is_active)

    def test_enter_deletes_a_verse_with_focus_away_from_the_button(self):
        page = self._page(reverse('web-song', args=[self.song.pk]))
        page.locator('[data-verse-edit]').first.dispatch_event('click')
        page.wait_for_selector('#editorContent [data-verse-delete]')
        page.locator('#editorContent [data-verse-delete]').first.dispatch_event('click')
        page.wait_for_selector('#editorModal [data-confirm-delete]')
        self._enter_away_from_control(page)
        page.wait_for_function("!document.querySelector('#editorModal').open")
        self._close_browser()
        self.assertEqual(songs.Verse.objects.filter(is_deleted=False).count(), 1)

    def test_enter_accepts_media_removal_with_focus_away_from_the_button(self):
        page = self._page(reverse('web-media-library'))
        page.evaluate("""() => {
            window.__removeClicks = 0;
            document.getElementById('mediaConfirmRemove')
              .addEventListener('click', () => { window.__removeClicks += 1; });
            document.getElementById('mediaRemoveDialog').showModal();
        }""")
        self._enter_away_from_control(page)
        expect(page.locator('#mediaRemoveDialog')).to_be_visible()
        self.assertEqual(page.evaluate('() => window.__removeClicks'), 1)
