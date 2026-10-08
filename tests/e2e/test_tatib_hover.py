"""Highlighting a hovered entry (spec 034).

Hovering an entry fills the whole row with the shared hover tint, without moving a
pixel of its text.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TatibHoverE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia beserta kita')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def test_hovering_an_item_highlights_it_without_moving_the_text(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        text = page.locator('.tatib__tx').first
        page.mouse.move(1400, 850)
        expect(item).to_have_css('background-color', 'rgba(0, 0, 0, 0)')
        before = text.bounding_box()
        item.hover()
        page.wait_for_timeout(250)
        background = item.evaluate('el => getComputedStyle(el).backgroundColor')
        self.assertNotIn(background, ('rgba(0, 0, 0, 0)', 'transparent'), background)
        after = text.bounding_box()
        self.assertEqual(round(before['x']), round(after['x']))       # no layout shift
        self.assertEqual(round(before['y']), round(after['y']))

    def test_keyboard_focus_within_highlights_the_item(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        page.mouse.move(1400, 850)
        expect(item).to_have_css('background-color', 'rgba(0, 0, 0, 0)')
        page.locator('[data-entry-edit]').first.focus()
        page.wait_for_timeout(250)
        background = item.evaluate('el => getComputedStyle(el).backgroundColor')
        self.assertNotIn(background, ('rgba(0, 0, 0, 0)', 'transparent'), background)

    def test_the_highlight_is_legible_in_both_themes(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        for theme in ('light', 'dark'):
            page.mouse.move(1400, 850)
            if theme == 'dark':
                page.locator('#themeBtn').click()
            page.wait_for_timeout(200)
            item.hover()
            page.wait_for_timeout(250)
            background = item.evaluate('el => getComputedStyle(el).backgroundColor')
            self.assertNotIn(background, ('rgba(0, 0, 0, 0)', 'transparent'), (theme, background))
