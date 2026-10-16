"""Targeted public-reading refresh and delete-settlement tests (spec 094)."""

from datetime import date
import unittest

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
class TargetedReadingUpdatesE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Targeted refresh service', date=date(2026, 10, 18), is_active=True)
        self.first = tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='First entry', text='First entry content')
        self.second = tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Second entry', text='Second entry content')
        self.other_service = tatib.TataIbadah.objects.create(
            name='Other service', date=date(2026, 10, 11), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.other_service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Other entry', text='Other service content')
        self.legacy_service = tatib.TataIbadah.objects.create(
            name='Legacy refresh service', date=date(2026, 10, 4), is_active=True)
        self.legacy_first = tatib.TataIbadahItem.objects.create(
            tatib=self.legacy_service, order_number=1,
            item_type=tatib.TataIbadahItemType.TEXT, text='Legacy first entry')
        self.legacy_second = tatib.TataIbadahItem.objects.create(
            tatib=self.legacy_service, order_number=2,
            item_type=tatib.TataIbadahItemType.TEXT, text='Legacy second entry')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _hold_delete_and_read(self, page, fail_read=False, item_id=None,
                              old_item=False, service=None):
        item_id = item_id or self.first.pk
        service = service or self.service
        page.evaluate('''({deletePath, readPath, failRead}) => {
          const realFetch = window.fetch.bind(window);
          window.__deleteCalls = 0;
          window.__readCalls = 0;
          window.__settleDelete = null;
          window.__settleRead = null;
          window.fetch = (input, init) => {
            const url = new URL(typeof input === 'string' ? input : input.url, location.href);
            const method = (init && init.method || 'GET').toUpperCase();
            if (method === 'POST' && url.pathname === deletePath) {
              window.__deleteCalls++;
              return new Promise(resolve => {
                window.__settleDelete = () => resolve(realFetch(input, init));
              });
            }
            if (method === 'GET' && url.pathname === readPath
                && init && init.headers && init.headers['X-Requested-With'] === 'fetch') {
              window.__readCalls++;
              return new Promise(resolve => {
                window.__settleRead = () => resolve(failRead
                  ? new Response('unavailable', {status: 503}) : realFetch(input, init));
              });
            }
            return realFetch(input, init);
          };
        }''', {
            'deletePath': reverse('web-old-item-delete' if old_item else 'web-entry-delete',
                                  args=[item_id]),
            'readPath': reverse('web-tatib-service', args=[service.pk]),
            'failRead': fail_read,
        })

    def _open_delete(self, page, item_id=None, old_item=False):
        item_id = item_id or self.first.pk
        selector = 'data-old-item-delete' if old_item else 'data-entry-delete'
        page.locator('[%s="%s"]' % (selector, item_id)).click()
        dialog = page.locator('#editorModal')
        expect(dialog).to_be_visible()
        return dialog

    def test_delete_remains_locked_until_targeted_refresh_finishes_and_keeps_unaffected_nodes(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.evaluate('''({stageId, tocHref}) => {
          window.__stagePeer = document.querySelector('[data-entry-pk="' + stageId + '"]');
          window.__tocPeer = document.querySelector('#chList a[href="' + tocHref + '"]').closest('li');
          window.__panelNode = document.querySelector('#panelBody .group');
          window.__railNode = document.querySelector('.rail');
        }''', {
            'stageId': self.second.pk,
            'tocHref': '#ti-e%s' % self.second.pk,
        })
        self._hold_delete_and_read(page)
        dialog = self._open_delete(page)
        delete_button = dialog.locator('[data-confirm-delete]')
        delete_button.click()
        expect(delete_button).to_be_disabled()

        # Repeated keyboard/programmatic activation must not start another POST.
        page.evaluate('document.querySelector("[data-confirm-delete]").click()')
        self.assertEqual(page.evaluate('window.__deleteCalls'), 1)
        page.evaluate('window.__settleDelete()')
        page.wait_for_function('window.__readCalls === 1')

        expect(dialog).to_be_visible()
        expect(dialog).to_have_attribute('aria-busy', 'true')
        expect(dialog.locator('[data-confirm-delete]')).to_be_disabled()
        page.keyboard.press('Escape')
        page.mouse.click(8, 8)
        expect(dialog).to_be_visible()
        expect(page.locator('.edit-toast[data-state="pending"]')).to_be_visible(timeout=1500)

        page.evaluate('window.__settleRead()')
        expect(dialog).not_to_be_visible()
        expect(page.locator('.edit-toast[data-state="success"]')).to_be_visible()
        self.assertEqual(page.evaluate('''({deletedId, peerId}) => ({
          deletedFromStage: !document.querySelector('[data-entry-pk="' + deletedId + '"]'),
          deletedFromSidebar: !document.querySelector('#chList a[href="#ti-e' + deletedId + '"]'),
          stagePeerKept: window.__stagePeer === document.querySelector('[data-entry-pk="' + peerId + '"]'),
          tocPeerKept: window.__tocPeer === document.querySelector('#chList a[href="#ti-e' + peerId + '"]').closest('li'),
          panelKept: window.__panelNode === document.querySelector('#panelBody .group'),
          railKept: window.__railNode === document.querySelector('.rail')
        })''', {'deletedId': self.first.pk, 'peerId': self.second.pk}), {
            'deletedFromStage': True,
            'deletedFromSidebar': True,
            'stagePeerKept': True,
            'tocPeerKept': True,
            'panelKept': True,
            'railKept': True,
        })

    def test_delete_post_failure_unlocks_dialog_and_keeps_old_view(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        dialog = self._open_delete(page)
        page.route('**/editor/entry/%s/delete/' % self.first.pk,
                   lambda route: route.fulfill(status=500, body='failed'))
        dialog.locator('[data-confirm-delete]').click()
        expect(dialog).to_be_visible()
        expect(dialog.locator('[data-confirm-delete]')).to_be_enabled(timeout=3000)
        expect(page.locator('[data-entry-pk="%s"]' % self.first.pk)).to_be_visible()
        expect(page.locator('.edit-toast[data-state="failure"]')).to_be_visible()

    def test_successful_delete_with_failed_read_removes_rows_locally_and_reports_unverified_view(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        self._hold_delete_and_read(page, fail_read=True)
        dialog = self._open_delete(page)
        dialog.locator('[data-confirm-delete]').click()
        page.evaluate('window.__settleDelete()')
        page.wait_for_function('window.__readCalls === 1')
        page.evaluate('window.__settleRead()')

        expect(dialog).not_to_be_visible(timeout=3000)
        expect(page.locator('[data-entry-pk="%s"]' % self.first.pk)).to_have_count(0)
        expect(page.locator('#chList a[href="#ti-e%s"]' % self.first.pk)).to_have_count(0)
        expect(page.locator('.edit-toast[data-state="failure"]')).to_contain_text(
            'latest view could not be verified')
        self.assertEqual(page.evaluate('window.__deleteCalls'), 1)

    def test_legacy_delete_with_failed_read_removes_both_rows_and_renumbers_locally(self):
        page = self._page(reverse('web-tatib-service', args=[self.legacy_service.pk]))
        self._hold_delete_and_read(page, fail_read=True, item_id=self.legacy_first.pk,
                                  old_item=True, service=self.legacy_service)
        dialog = self._open_delete(page, self.legacy_first.pk, old_item=True)
        dialog.locator('[data-confirm-delete]').click()
        page.evaluate('window.__settleDelete()')
        page.wait_for_function('window.__readCalls === 1')
        page.evaluate('window.__settleRead()')

        expect(dialog).not_to_be_visible(timeout=3000)
        expect(page.locator('[data-old-item-pk="%s"]' % self.legacy_first.pk)).to_have_count(0)
        expect(page.locator('#chList a[href="#ti-1"]')).to_have_count(0)
        expect(page.locator('#chList a[href="#ti-2"] .songrow__c')).to_have_text('1')
        expect(page.locator('.edit-toast[data-state="failure"]')).to_contain_text(
            'deletion succeeded')
        self.assertEqual(page.evaluate('window.__deleteCalls'), 1)

    def test_navigating_between_services_preserves_unchanged_first_sidebar_rows(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        stable_href = reverse('web-tatib-service', args=[self.service.pk])
        page.evaluate('''href => {
          window.__stableServiceRow = document.querySelector('#panelBody a.book[href="' + href + '"]');
          window.__stableServiceLi = window.__stableServiceRow.closest('li');
          window.__stableGroupLi = window.__stableServiceLi.parentNode;
          window.__stablePanelGroup = window.__stableServiceRow.closest('.group');
        }''', stable_href)
        page.locator('#panelBody a.book[href="%s"]' % reverse(
            'web-tatib-service', args=[self.other_service.pk])).click()
        page.wait_for_url('**%s' % reverse('web-tatib-service', args=[self.other_service.pk]))
        state = page.evaluate('''href => {
          const row = document.querySelector('#panelBody a.book[href="' + href + '"]');
          return {
            rowExists: !!row,
            rowSame: row === window.__stableServiceRow,
            groupSame: !!row && row.closest('.group') === window.__stablePanelGroup,
            oldConnected: !!window.__stableServiceRow && window.__stableServiceRow.isConnected,
            oldName: window.__stableServiceRow && window.__stableServiceRow.dataset.name,
            newName: row && row.dataset.name,
            oldHref: window.__stableServiceRow && window.__stableServiceRow.getAttribute('href'),
            newHref: row && row.getAttribute('href'),
            liSame: !!row && row.closest('li') === window.__stableServiceLi,
            groupListSame: !!row && row.closest('li').parentNode === window.__stableGroupLi,
            count: document.querySelectorAll('#panelBody a.book[href="' + href + '"]').length
        };
        }''', stable_href)
        self.assertTrue(state['rowSame'], state)

    def test_newer_navigation_supersedes_an_older_inflight_read(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        first_path = reverse('web-tatib-service', args=[self.other_service.pk])
        latest_path = reverse('web-tatib-service', args=[self.legacy_service.pk])
        page.evaluate('''firstPath => {
          window.GKPSOfflineRender = null;
          window.GKPSOffline = null;
          const realFetch = window.fetch.bind(window);
          window.__releaseOldRead = null;
          window.fetch = (input, init) => {
            const url = new URL(typeof input === 'string' ? input : input.url, location.href);
            if (url.pathname === firstPath && init && init.headers
                && init.headers['X-Requested-With'] === 'fetch') {
              return new Promise(resolve => {
                window.__releaseOldRead = () => resolve(realFetch(input, init));
              });
            }
            return realFetch(input, init);
          };
        }''', first_path)
        page.locator('#panelBody a.book[href="%s"]' % first_path).click()
        page.wait_for_function('typeof window.__releaseOldRead === "function"')
        page.locator('#panelBody a.book[href="%s"]' % latest_path).click()
        page.evaluate('window.__releaseOldRead()')
        page.wait_for_url('**%s' % latest_path)
        expect(page.locator('#readName')).to_have_text('Legacy refresh service')
        expect(page.locator('#readBody')).to_contain_text('Legacy first entry')
