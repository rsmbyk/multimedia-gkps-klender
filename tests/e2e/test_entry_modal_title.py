"""The large entry dialog's title band reads as a band, not a bare heading (spec 240).

Spec 226 moved the large frame's inset and divider onto `.editor__head`, but the entry
form renders its title directly in the content; the three large entry dialogs lost the
band. These cases measure the painted text and rule through the project's own routes.
"""
import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const dialog = document.getElementById('editorModal');
  const title = dialog.querySelector('#editorTitle');
  const range = document.createRange(); range.selectNodeContents(title);
  const text = range.getBoundingClientRect();
  const band = title.getBoundingClientRect();
  const frame = dialog.getBoundingClientRect();
  const style = getComputedStyle(title);
  const field = dialog.querySelector('.editor__form > .editor__field');
  return {
    title: title.textContent.trim(),
    textX: +(text.x - frame.x).toFixed(1), textY: +(text.y - frame.y).toFixed(1),
    band: +band.height.toFixed(1), padding: style.padding,
    border: style.borderBottomWidth, font: style.fontSize,
    frame: [Math.round(frame.width), Math.round(frame.height)],
    fieldY: field ? +(field.getBoundingClientRect().y - frame.y).toFixed(1) : null,
    scrolls: document.documentElement.scrollHeight > window.innerHeight,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EntryModalTitleE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Judul Entry', date=date(2026, 11, 24), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            text='Ayat pembuka untuk suntingan.')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        if getattr(self, 'playwright', None) is not None:
            self.browser.close()
            self.playwright.stop()
            self.playwright = None
        super().tearDown()

    def _page(self, width=1440, height=900):
        page = self.browser.new_page(
            viewport={'width': width, 'height': height},
            color_scheme='dark', device_scale_factor=1)
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.wait_for_load_state('networkidle')
        return page

    @staticmethod
    def _open_new(page, kind):
        page.locator(f'[data-entry-open="{kind}"]').first.evaluate('el => el.click()')
        page.wait_for_function(
            "() => { const t = document.querySelector('#editorTitle');"
            " return t && t.textContent.trim().startsWith('New ')"
            " && document.querySelector('#editorContent [data-editor-size=\"large\"]'); }")
        page.wait_for_timeout(350)  # the media dialog's 190ms entrance settles
        return page.evaluate(MEASURE)

    @staticmethod
    def _open_edit(page):
        control = page.locator('[data-entry-edit]').first
        control.evaluate('el => el.click()')
        page.wait_for_function(
            "() => document.querySelector('#editorTitle')?.textContent.trim() === 'Edit text'")
        page.wait_for_timeout(150)
        return page.evaluate(MEASURE)

    def _assert_band(self, state, x=26, y=21, band=72.5, padding='20px 26px',
                     frame=(840, 760)):
        self.assertEqual(state['frame'], list(frame))
        self.assertAlmostEqual(state['textX'], x, delta=1)
        self.assertAlmostEqual(state['textY'], y, delta=1)
        self.assertAlmostEqual(state['band'], band, delta=1)
        self.assertEqual(state['padding'], padding)
        self.assertEqual(state['border'], '1px')
        self.assertEqual(state['font'], '21px')

    def test_large_entry_titles_have_the_band(self):
        for kind in ('text', 'media'):
            with self.subTest(kind=kind):
                page = self._page()
                try:
                    self._assert_band(self._open_new(page, kind))
                finally:
                    page.close()
        page = self._page()
        try:
            self._assert_band(self._open_edit(page))
        finally:
            page.close()
        self._close_browser()

    def test_narrow_title_keeps_small_gutters(self):
        page = self._page(width=390, height=844)
        state = self._open_new(page, 'text')
        self.assertEqual(state['frame'], [352, 760])
        self._assert_band(state, x=18, y=17, band=64.5, padding='16px 18px',
                          frame=(352, 760))
        self.assertFalse(state['scrolls'])
        self._close_browser()

    def _close_browser(self):
        self.browser.close()
        self.playwright.stop()
        self.playwright = None
