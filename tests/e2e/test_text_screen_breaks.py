"""Preview-modal screen breaks for ordinary Tata Ibadah Text entries."""

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
class TextScreenBreakE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Screen break review', date=date(2026, 10, 13), is_active=True)
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Prayer', text='one\ntwo\nthree\nfour\nfive\nsix')
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

    def test_default_custom_reset_and_projector_sequence(self):
        context = self.browser.new_context(viewport={'width': 1300, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        opener = page.locator('[data-entry-pk]').locator('[data-preview-open]')
        opener.click()
        modal = page.locator('#previewModal')
        expect(modal).to_be_visible()
        expect(modal.locator('[data-preview-screen-mode]')).to_have_attribute('data-selected', 'multi_line')
        gap2 = modal.locator('[data-break-after="2"]')
        expect(gap2).to_have_class('preview__gap is-set')
        self.assertEqual(
            gap2.locator('span').evaluate('(label) => getComputedStyle(label).opacity'), '0')
        gap2.hover()
        self.assertEqual(
            gap2.locator('span').evaluate('(label) => getComputedStyle(label).opacity'), '1')
        gap1 = modal.locator('[data-break-after="1"]')
        gap1.hover()
        expect(gap1.locator('span')).to_have_text('Add break')
        gap1.focus()
        gap1.press('Enter')
        expect(modal.locator('[data-preview-screen-mode]')).to_have_attribute('data-selected', 'custom')
        for position in (1, 3, 5):
            expect(modal.locator(f'[data-break-after="{position}"]')).to_have_class(
                'preview__gap is-set')
        projector = context.new_page()
        projector.goto(self.live_server_url
                       + f'/projector?service={self.service.pk}')
        screens = projector.locator('#projectorScreens .screen[data-screen]')
        expect(screens).to_have_count(5)
        self.assertIn('one', screens.nth(0).text_content())
        self.assertNotIn('two', screens.nth(0).text_content())
        self.assertIn('two', screens.nth(1).text_content())
        self.assertIn('three', screens.nth(1).text_content())
        gap1.click()
        expect(gap1).not_to_have_class('preview__gap is-set')
        modal.locator('[data-preview-mode="multi_line"]').click()
        expect(modal.locator('[data-mode-confirm]')).to_be_visible()
        modal.locator('[data-confirm-accept]').click()
        expect(modal.locator('[data-preview-screen-mode]')).to_have_attribute('data-selected', 'multi_line')
        expect(gap2).to_have_class('preview__gap is-set')
        projector.reload()
        expect(projector.locator('#projectorScreens .screen[data-screen]')).to_have_count(4)
        gap2.click()
        expect(modal.locator('[data-preview-screen-mode]')).to_have_attribute('data-selected', 'custom')
        expect(gap2).not_to_have_class('preview__gap is-set')
        expect(modal.locator('[data-break-after="4"]')).to_have_class('preview__gap is-set')
        modal.locator('[data-preview-mode="multi_line"]').click()
        modal.locator('[data-confirm-accept]').click()
        context.close()

    def test_saved_break_reaches_an_open_projector(self):
        context = self.browser.new_context(viewport={'width': 1300, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        with page.expect_popup() as popup:
            page.locator('[data-project-open]').click()
        projector = popup.value
        projector.wait_for_load_state('networkidle')
        expect(projector.locator('#projectorScreens .screen[data-screen]')).to_have_count(4)
        page.locator('[data-entry-pk]').locator('[data-preview-open]').click()
        page.locator('#previewModal [data-break-after="1"]').click()
        expect(page.locator('#previewModal [data-preview-screen-mode]')).to_have_attribute('data-selected', 'custom')
        expect(projector.locator('#projectorScreens .screen[data-screen]')).to_have_count(5)
        context.close()
