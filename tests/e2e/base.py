"""Shared browser lifecycle for all e2e test classes."""

import unittest

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

# Shared singleton: one Playwright + Chromium instance lives for the lifetime
# of the whole test-class (one Django server thread is also a class-level concept).
# Each test subclass sets its own ``live_server_url`` via setUp / setUpClass.
_PLAYWRIGHT = None
_BROWSER = None


class BaseE2ETestCase(unittest.TestCase):
    """Mixin that manages a single browser instance per test class.

    Subclasses inherit setUp / tearDown and simply call ``super()``; the browser
    is started once in setUpClass and torn down once in tearDownClass, guaranteeing
    that Playwright stops *before* Django's database flush in the parent tearDown.
    """

    @classmethod
    def setUpClass(cls):
        if not HAS_PLAYWRIGHT:
            raise unittest.SkipTest('playwright is not installed')
        global _PLAYWRIGHT, _BROWSER
        _PLAYWRIGHT = sync_playwright().start()
        try:
            _BROWSER = _PLAYWRIGHT.chromium.launch()
        except Exception as error:
            _PLAYWRIGHT.stop()
            _PLAYWRIGHT = _BROWSER = None
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls._close_browser()
        super().tearDownClass()

    @classmethod
    def _close_browser(cls):
        global _PLAYWRIGHT, _BROWSER
        if _BROWSER is not None:
            _BROWSER.close()
            _BROWSER = None
        if _PLAYWRIGHT is not None:
            _PLAYWRIGHT.stop()
            _PLAYWRIGHT = None

    def _new_page(self, viewport=None):
        vp = viewport or {'width': 1440, 'height': 900}
        return _BROWSER.new_page(viewport=vp)

    def _new_context(self, **kwargs):
        return _BROWSER.new_context(**kwargs)
