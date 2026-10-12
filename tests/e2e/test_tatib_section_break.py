"""A section break as a clear divider (spec 035).

Both a legacy END_OF_SECTION row and a section_break entry draw one full-width rule
across the reading column, with the break's note beneath it and the break's own
controls on hover.
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
class SectionBreakE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.SECTION_BREAK,
            title='Persembahan')
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=3, kind=tatib.ServiceEntryKind.TEXT,
            title='Penutup', text='Amin')
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, order_number=4, item_type=tatib.TataIbadahItemType.END_OF_SECTION,
            text='Doa syafaat')
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

    def test_the_break_reads_as_a_full_width_divider(self):
        page = self._page()
        dividers = page.locator('.tatib__eos')
        self.assertEqual(dividers.count(), 2)
        entry_break, legacy_break = dividers.nth(0), dividers.nth(1)
        pane = page.locator('#readBody').bounding_box()
        for divider in (entry_break, legacy_break):
            box = divider.bounding_box()
            self.assertAlmostEqual(box['width'], pane['width'], delta=40)   # spans the column
        self.assertNotIn('persembahan', entry_break.inner_text().lower())   # no label (spec 038)
        self.assertIn('doa syafaat', legacy_break.inner_text().lower())     # the legacy note stays

    def test_the_divider_takes_the_same_box_as_the_entries(self):
        # Spec 055, amended by 068: the divider shares the entry box -- 56px,
        # no margins -- with
        # its rule at the centre, instead of the old 16px-margined hairline.
        page = self._page()
        page.mouse.move(1400, 850)
        for index in range(page.locator('.tatib__eos').count()):
            divider = page.locator('.tatib__eos').nth(index)
            self.assertEqual(divider.evaluate(
                'el => [getComputedStyle(el).marginTop, getComputedStyle(el).marginBottom]'),
                ['0px', '0px'], index)
            self.assertEqual(divider.evaluate('el => getComputedStyle(el).minHeight'), '56px', index)
            self.assertAlmostEqual(divider.bounding_box()['height'], 56, delta=0.6, msg=index)

    def test_the_legacy_note_sits_under_the_centred_rule(self):
        page = self._page()
        page.mouse.move(1400, 850)
        divider = page.locator('.tatib__eos').nth(1)          # the legacy row keeps its note
        note = divider.locator('.tatib__note')
        self.assertEqual(note.count(), 1)
        box, note_box = divider.bounding_box(), note.bounding_box()
        self.assertAlmostEqual(note_box['y'] - box['y'], 35, delta=2)   # 50% + 7px

    def test_plus_break_adds_the_break_at_once_without_a_dialog(self):
        page = self._page()
        before = page.locator('.tatib__eos').count()
        page.locator('.tatib__eos').first.hover()
        page.wait_for_timeout(400)
        # The add row reveals on hover; dispatching the click avoids the 2px rule moving under the pointer.
        page.locator('.entry__add-btn[data-entry-open="section_break"]').first.dispatch_event('click')
        page.wait_for_function(
            "document.querySelectorAll('.tatib__eos').length > %d" % before)
        self.assertEqual(page.locator('dialog[open]').count(), 0)   # no form opened (spec 057)
        self.assertEqual(page.locator('.tatib__eos').count(), before + 1)

    def test_the_divider_carries_its_own_controls(self):
        page = self._page()
        divider = page.locator('.tatib__eos').first
        acts = divider.locator('.entry__acts')
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        # With the collapsing add rows (spec 052) the first hover opens the rows
        # around the 2px divider, which pushes it down out from under the pointer;
        # the reader re-targets it once, and it stays put from then on.
        divider.hover()
        page.wait_for_timeout(400)
        divider.hover()
        expect(acts).to_have_css('opacity', '1')
        self.assertEqual(divider.locator('[data-entry-edit]').count(), 0)   # no Edit on a break (spec 057)
        self.assertEqual(divider.locator('[data-entry-delete]').count(), 1)
