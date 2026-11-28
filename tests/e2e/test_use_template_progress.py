"""Use template progress survives a close — browser acceptance for spec 253.

The same runner and the same rule as the other e2e suites: Playwright's loop must not
overlap Django's database access, so every DB assertion happens after the page is closed.
"""

import json
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


KEY_PREFIX = 'gkps:generate:'


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UseTemplateProgressE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        self.template_a = self._make_template('Skeleton A')
        self.fill_a = tatib.ServiceEntry.objects.create(
            tatib=self.template_a, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.TEXT, title='Doa A', order_number=2)
        self.choice_a = tatib.ServiceEntry.objects.create(
            tatib=self.template_a, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.TEXT, title='Pilihan A', order_number=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.template_a, kind=tatib.ServiceEntryKind.TEXT, parent=self.choice_a,
            order_number=4, title='Opsi Satu', text='Tuhan, berilah damai.')
        tatib.ServiceEntry.objects.create(
            tatib=self.template_a, kind=tatib.ServiceEntryKind.TEXT, parent=self.choice_a,
            order_number=5, title='Opsi Dua', text='Tuhan, berkati kami.')

        self.template_b = self._make_template('Skeleton B')
        self.fill_b = tatib.ServiceEntry.objects.create(
            tatib=self.template_b, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.TEXT, title='Doa B', order_number=2)
        self.choice_b = tatib.ServiceEntry.objects.create(
            tatib=self.template_b, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.TEXT, title='Pilihan B', order_number=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.template_b, kind=tatib.ServiceEntryKind.TEXT, parent=self.choice_b,
            order_number=4, title='Opsi B', text='Tuhan, dengarkanlah kami.')

        self.template_before = list(self.template_a.service_entries.order_by('order_number')
                                    .values_list('pk', 'kind', 'title', 'text', 'parent_id'))
        self.start_browser()

    @staticmethod
    def _make_template(name):
        template = tatib.TataIbadah.objects.create(name=name, is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=template, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita adalah dalam nama Tuhan.')
        return template

    def start_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        self._stopped = False

    def stop_browser(self):
        if getattr(self, '_stopped', True):
            return
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        self._stopped = True

    def restart_browser(self):
        self.stop_browser()
        self.start_browser()

    def tearDown(self):
        self.stop_browser()
        super().tearDown()

    # ---------------------------------------------------------------- helpers

    def open(self, template):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[template.pk]))
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()

    def settle_fill(self, fill, title='Doa Syafaat'):
        self.page.click('[data-slot-row="%d"] [data-slot-action]' % fill.pk)
        expect(self.page.locator('#editorContent form')).to_be_visible()
        self.page.fill('#editorContent input[name="title"]', title)
        self.page.fill('#editorContent textarea[name="text"]', 'Tuhan, dengarkanlah kami.')
        self.page.click('#editorContent .editor__save')
        expect(self.page.locator('[data-slot-row="%d"] .g-value' % fill.pk)).to_contain_text(title)

    def settle_choice(self):
        self.page.click('[data-choice-open]')
        self.page.locator('[data-choose-pick]').first.click()

    def record(self, template):
        return self.page.evaluate(
            """key => { const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : null; }""",
            KEY_PREFIX + str(template.pk))

    def all_records(self):
        return self.page.evaluate(
            """prefix => { const out = {}; for (let i = 0; i < localStorage.length; i++) {
                const k = localStorage.key(i);
                if (k.startsWith(prefix)) out[k] = JSON.parse(localStorage.getItem(k));
              } return out; }""", KEY_PREFIX)

    def close_via(self, how):
        if how == 'cancel':
            self.page.click('[data-generate-close]')
        elif how == 'escape':
            self.page.keyboard.press('Escape')
        else:
            # the dialog itself is the backdrop target in the real handler
            self.page.locator('#generateModal').evaluate('el => el.click()')

    def leave(self):
        self.close_via('cancel')
        expect(self.page.locator('[data-generate-leave]')).to_be_visible()
        self.page.click('[data-leave-accept]')
        expect(self.page.locator('#generateModal')).to_be_hidden()

    # ------------------------------------------------------------ US1: kept

    def test_progress_is_keyed_by_template_id(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.assertEqual(list(self.all_records()), [KEY_PREFIX + str(self.template_a.pk)])

    def test_settling_a_slot_writes_progress_for_that_template(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        record = self.record(self.template_a)
        self.assertIsNotNone(record)
        self.assertIn(str(self.fill_a.pk), record['settled'])

    def test_the_saved_record_holds_slots_step_name_and_date(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.settle_choice()
        self.page.click('[data-generate-next]')
        self.page.fill('[data-generate-name-input]', 'Ibadah Uji')
        self.page.eval_on_selector(
            '[data-generate-date]',
            "el => { el.value = '2026-12-06'; el.dispatchEvent(new Event('change', {bubbles: true})); }")
        record = self.record(self.template_a)
        self.assertEqual(record['v'], 2)
        self.assertEqual(record['step'], 2)
        self.assertEqual(set(record['settled']), {str(self.fill_a.pk), str(self.choice_a.pk)})
        self.assertEqual(record['name'], 'Ibadah Uji')
        self.assertEqual(record['date'], '2026-12-06')

    def test_every_slot_name_and_date_change_rewrites_progress(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.assertEqual(len(self.record(self.template_a)['settled']), 1)
        self.settle_choice()
        self.assertEqual(len(self.record(self.template_a)['settled']), 2)
        self.page.click('[data-generate-next]')
        self.assertEqual(self.record(self.template_a)['step'], 2)
        self.page.fill('[data-generate-name-input]', 'Nama Baru')
        self.assertEqual(self.record(self.template_a)['name'], 'Nama Baru')
        self.page.eval_on_selector(
            '[data-generate-date]',
            "el => { el.value = '2026-12-13'; el.dispatchEvent(new Event('change', {bubbles: true})); }")
        self.assertEqual(self.record(self.template_a)['date'], '2026-12-13')

    def test_reopening_restores_slots_step_name_and_date(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.settle_choice()
        self.page.click('[data-generate-next]')
        self.page.fill('[data-generate-name-input]', 'Ibadah Uji')
        self.page.eval_on_selector(
            '[data-generate-date]',
            "el => { el.value = '2026-12-06'; el.dispatchEvent(new Event('change', {bubbles: true})); }")
        self.leave()
        self.open(self.template_a)
        self.assertEqual(self.page.locator('[data-generate-step="2"]').is_visible(), True)
        self.assertEqual(self.page.input_value('[data-generate-name-input]'), 'Ibadah Uji')
        self.assertEqual(self.page.input_value('[data-generate-date]'), '2026-12-06')
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 2)

    def test_a_reload_restores_progress(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.page.reload()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('[data-slot-row="%d"] .g-value' % self.fill_a.pk)) \
            .to_contain_text('Doa Syafaat')

    def test_two_templates_hold_separate_progress(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.open(self.template_b)
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 0)
        self.assertEqual(list(self.all_records()), [KEY_PREFIX + str(self.template_a.pk)])
        self.page.click('[data-generate-close]')   # B is clean: no confirmation
        self.open(self.template_a)
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 1)

    def test_a_new_browser_context_starts_empty(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.restart_browser()                       # a new browser session
        self.open(self.template_a)
        self.assertEqual(self.all_records(), {})
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 0)

    def test_a_slot_removed_from_the_template_is_ignored_on_restore(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.settle_choice()
        self.leave()
        key = KEY_PREFIX + str(self.template_a.pk)
        raw = self.page.evaluate('key => localStorage.getItem(key)', key)
        self.stop_browser()
        tatib.ServiceEntry.objects.filter(pk=self.choice_a.pk).delete()
        self.start_browser()
        # a new browser session, but restore the saved record to test the stale id
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.template_a.pk]))
        self.page.evaluate('([key, raw]) => localStorage.setItem(key, raw)', [key, raw])
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.assertEqual(self.page.locator('.g-row--slot').count(), 1)
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 1)
        expect(self.page.locator('[data-generate-status]')).to_contain_text('All 1 entry settled.')

    # ------------------------------------------------------ US2: the word

    def test_cancel_backdrop_and_escape_each_show_the_leave_confirm(self):
        for how in ('cancel', 'backdrop', 'escape'):
            with self.subTest(how=how):
                self.open(self.template_a)
                self.settle_fill(self.fill_a)
                self.close_via(how)
                expect(self.page.locator('[data-generate-leave]')).to_be_visible()
                text = self.page.locator('[data-generate-leave]').inner_text()
                self.assertIn('saved on this browser for seven days', text)
                self.assertIn('pick up where you left off', text)
                self.page.click('[data-leave-stay]')
                self.page.click('[data-generate-close]')
                self.page.click('[data-leave-accept]')

    def test_a_clean_modal_closes_without_a_confirm(self):
        self.open(self.template_a)
        self.close_via('cancel')
        expect(self.page.locator('#generateModal')).to_be_hidden()
        expect(self.page.locator('[data-generate-leave]')).to_be_hidden()
        self.assertEqual(self.all_records(), {})

    def test_stay_keeps_the_modal_and_the_settled_rows(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.close_via('cancel')
        self.page.click('[data-leave-stay]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 1)

    def test_leave_closes_and_the_progress_survives(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.assertIsNotNone(self.record(self.template_a))
        self.open(self.template_a)
        expect(self.page.locator('[data-slot-row="%d"] .g-value' % self.fill_a.pk)) \
            .to_contain_text('Doa Syafaat')

    # ------------------------------------------------- Create consumes it

    def test_a_successful_create_clears_that_templates_progress(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.settle_choice()
        self.page.click('[data-generate-next]')
        self.assertIsNotNone(self.record(self.template_a))
        self.page.click('[data-generate-create]')
        expect(self.page.locator('[data-generate-confirm]')).to_be_visible()
        before = self.page.url
        self.page.click('[data-generate-accept]')
        self.page.wait_for_url(lambda url: url != before, wait_until='load')
        self.page.wait_for_timeout(200)
        self.assertIsNone(self.record(self.template_a))

    def test_the_template_is_byte_identical_after_close_and_create(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.page.reload()
        self.page.click('[data-generate-open]')
        self.settle_choice()
        self.page.click('[data-generate-next]')
        self.page.click('[data-generate-create]')
        self.page.click('[data-generate-accept]')
        self.page.wait_for_timeout(400)
        self.stop_browser()
        after = list(self.template_a.service_entries.order_by('order_number').values_list(
            'pk', 'kind', 'title', 'text', 'parent_id'))
        self.assertEqual(after, self.template_before)
