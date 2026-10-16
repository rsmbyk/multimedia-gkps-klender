"""The unified Text create choice and Preview mode control (spec 079)."""

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
class UnifiedTextScreenModeE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Mode review', date=date(2026, 10, 13), is_active=True)
        if self._testMethodName == 'test_viewer_sees_current_mode_without_edit_controls':
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
                default_screen_mode='single_screen', text='one\ntwo')
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

    def test_create_edit_switch_custom_confirmation_and_live_projector(self):
        context = self.browser.new_context(viewport={'width': 1300, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        expect(page.locator('[data-entry-open="text"]')).to_have_count(1)
        expect(page.locator('[data-entry-open="single_screen_text"]')).to_have_count(0)
        page.locator('[data-entry-open="text"]').click()
        form = page.locator('#editorModal [data-entry-form="text"]')
        expect(form.locator('[data-create-mode="multi_line"]')).to_have_attribute('aria-pressed', 'true')
        form.locator('[data-create-mode="single_screen"]').click()
        expect(form.locator('[data-create-mode-help]')).to_have_text('One fitted screen by default')
        form.locator('[name="title"]').fill('Prayer')
        form.locator('[name="text"]').fill('one\ntwo\n\nthree\nfour')
        form.locator('.editor__save').click()
        expect(page.locator('#editorModal')).not_to_be_visible()
        expect(page.locator('[data-entry-pk]')).to_have_count(1)

        with page.expect_popup() as popup:
            page.locator('[data-project-open]').click()
        projector = popup.value
        projector.wait_for_load_state('networkidle')
        screens = projector.locator('#projectorScreens .screen[data-screen]')
        expect(screens).to_have_count(2)

        page.locator('[data-entry-pk] [data-preview-open]').click()
        modal = page.locator('#previewModal')
        switcher = modal.locator('[data-preview-screen-mode]')
        expect(switcher).to_have_attribute('data-selected', 'single_screen')
        switcher.locator('[data-preview-mode="multi_line"]').click()
        expect(modal.locator('[data-mode-confirm]')).not_to_be_visible()
        expect(switcher).to_have_attribute('data-selected', 'multi_line')
        expect(screens).to_have_count(3)

        modal.locator('[data-break-after="1"]').click()
        expect(switcher).to_have_attribute('data-selected', 'custom')
        expect(switcher.locator('[data-preview-custom]')).to_have_attribute('role', 'status')
        switcher.locator('[data-preview-mode="single_screen"]').click()
        expect(modal.locator('[data-confirm-title]')).to_have_text('Switch to Single-screen?')
        modal.locator('[data-confirm-cancel]').click()
        expect(switcher).to_have_attribute('data-selected', 'custom')
        switcher.locator('[data-preview-mode="single_screen"]').click()
        modal.locator('[data-confirm-cancel]').press('Escape')
        expect(modal).to_be_visible()
        expect(switcher).to_have_attribute('data-selected', 'custom')
        switcher.locator('[data-preview-mode="single_screen"]').click()
        modal.locator('[data-confirm-accept]').click()
        expect(switcher).to_have_attribute('data-selected', 'single_screen')
        expect(screens).to_have_count(2)

        modal.press('Escape')
        page.locator('[data-entry-pk] [data-entry-edit]').click()
        edit = page.locator('#editorModal [data-entry-form="text"]')
        expect(edit.locator('[data-create-screen-mode]')).to_have_count(0)
        context.close()

    @override_settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True)
    def test_viewer_sees_current_mode_without_edit_controls(self):
        page = self.browser.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('[data-preview-open]').click()
        expect(page.locator('[data-mode-readonly]')).to_have_text('Single-screen')
        expect(page.locator('[data-preview-screen-mode]')).not_to_be_visible()
        expect(page.locator('#previewModal [data-break-after="1"]')).to_be_disabled()
