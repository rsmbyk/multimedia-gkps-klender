"""Actual local audio playback in Preview and on the projector (spec 115)."""
import io
import re
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

    def _page(self, path, available=True, payload=None):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        body = _wav() if payload is None else payload
        def serve(route):
            route.fulfill(status=200 if available else 404,
                          headers={'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                                   'Content-Type': 'application/octet-stream'},
                          body=body if available else b'')
        page.route('http://127.0.0.1:63174/v1/files/' + self.media.sha256, serve)
        page.goto(self.live_server_url + path)
        return page

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

    def test_preview_times_read_current_over_total_beside_the_bar(self):
        """The times read `current / total`, right-aligned under the seek bar (spec 154)."""
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.audio-player')).to_be_visible()
        expect(page.locator('.audio-player__times')).to_have_text(re.compile(r'^\d+:\d\d\s*/\s*\d+:\d\d$'))
        self._assert_times_are_one_right_aligned_pair(page)
        page.keyboard.press('Space')
        expect(page.locator('.audio-player__play')).to_have_attribute('data-playing', 'true')
        page.locator('.audio-player__seek').fill('1')
        page.wait_for_timeout(150)
        self._assert_times_are_one_right_aligned_pair(page)
        page.close()

    def _assert_times_are_one_right_aligned_pair(self, page):
        geometry = page.evaluate("""() => {
          const box = (el) => { const r = el.getBoundingClientRect();
            return {left: r.left, right: r.right, top: r.top, width: r.width}; };
          const root = document.querySelector('#previewModal');
          const times = root.querySelector('.audio-player__times');
          return {
            elapsed: box(root.querySelector('[data-audio-elapsed]')),
            separator: box(times.querySelector('.audio-player__separator')),
            total: box(root.querySelector('[data-audio-total]')),
            seek: box(root.querySelector('.audio-player__seek')),
          };
        }""")
        elapsed, separator = geometry['elapsed'], geometry['separator']
        total, seek = geometry['total'], geometry['seek']
        self.assertGreater(separator['width'], 0, 'the separator draws')
        self.assertAlmostEqual(elapsed['top'], total['top'], delta=1,
                               msg='the two times stand on one line')
        self.assertLessEqual(separator['left'] - elapsed['right'], 10,
                             '5px between the played time and the separator')
        self.assertLessEqual(total['left'] - separator['right'], 10,
                             '5px between the separator and the total')
        self.assertGreater(total['left'], elapsed['left'],
                           'the played time comes first, then the total')
        self.assertAlmostEqual(total['right'], seek['right'], delta=1,
                               msg="the pair ends on the seek bar's right edge")
        self.assertGreater(elapsed['left'], seek['left'] + (seek['right'] - seek['left']) / 2,
                           "the played time no longer sits at the bar's left end")

    def test_projector_space_navigation_and_reset(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__audio-player')).to_be_visible()
        page.keyboard.press('Space')
        expect(page.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'true')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__audio-player')).to_have_count(0)
        page.keyboard.press('Control+ArrowLeft')
        expect(page.locator('.screen.is-active .screen__audio-play')).to_have_attribute('data-playing', 'false')
        self.assertEqual(page.locator('.screen.is-active [data-audio-elapsed]').inner_text(), '0:00')
        page.close()

    def test_projector_audio_control_is_painted_and_toggles(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        control = page.locator('.screen.is-active .screen__audio-play')
        expect(control).to_be_visible()
        box = control.bounding_box()
        self.assertGreaterEqual(box['width'], 44)
        self.assertGreaterEqual(box['height'], 44)
        control.click()
        expect(control).to_have_attribute('data-playing', 'true')
        expect(control).to_have_attribute('aria-label', 'Pause audio')
        control.click()
        expect(control).to_have_attribute('data-playing', 'false')
        expect(control).to_have_attribute('aria-label', 'Play audio')
        page.close()

    def test_projector_audio_control_hides_as_the_chrome_settles_and_returns(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        control = page.locator('.screen.is-active .screen__audio-play')
        box = page.locator('.screen.is-active .screen__audio-box')
        self.assertEqual(control.evaluate('(el) => getComputedStyle(el, "::before").borderLeftWidth'), '12px')
        control.click()
        expect(control).to_have_attribute('data-playing', 'true')
        page.wait_for_timeout(3700)
        expect(box).to_have_class('screen__audio-box is-idle')
        expect(control).to_have_css('opacity', '0')
        self.assertEqual(control.evaluate('(el) => getComputedStyle(el).pointerEvents'), 'none')
        self.assertEqual(control.bounding_box()['height'], 48)
        expect(page.locator('.screen.is-active .screen__audio-seek')).to_have_css('opacity', '0.52')
        page.mouse.move(300, 300)
        page.wait_for_timeout(400)
        expect(box).not_to_have_class('screen__audio-box is-idle')
        expect(control).to_have_css('opacity', '1')
        self.assertEqual(control.evaluate('(el) => getComputedStyle(el, "::before").borderLeftWidth'), '0px')
        control.click()
        expect(control).to_have_attribute('data-playing', 'false')
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
