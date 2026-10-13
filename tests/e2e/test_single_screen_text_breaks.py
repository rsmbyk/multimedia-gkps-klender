"""Single-screen Text preview breaks and live projector refresh (spec 070)."""

from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SingleScreenBreakE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Single-screen break review', date=date(2026, 10, 13), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1,
            kind=tatib.ServiceEntryKind.SINGLE_SCREEN_TEXT,
            title='Prayer', text='one\ntwo\n\nthree\nfour\nfive\nsix')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def test_first_break_only_splits_in_two_then_toggle_reset_and_live_projector(self):
        context = self.browser.new_context(viewport={'width': 1300, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        with page.expect_popup() as popup:
            page.locator('[data-project-open]').click()
        projector = popup.value
        projector.wait_for_load_state('networkidle')
        screens = projector.locator('#projectorScreens .screen')
        expect(screens).to_have_count(2)
        page.locator('[data-entry-pk] [data-preview-open]').click()
        modal = page.locator('#previewModal')
        expect(modal.locator('[data-break-mode]')).to_have_text('Default · 1 screen')
        expect(modal.locator('.preview__gap.is-set')).to_have_count(0)
        gap = modal.locator('[data-break-after="1"]')
        gap.focus()
        gap.press('Enter')
        expect(modal.locator('[data-break-mode]')).to_have_text('Custom')
        expect(modal.locator('.preview__gap.is-set')).to_have_count(1)
        expect(gap).to_have_class('preview__gap is-set')
        expect(screens).to_have_count(3)
        self.assertIn('Prayer', screens.nth(0).text_content())
        self.assertIn('one', screens.nth(0).text_content())
        self.assertNotIn('two', screens.nth(0).text_content())
        self.assertIn('two', screens.nth(1).text_content())
        self.assertIn('three', screens.nth(1).text_content())
        self.assertIn('six', screens.nth(1).text_content())
        gap4 = modal.locator('[data-break-after="4"]')
        gap4.click()
        expect(modal.locator('.preview__gap.is-set')).to_have_count(2)
        expect(screens).to_have_count(4)
        gap.click()
        expect(gap).not_to_have_class('preview__gap is-set')
        expect(screens).to_have_count(3)
        gap4.click()
        expect(modal.locator('[data-break-mode]')).to_have_text('Custom')
        expect(modal.locator('.preview__gap.is-set')).to_have_count(0)
        expect(screens).to_have_count(2)
        modal.locator('[data-break-reset]').click()
        expect(modal.locator('[data-break-mode]')).to_have_text('Default · 1 screen')
        expect(screens).to_have_count(2)
        context.close()
