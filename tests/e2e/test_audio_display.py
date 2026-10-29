"""Actual local audio playback in Preview and on the projector (spec 115)."""
import io
import unittest
import wave
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


def _wav():
    output = io.BytesIO()
    with wave.open(output, 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(1)
        audio.setframerate(8000)
        audio.writeframes(bytes([128, 144, 160, 144]) * 20000)
    return output.getvalue()


DENY_FULLSCREEN = """Object.defineProperty(Element.prototype, 'requestFullscreen', {
  configurable: true, value: function () { return Promise.reject(new Error('denied')); }});"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AudioDisplayE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Audio service', date=date(2026, 10, 19), is_active=True)
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=1, title='Opening', text='Welcome')
        self.media = tatib.MediaIdentity.objects.create(
            sha256='b' * 64, byte_count=len(_wav()), family='audio', display_filename='recording.wav')
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=2,
            media=self.media, media_filename='recording.wav', title='Musik persembahan')
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=3, title='Closing', text='Amen')
        self.untitled = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=4,
            media=self.media, media_filename='recording.wav', title='')
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
        body = _wav() if payload is None else payload
        def serve(route):
            route.fulfill(status=200 if available else 404,
                          headers={'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                                   'Content-Type': 'application/octet-stream'},
                          body=body if available else b'')
        page.route('http://127.0.0.1:63174/v1/files/' + self.media.sha256, serve)
        if init_script:
            page.add_init_script(init_script)
        page.goto(self.live_server_url + path)
        return page

    def _open_projector_audio(self, page):
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__audio-player')).to_be_visible()

    def test_preview_plays_seeks_and_closes(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.audio-player')).to_be_visible()
        self.assertEqual(page.locator('#previewTitle').inner_text(), 'Musik persembahan')
        self.assertEqual(page.locator('.audio-player__filename').inner_text(), 'recording.wav')
        page.keyboard.press('Space')
        expect(page.locator('.audio-player__play')).to_have_attribute('data-playing', 'true')
        page.locator('.audio-player__seek').fill('1')
        self.assertGreater(page.locator('.preview__audio').evaluate(
            '(host) => Number(host.querySelector("[data-audio-elapsed]").textContent.split(":")[1])'), 0)
        page.keyboard.press('Escape')
        expect(page.locator('#previewModal')).not_to_be_visible()
        page.close()

    def test_projector_space_navigation_and_reset(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__audio-player')).to_be_visible()
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'true')
        # Spec 155: a playing recording holds the screen, so the pause comes first.
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'false')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__audio-player')).to_have_count(0)
        page.keyboard.press('Control+ArrowLeft')
        expect(page.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'false')
        self.assertEqual(page.locator('.screen.is-active [data-audio-elapsed]').inner_text(), '0:00')
        page.close()

    def test_projector_playing_audio_enters_fullscreen(self):
        page = self._page(f'/projector?service={self.service.pk}')
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        reading = page.evaluate("""() => {
            const element = document.fullscreenElement;
            const box = element.getBoundingClientRect();
            const style = getComputedStyle(element);
            return {
              isAudioBox: element.matches('.screen.is-active .screen__audio-box'),
              width: box.width, height: box.height, x: box.x, y: box.y,
              viewport: [window.innerWidth, window.innerHeight],
              background: style.backgroundColor,
              cueInside: element.contains(document.getElementById('corner-cue')),
            };
        }""")
        self.assertTrue(reading['isAudioBox'])
        self.assertEqual([reading['width'], reading['height']], reading['viewport'])
        self.assertEqual([reading['x'], reading['y']], [0, 0])
        self.assertEqual(reading['background'], 'rgb(23, 22, 19)')
        self.assertFalse(reading['cueInside'])
        page.close()

    def test_projector_playing_audio_locks_navigation(self):
        page = self._page(f'/projector?service={self.service.pk}')
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'true')
        current = page.locator('body').get_attribute('data-current-screen')
        for key in ['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp', 'PageDown', 'PageUp',
                    'Home', 'End', 'Control+ArrowRight', 'Shift+ArrowRight']:
            page.keyboard.press(key)
            self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current, key)
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'true')
        page.close()

    def test_projector_playing_audio_keeps_go_to_shut(self):
        page = self._page(f'/projector?service={self.service.pk}')
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'true')
        page.keyboard.press('g')
        expect(page.locator('#projectorFind')).to_be_hidden()
        page.keyboard.press('j')
        self.assertNotIn('entry-list-open', page.locator('body').get_attribute('class'))
        page.close()

    def test_projector_playing_audio_ignores_pointer_navigation(self):
        # A refused fullscreen leaves the zones painted, so the pointer guard is the one under test.
        page = self._page(f'/projector?service={self.service.pk}', init_script=DENY_FULLSCREEN)
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'true')
        current = page.locator('body').get_attribute('data-current-screen')
        zone = page.locator('.mouse-zone--next')
        zone.click(force=True)      # the first click belongs to the page's fullscreen attempt
        zone.click(force=True)
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current)
        page.locator('#cue-service').click(force=True)
        self.assertNotIn('entry-list-open', page.locator('body').get_attribute('class'))
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'true')
        page.close()

    def test_projector_pausing_audio_returns_the_screen(self):
        page = self._page(f'/projector?service={self.service.pk}')
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        current = page.locator('body').get_attribute('data-current-screen')
        # the clock starts counting a moment after the keypress (blob -> metadata -> play),
        # so wait for the readout rather than for a number of milliseconds
        page.wait_for_function("""() => {
            const elapsed = document.querySelector('.screen.is-active [data-audio-elapsed]');
            return elapsed && elapsed.textContent !== '0:00';
        }""")
        played = page.locator('.screen.is-active [data-audio-elapsed]').inner_text()
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement === null')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'false')
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current)
        self.assertNotEqual(played, '0:00')
        self.assertEqual(page.locator('.screen.is-active [data-audio-elapsed]').inner_text(), played)
        page.keyboard.press('Control+ArrowRight')
        self.assertNotEqual(page.locator('body').get_attribute('data-current-screen'), current)
        page.close()

    def test_projector_escape_leaves_fullscreen_and_pauses_audio(self):
        page = self._page(f'/projector?service={self.service.pk}')
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        current = page.locator('body').get_attribute('data-current-screen')
        page.keyboard.down('Escape')
        page.wait_for_timeout(1200)
        page.keyboard.up('Escape')
        page.wait_for_function('() => document.fullscreenElement === null')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'false')
        self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current)
        page.close()

    def test_projector_audio_end_returns_the_screen(self):
        page = self._page(f'/projector?service={self.service.pk}')
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        page.wait_for_function('() => document.fullscreenElement !== null')
        page.evaluate("""() => {
            const seek = document.querySelector('.screen.is-active [data-audio-seek]');
            const box = seek.getBoundingClientRect();
            seek.dispatchEvent(new PointerEvent('pointerdown', {clientX: box.left + box.width - 2,
                clientY: box.top + box.height / 2, pointerId: 1, bubbles: true}));
        }""")
        page.wait_for_function('() => document.fullscreenElement === null', timeout=8000)
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'false')
        page.close()

    def test_projector_refused_fullscreen_still_locks_audio(self):
        page = self._page(f'/projector?service={self.service.pk}', init_script=DENY_FULLSCREEN)
        self._open_projector_audio(page)
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'true')
        self.assertIsNone(page.evaluate('document.fullscreenElement'))
        current = page.locator('body').get_attribute('data-current-screen')
        for key in ['ArrowRight', 'Control+ArrowRight', 'Home']:
            page.keyboard.press(key)
            self.assertEqual(page.locator('body').get_attribute('data-current-screen'), current, key)
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active [data-audio-play]')).to_have_attribute(
            'data-playing', 'false')
        page.keyboard.press('Control+ArrowRight')
        self.assertNotEqual(page.locator('body').get_attribute('data-current-screen'), current)
        page.close()

    def test_missing_audio_states(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]), available=False)
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.preview__audio-unavailable')).to_be_visible()
        page.close()
        page = self._page(f'/projector?service={self.service.pk}', available=False)
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__image-missing')).to_be_visible()
        page.close()

    def test_untitled_preview_and_projector_idle_display_off(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.untitled.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('#previewModal .preview__head')).to_be_hidden()
        expect(page.locator('.audio-player__filename')).to_have_text('recording.wav')
        page.close()

        projector = self._page(f'/projector?service={self.service.pk}')
        projector.keyboard.press('Space')
        projector.keyboard.press('Control+ArrowRight')
        expect(projector.locator('.screen.is-active .screen__audio-player')).to_be_visible()
        self.assertNotIn('recording.wav', projector.locator('.screen.is-active').inner_text())
        projector.keyboard.press('Space')
        expect(projector.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'true')
        projector.wait_for_timeout(3700)
        expect(projector.locator('.screen.is-active .screen__audio-box')).to_have_class('screen__audio-box is-idle')
        projector.keyboard.press('Space')
        expect(projector.locator('.screen.is-active .screen__audio-box')).not_to_have_class('screen__audio-box is-idle')
        projector.keyboard.press('Space')
        expect(projector.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'true')
        projector.evaluate("""() => {
          const channel = new BroadcastChannel('gkps-service-display');
          channel.postMessage({type: 'stop'});
          channel.close();
        }""")
        expect(projector.locator('body')).to_have_attribute('data-showing', 'false')
        expect(projector.locator('.screen.is-active .screen__audio-player')).to_be_hidden()
        projector.close()

    def test_unrecognized_audio_bytes_show_missing(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]), payload=b'not audio')
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.preview__audio-unavailable')).to_be_visible()
        page.close()
