"""Browser acceptance for the local Media Library shell and media entry picker."""
from datetime import date, datetime, timezone
import json
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

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
                                    'test_service_media_status_dialog_has_ordered_availability',
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
        if self._testMethodName in ('test_share_online_from_fresh_library_page_sends_csrf_token',):
            self.share_media = MediaIdentity.objects.create(
                sha256='a' * 64, byte_count=2048, family='pdf', display_filename='notes.pdf')
        if self._testMethodName in ('test_a_library_refresh_never_moves_a_row',
                                    'test_clicking_share_online_never_moves_a_library_row',
                                    'test_the_library_list_is_drawn_once_per_refresh',
                                    'test_a_known_reference_never_shows_the_placeholder',
                                    'test_a_failed_references_request_draws_the_placeholder_once',
                                    'test_the_status_poll_leaves_the_list_where_it_is'):
            # spec 148: one file used by two past services — a tall row, removable, not protected
            self.referenced_media = MediaIdentity.objects.create(
                sha256='c' * 64, byte_count=4096, family='pdf', display_filename='notes.pdf')
            for service_date, name in ((date(2026, 10, 18), 'Ibadah Minggu'),
                                       (date(2026, 10, 11), 'Ibadah Pemuda')):
                service = TataIbadah.objects.create(name=name, date=service_date, is_active=True)
                ServiceEntry.objects.create(tatib=service, order_number=1,
                                            kind=ServiceEntryKind.MEDIA,
                                            media=self.referenced_media,
                                            media_filename='notes.pdf', title='')
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
        status_requests = {'drop_after_settings': False}
        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                if status_requests['drop_after_settings']:
                    route.abort()
                    return
                payload = {'connection': 'connected', 'file_count': 0, 'total_size': 0,
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': []}
            elif url.endswith('/settings'):
                status_requests['drop_after_settings'] = True
                payload = {'retention': '30'}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:63174/**', companion)
        page._media_status_state = status_requests
        page.goto(self.live_server_url + path)
        return page

    TRANSFER_NAMES = (
        'images (1).jpeg',
        'side-view-silhouette-african-elephant-walking-across-green-ground-against-light-blue-sky'
        '-stately-wild-bull-marching-proudly-481645534.webp',
        'random.jpg',
        'Sujud & Terima Kasih - JCC Worship [Official Music Video] - Ibadah Raya JCC Jakarta.webm',
        'Slide Warta Jemaat GKPS Klender Tgl 25 Oktober 2026.pptx',
        'images.jpeg',
        'Invoice-AATTCSTN-0002.pdf',
        'Receipt-2773-9204.png',
        'Invoice-AATTCSTN-0002.pdf',
    )

    def transfers_page(self, width=1440):
        """The library with the Transfers dialog open on nine finished uploads, two of them long."""
        jobs = [{'id': index, 'direction': 'upload', 'sha256': f'{index:064d}', 'name': name,
                 'size': 2048, 'bytes_done': 2048, 'status': 'completed', 'automatic': 0,
                 'started_at': '2026-10-28T09:00:00+00:00',
                 'ended_at': '2026-10-28T09:01:00+00:00'}
                for index, name in enumerate(self.TRANSFER_NAMES, start=1)]
        page = self.browser.new_page(viewport={'width': width, 'height': 900})
        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': 0, 'total_size': 0,
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/transfers'):
                payload = {'transfers': jobs, 'retrying': []}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': []}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + reverse('web-media-library'))
        page.locator('#mediaTransfersButton').click()
        expect(page.locator('#mediaTransfersList .media-transfers__row')).to_have_count(len(jobs))
        # the dialog's own 190ms scale-in would be measured mid-flight: 32px of column reads 31.38
        page.evaluate("""() => Promise.all(document.querySelector('#mediaTransfersDialog')
            .getAnimations().map(animation => animation.finished))""")
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
        tabs = page.locator('.media-entry__tabs')
        thumb = page.locator('.media-entry__tab-thumb')
        expect(thumb).to_have_count(1)
        expect(thumb).to_have_attribute('aria-hidden', 'true')
        self.assertEqual(upload.get_attribute('aria-selected'), 'true')
        start_x = thumb.bounding_box()['x'] - tabs.bounding_box()['x']

        thumb.evaluate('el => { el.style.transitionDuration = "3s"; }')
        library.click()
        expect(library).to_have_attribute('aria-selected', 'true')
        expect(page.locator('[data-media-panel="library"]')).to_be_visible()
        page.wait_for_function(
            'el => el.getAnimations().some(animation => animation.playState === "running")',
            arg=thumb.element_handle())
        thumb.evaluate('el => el.getAnimations().forEach(animation => animation.finish())')
        library_x = thumb.bounding_box()['x'] - tabs.bounding_box()['x']
        self.assertGreater(library_x, start_x)

        upload.focus()
        upload.press('Enter')
        expect(upload).to_have_attribute('aria-selected', 'true')
        expect(page.locator('[data-media-panel="upload"]')).to_be_visible()
        page.wait_for_function(
            'el => el.getAnimations().some(animation => animation.playState === "running")',
            arg=thumb.element_handle())
        thumb.evaluate('el => el.getAnimations().forEach(animation => animation.finish())')
        self.assertAlmostEqual(thumb.bounding_box()['x'] - tabs.bounding_box()['x'], start_x, delta=2)

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

    def test_share_online_from_fresh_library_page_sends_csrf_token(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        self.assertEqual(page.context.cookies(), [])
        sample = {'sha256': 'a' * 64, 'name': 'notes.pdf', 'family': 'pdf', 'size': 2048,
                  'uploaded_at': '2026-10-17T12:00:00+00:00', 'unused_since': None, 'delete_at': None}

        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': 1, 'total_size': 2048,
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': [sample]}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})

        page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + reverse('web-media-library'))
        self.assertTrue(any(cookie['name'] == 'csrftoken'
                            for cookie in page.context.cookies()))
        share_url = self.live_server_url + reverse(
            'web-media-share', args=[self.share_media.pk, 'begin'])
        captured = {}
        alerts = []
        page.on('dialog', lambda dialog: (alerts.append(dialog.message), dialog.dismiss()))
        share = page.locator('.media-library__cloud-button[title="Share online"]')
        expect(share).to_be_visible()

        with patch('multimedia.web.reading.views.media_handoff.begin_share',
                   return_value=(None, SimpleNamespace(
                       expires_at=datetime(2026, 10, 25, tzinfo=timezone.utc)))) as begin_share:
            with page.expect_response(share_url) as response_info:
                share.click()
            captured.update(response_info.value.request.all_headers())

        self.assertEqual(response_info.value.status, 200)
        self.assertTrue(captured.get('x-csrftoken'))
        self.assertEqual(alerts, [])
        begin_share.assert_called_once()

    def test_service_media_status_dialog_has_ordered_availability(self):
        page = self.page(reverse('web-tatib-service', args=[self.service.pk]))
        expect(page.locator('#serviceMediaButton')).to_be_visible()
        page.locator('#serviceMediaButton').click()
        dialog = page.locator('#serviceMediaDialog')
        expect(dialog).to_be_visible()
        expect(dialog.locator('.service-media__row')).to_have_count(1)
        expect(dialog.locator('.service-media__main strong')).to_have_text('service.pdf')
        expect(dialog.locator('[data-online-state]')).to_have_attribute('aria-label', 'Unavailable online')
        expect(dialog.locator('[data-local-state]')).to_have_attribute('aria-label', 'Local library unavailable')
        page.keyboard.press('Escape')
        expect(dialog).not_to_be_visible()

    def test_sidebar_transfer_session_shows_active_then_finished(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        job = {'id': 1, 'direction': 'upload', 'sha256': 'a' * 64,
               'name': 'service.pdf', 'size': 100, 'bytes_done': 25,
               'status': 'active', 'automatic': 0,
               'started_at': '2026-10-18T09:00:00+00:00', 'ended_at': None}
        state = {'job': job}
        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': 0, 'total_size': 0,
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/transfers'):
                payload = {'transfers': [state['job']], 'retrying': []}
            else:
                payload = {'files': []}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})
        page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + reverse('web-media-library'))
        rail = page.locator('#mediaTransferRail')
        expect(rail).to_be_visible()
        expect(page.locator('#mediaTransferRailDot')).to_have_attribute('data-state', 'active')
        rail.click()
        expect(page.locator('#mediaTransfersList')).to_contain_text('25%')
        page.keyboard.press('Escape')
        expect(page.locator('#mediaTransfersDialog')).not_to_be_visible()
        state['job'] = dict(job, status='completed', bytes_done=100,
                            ended_at='2026-10-18T09:01:00+00:00')
        expect(page.locator('#mediaTransferRailDot')).to_have_attribute('data-state', 'completed')
        rail.click()
        expect(page.locator('#mediaTransfersList')).to_contain_text('Completed')
        page.keyboard.press('Escape')
        expect(rail).not_to_be_visible()

    def transfer_job(self, job_id, name, status='completed', ended_at='2026-10-28T09:00:00+00:00'):
        return {'id': job_id, 'direction': 'upload', 'sha256': f'{job_id:064d}',
                'name': name, 'size': 1000, 'bytes_done': 1000, 'status': status,
                'automatic': 0, 'started_at': '2026-10-28T08:59:00+00:00',
                'ended_at': ended_at if status == 'completed' else None}

    def finished_jobs(self, jobs, finished):
        """The same jobs, with the ones that were active now completed just now."""
        return [dict(job, status='completed', bytes_done=job['size'],
                     ended_at=finished if job['status'] == 'active' else job['ended_at'])
                for job in jobs]

    def transfer_list_page(self, jobs):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        state = {'jobs': list(jobs)}

        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': 0, 'total_size': 0,
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/transfers'):
                payload = {'transfers': state['jobs'], 'retrying': []}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': []}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})

        page.route('http://127.0.0.1:63174/**', companion)
        page._transfer_state = state
        page.goto(self.live_server_url + reverse('web-media-library'))
        return page

    SEAM_PROBE = """() => {
      const list = document.querySelector('#mediaTransfersList');
      const rows = [...list.querySelectorAll('.media-transfers__row')];
      const divider = list.querySelector('.media-transfers__divider');
      if (!divider) return { dividers: 0, rows: rows.length };
      const before = divider.previousElementSibling;
      const border = parseFloat(getComputedStyle(before).borderBottomWidth);
      const dividerBox = divider.getBoundingClientRect();
      const beforeBox = before.getBoundingClientRect();
      let near = parseFloat(getComputedStyle(divider).borderTopWidth) > 0 ? 1 : 0;
      rows.forEach(row => {
        const width = parseFloat(getComputedStyle(row).borderBottomWidth);
        const gap = dividerBox.top - row.getBoundingClientRect().bottom;
        if (width > 0 && gap >= -1 && gap <= 20) near += 1;
      });
      return {
        dividers: list.querySelectorAll('.media-transfers__divider').length,
        rows: rows.length,
        border,
        dividerBorder: parseFloat(getComputedStyle(divider).borderTopWidth),
        near,
        above: Math.round((dividerBox.top - (beforeBox.bottom - border)) * 10) / 10,
        below: Math.round((rows[rows.indexOf(before) + 1].getBoundingClientRect().top - dividerBox.bottom) * 10) / 10,
      };
    }"""

    def test_the_session_seam_draws_one_line(self):
        jobs = [self.transfer_job(1, 'images (1).jpeg', status='active'),
                self.transfer_job(2, 'elephant.webp', status='active')]
        jobs += [self.transfer_job(index, f'service-{index}.pdf') for index in range(3, 10)]
        page = self.transfer_list_page(jobs)
        rail = page.locator('#mediaTransferRail')
        expect(rail).to_be_visible()
        rail.click()
        expect(page.locator('#mediaTransfersList')).to_contain_text('100%')

        page._transfer_state['jobs'] = self.finished_jobs(jobs, datetime.now(timezone.utc).isoformat())
        expect(page.locator('#mediaTransfersList')).to_contain_text('Completed')
        expect(page.locator('#mediaTransfersList .media-transfers__row')).to_have_count(9)

        seam = page.evaluate(self.SEAM_PROBE)
        self.assertEqual(seam['dividers'], 1)
        self.assertEqual(seam['rows'], 9)
        self.assertEqual(seam['border'], 0, 'the row above the seam keeps its own border')
        self.assertEqual(seam['dividerBorder'], 2)
        self.assertEqual(seam['near'], 1, 'two boundaries are drawn at the seam')

        page.keyboard.press('Escape')
        page.locator('#mediaTransfersButton').click()
        expect(page.locator('#mediaTransfersDialog')).to_be_visible()
        self.assertEqual(page.locator('#mediaTransfersList .media-transfers__divider').count(), 0,
                         'a dialog opened from the media library draws no session seam')
        page.keyboard.press('Escape')

    def test_the_seam_keeps_equal_space_either_side(self):
        jobs = [self.transfer_job(1, 'images (1).jpeg', status='active')]
        jobs += [self.transfer_job(index, f'service-{index}.pdf') for index in range(2, 10)]
        page = self.transfer_list_page(jobs)
        page.locator('#mediaTransferRail').click()
        page._transfer_state['jobs'] = self.finished_jobs(jobs, datetime.now(timezone.utc).isoformat())
        expect(page.locator('#mediaTransfersList .media-transfers__divider')).to_have_count(1)

        seam = page.evaluate(self.SEAM_PROBE)
        self.assertEqual(seam['above'], 9, 'the seam sits 9px under the row above')
        self.assertEqual(seam['below'], 9, 'and 9px above the row below')
        page.close()

    def test_a_long_transfer_list_scrolls_inside_the_dialog(self):
        jobs = [self.transfer_job(index, f'worship-{index}.pdf') for index in range(1, 16)]
        page = self.transfer_list_page(jobs)
        page.locator('#mediaTransfersButton').click()
        dialog = page.locator('#mediaTransfersDialog')
        expect(dialog).to_be_visible()
        expect(page.locator('#mediaTransfersList .media-transfers__row')).to_have_count(15)
        page.wait_for_timeout(400)   # the dialog scales in over 190ms; measure it at rest

        measured = page.evaluate("""() => {
          const dialog = document.querySelector('#mediaTransfersDialog');
          const list = document.querySelector('#mediaTransfersList');
          const style = getComputedStyle(dialog);
          const box = dialog.getBoundingClientRect();
          const listBox = list.getBoundingClientRect();
          const title = dialog.querySelector('h2').getBoundingClientRect().top;
          const border = parseFloat(style.borderBottomWidth);
          const innerBottom = box.bottom - border - parseFloat(style.paddingBottom);
          list.scrollTop = list.scrollHeight;
          const rows = [...list.querySelectorAll('.media-transfers__row')];
          const last = rows[rows.length - 1].getBoundingClientRect();
          const result = {
            scrolls: list.scrollHeight > list.clientHeight + 1,
            dialogScrolls: dialog.scrollHeight > dialog.clientHeight + 1,
            past: Math.round((listBox.bottom - innerBottom) * 10) / 10,
            endGap: Math.round((innerBottom - last.bottom + parseFloat(style.paddingBottom)) * 10) / 10,
            inside: last.bottom <= innerBottom + 0.5,
            titleHeld: dialog.querySelector('h2').getBoundingClientRect().top === title,
            scrolled: list.scrollTop,
          };
          list.scrollTop = 0;
          return result;
        }""")
        self.assertTrue(measured['scrolls'], 'the list itself scrolls')
        self.assertFalse(measured['dialogScrolls'], 'the dialog does not scroll its title away')
        self.assertLessEqual(measured['past'], 0.5, 'the list paints past the dialog padding')
        self.assertTrue(measured['inside'], 'a row paints outside the dialog')
        self.assertAlmostEqual(measured['endGap'], 22, delta=0.5,
                               msg='the last row ends the dialog padding above its border')
        self.assertTrue(measured['titleHeld'], 'the title moved while the list scrolled')
        self.assertGreater(measured['scrolled'], 0)
        page.close()

    def test_a_short_transfer_list_keeps_its_natural_height(self):
        jobs = [self.transfer_job(index, f'notes-{index}.pdf') for index in range(1, 3)]
        page = self.transfer_list_page(jobs)
        page.locator('#mediaTransfersButton').click()
        expect(page.locator('#mediaTransfersList .media-transfers__row')).to_have_count(2)

        measured = page.evaluate("""() => {
          const dialog = document.querySelector('#mediaTransfersDialog');
          const list = document.querySelector('#mediaTransfersList');
          const rows = [...list.querySelectorAll('.media-transfers__row')];
          return {
            dividers: list.querySelectorAll('.media-transfers__divider').length,
            clientHeight: list.clientHeight,
            scrollHeight: list.scrollHeight,
            height: Math.round(dialog.getBoundingClientRect().height),
            borders: rows.map(row => getComputedStyle(row).borderBottomWidth),
            heights: rows.map(row => Math.round(row.getBoundingClientRect().height)),
          };
        }""")
        self.assertEqual(measured['dividers'], 0, 'two completed transfers carry no seam')
        self.assertEqual(measured['clientHeight'], measured['scrollHeight'], 'a two-row list scrolls')
        self.assertLess(measured['height'], 700, 'the dialog took its max height for two rows')
        self.assertEqual(measured['borders'], ['1px', '1px'])
        self.assertEqual(measured['heights'][0], measured['heights'][1])
        page.close()

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
        page._media_status_state['drop_after_settings'] = False
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

    def sample_companion(self, page, files):
        """A connected companion whose reported size is the bytes the browser actually sent."""
        header = {'Access-Control-Allow-Origin': self.live_server_url}
        def companion(route):
            url = route.request.url
            body = route.request.post_data_buffer or b''
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': len(files),
                           'total_size': sum(f['size'] for f in files),
                           'retention': '30', 'write_token': 'test-token'}
            elif url.endswith('/inspect'):
                uploaded = {'sha256': 'c' * 64, 'name': 'images (1).jpeg', 'family': 'image',
                            'size': len(body), 'reused': False}
                payload = dict(uploaded, uploaded_at='2026-10-28T12:00:00+00:00',
                               unused_since=None, delete_at=None)
            else:
                payload = {'files': files}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers=header)
        page.route('http://127.0.0.1:63174/**', companion)
        return page

    def choose_bytes(self, page, count):
        page.locator('[data-media-file]').set_input_files({
            'name': 'images (1).jpeg', 'mimeType': 'image/jpeg', 'buffer': b'\xff' * count})

    def test_media_size_reads_in_the_smallest_unit_that_shows_a_number(self):
        page = self.sample_companion(
            self.browser.new_page(viewport={'width': 1440, 'height': 900}),
            [{'sha256': 'c' * 64, 'name': 'images (1).jpeg', 'family': 'image', 'size': 12345,
              'uploaded_at': '2026-10-28T12:00:00+00:00', 'unused_since': None, 'delete_at': None}])
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-entry-open="media"]').first.dispatch_event('click')
        meta = page.locator('[data-media-selected-meta]')
        self.choose_bytes(page, 12345)
        expect(meta).to_have_text('Image · 12.3 KB')
        self.choose_bytes(page, 512)
        expect(meta).to_have_text('Image · 512 B')
        self.choose_bytes(page, 1000000)
        expect(meta).to_have_text('Image · 1 MB')
        self.choose_bytes(page, 999999)
        expect(meta).to_have_text('Image · 1 MB')
        # The cap and the gigabyte boundary cannot be uploaded as a body; the shipped function is asked
        # directly, so the whole unit chain is still asserted rather than assumed.
        self.assertEqual(page.evaluate('window.gkpsFormatSize(200000000)'), '200 MB')
        self.assertEqual(page.evaluate('window.gkpsFormatSize(1000000000)'), '1 GB')
        self.assertEqual(page.evaluate('window.gkpsFormatSize(0)'), '0 B')
        page.locator('[data-media-tab-button="library"]').click()
        expect(page.locator('[data-media-hash] small').first).to_have_text('Image · 12.3 KB')

    def test_media_library_row_and_total_use_the_chosen_label(self):
        files = [
            {'sha256': 'a' * 64, 'name': 'images (1).jpeg', 'family': 'image', 'size': 12345,
             'uploaded_at': '2026-10-28T12:00:00+00:00', 'unused_since': None, 'delete_at': None},
            {'sha256': 'b' * 64, 'name': 'edge.jpeg', 'family': 'image', 'size': 999999,
             'uploaded_at': '2026-10-27T12:00:00+00:00', 'unused_since': None, 'delete_at': None},
        ]
        page = self.sample_companion(
            self.browser.new_page(viewport={'width': 1440, 'height': 900}), files)
        page.goto(self.live_server_url + reverse('web-media-library'))
        rows = page.locator('.media-library__meta')
        expect(rows.nth(0)).to_have_text('Image · 28 Oktober 2026 · 12.3 KB')
        expect(rows.nth(1)).to_have_text('Image · 27 Oktober 2026 · 1 MB')
        page.locator('#mediaStatusButton').click()
        expect(page.locator('#mediaTotalSize')).to_have_text('1 MB')

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
        # spec 140: the right padding is the controls' reserved column, not the
        # spec 117 resting inset
        desktop_acts = desktop_row.locator('.entry__acts').bounding_box()['width']
        self.assertGreaterEqual(
            desktop_row.evaluate('el => parseFloat(getComputedStyle(el).paddingRight)'),
            desktop_acts + 4)
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
        phone_acts = row.locator('.entry__acts').bounding_box()['width']
        self.assertGreaterEqual(
            row.evaluate('el => parseFloat(getComputedStyle(el).paddingRight)'),
            phone_acts + 4)
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

    def test_every_transfer_row_shares_one_icon_column(self):
        page = self.transfers_page()
        marks = page.evaluate("""() => [...document.querySelectorAll(
            '#mediaTransfersList .media-transfers__mark')]
            .map(mark => Math.round(mark.getBoundingClientRect().width * 100) / 100)""")
        self.assertEqual(set(marks), {32.0}, 'the mark column is not one 32px column')
        edges = page.evaluate("""() => {
            const rows = [...document.querySelectorAll('#mediaTransfersList .media-transfers__row')];
            const lefts = selector => rows.map(row => row.querySelector(selector).getBoundingClientRect().left);
            return {glyph: lefts('.media-transfers__mark svg'),
                    name: lefts('.media-transfers__main strong'),
                    label: lefts('.media-transfers__main span')};
        }""")
        for key, values in edges.items():
            spread = max(values) - min(values)
            self.assertLessEqual(
                spread, 0.5,
                f'{key} left edges differ by {spread:.1f}px: {sorted(round(v, 1) for v in values)}')

    def test_a_long_transfer_name_still_ellipsizes_at_the_pinned_column(self):
        page = self.transfers_page()
        rows = page.evaluate("""() => [...document.querySelectorAll('#mediaTransfersList .media-transfers__row')]
            .map(row => {
                const name = row.querySelector('strong');
                return {name: name.textContent, scroll: name.scrollWidth, client: name.clientWidth,
                        height: row.getBoundingClientRect().height};
            })""")
        long_rows = [row for row in rows if row['scroll'] > row['client']]
        self.assertEqual(len(long_rows), 2, 'the two long names no longer truncate')
        for row in long_rows:
            # the list's 534px − 8px of row padding − 32px of mark − the 12px gap
            self.assertEqual(row['client'], 482, row['name'])
            self.assertEqual(round(row['height']), 72, row['name'])

    def test_the_icon_column_holds_in_a_narrow_dialog(self):
        page = self.transfers_page(width=420)
        dialog = page.locator('#mediaTransfersDialog').bounding_box()
        self.assertEqual(round(dialog['width']), 382,
                         'a 420px window renders the dialog at 382px')
        rows = page.evaluate("""() => {
            const dialog = document.querySelector('#mediaTransfersDialog').getBoundingClientRect();
            return [...document.querySelectorAll('#mediaTransfersList .media-transfers__row')].map(row => {
                const name = row.querySelector('strong');
                const mark = row.querySelector('.media-transfers__mark').getBoundingClientRect();
                return {scroll: name.scrollWidth, client: name.clientWidth,
                        mark: Math.round(mark.width * 100) / 100,
                        glyph: row.querySelector('.media-transfers__mark svg').getBoundingClientRect().left,
                        name_left: name.getBoundingClientRect().left,
                        overflow: row.getBoundingClientRect().right - dialog.right};
            });
        }""")
        self.assertEqual({row['mark'] for row in rows}, {32.0}, 'the mark column collapsed')
        self.assertLessEqual(max(row['glyph'] for row in rows) - min(row['glyph'] for row in rows), 0.5)
        self.assertLessEqual(max(row['name_left'] for row in rows) - min(row['name_left'] for row in rows),
                             0.5)
        self.assertLessEqual(max(row['overflow'] for row in rows), 0, 'a row is wider than the dialog')
        truncating = [row for row in rows if row['scroll'] > row['client']]
        self.assertEqual(len(truncating), 3, 'the narrow dialog no longer truncates three names')
        for row in truncating:
            self.assertEqual(row['client'], 284, 'the text column is not what the layout reserves')


    # ---- spec 148: the file list holds still while it refreshes ----

    SAMPLER = """(function () {
      if (window.__sampling) return;
      window.__sampling = true;
      window.__samples = [];
      window.__draws = 0;      // frames whose list differed from the one before: a draw that showed
      window.__sig = null;     // the signature of the last list drawn
      function sample() {
        var list = document.getElementById('mediaFileList');
        if (list) {
          var rows = [].slice.call(list.querySelectorAll('.media-library__file'));
          var tops = rows.map(function (row) {
            return Math.round(row.getBoundingClientRect().top * 100) / 100;
          });
          var listHeight = Math.round(list.getBoundingClientRect().height * 100) / 100;
          var signature = rows.length + '|' + tops.join(',') + '|' + listHeight;
          if (window.__sig === null) { window.__sig = signature; }
          else if (signature !== window.__sig) { window.__sig = signature; window.__draws += 1; }
          window.__samples.push({
            rows: rows.length,
            tops: tops,
            placeholder: list.querySelectorAll('.media-library__unused').length,
            listHeight: listHeight
          });
        }
        requestAnimationFrame(sample);
      }
      requestAnimationFrame(sample);
    })();"""

    def _sampled_library(self, media, references=None, extra_row=False):
        """A connected library page that records every frame of its file list."""
        inventory = [{'sha256': media.pk, 'name': media.display_filename,
                      'family': media.family, 'size': media.byte_count,
                      'uploaded_at': '2026-10-28T09:00:00+00:00',
                      'unused_since': None, 'delete_at': None}]
        if extra_row:
            inventory.append({'sha256': 'd' * 64, 'name': 'poster.png', 'family': 'image',
                              'size': 1024, 'uploaded_at': '2026-10-27T09:00:00+00:00',
                              'unused_since': None, 'delete_at': None})

        def companion(route):
            url = route.request.url
            if url.endswith('/status'):
                payload = {'connection': 'connected', 'file_count': len(inventory),
                           'total_size': media.byte_count, 'retention': '30',
                           'write_token': 'test-token'}
            elif url.endswith('/settings'):
                payload = {'retention': '30'}
            elif url.endswith('/files') or url.endswith('/references'):
                payload = {'files': inventory}
            else:
                payload = {'error': 'Not found'}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                          headers={'Access-Control-Allow-Origin': self.live_server_url})

        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.route('http://127.0.0.1:63174/**', companion)
        if references is not None:
            page.route('**/media-library/references/', references)
        page.add_init_script(self.SAMPLER)
        page.goto(self.live_server_url + reverse('web-media-library'))
        expect(page.locator('.media-library__filename').first).to_have_text('notes.pdf')
        page.wait_for_timeout(300)
        return page

    def _reset_sampler(self, page):
        page.evaluate('() => { window.__samples = []; window.__draws = 0; window.__sig = null; }')

    def _assert_no_row_moved(self, page, label):
        frames = page.evaluate('() => window.__samples')
        self.assertTrue(frames, 'the sampler recorded no frame while ' + label)
        settled = frames[-1]
        self.assertGreater(settled['rows'], 0, 'the list never drew a row while ' + label)
        spread = [0.0] * settled['rows']
        for frame in frames:
            if frame['rows'] != settled['rows']:
                continue
            for index, top in enumerate(frame['tops']):
                spread[index] = max(spread[index], abs(top - settled['tops'][index]))
        self.assertEqual(spread, [0.0] * settled['rows'],
                         'rows moved while ' + label + ': ' + repr(spread))

    @staticmethod
    def _cancel_remove(page):
        page.locator('.media-library__remove').first.click()
        expect(page.locator('#mediaRemoveDialog')).to_be_visible()
        page.keyboard.press('Escape')
        expect(page.locator('#mediaRemoveDialog')).not_to_be_visible()

    @staticmethod
    def _save_settings(page):
        page.locator('#mediaSettingsButton').click()
        page.locator('#mediaSaveSettings').click()
        expect(page.locator('#mediaSettingsDialog')).not_to_be_visible()

    def test_a_library_refresh_never_moves_a_row(self):
        page = self._sampled_library(self.referenced_media, extra_row=True)
        for label, trigger in (('a cancelled remove', self._cancel_remove),
                               ('a saved setting', self._save_settings)):
            self._reset_sampler(page)
            trigger(page)
            page.wait_for_timeout(500)
            self._assert_no_row_moved(page, label)
        page.close()

    def test_clicking_share_online_never_moves_a_library_row(self):
        page = self._sampled_library(self.referenced_media, extra_row=True)
        share = page.locator('.media-library__cloud-button[title="Share online"]').first
        expect(share).to_be_visible()
        self._reset_sampler(page)
        with patch('multimedia.web.reading.views.media_handoff.begin_share',
                   return_value=(None, SimpleNamespace(
                       expires_at=datetime(2026, 10, 28, tzinfo=timezone.utc)))):
            share.click()
            page.wait_for_timeout(600)
        self._assert_no_row_moved(page, 'Share online')
        page.close()

    def test_the_library_list_is_drawn_once_per_refresh(self):
        page = self._sampled_library(self.referenced_media, extra_row=True)
        self._reset_sampler(page)
        self._cancel_remove(page)
        page.wait_for_timeout(500)
        # a cancelled remove changes nothing about the library, so a correct page draws the same
        # picture twice: what this catches is the extra pass that draws a different one
        self.assertLessEqual(page.evaluate('() => window.__draws'), 1,
                             'one refresh drew the file list more than once')

        page.evaluate('() => { window.__samples = []; window.__sig = null; }')
        page.reload()
        page.wait_for_timeout(800)
        frames = [frame for frame in page.evaluate('() => window.__samples') if frame['rows']]
        self.assertTrue(frames, 'the first load never drew a row')
        self.assertEqual(frames[0]['listHeight'], frames[-1]['listHeight'],
                         'the first load drew a short list and then grew it')
        self.assertEqual(max(f['listHeight'] for f in frames), frames[-1]['listHeight'],
                         'the list grew after it first appeared')
        page.close()

    def test_a_known_reference_never_shows_the_placeholder(self):
        media = self.referenced_media

        def held(route):
            time.sleep(0.2)
            route.continue_()

        page = self._sampled_library(media, references=held)
        frames = page.evaluate('() => window.__samples')
        self.assertTrue(frames)
        placeholders = [frame['placeholder'] for frame in frames if frame['rows']]
        self.assertEqual(placeholders, [0] * len(placeholders),
                         'a file with known references showed "Service uses unavailable"')
        page.close()

    def test_a_failed_references_request_draws_the_placeholder_once(self):
        def broken(route):
            route.fulfill(status=500, body='{}', content_type='application/json')

        page = self._sampled_library(self.referenced_media, references=broken,
                                     extra_row=True)
        expect(page.locator('.media-library__unused').first).to_contain_text(
            'Service uses unavailable')
        self._reset_sampler(page)
        self._save_settings(page)
        page.wait_for_timeout(500)
        # the degraded state is one picture either way, so this counts visible draws: the guarded
        # failure is a page that redraws it repeatedly or moves a row, not the pass count itself
        self.assertLessEqual(page.evaluate('() => window.__draws'), 1,
                             'a failed references read redrew the file list')
        expect(page.locator('.media-library__unused').first).to_contain_text(
            'Service uses unavailable')
        self._assert_no_row_moved(page, 'a failed references read')
        page.close()

    def test_the_status_poll_leaves_the_list_where_it_is(self):
        page = self._sampled_library(self.referenced_media, extra_row=True)
        self._reset_sampler(page)
        page.wait_for_timeout(2500)  # one 2s poll
        self._assert_no_row_moved(page, 'a status poll')
        page.close()
