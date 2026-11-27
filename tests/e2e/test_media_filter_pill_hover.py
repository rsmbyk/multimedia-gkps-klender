"""Hover feedback on the Media Library's six filter pills (spec 239).

The filter row's unpressed pills must take the same border/fill pair as the sort
and icon buttons beside them; a pressed pill must keep its accent fill. The rule
is a plain :hover selector, so these tests drive real pointer movement rather
than reading a media-query-dependent computed style.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


PILLS = ('[data-media-type="image"]', '[data-media-type="audio"]',
         '[data-media-type="video"]', '[data-media-type="pdf"]',
         '[data-media-type="slides"]', '#mediaUnusedFilter')
EXPECTED = {
    'light': {'hover_bg': 'rgba(31, 31, 29, 0.08)', 'hover_border': 'rgb(28, 92, 60)',
              'rest_bg': 'rgba(0, 0, 0, 0)', 'rest_border': 'rgb(217, 214, 205)',
              'ink': 'rgb(31, 31, 29)', 'active_bg': 'rgb(28, 92, 60)'},
    'dark': {'hover_bg': 'rgba(255, 255, 255, 0.09)', 'hover_border': 'rgb(124, 156, 240)',
             'rest_bg': 'rgba(0, 0, 0, 0)', 'rest_border': 'rgb(58, 54, 47)',
             'ink': 'rgb(245, 243, 238)', 'active_bg': 'rgb(124, 156, 240)'},
}
SNAP = """selector => {
  const el = document.querySelector(selector), s = getComputedStyle(el);
  const b = el.getBoundingClientRect();
  return {background: s.backgroundColor, border: s.borderColor, color: s.color,
          width: +b.width.toFixed(2), height: +b.height.toFixed(2),
          outline: s.outlineWidth, outlineStyle: s.outlineStyle,
          outlineColor: s.outlineColor, outlineOffset: s.outlineOffset};
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MediaFilterPillHoverE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch(
                executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        except Exception:
            self.browser = self._playwright.chromium.launch()
        self.pages = []

    def tearDown(self):
        for page in self.pages:
            page.close()
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open_library(self, scheme='light'):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900},
                                     color_scheme=scheme, device_scale_factor=1)
        page.goto(self.live_server_url + reverse('web-media-library'))
        page.wait_for_load_state('networkidle')
        page.mouse.move(1400, 850)
        self.pages.append(page)
        return page

    def snap(self, page, selector=PILLS[0]):
        return page.evaluate(SNAP, selector)

    def test_all_unpressed_pills_take_the_hover_pair(self):
        for scheme, expected in EXPECTED.items():
            with self.subTest(scheme=scheme):
                page = self.open_library(scheme)
                for selector in PILLS:
                    with self.subTest(pill=selector):
                        page.mouse.move(1400, 850)
                        self.assertEqual(self.snap(page, selector)['background'], expected['rest_bg'])
                        page.locator(selector).hover()
                        page.wait_for_timeout(80)
                        hovered = self.snap(page, selector)
                        self.assertEqual(hovered['background'], expected['hover_bg'])
                        self.assertEqual(hovered['border'], expected['hover_border'])

    def test_pointer_leave_restores_rest_colours(self):
        for scheme, expected in EXPECTED.items():
            with self.subTest(scheme=scheme):
                page = self.open_library(scheme)
                page.locator(PILLS[0]).hover()
                page.wait_for_timeout(80)
                self.assertEqual(self.snap(page)['background'], expected['hover_bg'])
                page.mouse.move(1400, 850)
                page.wait_for_timeout(80)
                rest = self.snap(page)
                self.assertEqual(rest['background'], expected['rest_bg'])
                self.assertEqual(rest['border'], expected['rest_border'])

    def test_hover_keeps_box_and_label(self):
        for scheme, expected in EXPECTED.items():
            with self.subTest(scheme=scheme):
                page = self.open_library(scheme)
                rest = self.snap(page)
                page.locator(PILLS[0]).hover()
                page.wait_for_timeout(80)
                hovered = self.snap(page)
                for key in ('width', 'height', 'color'):
                    self.assertEqual(hovered[key], rest[key], msg=key)
                self.assertEqual(rest['color'], expected['ink'])
                self.assertAlmostEqual(rest['width'], 63.36, delta=1)
                self.assertAlmostEqual(rest['height'], 30, delta=1)

    def test_pressed_pill_keeps_its_accent_fill(self):
        for scheme, expected in EXPECTED.items():
            with self.subTest(scheme=scheme):
                page = self.open_library(scheme)
                page.locator(PILLS[0]).click()
                page.mouse.move(1400, 850)
                page.wait_for_timeout(80)
                rest = self.snap(page)
                self.assertEqual(rest['background'], expected['active_bg'])
                page.locator(PILLS[0]).hover()
                page.wait_for_timeout(80)
                hovered = self.snap(page)
                for key in ('background', 'border', 'color'):
                    self.assertEqual(hovered[key], rest[key], msg=key)

    def test_keyboard_focus_keeps_its_outline(self):
        page = self.open_library()
        for _ in range(30):
            page.keyboard.press('Tab')
            focused = page.evaluate("() => document.activeElement.matches("
                                    "'[data-media-type=\"image\"]')")
            if focused:
                break
        self.assertTrue(focused, 'Tab never reached the Images pill')
        outline = self.snap(page)
        self.assertEqual(outline['outlineStyle'], 'solid')
        self.assertEqual(outline['outline'], '2px')
        self.assertEqual(outline['outlineOffset'], '2px')
        self.assertEqual(outline['outlineColor'], 'rgb(28, 92, 60)')
