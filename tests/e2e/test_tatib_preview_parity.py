"""The shipped Tata Ibadah views against the preview the spec was accepted on (spec 167).

The preview is the reference: every number in the spec's `## UI/UX` came from it. This
module measures the two side by side — the live page from a real server, the preview as the
static file it is — and fails when the product drifts from what was signed off. Text is
never compared (the fixtures differ); only the box and type facts the preview fixed.
"""

import pathlib
import unittest

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


PREVIEW = pathlib.Path(settings.BASE_DIR) / 'specs' / '167-tata-ibadah-templates' / 'preview' / 'index.html'

MEASURE = """() => {
  const box = el => { const r = el.getBoundingClientRect(); return {x: r.x, w: r.width, h: r.height}; };
  const cs = el => getComputedStyle(el);
  const bar = document.querySelector('[data-entry-start] .entry__add-inner')
           || document.querySelector('#read .entry__add-inner');
  const item = document.querySelector('[data-slot-kind="choice"]')
            || document.querySelector('.slot[data-kind="choice"]')
            || document.querySelector('.choice')
            || document.querySelector('.tatib__item--slot');
  const title = item && item.querySelector('.read__sec, .slot__title');
  const option = document.querySelector('[data-option-of], .choice__option');
  const optionText = option && (option.querySelector('.read__sec, .choice__ref') || option);
  const addOption = document.querySelector('[data-add-option], .choice__add');
  return {
    order: [].slice.call(bar ? bar.querySelectorAll('.entry__add-btn') : [])
             .map(b => b.textContent.trim()),
    slotTitle: title && {size: cs(title).fontSize, weight: cs(title).fontWeight,
                         family: cs(title).fontFamily, align: cs(title).textAlign},
    mark: !!document.querySelector('.slot__mark'),
    option: option && {borderLeft: cs(option).borderLeftWidth},
    optionTextX: optionText ? box(optionText).x : null,
    addOptionX: addOption ? box(addOption).x : null,
  };
}"""

GENERATE = """() => {
  const m = document.getElementById('generateModal');
  const fixed = m.querySelector('.g-fixed, .g-stage-row[data-fixed]');
  const title = fixed && fixed.querySelector('.read__sec');
  const body = fixed && fixed.querySelector('.tatib__tx');
  const box = el => el ? el.getBoundingClientRect() : null;
  return {
    titleSize: title ? getComputedStyle(title).fontSize : null,
    bodySize: body ? getComputedStyle(body).fontSize : null,
    rowHeight: fixed ? box(fixed).height : null,
    opacity: fixed ? getComputedStyle(fixed).opacity : null,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PreviewParityTests(StaticLiveServerTestCase):
    def setUp(self):
        self.service = tatib.TataIbadah.objects.create(
            name='Parity skeleton', is_active=True)   # no date: a template
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita adalah dalam nama Tuhan, yang menjadikan langit dan bumi.')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.SONG, title='Nyanyian Pembuka', order_number=2)
        choice = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.TEXT, title='Doa Pengutusan', order_number=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, parent=choice,
            order_number=4, title='Doa Damai', text='Tuhan, berilah damai.')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, parent=choice,
            order_number=5, title='Doa Berkat', text='Tuhan, berkati kami.')

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def tearDown(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def live(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(500)
        return self.page.evaluate(MEASURE)

    def preview(self):
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(500)
        return self.page.evaluate(MEASURE)

    def test_the_add_bar_offers_the_same_six_buttons_in_the_same_order(self):
        self.assertEqual(self.live()['order'], self.preview()['order'])

    def test_the_page_slot_row_keeps_the_preview_type(self):
        live, preview = self.live(), self.preview()
        self.assertEqual(live['slotTitle']['size'], preview['slotTitle']['size'])
        self.assertEqual(live['slotTitle']['weight'], preview['slotTitle']['weight'])
        self.assertIn('serif', live['slotTitle']['family'].lower())
        self.assertIn('serif', preview['slotTitle']['family'].lower())
        self.assertEqual(live['slotTitle']['align'], 'left')

    def test_a_slot_row_draws_its_mark(self):
        self.assertTrue(self.live()['mark'])
        self.assertTrue(self.preview()['mark'])

    def test_the_option_carries_no_rule_of_its_own(self):
        live, preview = self.live(), self.preview()
        self.assertEqual(live['option']['borderLeft'], '0px')
        self.assertEqual(preview['option']['borderLeft'], '0px')

    def test_add_option_sits_on_the_option_text(self):
        live, preview = self.live(), self.preview()
        self.assertLessEqual(abs((live['addOptionX'] - live['optionTextX'])), 2)
        self.assertLessEqual(abs((preview['addOptionX'] - preview['optionTextX'])), 2)

    def test_the_muted_rows_in_use_template_are_the_preview_size(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        self.page.click('[data-generate-open]')
        self.page.wait_for_timeout(400)
        live = self.page.evaluate(GENERATE)
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(400)
        self.page.click('[data-surface="generate"]')
        self.page.wait_for_timeout(400)
        preview = self.page.evaluate(GENERATE)
        self.assertEqual(live['titleSize'], preview['titleSize'])
        self.assertEqual(live['bodySize'], preview['bodySize'])
        self.assertEqual(live['opacity'], preview['opacity'])
        self.assertLessEqual(abs(live['rowHeight'] - preview['rowHeight']), preview['rowHeight'] * 0.15,
                             f"{live['rowHeight']} vs {preview['rowHeight']}")
