"""The Preview body's focus ring and the play shortcut (spec 159).

The body holds focus while a preview is open, so the space bar that plays or pauses a preview also
flips the browser's `:focus-visible` on it — and because the body is laid out over the dialog's whole
box in audio and video previews, its inset ring reads as a border on the modal.

These cases assert the painted result, not `:focus-visible`: the body keeps focus by design
(`research.md` D003), so the flag stays true while the outline is what changes.
"""
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


OUTLINE = """() => {
  const body = document.querySelector('.preview__body');
  if (!body) return 'no body';
  const cs = getComputedStyle(body);
  if (cs.outlineStyle === 'none') return 'none';
  return cs.outlineWidth + ' ' + cs.outlineStyle + ' ' + cs.outlineColor + ' offset ' + cs.outlineOffset;
}"""

RING = '2px solid rgb(28, 92, 60) offset -2px'


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PreviewBodyRingE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ring service', date=date(2026, 10, 29), is_active=True)
        self.sound = tatib.MediaIdentity.objects.create(
            sha256='c' * 64, byte_count=len(_wav()), family='audio', display_filename='recording.wav')
        self.moving = tatib.MediaIdentity.objects.create(
            sha256='d' * 64, byte_count=1024, family='video', display_filename='clip.mp4')
        self.audio = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=1,
            media=self.sound, media_filename='recording.wav', title='Musik persembahan')
        self.video = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=2,
            media=self.moving, media_filename='clip.mp4', title='Video penyembahan')
        self.topic = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=3,
            title='Renungan', text='Kalimat yang panjang untuk diuji. ' * 260)
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

    def _page(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

        def serve(route):
            route.fulfill(status=200, headers={
                'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                'Content-Type': 'application/octet-stream'}, body=_wav())

        page.route('http://127.0.0.1:63174/v1/files/' + self.sound.sha256, serve)
        page.route('http://127.0.0.1:63174/v1/files/' + self.moving.sha256, serve)
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        return page

    def _opener(self, page, entry):
        row = page.locator('#ti-e' + str(entry.pk))
        row.scroll_into_view_if_needed()
        return row.locator('[data-preview-open]')

    def _open_by_pointer(self, page, entry):
        self._opener(page, entry).click()
        expect(page.locator('.preview__body')).to_be_visible()

    def _open_by_keyboard(self, page, entry):
        self._opener(page, entry).focus()
        page.keyboard.press('Enter')
        expect(page.locator('.preview__body')).to_be_visible()

    def test_a_space_press_leaves_no_ring_on_the_audio_preview(self):
        page = self._page()
        self._open_by_pointer(page, self.audio)
        expect(page.locator('.audio-player')).to_be_visible()   # the player is only ready once its bytes load
        self.assertEqual(page.evaluate(OUTLINE), 'none')       # a pointer open paints nothing
        page.keyboard.press('Space')
        expect(page.locator('.audio-player__play')).to_have_attribute('data-playing', 'true')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.keyboard.press('Space')
        expect(page.locator('.audio-player__play')).to_have_attribute('data-playing', 'false')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.locator('.preview__body').click(position={'x': 8, 'y': 8})   # focus it again, as a person would
        page.keyboard.press('Space')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.close()

    def test_a_space_press_leaves_no_ring_on_the_video_preview(self):
        page = self._page()
        self._open_by_pointer(page, self.video)
        expect(page.locator('.preview__video')).to_be_visible()
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.keyboard.press('Space')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.keyboard.press('Space')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.close()

    def test_a_keyboard_opened_preview_wears_the_ring_until_the_first_space(self):
        page = self._page()
        self._open_by_keyboard(page, self.audio)
        self.assertEqual(page.evaluate(OUTLINE), RING)          # panel A: the reader sees where focus is
        page.keyboard.press('Space')
        self.assertEqual(page.evaluate(OUTLINE), 'none')        # and the shortcut takes it away
        page.close()

    def test_tab_brings_the_ring_back_after_a_space_press(self):
        page = self._page()
        self._open_by_pointer(page, self.audio)
        page.keyboard.press('Space')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        for _ in range(8):
            page.keyboard.press('Tab')
            if page.evaluate("() => document.activeElement === document.querySelector('.preview__body')"):
                break
        self.assertEqual(page.evaluate(OUTLINE), RING)
        page.close()

    def test_the_next_preview_gets_its_ring_back(self):
        page = self._page()
        self._open_by_pointer(page, self.audio)
        page.keyboard.press('Space')
        self.assertEqual(page.evaluate(OUTLINE), 'none')
        page.keyboard.press('Escape')
        expect(page.locator('.preview__body')).not_to_be_visible()
        self._open_by_keyboard(page, self.audio)
        self.assertEqual(page.evaluate(OUTLINE), RING)          # the class did not outlive its dialog
        page.close()

    def test_a_space_press_leaves_focus_on_the_body(self):
        """FR-003's invariant: the shortcut suppresses the paint, never the focus."""
        page = self._page()
        self._open_by_pointer(page, self.audio)
        page.keyboard.press('Space')
        self.assertTrue(page.evaluate(
            "() => document.activeElement === document.querySelector('.preview__body')"))
        page.close()

    def test_arrow_keys_still_scroll_a_long_text_preview(self):
        """The behaviour the body was made focusable for (spec 071), with this slice's rule in place."""
        page = self._page()
        self._open_by_pointer(page, self.topic)
        body = page.locator('.preview__body')
        self.assertGreater(body.evaluate('(el) => el.scrollHeight - el.clientHeight'), 100)
        self.assertEqual(body.evaluate('(el) => Math.round(el.scrollTop)'), 0)
        for _ in range(3):
            page.keyboard.press('ArrowDown')
        page.wait_for_function(                      # the body scrolls smoothly; sample the settled value
            "() => document.querySelector('.preview__body').scrollTop > 0")
        for _ in range(10):     # at the top the guard swallows the extra presses (spec 071)
            page.keyboard.press('ArrowUp')
        page.wait_for_function(
            "() => document.querySelector('.preview__body').scrollTop === 0")
        page.close()
