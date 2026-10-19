"""Video playback in the service Preview and projector (spec 116)."""
import hashlib
import re
import unittest
from datetime import date
from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


def _webm():
    return (Path(__file__).resolve().parents[2]
            / 'specs/116-video-media-display/demo.webm').read_bytes()


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class VideoDisplayE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.video_bytes = _webm()
        self.sha = hashlib.sha256(self.video_bytes).hexdigest()
        self.service = tatib.TataIbadah.objects.create(
            name='Video service', date=date(2026, 10, 19), is_active=True)
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=1, title='Opening', text='Welcome')
        self.media = tatib.MediaIdentity.objects.create(
            sha256=self.sha, byte_count=len(self.video_bytes), family='video',
            display_filename='library-demo.webm')
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=2,
            media=self.media, media_filename='misleading-extension.mp4', title='Welcome video')
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=3, title='Closing', text='Amen')
        self.untitled = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=4,
            media=self.media, media_filename='misleading-extension.mp4', title='')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _page(self, path, available=True, payload=None, init_script=None):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        body = self.video_bytes if payload is None else payload

        def serve(route):
            route.fulfill(status=200 if available else 404,
                          headers={'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                                   'Content-Type': 'application/octet-stream'},
                          body=body if available else b'')

        page.route('http://127.0.0.1:63174/v1/files/' + self.sha, serve)
        if init_script:
            page.add_init_script(init_script)
        page.goto(self.live_server_url + path)
        return page

    def _open_projector_video(self, page, available=True):
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        video = page.locator('.screen.is-active [data-media-video]')
        expect(video).to_be_visible()
        if available:
            expect(video.locator('video')).to_be_visible()
        return video

    def test_preview_plays_seeks_and_closes(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        player = page.locator('.preview__video')
        expect(player).to_be_visible()
        expect(page.locator('#previewTitle')).to_have_text('Welcome video')
        expect(player.locator('.preview__video-filename')).to_have_text('misleading-extension.mp4')
        video = player.locator('video')
        expect(video).to_have_js_property('paused', True)
        player.locator('[data-video-play]').first.click()
        expect(player.locator('[data-video-play]').first).to_have_attribute('data-playing', 'true')
        seek = player.locator('[data-video-seek]')
        seek.evaluate("""el => {
          el.value = '2';
          el.dispatchEvent(new Event('input', {bubbles:true}));
        }""")
        expect(video).to_have_js_property('currentTime', 2)
        page.keyboard.press('Space')
        expect(video).to_have_js_property('paused', True)
        page.keyboard.press('Escape')
        expect(page.locator('#previewModal')).not_to_be_visible()
        page.close()

    def test_untitled_preview_has_no_header_and_missing_video_is_named(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.untitled.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('#previewModal .preview__head')).to_be_hidden()
        expect(page.locator('.preview__video-filename')).to_have_text('misleading-extension.mp4')
        page.keyboard.press('Escape')
        page.close()

        missing = self._page(reverse('web-tatib-service', args=[self.service.pk]), available=False)
        row = missing.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(missing.locator('.preview__video-unavailable')) \
            .to_contain_text('Video unavailable on this computer')
        missing.close()

    def test_projector_fullscreen_play_pause_and_navigation_guard(self):
        page = self._page(reverse('web-service-projector', args=[self.service.pk]))
        host = self._open_projector_video(page)
        video = host.locator('video')
        page.keyboard.press('Space')
        expect(video).to_have_js_property('paused', False)
        page.wait_for_function('document.fullscreenElement === document.querySelector(".screen.is-active [data-media-video]")')
        current_screen = page.locator('body').get_attribute('data-current-screen')
        self.assertTrue(page.evaluate("""() => {
          const host = document.querySelector('.screen.is-active [data-media-video]');
          return document.fullscreenElement === host && host.classList.contains('is-playing');
        }"""))
        page.keyboard.press('ArrowRight')
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current_screen)
        page.keyboard.press('Control+ArrowRight')
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current_screen)
        expect(host.locator('[data-video-controls]')).to_be_visible()
        page.keyboard.press('Space')
        expect(video).to_have_js_property('paused', True)
        page.wait_for_function('document.fullscreenElement === null')
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current_screen)
        page.keyboard.press('Control+ArrowRight')
        self.assertNotEqual(page.locator('body').get_attribute('data-current-screen'), current_screen)
        page.close()

    def test_fullscreen_idle_hides_controls_and_escape_pauses(self):
        page = self._page(reverse('web-service-projector', args=[self.service.pk]))
        host = self._open_projector_video(page)
        page.keyboard.press('Space')
        page.wait_for_function('document.fullscreenElement !== null')
        page.wait_for_timeout(2200)
        expect(host).to_have_class(re.compile(r'\bis-idle\b'))
        page.keyboard.press('Escape')
        page.wait_for_function('document.fullscreenElement === null')
        expect(host.locator('video')).to_have_js_property('paused', True)
        page.close()

    def test_fullscreen_denial_keeps_normal_projector_playback(self):
        page = self._page(
            reverse('web-service-projector', args=[self.service.pk]),
            init_script="""Object.defineProperty(Element.prototype, 'requestFullscreen', {
              configurable: true, value: function () { return Promise.reject(new Error('denied')); }
            });""")
        host = self._open_projector_video(page)
        page.keyboard.press('Space')
        expect(host.locator('video')).to_have_js_property('paused', False)
        page.wait_for_timeout(150)
        self.assertIsNone(page.evaluate('document.fullscreenElement'))
        current_screen = page.locator('body').get_attribute('data-current-screen')
        page.keyboard.press('Control+ArrowRight')
        self.assertNotEqual(page.locator('body').get_attribute('data-current-screen'), current_screen)
        page.close()

    def test_navigation_and_display_off_stop_and_reset_video(self):
        page = self._page(reverse('web-service-projector', args=[self.service.pk]))
        self._open_projector_video(page)
        video = page.locator('[data-media-video] video').first
        video.evaluate('(element) => { element.currentTime = 2; }')
        page.keyboard.press('Space')
        expect(video).to_have_js_property('paused', False)
        page.keyboard.press('Space')
        page.wait_for_function('document.fullscreenElement === null')
        page.keyboard.press('Control+ArrowRight')
        expect(video).to_have_js_property('paused', True)
        self.assertIsNone(video.get_attribute('src'))

        page.keyboard.press('Control+ArrowLeft')
        expect(video).to_be_visible()
        expect(video).to_have_js_property('paused', True)
        self.assertEqual(video.evaluate('(element) => element.currentTime'), 0)
        page.keyboard.press('Space')
        expect(video).to_have_js_property('paused', False)
        page.evaluate("""() => {
          const channel = new BroadcastChannel('gkps-service-display');
          channel.postMessage({type: 'stop'});
          channel.close();
        }""")
        expect(page.locator('body')).to_have_attribute('data-showing', 'false')
        expect(video).to_have_js_property('paused', True)
        self.assertIsNone(video.get_attribute('src'))
        page.wait_for_function('document.fullscreenElement === null')
        page.close()

    def test_pending_video_request_cannot_replace_newer_screen(self):
        init_script = f"""(() => {{
          const originalFetch = window.fetch.bind(window);
          const target = '/v1/files/{self.sha}';
          window.fetch = (input, options) => String(input).includes(target)
            ? new Promise((resolve, reject) => setTimeout(() =>
                originalFetch(input, options).then(resolve, reject), 600))
            : originalFetch(input, options);
        }})();"""
        page = self._page(reverse('web-service-projector', args=[self.service.pk]),
                          init_script=init_script)
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        video_screen = page.locator('.screen.is-active [data-media-video]')
        expect(video_screen).to_be_visible()
        page.keyboard.press('Control+ArrowRight')
        current_screen = page.locator('body').get_attribute('data-current-screen')
        page.wait_for_timeout(750)
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current_screen)
        expect(page.locator('.screen.is-active [data-media-video]')).to_have_count(0)
        self.assertTrue(page.locator('video').evaluate_all('(elements) => elements.every((item) => item.paused)'))
        page.close()

    def test_missing_and_unrecognized_video_bytes_use_video_missing_state(self):
        page = self._page(reverse('web-service-projector', args=[self.service.pk]), available=False)
        host = self._open_projector_video(page, available=False)
        expect(host.locator('.screen__video-missing')).to_be_visible()
        page.close()

        page = self._page(reverse('web-tatib-service', args=[self.service.pk]), payload=b'not a video')
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.preview__video-unavailable')).to_be_visible()
        page.close()
