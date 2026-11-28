"""Use template progress persists for seven days, and the button marks a draft (spec 255).

A persistent browser profile is used so "close the browser and reopen" is real: the same
Chromium profile directory is relaunched, which is exactly how localStorage outlives a session.
"""

import json
import shutil
import tempfile
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
WEEK_MS = 7 * 24 * 60 * 60 * 1000


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UseTemplateProgressPersistE2ETests(StaticLiveServerTestCase):
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

        self.template_b = self._make_template('Skeleton B')
        self.fill_b = tatib.ServiceEntry.objects.create(
            tatib=self.template_b, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.TEXT, title='Doa B', order_number=2)

        self.template_before = list(self.template_a.service_entries.order_by('order_number')
                                    .values_list('pk', 'kind', 'title', 'text', 'parent_id'))
        self.profile = tempfile.mkdtemp(prefix='gkps-persist-')
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
        self.context = self.playwright.chromium.launch_persistent_context(
            self.profile, headless=True,
            viewport={'width': 1440, 'height': 900}, color_scheme='dark')
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self._stopped = False

    def stop_browser(self):
        if getattr(self, '_stopped', True):
            return
        self.context.close()
        self.playwright.stop()
        self._stopped = True

    def restart_browser(self):
        self.stop_browser()
        self.start_browser()

    def tearDown(self):
        self.stop_browser()
        shutil.rmtree(self.profile, ignore_errors=True)
        super().tearDown()

    # ---------------------------------------------------------------- helpers

    def url(self, template):
        return self.live_server_url + reverse('web-tatib-service', args=[template.pk])

    def open(self, template):
        self.page.goto(self.url(template))
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

    def settle_all(self):
        self.settle_fill(self.fill_a)
        self.settle_choice()

    def leave(self):
        self.page.click('[data-generate-close]')
        expect(self.page.locator('[data-generate-leave]')).to_be_visible()
        self.page.click('[data-leave-accept]')
        expect(self.page.locator('#generateModal')).to_be_hidden()

    def record(self, template):
        return self.page.evaluate(
            """key => { const raw = localStorage.getItem(key); return raw ? JSON.parse(raw) : null; }""",
            KEY_PREFIX + str(template.pk))

    def seed(self, template, record, age_ms=0):
        self.page.goto(self.url(template))
        self.page.evaluate("""([key, value, age]) => {
            const copy = Object.assign({}, value);
            copy.savedAt = Date.now() - age;
            localStorage.setItem(key, JSON.stringify(copy));
        }""", [KEY_PREFIX + str(template.pk), record, age_ms])

    def mark(self):
        return self.page.evaluate("""() => {
          const btn = document.querySelector('[data-generate-open]');
          const dot = btn && btn.querySelector('.read__draft-dot');
          const b = btn && btn.getBoundingClientRect();
          const d = dot && dot.getBoundingClientRect();
          return {
            draft: btn ? btn.dataset.draft : null,
            label: btn ? btn.getAttribute('aria-label') : null,
            hasDot: d ? d.width > 0 : false,
            dotW: d ? +d.width.toFixed(1) : 0, dotH: d ? +d.height.toFixed(1) : 0,
            insetX: d ? +(b.right - d.right).toFixed(1) : null,
            insetY: d ? +(d.top - b.top).toFixed(1) : null,
            width: b ? +b.width.toFixed(1) : 0
          };
        }""")

    # ------------------------------------------------------------- the store

    def test_the_record_is_stored_locally_with_a_timestamp(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        record = self.record(self.template_a)
        self.assertEqual(record['v'], 2)
        self.assertIn('savedAt', record)
        age = self.page.evaluate('n => Date.now() - n', record['savedAt'])
        self.assertLess(age, 10000)
        self.assertIsNone(self.page.evaluate(
            'key => sessionStorage.getItem(key)', KEY_PREFIX + str(self.template_a.pk)))

    def test_progress_survives_a_new_browser_session(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.restart_browser()                       # the browser is closed and reopened
        self.open(self.template_a)
        expect(self.page.locator('[data-slot-row="%d"] .g-value' % self.fill_a.pk)) \
            .to_contain_text('Doa Syafaat')

    def test_an_expired_record_is_ignored_and_removed(self):
        self.seed(self.template_a, {
            'v': 2, 'step': 1, 'settled': {str(self.fill_a.pk): {'label': 'Old', 'data': {}}},
            'name': 'Lama', 'date': ''}, age_ms=WEEK_MS + 1000)
        self.page.wait_for_timeout(100)
        self.open(self.template_a)
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 0)
        self.assertIsNone(self.record(self.template_a))

    def test_a_save_on_day_six_restarts_the_clock(self):
        self.seed(self.template_a, {
            'v': 2, 'step': 1,
            'settled': {str(self.fill_a.pk): {'label': 'Doa Syafaat', 'data': {}},
                        str(self.choice_a.pk): {'main': 'Opsi Satu', 'mute': ''}},
            'name': 'Ibadah', 'date': ''}, age_ms=WEEK_MS - 24 * 3600 * 1000)
        self.page.wait_for_timeout(100)
        self.open(self.template_a)
        self.page.click('[data-generate-next]')
        self.page.fill('[data-generate-name-input]', 'Nama Baru')
        record = self.record(self.template_a)
        age = self.page.evaluate('n => Date.now() - n', record['savedAt'])
        self.assertLess(age, 10000, 'the clock did not restart on a save')

    def test_every_change_refreshes_the_timestamp(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        first = self.record(self.template_a)['savedAt']
        self.page.wait_for_timeout(20)
        self.settle_choice()
        second = self.record(self.template_a)['savedAt']
        self.assertGreater(second, first)

    def test_two_templates_keep_separate_clocks(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.open(self.template_b)
        self.settle_fill(self.fill_b, 'Doa B')
        a = self.record(self.template_a)
        b = self.record(self.template_b)
        self.assertNotEqual(a['savedAt'], b['savedAt'])
        self.assertIn(str(self.fill_a.pk), a['settled'])
        self.assertNotIn(str(self.fill_a.pk), b['settled'])

    def test_reopening_restores_slots_step_name_and_date(self):
        self.open(self.template_a)
        self.settle_all()
        self.page.click('[data-generate-next]')
        self.page.fill('[data-generate-name-input]', 'Ibadah Uji')
        self.page.eval_on_selector(
            '[data-generate-date]',
            "el => { el.value = '2026-12-06'; el.dispatchEvent(new Event('change', {bubbles: true})); }")
        self.leave()
        self.restart_browser()
        self.open(self.template_a)
        self.assertTrue(self.page.locator('[data-generate-step="2"]').is_visible())
        self.assertEqual(self.page.input_value('[data-generate-name-input]'), 'Ibadah Uji')
        self.assertEqual(self.page.input_value('[data-generate-date]'), '2026-12-06')
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 2)

    # ----------------------------------------------------------- the mark

    def test_the_button_marks_a_live_draft(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.page.reload()
        state = self.mark()
        self.assertEqual(state['draft'], 'true')
        self.assertTrue(state['hasDot'])
        self.assertEqual((state['dotW'], state['dotH']), (7.0, 7.0))
        self.assertEqual((state['insetX'], state['insetY']), (4.0, 4.0))

    def test_the_button_has_no_mark_without_a_draft(self):
        self.page.goto(self.url(self.template_a))
        state = self.mark()
        self.assertNotEqual(state['draft'], 'true')
        self.assertIsNone(state['label'])
        self.assertFalse(state['hasDot'])

    def test_the_mark_appears_after_the_first_save(self):
        self.open(self.template_a)
        self.assertNotEqual(self.mark()['draft'], 'true')
        self.settle_fill(self.fill_a)
        self.leave()
        self.assertEqual(self.mark()['draft'], 'true')

    def test_the_mark_is_gone_after_create(self):
        self.open(self.template_a)
        self.settle_all()
        self.page.click('[data-generate-next]')
        self.page.click('[data-generate-create]')
        expect(self.page.locator('[data-generate-confirm]')).to_be_visible()
        before = self.page.url
        self.page.click('[data-generate-accept]')
        self.page.wait_for_url(lambda url: url != before, wait_until='load')
        self.page.goto(self.url(self.template_a))
        state = self.mark()
        self.assertNotEqual(state['draft'], 'true')
        self.assertIsNone(state['label'])

    def test_the_mark_names_the_saved_draft(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.page.reload()
        self.assertEqual(self.mark()['label'], 'Use template, draft saved')

    def test_the_mark_does_not_change_the_button_width(self):
        self.page.goto(self.url(self.template_a))
        bare = self.mark()['width']
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.leave()
        self.page.reload()
        self.assertEqual(self.mark()['width'], bare)

    def test_the_leave_confirmation_names_the_seven_day_lifetime(self):
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.page.click('[data-generate-close]')
        expect(self.page.locator('[data-generate-leave]')).to_be_visible()
        text = self.page.locator('[data-generate-leave]').inner_text()
        self.assertIn('seven days', text)
        self.assertNotIn('browser session', text)

    def test_storage_failure_does_not_break_the_modal(self):
        self.page.add_init_script(
            "Object.defineProperty(window, 'localStorage', { get() { throw new Error('denied'); } });")
        self.open(self.template_a)
        self.settle_fill(self.fill_a)
        self.assertEqual(self.page.locator('.g-row--slot[data-set="true"]').count(), 1)
        self.assertNotEqual(self.mark()['draft'], 'true')

    def test_the_template_is_byte_identical_after_create(self):
        self.open(self.template_a)
        self.settle_all()
        self.page.click('[data-generate-next]')
        self.page.click('[data-generate-create]')
        self.page.click('[data-generate-accept]')
        self.page.wait_for_timeout(400)
        self.stop_browser()
        after = list(self.template_a.service_entries.order_by('order_number').values_list(
            'pk', 'kind', 'title', 'text', 'parent_id'))
        self.assertEqual(after, self.template_before)