"""Spec 119 — the caption overlay: words, type, and nothing to press.

The overlay is a browser source for OBS: it renders the browser-local display state
and carries no controls at all. Its type comes from the bundled Source Sans 3.
"""

import re
import unittest
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ObsOverlayE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None
        super().tearDown()

    def test_the_caption_wears_the_bundled_face_and_balances(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        dock = context.new_page()
        dock.goto(self.live_server_url + '/obs/dock')
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        dock.locator('.entryrow').first.click()
        dock.wait_for_function(
            "service => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s && s.service === service && s.on === true; }", arg=self.service.pk)

        overlay = context.new_page()
        overlay.goto(self.live_server_url + '/obs/source/overlay')
        overlay.wait_for_selector('.obs-overlay__caption')
        self.assertIn('Kasih karunia', overlay.locator('.obs-overlay__caption').inner_text())

        # The bundled face really loads, and the caption follows the accepted formula.
        overlay.wait_for_function("() => document.fonts.check('800 20px \"Source Sans 3\"')")
        style = overlay.evaluate("""() => {
          const caption = document.querySelector('.obs-overlay__caption');
          const cs = getComputedStyle(caption);
          return {family: cs.fontFamily, size: parseFloat(cs.fontSize),
                  weight: cs.fontWeight, wrap: cs.textWrap, background: cs.backgroundColor};
        }""")
        self.assertTrue(style['family'].startswith('"Source Sans 3"'), style['family'])
        self.assertEqual(style['weight'], '800')
        self.assertEqual(style['wrap'], 'balance')
        # At 1280 px wide the cqw term (37.1px) is above the cap, so the caption must
        # render at exactly the cap the stylesheet declares — read it rather than
        # repeating the number here, which would rot on the next type tweak.
        css = (Path(settings.BASE_DIR) / 'static' / 'styles' / 'design'
               / 'obs-overlay.css').read_text(encoding='utf-8')
        cap = float(re.search(r'font-size: clamp\(9px, 2\.9cqw, (\d+)px\)', css).group(1))
        self.assertEqual(style['size'], cap)
        context.close()

    def test_hide_empties_the_overlay_and_nothing_is_focusable(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        dock = context.new_page()
        dock.goto(self.live_server_url + '/obs/dock')
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        dock.locator('.entryrow').first.click()
        dock.wait_for_function(
            "service => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s && s.service === service && s.on === true; }", arg=self.service.pk)

        overlay = context.new_page()
        overlay.goto(self.live_server_url + '/obs/source/overlay')
        overlay.wait_for_selector('.obs-overlay__caption')

        # Listen-only: no button, link, input, or tab stop exists on the page.
        self.assertEqual(overlay.evaluate("""() => document.querySelectorAll(
            'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])').length"""), 0)

        dock.evaluate("window.gkpsDisplay.hide()")
        overlay.wait_for_function(
            "() => document.querySelectorAll('.obs-overlay__caption').length === 0")
        self.assertEqual(overlay.evaluate("document.getElementById('overlayStage').children.length"), 0)
        context.close()
