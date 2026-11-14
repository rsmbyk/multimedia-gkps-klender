"""The page an old OBS source lands on (spec 193).

A browser source left in a scene file still points at one of the four old overlay
addresses. This release answers each with a 302 to /obs/blank, which paints
nothing but one corner note: the operator sees that the source is stale, the
viewer sees nothing. The note is 20% white at rest and reveals the live overlay's
address on hover — the hover state is only reachable by a human in OBS's
*Interact* window, which is exactly who it is for.

The colour at rest is the owner's number (20% opacity), so this test reads the
computed colour rather than the stylesheet: a later refactor may move the rule.
"""

import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RetiredRoutesE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
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

    def test_the_note_is_a_watermark_until_hovered(self):
        """FR-006a: invisible enough for the congregation, legible for the operator."""
        page = self.browser.new_page()
        page.goto(self.live_server_url + '/obs/blank')
        note = page.locator('.retired')
        anchor = page.locator('.retired a')

        self.assertEqual(note.evaluate('el => getComputedStyle(el).color'),
                         'rgba(255, 255, 255, 0.2)')
        self.assertEqual(note.evaluate('el => getComputedStyle(el).backgroundColor'),
                         'rgba(0, 0, 0, 0)')
        self.assertEqual(anchor.evaluate('el => getComputedStyle(el).display'), 'none')

        note.hover()

        self.assertEqual(note.evaluate('el => getComputedStyle(el).color'),
                         'rgba(255, 255, 255, 0.95)')
        self.assertEqual(note.evaluate('el => getComputedStyle(el).backgroundColor'),
                         'rgba(20, 20, 18, 0.82)')
        self.assertEqual(anchor.evaluate('el => getComputedStyle(el).display'), 'block')
        self.assertEqual(anchor.inner_text(), 'Switch to /obs/source/overlay')
