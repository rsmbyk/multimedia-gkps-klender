"""A grouped sidebar never keeps a heading after its last row is deleted (spec 252).

The reader's sidebar renders date buckets and the unheaded songbook groups from
server data, then removes a deleted row in place. These tests drive that real
delete path and check that the row's whole section goes with it -- on screen and
after a fresh render. Same runner and skip behaviour as the other reading suites.
"""

import unittest
from datetime import date
from unittest.mock import patch

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


TODAY = date(2026, 8, 26)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EmptyDateGroupE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        clock = patch('multimedia.web.reading.date_buckets.present_day',
                      return_value=TODAY)
        clock.start()
        self.addCleanup(clock.stop)
        self.recent = [tatib.TataIbadah.objects.create(
            name=name, date=TODAY.replace(day=25 - index), is_active=True)
            for index, name in enumerate(('Alpha', 'Beta'))]
        self.older = tatib.TataIbadah.objects.create(
            name='Gamma', date=date(2026, 6, 1), is_active=True)
        self.templates = [tatib.TataIbadah.objects.create(
            name=name, kind=tatib.TataIbadahKind.TEMPLATE, is_active=True)
            for name in ('Polos', 'Polos Dua')]
        self.hymn = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        self.ordinary = songs.Book.objects.create(name='Lagu Lain', short_name='LL')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + path)
        page.wait_for_load_state('networkidle')
        return page

    def _delete(self, page, scope, kind, pk):
        button = page.locator(
            f'{scope} button[data-editor-delete="{kind}"][data-editor-id="{pk}"]')
        button.locator('xpath=..').hover()
        button.click()
        page.locator('#editorModal [data-editor-delete-form] button[type="submit"]').click()
        page.wait_for_function("!document.querySelector('dialog[open]')", timeout=10000)

    def test_deleting_the_last_service_in_a_bucket_removes_its_heading(self):
        page = self._page('/tatib/')
        bucket = '#panelBody section.group[data-bucket="last-30-days"]'
        expect(page.locator(bucket)).to_have_count(1)
        expect(page.locator(bucket + ' .group__head')).to_have_text('Last 30 days')
        for service in self.recent:
            self._delete(page, bucket, 'tatib', service.pk)
        expect(page.locator(bucket)).to_have_count(0)
        expect(page.locator('#panelBody section.group[data-bucket="earlier-this-year"]')).to_have_count(1)
        # A fresh render agrees: the heading is not merely hidden in this tab.
        page.reload()
        page.wait_for_load_state('networkidle')
        expect(page.locator(bucket)).to_have_count(0)
        expect(page.locator(f'#panelBody .book[data-name="{self.older.pk}"]')).to_have_count(1)

    def test_deleting_the_last_template_leaves_no_empty_group(self):
        page = self._page('/tatib/?mode=template')
        expect(page.locator('#panelBody section.group')).to_have_count(1)
        for template in self.templates:
            self._delete(page, '#panelBody', 'template', template.pk)
        expect(page.locator('#panelBody section.group')).to_have_count(0)
        page.reload()
        page.wait_for_load_state('networkidle')
        expect(page.locator('#panelBody section.group')).to_have_count(0)

    def test_deleting_the_last_songbook_removes_its_unheaded_group(self):
        page = self._page('/songs/')
        expect(page.locator('#panelBody section.group')).to_have_count(2)
        self._delete(page, '#panelBody', 'songbook', self.ordinary.pk)
        expect(page.locator('#panelBody section.group')).to_have_count(1)
        expect(page.locator(f'#panelBody .book[data-name="{self.hymn.pk}"]')).to_have_count(1)

    def test_deleting_the_last_visible_row_hides_a_filtered_group(self):
        page = self._page('/tatib/')
        bucket = '#panelBody section.group[data-bucket="last-30-days"]'
        page.fill('#bookFilter', 'Alpha')
        expect(page.locator(bucket)).to_be_visible()
        self._delete(page, bucket, 'tatib', self.recent[0].pk)
        expect(page.locator(bucket)).to_be_hidden()
        page.fill('#bookFilter', '')
        expect(page.locator(bucket)).to_be_visible()
