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
                                    'test_edit_media_only_exposes_title',
                                    'test_titled_media_entry_heading_aligns_with_file_icon',
                                    'test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen'):
            filename = ('Invoice-AATTCSTN-0002-with-a-long-filename-for-narrow-screens.pdf'
                        if self._testMethodName == 'test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen'
                        else 'service.pdf')
            media = MediaIdentity.objects.create(sha256='b' * 64, byte_count=2048,
                                                 family='pdf', display_filename=filename)
            ServiceEntry.objects.create(tatib=self.service, order_number=1,
                                        kind=ServiceEntryKind.MEDIA, media=media,
                                        media_filename=filename,
                                        title='Tingting' if self._testMethodName == 'test_titled_media_entry_heading_aligns_with_file_icon' else '')
            if self._testMethodName == 'test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen':
                ServiceEntry.objects.create(tatib=self.service, order_number=2,
                                            kind=ServiceEntryKind.TEXT, text='Opening words')
                ServiceEntry.objects.create(tatib=self.service, order_number=3,
                                            kind=ServiceEntryKind.SECTION_BREAK)
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
        page.route('http://127.0.0.1:63174/**', lambda route: route.abort())
        page.goto(self.live_server_url + path)
        return page

    def connected_page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        sample = {'sha256': 'a' * 64, 'name': 'notes.pdf', 'family': 'pdf', 'size': 2048,
                  'uploaded_at': '2026-10-17T12:00:00+00:00', 'unused_since': None, 'delete_at': None}
        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected',
                           'file_count': 1, 'total_size': 2048, 'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': [sample]}
            elif url.endswith('/import') or url.endswith('/inspect'):
                payload = {**sample, 'reused': True}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + path)
        return page

    def empty_connected_page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        def companion(route):
            if route.request.url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': 0, 'total_size': 0,
                           'retention': '30', 'write_token': 'test-token'}
            elif route.request.url.endswith('/files') or route.request.url.endswith('/references'):
                payload = {'files': []}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + path)
        return page

    def connection_drops_after_settings_save_page(self, path):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        status_requests = {'count': 0}
        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                status_requests['count'] += 1
                if status_requests['count'] == 2:
                    route.abort()
                    return
                payload = {'connection': 'connected', 'file_count': 0, 'total_size': 0,
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': []}
            elif url.endswith('/settings'):
                payload = {'retention': '30'}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + path)
        return page

    def test_disconnected_library_hides_local_inventory_details(self):
        page = self.page(reverse('web-media-library'))
        page.locator('#mediaStatusButton').click()
        expect(page.locator('#mediaConnection')).to_have_text('Unavailable')
        expect(page.locator('#mediaConnection')).to_have_attribute('data-state', 'unavailable')
        expect(page.locator('#mediaConnection .media-library__connection-icon--unavailable')).to_be_visible()
        expect(page.locator('#mediaConnection .media-library__connection-icon--unavailable')).to_have_attribute('aria-hidden', 'true')
        expect(page.locator('#mediaConnection .media-library__connection-icon--connected')).not_to_be_visible()
        expect(page.locator('#mediaStatusPopup')).not_to_contain_text('Folder')
        expect(page.locator('#mediaCount')).not_to_be_visible()
        expect(page.locator('#mediaTotalSize')).not_to_be_visible()
        expect(page.locator('#mediaEmpty')).to_contain_text('unavailable')

    def test_media_create_picker_defaults_to_upload_and_save_stays_disabled(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        expect(page.locator('form[data-media-create]')).to_be_visible()
        hint = page.locator('.media-entry__drop [data-media-prompt] p')
        self.assertEqual(hint.inner_text().splitlines(), [
            'Supported files: images, audio, video, PDF, and PPT/PPTX',
            'Maximum 200 MB per file',
        ])
        self.assertEqual(hint.locator('strong').nth(1).inner_text(), 'Maximum 200 MB')
        expect(page.locator('[data-media-tab-button="upload"]')).to_have_attribute('aria-selected', 'true')
        expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()
        page.locator('[data-media-tab-button="library"]').click()
        expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()
        expect(page.locator('[data-media-library-list]')).to_contain_text('unavailable')

    def test_empty_library_keeps_tall_create_modal_and_quiet_empty_state(self):
        page = self.empty_connected_page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        expect(page.locator('form[data-media-create]')).to_be_visible()
        dialog = page.locator('#editorModal')
        dialog.evaluate('async el => { await Promise.all(el.getAnimations().map(animation => animation.finished)); }')
        upload_box = dialog.bounding_box()
        upload_cancel_box = dialog.locator('.editor__cancel').bounding_box()
        upload_footer_gap = upload_box['y'] + upload_box['height'] - (
            upload_cancel_box['y'] + upload_cancel_box['height'])
        self.assertLessEqual(upload_footer_gap, 24)
        page.locator('[data-media-tab-button="library"]').click()
        empty_state = page.locator('[data-media-library-list] .media-entry__empty')
        expect(empty_state).to_contain_text('No media in this library yet')
        expect(empty_state).to_contain_text(
            'Upload a file to add it to this computer’s Media Library.')
        expect(empty_state).to_have_attribute('role', 'status')
        expect(page.locator('form[data-media-create] .editor__save')).to_be_disabled()
        library_box = dialog.bounding_box()
        library_cancel_box = dialog.locator('.editor__cancel').bounding_box()
        library_footer_gap = library_box['y'] + library_box['height'] - (
            library_cancel_box['y'] + library_cancel_box['height'])
        self.assertLessEqual(library_footer_gap, 24)
        self.assertAlmostEqual(upload_box['height'], 760, delta=1)
        self.assertAlmostEqual(library_box['height'], upload_box['height'], delta=1)
        expect(dialog.locator('[name="title"]')).to_be_visible()
        expect(dialog.locator('.editor__cancel')).to_be_visible()

        page.set_viewport_size({'width': 390, 'height': 440})
        small_box = dialog.bounding_box()
        self.assertGreaterEqual(small_box['x'], 0)
        self.assertLessEqual(small_box['x'] + small_box['width'], 390)
        self.assertGreaterEqual(small_box['y'], 0)
        self.assertLessEqual(small_box['y'] + small_box['height'], 440)
        expect(dialog.locator('[name="title"]')).to_be_visible()
        expect(dialog.locator('.editor__cancel')).to_be_visible()
        library_panel = page.locator('[data-media-panel="library"]')
        self.assertGreater(library_panel.evaluate('el => el.scrollHeight'),
                           library_panel.evaluate('el => el.clientHeight'))

    def test_supported_files_text_size_and_inactive_tab_hover_match_app_switches(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        supported = page.locator('.media-entry__drop [data-media-prompt] p')
        label = supported.locator('strong').first
        self.assertEqual(supported.evaluate('el => getComputedStyle(el).fontSize'), '12px')
        self.assertEqual(label.evaluate('el => getComputedStyle(el).fontSize'), '12px')

        upload = page.locator('[data-media-tab-button="upload"]')
        library = page.locator('[data-media-tab-button="library"]')
        initial_background = library.evaluate('el => getComputedStyle(el).backgroundColor')
        active_background = upload.evaluate('el => getComputedStyle(el).backgroundColor')
        initial_color = library.evaluate('el => getComputedStyle(el).color')
        library.hover()
        page.wait_for_timeout(250)
        self.assertNotEqual(library.evaluate('el => getComputedStyle(el).backgroundColor'), initial_background)
        self.assertNotEqual(library.evaluate('el => getComputedStyle(el).color'), initial_color)
        self.assertEqual(upload.evaluate('el => getComputedStyle(el).backgroundColor'), active_background)

    def test_media_source_tabs_slide_thumb_in_both_directions(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        upload = page.locator('[data-media-tab-button="upload"]')
        library = page.locator('[data-media-tab-button="library"]')
        thumb = page.locator('.media-entry__tab-thumb')
        expect(thumb).to_have_count(1)
        expect(thumb).to_have_attribute('aria-hidden', 'true')
        self.assertEqual(upload.get_attribute('aria-selected'), 'true')
        start_x = thumb.bounding_box()['x']

        thumb.evaluate('el => { el.style.transitionDuration = "3s"; }')
        library.click()
        expect(library).to_have_attribute('aria-selected', 'true')
        expect(page.locator('[data-media-panel="library"]')).to_be_visible()
        page.wait_for_function(
            'el => el.getAnimations().some(animation => animation.playState === "running")',
            arg=thumb.element_handle())
        thumb.evaluate('el => el.getAnimations().forEach(animation => animation.finish())')
        library_x = thumb.bounding_box()['x']
        self.assertGreater(library_x, start_x)

        upload.focus()
        upload.press('Enter')
        expect(upload).to_have_attribute('aria-selected', 'true')
        expect(page.locator('[data-media-panel="upload"]')).to_be_visible()
        page.wait_for_function(
            'el => el.getAnimations().some(animation => animation.playState === "running")',
            arg=thumb.element_handle())
        thumb.evaluate('el => el.getAnimations().forEach(animation => animation.finish())')
        self.assertAlmostEqual(thumb.bounding_box()['x'], start_x, delta=2)

    def test_media_source_thumb_respects_reduced_motion(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        page.emulate_media(reduced_motion='reduce')
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        thumb = page.locator('.media-entry__tab-thumb')
        expect(thumb).to_have_count(1)
        self.assertEqual(thumb.evaluate('el => getComputedStyle(el).transitionProperty'), 'none')
        page.locator('[data-media-tab-button="library"]').click()
        expect(page.locator('[data-media-tab-button="library"]')).to_have_attribute('aria-selected', 'true')
        self.assertEqual(thumb.evaluate('el => el.getAnimations().length'), 0)

    def test_media_library_current_marker_clears_when_another_main_menu_is_clicked(self):
        library_path = reverse('web-media-library')
        page = self.page(library_path)
        media_link = page.locator('.rail__btn[data-tip="Media Library"]')
        expect(media_link).to_have_attribute('aria-current', 'page')

        page.locator('.rail__btn[data-panel="alkitab"]').click()
        expect(page.locator('.rail__btn[data-panel="alkitab"]')).to_have_attribute('aria-expanded', 'true')
        expect(media_link).not_to_have_attribute('aria-current', 'page')

        page.goto(self.live_server_url + library_path)
        expect(media_link).to_have_attribute('aria-current', 'page')
        page.locator('.rail__btn[data-panel="kidung"]').click()
        expect(page.locator('.rail__btn[data-panel="kidung"]')).to_have_attribute('aria-expanded', 'true')
        expect(media_link).not_to_have_attribute('aria-current', 'page')

        page.goto(self.live_server_url + library_path)
        expect(media_link).to_have_attribute('aria-current', 'page')
        page.locator('.rail__btn[data-panel="tatib"]').click()
        expect(page.locator('.rail__btn[data-panel="tatib"]')).to_have_attribute('aria-expanded', 'true')
        expect(media_link).not_to_have_attribute('aria-current', 'page')

    def test_media_library_current_marker_tracks_browser_history(self):
        library_path = reverse('web-media-library')
        page = self.page(library_path)
        media_link = page.locator('.rail__btn[data-tip="Media Library"]')
        expect(media_link).to_have_attribute('aria-current', 'page')
        page.locator('.rail__btn[data-panel="tatib"]').click()
        service_link = page.locator('#panelBody a.book').filter(has_text=self.service.name)
        service_link.click()
        service_path = reverse('web-tatib-service', args=[self.service.pk])
        page.wait_for_function('path => location.pathname === path', arg=service_path)
        expect(media_link).not_to_have_attribute('aria-current', 'page')

        page.go_back()
        page.wait_for_function('path => location.pathname === path', arg=library_path)
        expect(media_link).to_have_attribute('aria-current', 'page')
        page.go_forward()
        page.wait_for_function('path => location.pathname === path', arg=service_path)
        expect(media_link).not_to_have_attribute('aria-current', 'page')

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
        expect(page.locator('#mediaConnection')).to_have_attribute('data-state', 'connected')
        expect(page.locator('#mediaConnection .media-library__connection-icon--connected')).to_be_visible()
        expect(page.locator('#mediaConnection .media-library__connection-icon--connected')).to_have_attribute('aria-hidden', 'true')
        expect(page.locator('#mediaConnection .media-library__connection-icon--unavailable')).not_to_be_visible()
        expect(page.locator('#mediaConnection')).to_have_css('gap', '7px')
        expect(page.locator('#mediaConnection .media-library__connection-icon--connected')).to_have_css('width', '17px')
        expect(page.locator('#mediaStatusPopup')).not_to_contain_text('Folder')
        expect(page.locator('#mediaCount')).to_have_text('1')
        expect(page.locator('#mediaTotalSize')).to_have_text('2 KB')

    def test_connection_icon_tracks_status_refresh(self):
        page = self.connection_drops_after_settings_save_page(reverse('web-media-library'))
        page.locator('#mediaSettingsButton').click()
        page.locator('#mediaSaveSettings').click()
        expect(page.locator('#mediaSettingsDialog')).not_to_be_visible()
        page.locator('#mediaStatusButton').click()
        expect(page.locator('#mediaConnection')).to_have_text('Unavailable')
        expect(page.locator('#mediaConnection')).to_have_attribute('data-state', 'unavailable')
        expect(page.locator('#mediaConnection .media-library__connection-icon--unavailable')).to_be_visible()
        expect(page.locator('#mediaConnection .media-library__connection-icon--connected')).not_to_be_visible()
        page.reload()
        page.locator('#mediaStatusButton').click()
        expect(page.locator('#mediaConnection')).to_have_text('Connected')
        expect(page.locator('#mediaConnection')).to_have_attribute('data-state', 'connected')
        expect(page.locator('#mediaConnection .media-library__connection-icon--connected')).to_be_visible()
        expect(page.locator('#mediaConnection .media-library__connection-icon--unavailable')).not_to_be_visible()

    def test_library_filter_sort_and_dialogs(self):
        page = self.connected_page(reverse('web-media-library'))
        expect(page.locator('.media-library__filename')).to_have_text('notes.pdf')
        self.assertEqual(page.locator('#railMediaLibrary svg path').count(), 3)
        expect(page.locator('#mediaSortButton svg')).to_be_visible()
        page.locator('[data-media-type="image"]').click()
        expect(page.locator('#mediaResultCount')).to_have_text('0 of 1 files shown')
        page.locator('[data-media-type="pdf"]').click()
        expect(page.locator('#mediaResultCount')).to_have_text('1 of 1 files shown')
        page.locator('#mediaSortButton').click()
        page.locator('[data-media-sort="size-asc"]').click()
        expect(page.locator('#mediaSortButton')).to_have_text('File size · smallest')
        expect(page.locator('#mediaSortButton svg')).to_be_visible()
        expect(page.locator('#mediaSortButton')).to_have_attribute('aria-label', 'Sort files: File size · smallest')
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
        self.assertEqual(row.locator('.read__sec').evaluate('el => getComputedStyle(el).marginTop'), '0px')
        self.assertFalse('is-missing' in row.get_attribute('class'))
        page.route('http://127.0.0.1:63174/**', lambda route: route.fulfill(
            status=200, content_type='application/json', body='{"files":[]}',
            headers={'Access-Control-Allow-Origin': self.live_server_url}))
        page.reload()
        page.wait_for_function("document.querySelector('.tatib__item--media').classList.contains('is-missing')")
        expect(row).not_to_contain_text('Local library unavailable')

    def test_titled_media_entry_heading_aligns_with_file_icon(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('.tatib__item--media')
        expect(row.locator('.read__sec')).to_have_text('Tingting')
        self.assertEqual(row.locator('.read__sec').evaluate('el => getComputedStyle(el).marginTop'), '0px')
        self.assertEqual(row.locator('.read__sub').evaluate('el => getComputedStyle(el).marginTop'), '0px')

    def test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen(self):
        desktop_page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        desktop_row = desktop_page.locator('.tatib__item--media')
        desktop_icon = desktop_row.locator('.entry__media-icon')
        self.assertEqual(desktop_row.evaluate('el => getComputedStyle(el).minHeight'), '80px')
        self.assertEqual(desktop_row.evaluate('el => getComputedStyle(el).paddingTop'), '16px')
        self.assertEqual(desktop_row.evaluate('el => getComputedStyle(el).paddingBottom'), '16px')
        self.assertEqual(desktop_row.evaluate('el => getComputedStyle(el).paddingLeft'), '64px')
        self.assertEqual(desktop_row.evaluate('el => getComputedStyle(el).paddingRight'), '16px')
        desktop_box, desktop_icon_box = desktop_row.bounding_box(), desktop_icon.bounding_box()
        self.assertAlmostEqual(desktop_box['y'] + desktop_box['height'] / 2,
                               desktop_icon_box['y'] + desktop_icon_box['height'] / 2, delta=1)

        page = self.browser.new_page(viewport={'width': 390, 'height': 800})
        page.route('http://127.0.0.1:63174/**', lambda route: route.abort())
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('.tatib__item--media')
        icon = row.locator('.entry__media-icon')
        self.assertEqual(row.evaluate('el => getComputedStyle(el).minHeight'), '80px')
        self.assertEqual(row.evaluate('el => getComputedStyle(el).paddingTop'), '16px')
        self.assertEqual(row.evaluate('el => getComputedStyle(el).paddingBottom'), '16px')
        self.assertEqual(row.evaluate('el => getComputedStyle(el).paddingLeft'), '60px')
        self.assertEqual(row.evaluate('el => getComputedStyle(el).paddingRight'), '12px')
        heading = row.locator('.read__sec')
        expect(heading).to_contain_text('Invoice-AATTCSTN-0002-with-a-long-filename-for-narrow-screens.pdf')
        self.assertGreater(heading.bounding_box()['height'], 24)
        row_box, icon_box = row.bounding_box(), icon.bounding_box()
        self.assertAlmostEqual(row_box['y'] + row_box['height'] / 2,
                               icon_box['y'] + icon_box['height'] / 2, delta=1)
        text_row = page.locator('.tatib__item--acts:not(.tatib__item--media)')
        break_row = page.locator('.tatib__eos')
        self.assertEqual(text_row.evaluate('el => getComputedStyle(el).minHeight'), '56px')
        self.assertEqual(text_row.evaluate('el => getComputedStyle(el).paddingTop'), '8px')
        self.assertEqual(break_row.evaluate('el => getComputedStyle(el).minHeight'), '56px')
        self.assertEqual(break_row.evaluate('el => getComputedStyle(el).paddingTop'), '8px')
        self.assertAlmostEqual(text_row.bounding_box()['y'] - row_box['y'] - row_box['height'],
                               12, delta=1)
        self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'),
                             page.evaluate('document.documentElement.clientWidth'))
        self.assertGreater(row.bounding_box()['height'], 80)

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
