"""Editing and deleting old TataIbadahItem rows from the service pane (spec 007)."""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LegacyRowE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Legacy service', date=date(2026, 10, 4), is_active=True)
        self.first = tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembukaan', text='KJ 120', order_number=1)
        self.middle = tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.END_OF_SECTION,
            title='', text='Catatan operator', order_number=2)
        self.last = tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Penutup', text='Doa', order_number=3)
        self._start_browser()

    def _start_browser(self):
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
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    def _open_from_home(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + reverse('web-index'))
        page.wait_for_load_state('networkidle')
        page.locator('[data-panel="tatib"]').click()
        page.locator(f'.book[href="{reverse("web-tatib-service", args=[self.service.pk])}"]').click()
        page.wait_for_function("document.querySelector('#readName').textContent.trim() === 'Legacy service'")
        return page

    def _reveal_row_controls(self, page, item):
        # A collapsed add row has no box of its own (spec 052): it is reached
        # through the item above it, which reveals the row below.
        page.locator(f'#readBody [data-old-item-pk="{item.pk}"]').first.hover()
        row = page.locator(f'#readBody [data-entry-after="l{item.pk}"]')
        return row

    def test_editing_a_legacy_row_from_home_updates_the_pane_and_old_api(self):
        page = self._open_from_home()
        self._reveal_row_controls(page, self.first)
        page.locator(f'[data-old-item-edit="{self.first.pk}"]').click()
        page.wait_for_selector('dialog[open]', timeout=1500)
        expect(page.locator('[data-old-item-form="text"]')).to_be_visible()
        expect(page.locator('[name=title]')).to_have_value('Pembukaan')
        expect(page.locator('[name=text]')).to_have_value('KJ 120')

        page.fill('[name=title]', 'Nyanyian Pembukaan')
        page.fill('[name=text]', 'KJ 152')
        with page.expect_response(lambda response: response.url.endswith(
                reverse('web-old-item-save', args=[self.first.pk])) and response.request.method == 'POST') as saving:
            page.locator('.editor__save').click()
        self.assertEqual(saving.value.status, 200, saving.value.text()[:500])
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(page.locator('#readName')).to_have_text('Legacy service')
        expect(page.locator('#readBody')).to_contain_text('Nyanyian Pembukaan')
        expect(page.locator('#readBody')).to_contain_text('KJ 152')
        saved_item = page.locator(f'#readBody [data-old-item-pk="{self.first.pk}"]')
        expect(saved_item).to_be_focused(timeout=5000)
        self.assertEqual(saved_item.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

        self._close_browser()                         # ORM/API assertions stay outside Playwright's loop
        response = self.client.get('/api/tatib/items', {'tatib': self.service.pk})
        self.assertEqual(response.status_code, 200)
        row = response.json()[0]
        self.assertEqual((row['id'], row['title'], row['text']),
                         (self.first.pk, 'Nyanyian Pembukaan', 'KJ 152'))

    def test_legacy_item_cancel_restores_row_without_outline_or_revealed_actions(self):
        page = self._open_from_home()
        self._reveal_row_controls(page, self.first)
        item = page.locator(f'#readBody [data-old-item-pk="{self.first.pk}"]')
        page.locator(f'[data-old-item-edit="{self.first.pk}"]').click()
        page.wait_for_selector('dialog[open]', timeout=1500)
        page.mouse.move(1400, 850)
        page.keyboard.press('Enter')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(item).to_be_focused()
        self.assertEqual(item.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
        self._close_browser()

    def test_deleting_a_legacy_row_requires_confirmation_and_removes_it_from_old_api(self):
        page = self._open_from_home()
        self._reveal_row_controls(page, self.last)
        page.locator(f'[data-old-item-delete="{self.last.pk}"]').click()
        page.wait_for_selector('dialog[open]', timeout=1500)
        expect(page.locator('#editorContent')).to_contain_text('Delete this row?')
        delete_url = reverse('web-old-item-delete', args=[self.last.pk])
        with page.expect_response(lambda response: response.url.endswith(delete_url)
                                  and response.request.method == 'POST', timeout=5000) as deleting:
            page.locator('[data-confirm-delete]').click()
        self.assertEqual(deleting.value.status, 200, deleting.value.text()[:500])
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(page.locator('#readBody')).not_to_contain_text('Penutup')
        target = page.locator(f'#readBody [data-old-item-pk="{self.middle.pk}"]')
        expect(target).to_be_focused(timeout=5000)
        self.assertEqual(target.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

        self._close_browser()
        response = self.client.get('/api/tatib/items', {'tatib': self.service.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row['id'] for row in response.json()], [self.first.pk, self.middle.pk])

    def test_adding_under_the_second_old_row_places_the_entry_immediately_after_it(self):
        self._close_browser()
        later = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
            title='Later', text='After the old rows', order_number=4)
        self._start_browser()

        page = self._open_from_home()
        add = self._reveal_row_controls(page, self.middle)
        add.locator('[data-entry-open="text"]').click()
        page.wait_for_selector('dialog[open]', timeout=1500)
        page.fill('[name=title]', 'Inserted')
        page.fill('[name=text]', 'Between the rows')
        with page.expect_response(lambda response: '/editor/entry/new/save/' in response.url) as saving:
            page.locator('.editor__save').click()
        self.assertEqual(saving.value.status, 200, saving.value.text()[:500])
        page.wait_for_function("!document.querySelector('dialog[open]')")
        inserted_pk = saving.value.json()['id']
        page.wait_for_selector(f'#readBody #ti-e{inserted_pk}', timeout=5000)
        anchors = page.locator('#readBody > [data-anchor]').evaluate_all(
            '(nodes) => nodes.map(node => node.dataset.anchor)')
        self.assertEqual(anchors, [
            '1', '2', f'e{inserted_pk}', '4', f'e{later.pk}',
        ])
        self.assertEqual(page.locator('#chList [data-i]').evaluate_all(
            '(nodes) => nodes.map(node => node.dataset.i)'), anchors)
        self._close_browser()
        actual = sorted(
            [(row.order_number, 'legacy', row.pk) for row in self.service.tataibadahitem_set.all()]
            + [(row.order_number, 'entry', row.pk) for row in self.service.service_entries.all()])
        self.assertEqual(actual, [
            (1, 'legacy', self.first.pk), (2, 'legacy', self.middle.pk),
            (3, 'entry', inserted_pk), (4, 'legacy', self.last.pk),
            (5, 'entry', later.pk),
        ])
