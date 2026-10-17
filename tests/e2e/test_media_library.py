"""Browser acceptance for the local Media Library shell and media entry picker."""
from datetime import date
import json
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib.models import TataIbadah, MediaIdentity, ServiceEntry, ServiceEntryKind

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MediaLibraryE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = TataIbadah.objects.create(name='Ibadah Minggu', date=date(2026, 10, 18), is_active=True)
        if self._testMethodName in ('test_service_entry_distinguishes_disconnected_and_missing',
                                    'test_edit_media_only_exposes_title'):
            media = MediaIdentity.objects.create(sha256='b' * 64, byte_count=2048,
                                                 family='pdf', display_filename='service.pdf')
            ServiceEntry.objects.create(tatib=self.service, order_number=1,
                                        kind=ServiceEntryKind.MEDIA, media=media,
                                        media_filename='service.pdf')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.route('http://127.0.0.1:47863/**', lambda route: route.abort())
        page.goto(self.live_server_url + path)
        return page

    def connected_page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        sample = {'sha256': 'a' * 64, 'name': 'notes.pdf', 'family': 'pdf', 'size': 2048,
                  'uploaded_at': '2026-10-17T12:00:00+00:00', 'unused_since': None, 'delete_at': None}
        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'folder': '/test/media-library',
                           'file_count': 1, 'total_size': 2048, 'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': [sample]}
            elif url.endswith('/import') or url.endswith('/inspect'):
                payload = {**sample, 'reused': True}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:47863/**', companion)
        page.goto(self.live_server_url + path)
        return page

    def test_disconnected_library_hides_local_inventory_details(self):
        page = self.page(reverse('web-media-library'))
        page.locator('#mediaStatusButton').click()
        expect(page.locator('#mediaConnection')).to_have_text('Unavailable')
        expect(page.locator('#mediaFolder')).not_to_be_visible()
        expect(page.locator('#mediaCount')).not_to_be_visible()
        expect(page.locator('#mediaTotalSize')).not_to_be_visible()
        expect(page.locator('#mediaEmpty')).to_contain_text('unavailable')

    def test_media_create_picker_defaults_to_upload_and_save_stays_disabled(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        expect(page.locator('form[data-media-create]')).to_be_visible()
        expect(page.locator('[data-media-tab-button="upload"]')).to_have_attribute('aria-selected', 'true')
        expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()
        page.locator('[data-media-tab-button="library"]').click()
        expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()
        expect(page.locator('[data-media-library-list]')).to_contain_text('unavailable')

    def test_library_selection_survives_tab_switch_but_save_follows_visible_tab(self):
        page = self.connected_page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        page.locator('[data-media-tab-button="library"]').click()
        page.locator('[data-media-hash="' + 'a' * 64 + '"]').click()
        expect(page.locator('form[data-media-create] .editor__save')).to_be_enabled()
        page.locator('[data-media-tab-button="upload"]').click()
        expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()
        page.locator('[data-media-tab-button="library"]').click()
        expect(page.locator('[data-media-hash="' + 'a' * 64 + '"]')).to_have_attribute('aria-selected', 'true')
        expect(page.locator('form[data-media-create] .editor__save')).to_be_enabled()

    def test_connected_library_shows_file_and_status_details(self):
        page = self.connected_page(reverse('web-media-library'))
        expect(page.locator('.media-library__filename')).to_have_text('notes.pdf')
        page.locator('#mediaStatusButton').click()
        expect(page.locator('#mediaConnection')).to_have_text('Connected')
        expect(page.locator('#mediaFolder')).to_have_text('/test/media-library')
        expect(page.locator('#mediaCount')).to_have_text('1')

    def test_library_filter_sort_and_dialogs(self):
        page = self.connected_page(reverse('web-media-library'))
        expect(page.locator('.media-library__filename')).to_have_text('notes.pdf')
        page.locator('[data-media-type="image"]').click()
        expect(page.locator('#mediaResultCount')).to_have_text('0 of 1 files shown')
        page.locator('[data-media-type="pdf"]').click()
        expect(page.locator('#mediaResultCount')).to_have_text('1 of 1 files shown')
        page.locator('#mediaSortButton').click()
        page.locator('[data-media-sort="size-asc"]').click()
        expect(page.locator('#mediaSortButton')).to_have_text('File size · smallest')
        page.locator('#mediaSettingsButton').click()
        expect(page.locator('#mediaSettingsDialog')).to_be_visible()
        page.locator('#mediaSettingsDialog [data-media-close]').click()
        expect(page.locator('#mediaSettingsDialog')).not_to_be_visible()
        page.locator('.media-library__remove').click()
        expect(page.locator('#mediaRemoveDialog')).to_be_visible()
        page.locator('#mediaRemoveDialog [data-media-close]').click()
        expect(page.locator('#mediaRemoveDialog')).not_to_be_visible()

    def test_selected_library_file_creates_media_entry(self):
        page = self.connected_page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        page.locator('[data-media-tab-button="library"]').click()
        page.locator('[data-media-hash="' + 'a' * 64 + '"]').click()
        page.locator('form[data-media-create] .editor__save').click()
        expect(page.locator('.tatib__item--media')).to_be_visible()
        expect(page.locator('.tatib__item--media')).to_have_attribute('data-media-hash', 'a' * 64)
        expect(page.locator('.tatib__item--media')).to_contain_text('notes.pdf')

    def test_duplicate_upload_uses_library_filename(self):
        page = self.connected_page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        page.locator('[data-media-file]').set_input_files({
            'name': 'renamed.png', 'mimeType': 'application/pdf',
            'buffer': b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n',
        })
        expect(page.locator('[data-media-existing]')).to_be_visible()
        expect(page.locator('[data-media-library-name]')).to_have_text('Library filename: notes.pdf')
        page.locator('form[data-media-create] .editor__save').click()
        expect(page.locator('.tatib__item--media')).to_contain_text('notes.pdf')

    def test_service_entry_distinguishes_disconnected_and_missing(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('.tatib__item--media')
        expect(row).to_contain_text('Local library unavailable')
        self.assertFalse('is-missing' in row.get_attribute('class'))
        page.route('http://127.0.0.1:47863/**', lambda route: route.fulfill(
            status=200, content_type='application/json', body='{"files":[]}',
            headers={'Access-Control-Allow-Origin': self.live_server_url}))
        page.reload()
        page.wait_for_function("document.querySelector('.tatib__item--media').classList.contains('is-missing')")
        expect(row).not_to_contain_text('Local library unavailable')

    def test_create_dialog_fits_small_screen_and_reduced_motion(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.set_viewport_size({'width': 390, 'height': 700})
        page.emulate_media(reduced_motion='reduce')
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        dialog = page.locator('#editorModal')
        box = dialog.bounding_box()
        self.assertGreaterEqual(box['x'], 0)
        self.assertLessEqual(box['x'] + box['width'], 390)
        self.assertGreaterEqual(page.locator('[data-media-drop]').bounding_box()['height'], 220)
        self.assertEqual(dialog.evaluate('el => getComputedStyle(el).animationName'), 'none')

    def test_edit_media_only_exposes_title(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-edit]').first.dispatch_event('click')
        form = page.locator('form[data-entry-form="media"]')
        expect(form).to_be_visible()
        self.assertEqual(form.locator('[data-media-file]').count(), 0)
        expect(form.locator('[data-media-edit-availability]')).to_have_text('Local library unavailable')
        form.locator('[name="title"]').fill('Changed title')
        form.locator('.editor__save').click()
        expect(page.locator('.tatib__item--media')).to_contain_text('Changed title')
        expect(page.locator('.tatib__item--media')).to_contain_text('service.pdf')
