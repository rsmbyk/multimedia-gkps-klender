"""Shared toast feedback and pending-write guards for reading editors (spec 093)."""

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
class EditRequestFeedbackE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Feedback test service', date=date(2026, 10, 16), is_active=True)
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Opening', text='Opening words\nSecond line\nThird line')
        self.other_entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Response', text='Response words')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _hold_post(self, page, url_fragment, status=500, body='{}'):
        """Hold one POST response so the pending UI can be inspected deterministically."""
        page.evaluate('''({fragment, status, body}) => {
          const nativeFetch = window.fetch.bind(window);
          window.__heldWriteCount = 0;
          window.__settleHeldWrite = null;
          window.fetch = (input, init) => {
            const url = typeof input === 'string' ? input : input.url;
            if (init && init.method === 'POST' && url.includes(fragment)) {
              window.__heldWriteCount++;
              return new Promise(resolve => {
                window.__settleHeldWrite = () => resolve(new Response(body, {
                  status, headers: {'Content-Type': 'application/json'}
                }));
              });
            }
            return nativeFetch(input, init);
          };
        }''', {'fragment': url_fragment, 'status': status, 'body': body})

    def test_pending_form_write_locks_the_dialog_and_failure_toast_sits_above_it(self):
        page = self._page(reverse('web-home'))
        page.locator('.rail__btn[aria-label="Kidung"]').click()
        page.locator('#panelAdd').click()
        dialog = page.locator('#editorModal')
        expect(dialog).to_be_visible()
        page.locator('[name="name"]').fill('New feedback book')
        self._hold_post(page, '/editor/songbook/new/save/')

        page.locator('.editor__save').click()
        pending = page.locator('.edit-toast[data-state="pending"]')
        expect(pending).to_be_visible(timeout=1500)
        expect(page.locator('#editorContent input[name="name"]')).to_be_disabled()
        expect(page.locator('#editorContent [data-editor-close]')).to_be_disabled()
        page.keyboard.press('Escape')
        page.mouse.click(8, 8)
        expect(dialog).to_be_visible()
        layer_state = page.evaluate('''() => {
          const host = document.getElementById('editToastHost');
          const toast = document.querySelector('.edit-toast[data-state="pending"]');
          const rect = toast.getBoundingClientRect();
          return {hostOpen: host.matches(':popover-open'),
            dialogOpen: document.querySelector('dialog[open]') !== null,
            toastVisible: rect.width > 0 && rect.height > 0
              && getComputedStyle(toast).opacity === '1',
            toastRect: {left: rect.left, top: rect.top, width: rect.width, height: rect.height}};
        }''')
        self.assertTrue(layer_state['hostOpen'] and layer_state['dialogOpen']
                        and layer_state['toastVisible'],
                        f'the toast popover must remain visible while the dialog is open: {layer_state}')

        page.evaluate('window.__settleHeldWrite()')
        failure = page.locator('.edit-toast[data-state="failure"]')
        expect(failure).to_be_visible()
        expect(failure).to_contain_text('Could not save songbook')
        expect(dialog).to_be_visible()
        expect(page.locator('#editorContent input[name="name"]')).to_be_enabled()
        expect(page.locator('#editorContent input[name="name"]')).to_have_value(
            'New feedback book')
        self.assertEqual(page.evaluate('window.__heldWriteCount'), 1)
        failure.locator('.edit-toast__dismiss').click()
        expect(failure).to_have_count(0)
        expect(dialog).to_be_visible()

    def test_fast_success_shows_one_result_toast_and_closes_the_editor(self):
        page = self._page(reverse('web-home'))
        page.locator('.rail__btn[aria-label="Kidung"]').click()
        page.locator('#panelAdd').click()
        page.locator('[name="name"]').fill('Toast success book')
        page.locator('.editor__save').click()
        success = page.locator('.edit-toast[data-state="success"]')
        expect(success).to_be_visible(timeout=5000)
        expect(success).to_contain_text('Songbook saved')
        expect(page.locator('#editorModal')).not_to_be_visible()
        expect(page.locator('.edit-toast')).to_have_count(1)

    def test_failed_editor_load_shows_a_toast_without_opening_an_empty_dialog(self):
        page = self._page(reverse('web-home'))
        page.locator('.rail__btn[aria-label="Kidung"]').click()
        page.route('**/editor/songbook/new/**', lambda route: route.fulfill(
            status=503, body='Temporarily unavailable'))
        page.locator('#panelAdd').click()
        expect(page.locator('.edit-toast[data-state="failure"] .edit-toast__title'))\
            .to_have_text('Could not load editor')
        expect(page.locator('#editorModal')).not_to_be_visible()

    def test_failed_song_picker_load_uses_the_shared_toast(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.route('**/editor/entry/songs/**', lambda route: route.fulfill(
            status=503, body='Temporarily unavailable'))
        page.locator('[data-entry-open="song"]').first.evaluate('(button) => button.click()')
        modal = page.locator('#editorModal')
        expect(modal).to_be_visible()
        page.locator('#entry-song-trigger').click()
        expect(page.locator('.edit-toast[data-state="failure"] .edit-toast__title'))\
            .to_have_text('Could not load songs', timeout=3000)

    def test_non_modal_break_write_disables_only_its_initiating_button(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        opener = page.locator('[data-entry-open="section_break"]').first
        self._hold_post(page, '/editor/entry/new/save/')
        opener.evaluate('(button) => button.click()')
        expect(opener).to_be_disabled()
        page.wait_for_timeout(220)
        expect(page.locator('.edit-toast[data-state="pending"]')).to_be_visible()
        self.assertEqual(page.evaluate('window.__heldWriteCount'), 1)
        page.evaluate('window.__settleHeldWrite()')
        expect(page.locator('.edit-toast[data-state="failure"]')).to_be_visible()
        expect(opener).to_be_enabled()
        expect(page.locator('.preview__error')).to_have_count(0)

    def test_failed_reorder_restores_the_last_confirmed_order_and_reports_failure(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        grip = page.locator('[data-move-grip]').first
        original = page.locator('[data-move-grip]').evaluate_all(
            'nodes => nodes.map(node => Number(node.dataset.moveGrip))')
        self.assertEqual(original, [self.entry.pk, self.other_entry.pk])
        self._hold_post(page, '/editor/entry/reorder/')
        grip.focus()
        page.wait_for_timeout(120)
        page.keyboard.press('ArrowDown')
        page.wait_for_timeout(300)
        pending = page.locator('.edit-toast[data-state="pending"]')
        expect(pending).to_be_visible()
        changed = page.locator('[data-move-grip]').evaluate_all(
            'nodes => nodes.map(node => Number(node.dataset.moveGrip))')
        self.assertEqual(changed, list(reversed(original)))
        page.evaluate('window.__settleHeldWrite()')
        expect(page.locator('.edit-toast[data-state="failure"] .edit-toast__title'))\
            .to_have_text('Could not save entry order')
        page.wait_for_function('''expected => JSON.stringify(
          [...document.querySelectorAll('[data-move-grip]')]
            .map(node => Number(node.dataset.moveGrip))) === JSON.stringify(expected)''',
                               arg=original)
        self.assertEqual(page.locator('[data-move-grip]').evaluate_all(
            'nodes => nodes.map(node => Number(node.dataset.moveGrip))'), original)

    def test_failed_screen_break_write_preserves_the_confirmed_breaks_and_modal_state(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        opener = page.locator('[data-entry-pk]').locator('[data-preview-open]').first
        opener.click()
        modal = page.locator('#previewModal')
        gap = modal.locator('.preview__split [data-break-after]:not([hidden])').first
        before = gap.get_attribute('aria-pressed')
        self._hold_post(page, '/screen-breaks/', status=500,
                        body='{"error":"temporary failure"}')
        gap.click()
        expect(page.locator('.edit-toast[data-state="pending"]')).to_be_visible(timeout=1500)
        expect(gap).to_be_disabled()
        page.keyboard.press('Escape')
        page.mouse.click(8, 8)
        expect(modal).to_be_visible()
        page.evaluate('window.__settleHeldWrite()')
        expect(page.locator('.edit-toast[data-state="failure"] .edit-toast__title'))\
            .to_have_text('Could not save screen breaks')
        expect(gap).to_be_enabled()
        expect(gap).to_have_attribute('aria-pressed', before)
        expect(modal.locator('[data-preview-screen-mode]'))\
            .to_have_attribute('data-selected', 'multi_line')

    def test_four_toasts_use_short_result_durations_and_append_newest_at_bottom(self):
        page = self._page(reverse('web-home'))
        page.evaluate('''() => {
          const actions = Array.from({length: 4}, (_, index) =>
            window.gkpsEditFeedback.beginAction({
              pendingTitle: `Saving ${index + 1}`,
              successTitle: `Saved ${index + 1}`,
              failureTitle: `Failed ${index + 1}`
            }));
          actions.slice(0, 3).forEach(action => action.success());
          actions[3].failure('Request failed.');
        }''')
        toasts = page.locator('.edit-toast')
        expect(toasts).to_have_count(4)
        expect(page.locator('.edit-toast').last.locator('.edit-toast__title')).to_have_text('Failed 4')
        durations = page.locator('.edit-toast').evaluate_all(
            'nodes => nodes.map(node => Number(node.dataset.closeMs))')
        self.assertEqual(durations, [1000, 1000, 1000, 1618])
        expect(page.locator('.edit-toast[data-state="pending"]')).to_have_count(0)

    def test_dark_state_colors_and_reduced_motion_are_respected(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900},
                                           color_scheme='dark', reduced_motion='reduce')
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-home'))
        page.wait_for_load_state('networkidle')
        page.evaluate('''() => {
          window.__feedbackAction = window.gkpsEditFeedback.beginAction({
            pendingTitle: 'Saving', successTitle: 'Saved'
          });
        }''')
        pending = page.locator('.edit-toast[data-state="pending"]')
        expect(pending).to_be_visible(timeout=1500)
        pending_style = pending.evaluate('''node => ({
          color: getComputedStyle(node.querySelector('.edit-toast__mark')).color,
          animation: getComputedStyle(node.querySelector('circle')).animationDuration,
          transition: getComputedStyle(node).transitionDuration
        })''')
        self.assertEqual(pending_style['color'], 'rgb(213, 173, 98)')
        self.assertLessEqual(float(pending_style['animation'].removesuffix('s')), 0.00002)
        self.assertLessEqual(float(pending_style['transition'].removesuffix('s')), 0.00002)
        page.evaluate('window.__feedbackAction.success()')
        expect(page.locator('.edit-toast[data-state="success"] .edit-toast__mark')).to_have_css(
            'color', 'rgb(131, 197, 162)')
        context.close()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
