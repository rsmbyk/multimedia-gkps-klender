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
        # Tall enough that the start bar's reveal cannot slide the item out from
        # under a pointer placed at its centre (spec 055's wrapped-bar case).
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text=('Kasih karunia beserta kita. ' * 6 + '\n') * 8)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Survivor', text='Second entry')
        self.legacy = tatib.TataIbadah.objects.create(
            name='Legacy service', date=date(2026, 10, 4), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.legacy, item_type=tatib.TataIbadahItemType.TEXT,
            title='Legacy', text='Old row text\n' * 8, order_number=1)
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

    def _resting_background(self, page):
        # An entry draws no surface at rest (spec 142): the theme tokens that
        # used to hold the fill and the ring are gone, so the resting colour is
        # the canvas itself and Chromium reports a fully transparent colour.
        # A constant, not a re-read of the element: some callers ask for it
        # while the pointer is already ON the entry, and there the element
        # reports the hover tint instead.
        return 'rgba(0, 0, 0, 0)'

    def test_hovering_the_first_entry_moves_it_once_then_settles(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        text = page.locator('.tatib__tx').first
        page.mouse.move(1400, 850)
        expect(item).to_have_css('background-color', self._resting_background(page))
        before = text.bounding_box()
        item.hover()
        page.wait_for_timeout(600)                   # past the start bar's expand
        after = text.bounding_box()
        background = item.evaluate('el => getComputedStyle(el).backgroundColor')
        self.assertNotEqual(background, self._resting_background(page), background)
        # The start bar revealing (spec 055) moves the first entry ONCE, by the
        # bar's revealed height minus the page head's 30px margin (13.6px on one
        # line; ~47px when the five buttons wrap at this width). The text itself
        # never reflows horizontally, and nothing drifts after it settles.
        self.assertEqual(round(before['x']), round(after['x']))
        bar_h = page.locator('#readBody > .entry__start').evaluate(
            'el => el.getBoundingClientRect().height')
        shift = after['y'] - before['y']
        self.assertAlmostEqual(shift, bar_h - 30, delta=2, msg=(shift, bar_h))
        page.wait_for_timeout(400)
        self.assertEqual(text.bounding_box()['y'], after['y'])

    def test_keyboard_focus_within_highlights_the_item(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        page.mouse.move(1400, 850)
        expect(item).to_have_css('background-color', self._resting_background(page))
        page.locator('[data-entry-edit]').first.focus()
        page.wait_for_timeout(250)
        background = item.evaluate('el => getComputedStyle(el).backgroundColor')
        self.assertNotEqual(background, self._resting_background(page), background)

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
            self.assertNotEqual(background, self._resting_background(page), (theme, background))

    def _expect_idle(self, page, item):
        page.mouse.move(1400, 850)
        expect(item).to_have_css('background-color', self._resting_background(page))
        expect(item.locator('.entry__acts')).to_have_css('opacity', '0')
        self.assertTrue(page.evaluate('document.activeElement !== document.body'))

    def test_pointer_modal_dismissal_clears_highlight_and_controls(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        for theme in ('light', 'dark'):
            if theme == 'dark':
                page.locator('#themeBtn').click()
            for opener, modal in (('[data-preview-open]', '#previewModal'),
                                  ('[data-entry-edit]', '#editorModal'),
                                  ('[data-entry-delete]', '#editorModal')):
                dismissals = ('escape', 'backdrop') if modal == '#previewModal' else (
                    'button', 'escape', 'backdrop')
                for dismissal in dismissals:
                    with self.subTest(theme=theme, opener=opener, dismissal=dismissal):
                        item.hover()
                        item.locator(opener).click()
                        dialog = page.locator(modal)
                        expect(dialog).to_be_visible()
                        page.mouse.move(1400, 850)
                        if dismissal == 'escape':
                            page.keyboard.press('Escape')
                        elif dismissal == 'backdrop':
                            page.mouse.click(5, 5)
                        else:
                            dialog.locator('[data-editor-close]').click()
                        expect(dialog).not_to_be_visible()
                        self._expect_idle(page, item)
                        item.hover()
                        expect(item).not_to_have_css('background-color', self._resting_background(page))
                        expect(item.locator('.entry__acts')).to_have_css('opacity', '1')
                        self._expect_idle(page, item)

    def test_keyboard_modal_return_remains_visible(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        page.mouse.move(1400, 850)
        for opener, modal in (('[data-preview-open]', '#previewModal'),
                              ('[data-entry-edit]', '#editorModal'),
                              ('[data-entry-delete]', '#editorModal')):
            control = item.locator(opener)
            control.focus()
            control.press('Enter')
            expect(page.locator(modal)).to_be_visible()
            page.keyboard.press('Escape')
            expect(page.locator(modal)).not_to_be_visible()
            expect(control).to_be_focused()
            expect(item).not_to_have_css('background-color', self._resting_background(page))
            expect(item.locator('.entry__acts')).to_have_css('opacity', '1')
            self.assertFalse(control.evaluate("el => el.classList.contains('focus-restore-quiet')"))

    def test_tab_after_quiet_return_restores_controls(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        item.hover()
        item.locator('[data-entry-edit]').click()
        expect(page.locator('#editorModal')).to_be_visible()
        page.keyboard.press('Escape')
        self._expect_idle(page, item)
        page.keyboard.press('Tab')
        expect(item.locator('.entry__acts')).to_have_css('opacity', '1')
        expect(item).not_to_have_css('background-color', self._resting_background(page))
        page.keyboard.press('Shift+Tab')
        page.keyboard.press('Tab')
        expect(item.locator('.entry__acts')).to_have_css('opacity', '1')

    def test_pointer_save_and_delete_do_not_highlight_surviving_entries(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        item.hover()
        item.locator('[data-entry-edit]').click()
        page.locator('#id_title').fill('Updated')
        page.locator('.editor__save').click()
        expect(page.locator('#editorModal')).not_to_be_visible()
        expect(item).to_contain_text('Updated')
        self._expect_idle(page, item)
        item.hover()
        item.locator('[data-entry-delete]').click()
        page.locator('[data-confirm-delete]').click()
        expect(page.locator('#editorModal')).not_to_be_visible()
        expect(page.locator('.tatib__item')).to_have_count(1)
        expect(item).to_contain_text('Survivor')
        self._expect_idle(page, item)

    def test_touch_controls_remain_visible_after_dismissal(self):
        context = self.browser.new_context(
            viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        item = page.locator('.tatib__item').first
        page.locator('#panelCollapse').tap()
        page.locator('#chCollapse').tap()
        item.locator('[data-preview-open]').tap()
        expect(page.locator('#previewModal')).to_be_visible()
        page.touchscreen.tap(5, 5)
        expect(page.locator('#previewModal')).not_to_be_visible()
        expect(item.locator('.entry__acts')).to_have_css('opacity', '1')

    def test_legacy_row_modal_return_is_quiet(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.legacy.pk]))
        item = page.locator('.tatib__item').first
        for opener, modal in (('[data-preview-open]', '#previewModal'),
                              ('[data-old-item-edit]', '#editorModal'),
                              ('[data-old-item-delete]', '#editorModal')):
            item.hover()
            item.locator(opener).click()
            expect(page.locator(modal)).to_be_visible()
            page.mouse.move(1400, 850)
            page.keyboard.press('Escape')
            expect(page.locator(modal)).not_to_be_visible()
            self._expect_idle(page, item)

    def _settled_state(self, page, item):
        """Read the entry's fill and control opacity once, after the 200ms fade.

        A retrying ``expect`` would pass while a dropped highlight is still fading.
        """
        page.wait_for_timeout(400)
        return item.evaluate("""el => ({
            background: getComputedStyle(el).backgroundColor,
            controls: getComputedStyle(el.querySelector('.entry__acts')).opacity,
        })""")

    def _assert_held(self, page, item):
        state = self._settled_state(page, item)
        self.assertNotEqual(state['background'], self._resting_background(page), state)
        self.assertEqual(state['controls'], '1', state)

    def _assert_resting(self, page, item):
        state = self._settled_state(page, item)
        self.assertEqual(state['background'], self._resting_background(page), state)
        self.assertEqual(state['controls'], '0', state)

    def test_pointer_opened_modal_holds_only_the_origin_entry(self):
        """Spec 065: the origin entry keeps its hover look until its modal closes."""
        page = self._page()
        item = page.locator('.tatib__item').first
        other = page.locator('.tatib__item').nth(1)
        for theme in ('light', 'dark'):
            if theme == 'dark':
                page.mouse.move(1400, 850)
                page.locator('#themeBtn').click()
            for opener, modal in (('[data-preview-open]', '#previewModal'),
                                  ('[data-entry-edit]', '#editorModal'),
                                  ('[data-entry-delete]', '#editorModal')):
                with self.subTest(theme=theme, opener=opener):
                    item.hover()
                    item.locator(opener).click()
                    dialog = page.locator(modal)
                    expect(dialog).to_be_visible()
                    page.mouse.move(1400, 850)
                    self._assert_held(page, item)
                    self._assert_resting(page, other)
                    page.keyboard.press('Escape')
                    expect(dialog).not_to_be_visible()
                    self._expect_idle(page, item)

    def test_keyboard_opened_modal_holds_the_origin_entry(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        page.mouse.move(1400, 850)
        for opener, modal in (('[data-preview-open]', '#previewModal'),
                              ('[data-entry-edit]', '#editorModal'),
                              ('[data-entry-delete]', '#editorModal')):
            with self.subTest(opener=opener):
                control = item.locator(opener)
                control.focus()
                control.press('Enter')
                expect(page.locator(modal)).to_be_visible()
                self._assert_held(page, item)
                page.keyboard.press('Escape')
                expect(page.locator(modal)).not_to_be_visible()
                expect(control).to_be_focused()

    def test_legacy_row_is_held_while_its_modal_is_open(self):
        page = self._page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.legacy.pk]))
        item = page.locator('.tatib__item').first
        for opener, modal in (('[data-preview-open]', '#previewModal'),
                              ('[data-old-item-edit]', '#editorModal'),
                              ('[data-old-item-delete]', '#editorModal')):
            with self.subTest(opener=opener):
                item.hover()
                item.locator(opener).click()
                expect(page.locator(modal)).to_be_visible()
                page.mouse.move(1400, 850)
                self._assert_held(page, item)
                page.keyboard.press('Escape')
                expect(page.locator(modal)).not_to_be_visible()
                self._expect_idle(page, item)

    def test_failed_edit_load_holds_nothing(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        page.route('**/editor/entry/*/edit/', lambda route: route.abort())
        item.hover()
        item.locator('[data-entry-edit]').click()
        expect(page.locator('.edit-toast[data-state="failure"] .edit-toast__title'))\
            .to_have_text('Could not load editor')
        expect(page.locator('#editorModal')).not_to_be_visible()
        page.mouse.move(1400, 850)
        # The clicked control keeps ordinary click focus; drop it to see the entry alone.
        page.evaluate('document.activeElement.blur()')
        self._assert_resting(page, item)

    def test_keyboard_save_and_delete_preserve_visible_focus_after_refresh(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        page.mouse.move(1400, 850)
        edit = item.locator('[data-entry-edit]')
        edit.focus()
        edit.press('Enter')
        page.locator('#id_title').fill('Keyboard update')
        page.locator('.editor__save').press('Enter')
        expect(page.locator('#editorModal')).not_to_be_visible()
        expect(item).to_contain_text('Keyboard update')
        expect(item.locator('.entry__acts')).to_have_css('opacity', '1')
        expect(item).not_to_have_css('background-color', self._resting_background(page))
        delete = item.locator('[data-entry-delete]')
        delete.focus()
        delete.press('Enter')
        page.locator('[data-confirm-delete]').press('Enter')
        expect(page.locator('.tatib__item')).to_have_count(1)
        expect(item).to_contain_text('Survivor')
        expect(item.locator('.entry__acts')).to_have_css('opacity', '1')
        self.assertTrue(item.evaluate('el => el.contains(document.activeElement)'))
