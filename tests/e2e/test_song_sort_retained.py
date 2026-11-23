"""End-to-end tests for spec 233: the song list keeps its chosen order.

Every refresh goes through the shell's shared reconciliation path; these tests pin
that the operator's sort choice survives it, using explicit modification stamps so
server order and alphabetical order differ deterministically.
"""

import unittest
from datetime import datetime, timezone

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
class SongSortRetainedTests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(name='Kidung Harian', short_name='KH')
        self.alpha = songs.Song.objects.create(book=self.book, title='Alpha')
        self.zebra = songs.Song.objects.create(book=self.book, title='Zebra')
        songs.Song.objects.filter(pk=self.alpha.pk).update(
            modified=datetime(2020, 1, 1, tzinfo=timezone.utc))
        songs.Song.objects.filter(pk=self.zebra.pk).update(
            modified=datetime(2020, 1, 2, tzinfo=timezone.utc))
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch()

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    # --- helpers -------------------------------------------------------------

    def _page(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + reverse('web-book', args=[self.book.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def order(self, page):
        return page.locator('#chList .songrow').evaluate_all(
            "els => els.map(el => el.querySelector('.songrow__t')?.textContent.trim())")

    def _sort(self, page):
        return page.locator('#songSort')

    def _create(self, page, title):
        before = page.locator('#chList .songrow').count()
        page.click('#songAdd')
        page.wait_for_selector('#editorContent input[name="title"]')
        page.fill('#editorContent input[name="title"]', title)
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')", timeout=10000)
        page.wait_for_function(
            f"document.querySelectorAll('#chList .songrow').length === {before + 1}",
            timeout=10000)

    def _row(self, page, title):
        return page.locator('#chList li:has(.songrow)').filter(has_text=title).first

    # --- US1 -----------------------------------------------------------------

    def test_create_keeps_alphabetical_order(self):
        page = self._page()
        expect(self._sort(page)).to_have_attribute('data-order', 'm')
        assert self.order(page) == ['Zebra', 'Alpha'], self.order(page)
        page.evaluate("window.__gkps233 = 'alive'")
        origin = page.evaluate('performance.timeOrigin')

        self._sort(page).click()
        expect(self._sort(page)).to_have_attribute('data-order', 'title')
        assert self.order(page) == ['Alpha', 'Zebra'], self.order(page)

        self._create(page, 'Beta')
        assert self.order(page) == ['Alpha', 'Beta', 'Zebra'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'title')
        assert page.evaluate('performance.timeOrigin') == origin
        assert page.evaluate('window.__gkps233') == 'alive'

    def test_create_in_default_order_leads(self):
        page = self._page()
        self._create(page, 'Beta')
        assert self.order(page) == ['Beta', 'Zebra', 'Alpha'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'm')

    # --- US2 -----------------------------------------------------------------

    def test_edit_refresh_keeps_alphabetical_order(self):
        page = self._page()
        self._create(page, 'Beta')
        self._sort(page).click()
        row = self._row(page, 'Zebra')
        row.hover()
        row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        page.fill('#editorContent input[name="title"]', 'Zebra 2')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')", timeout=10000)
        page.wait_for_function(
            "!![...document.querySelectorAll('#chList .songrow__t')]"
            ".some(el => el.textContent.includes('Zebra 2'))", timeout=10000)
        assert self.order(page) == ['Alpha', 'Beta', 'Zebra 2'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'title')

    def test_delete_refresh_keeps_alphabetical_order(self):
        page = self._page()
        self._create(page, 'Beta')
        self._sort(page).click()
        # Delete the song that is on the stage, so the shell runs its refresh path
        # rather than removing a single node from the DOM by hand.
        self._row(page, 'Zebra').locator('.songrow').click()
        page.wait_for_function("document.documentElement.dataset.read === 'on'", timeout=10000)
        row = self._row(page, 'Zebra')
        row.hover()
        row.locator('button[data-editor-delete="song"]').click()
        page.locator('#editorModal [data-editor-delete-form] button[type="submit"]').click()
        page.wait_for_function("!document.querySelector('dialog[open]')", timeout=10000)
        page.wait_for_function(
            "document.querySelectorAll('#chList .songrow').length === 2", timeout=10000)
        assert self.order(page) == ['Alpha', 'Beta'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'title')

    def test_row_click_refresh_keeps_alphabetical_order(self):
        page = self._page()
        self._create(page, 'Beta')
        self._sort(page).click()
        assert self.order(page) == ['Alpha', 'Beta', 'Zebra'], self.order(page)
        self._row(page, 'Zebra').locator('.songrow').click()
        page.wait_for_function("document.documentElement.dataset.read === 'on'", timeout=10000)
        expect(page.locator('.read__title')).to_contain_text('Zebra')
        assert self.order(page) == ['Alpha', 'Beta', 'Zebra'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'title')

    # --- US3 -----------------------------------------------------------------

    def test_default_order_and_other_sections_unchanged(self):
        page = self._page()
        assert self.order(page) == ['Zebra', 'Alpha'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'm')
        self._sort(page).click()

        page.locator('.rail [data-panel="alkitab"]').click()
        page.wait_for_function(
            "document.documentElement.dataset.section === 'alkitab'", timeout=10000)
        assert page.locator('#chList .songrow').count() == 0
        page.locator('.rail [data-panel="kidung"]').click()
        page.wait_for_function(
            "document.documentElement.dataset.section === 'kidung'", timeout=10000)
        # A rail switch closes the second pane; reopen the book for its song list.
        page.locator('#panelBody .book').filter(has_text='Kidung Harian').first.click()
        page.wait_for_function(
            "document.querySelectorAll('#chList .songrow').length === 2", timeout=10000)

        assert self.order(page) == ['Alpha', 'Zebra'], self.order(page)
        expect(self._sort(page)).to_have_attribute('data-order', 'title')
