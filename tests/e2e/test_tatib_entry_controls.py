"""The entry controls, floated in their item (spec 033).

Preview, Edit and Delete belong to their item: they sit at its top-right, over the
words, on a brief backing, and appear while the item is hovered or holds keyboard
focus — and always on a device with no hover.
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
class EntryControlsE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        # Both entries are long enough to be tall items: a hidden add row must not
        # be able to slip under the pointer when its neighbour expands (spec 052).
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia beserta kita semua. ' * 12)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Penutup', text='Amin. Terima kasih untuk semuanya. ' * 12)
        # A second service carries a section break, so its separation can be measured
        # without writing to the database mid-test (spec 052).
        self.with_break = tatib.TataIbadah.objects.create(
            name='Ibadah Berbagi', date=date(2026, 10, 11), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.with_break, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')
        tatib.ServiceEntry.objects.create(
            tatib=self.with_break, order_number=2, kind=tatib.ServiceEntryKind.SECTION_BREAK,
            title='Persembahan')
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

    def _page(self, service=None):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse(
            'web-tatib-service', args=[(service or self.tatib).pk]))
        page.wait_for_load_state('networkidle')
        return page

    def test_hovering_the_item_reveals_its_controls_over_the_text(self):
        page = self._page()
        acts = page.locator('.tatib__item .entry__acts').first
        item = page.locator('.tatib__item').first
        self.assertEqual(acts.count(), 1)
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        item.hover()
        expect(acts).to_have_css('opacity', '1')
        item_box, acts_box = item.bounding_box(), acts.bounding_box()
        self.assertGreater(acts_box['x'], item_box['x'] + item_box['width'] / 2)
        self.assertLess(acts_box['y'], item_box['y'] + item_box['height'] / 2)

    def test_keyboard_focus_reveals_the_controls(self):
        page = self._page()
        acts = page.locator('.tatib__item .entry__acts').first
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        page.locator('[data-entry-edit]').first.focus()
        expect(acts).to_have_css('opacity', '1')

    def test_the_add_row_is_not_part_of_the_item(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        bar = page.locator('.entry__add').first
        acts = page.locator('.entry__acts').first
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        self.assertEqual(bar.bounding_box()['height'], 0)   # collapsed at rest (spec 052)
        item.hover()                             # a collapsed row has no box to hover
        expect(bar).to_have_css('opacity', '1')
        page.wait_for_timeout(250)               # past the reveal transition
        bar.hover()
        expect(bar).to_have_css('opacity', '1')               # the bar's own hover keeps it
        expect(acts).to_have_css('opacity', '0')              # the item above is not revealed
        expect(item).to_have_css('background-color', 'rgba(0, 0, 0, 0)')
        item_box, bar_box = item.bounding_box(), bar.bounding_box()
        self.assertLessEqual(item_box['y'] + item_box['height'], bar_box['y'] + 1)   # no overlap

    def test_hovering_the_item_still_reveals_its_add_row(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        bar = page.locator('.entry__add').first
        page.mouse.move(1400, 850)
        expect(bar).to_have_css('opacity', '0')
        item.hover()
        expect(bar).to_have_css('opacity', '1')

    def test_hovering_an_item_reveals_the_add_rows_around_it(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)     # the row between the two items
        below = page.locator('.entry__add').nth(1)     # the row after the second item
        page.mouse.move(1400, 850)
        expect(above).to_have_css('opacity', '0')
        expect(below).to_have_css('opacity', '0')
        second.hover()
        expect(above).to_have_css('opacity', '1')
        expect(below).to_have_css('opacity', '1')

    def test_focus_within_an_item_reveals_the_add_rows_around_it(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        page.mouse.move(1400, 850)
        expect(above).to_have_css('opacity', '0')
        second.locator('[data-entry-edit]').first.focus()
        expect(above).to_have_css('opacity', '1')
        expect(below).to_have_css('opacity', '1')

    def test_moving_onto_an_add_row_shows_only_that_row(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        second.hover()
        expect(below).to_have_css('opacity', '1')
        above.hover()
        expect(above).to_have_css('opacity', '1')
        expect(below).to_have_css('opacity', '0')

    # --- at rest the rows reserve nothing (spec 052) --------------------------

    def test_at_rest_the_add_rows_reserve_no_space(self):
        page = self._page()
        page.mouse.move(1400, 850)
        for row in page.locator('#readBody > .entry__add').all():
            self.assertEqual(row.bounding_box()['height'], 0)
        # And the spacing between entries carries nothing else: it differs from the
        # editors-off page (where no row exists between the items) by at most one
        # paragraph margin -- the row's own box is zero, so only the loss of margin
        # collapsing across the interposed row can show, never reserved height.
        on = [page.locator('.tatib__item').nth(i).bounding_box() for i in (0, 1)]
        with override_settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True):
            off_page = self._page()
        off = [off_page.locator('.tatib__item').nth(i).bounding_box() for i in (0, 1)]
        gap_on = round(on[1]['y'] - (on[0]['y'] + on[0]['height']), 1)
        gap_off = round(off[1]['y'] - (off[0]['y'] + off[0]['height']), 1)
        self.assertLessEqual(gap_on - gap_off, 4)

    def test_hovering_an_entry_settles_with_both_rows_open(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        page.mouse.move(1400, 850)
        before = second.bounding_box()
        # hover the entry at its centre, where a reader points
        page.mouse.move(before['x'] + before['width'] / 2,
                        before['y'] + before['height'] / 2, steps=4)
        page.wait_for_timeout(600)                    # past expand + hide delays
        self.assertGreater(above.bounding_box()['height'], 0)
        self.assertGreater(below.bounding_box()['height'], 0)
        # the reveal settles: the entry stays under the pointer (its controls show)
        # and nothing flickers -- both rows are still open after the hide window
        expect(second.locator('.entry__acts')).to_have_css('opacity', '1')
        page.wait_for_timeout(400)
        self.assertGreater(above.bounding_box()['height'], 0)
        self.assertGreater(below.bounding_box()['height'], 0)
        # the closed row above opens by pushing the entry down once, by at most
        # that row's height; the shift is bounded, never unbounded churn
        shift = second.bounding_box()['y'] - before['y']
        self.assertLessEqual(shift, above.bounding_box()['height'] + 1)
        # and each row's box starts below its item's box (spec 036: no overlap)
        item_above = page.locator('.tatib__item').nth(0)
        self.assertLessEqual(item_above.bounding_box()['y'] + item_above.bounding_box()['height'],
                             above.bounding_box()['y'] + 1)
        after = second.bounding_box()
        self.assertLessEqual(after['y'] + after['height'], below.bounding_box()['y'] + 1)

    def test_tabbing_into_a_collapsed_row_expands_it(self):
        page = self._page()
        page.mouse.move(1400, 850)
        row = page.locator('#readBody > .entry__add').first
        self.assertEqual(row.bounding_box()['height'], 0)
        row.locator('[data-entry-open]').first.focus()
        expect(row).to_have_css('opacity', '1')
        self.assertGreater(row.bounding_box()['height'], 0)

    def test_the_break_separation_is_tighter(self):
        page = self._page(self.with_break)          # the service that carries a break
        margins = page.locator('.tatib__eos').first.evaluate(
            'el => [getComputedStyle(el).marginTop, getComputedStyle(el).marginBottom]')
        self.assertEqual(margins, ['16px', '16px'])

    def test_the_no_hover_rule_shows_the_add_rows(self):
        # Chromium in CI cannot emulate a touch device, so assert the rule that
        # serves one exists and would show the add rows outright (spec 052).
        page = self._page()
        applied = page.evaluate("""() => {
          for (const sheet of document.styleSheets) {
            let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
            for (const rule of rules) {
              if (!rule.media || !rule.media.mediaText.includes('pointer: coarse')) continue;
              for (const inner of rule.cssRules) {
                if (inner.selectorText && inner.selectorText.includes('.entry__add')
                    && inner.style.opacity === '1') return true;
              }
            }
          }
          return false;
        }""")
        self.assertTrue(applied, 'the no-hover rule for the add rows is missing')

    def test_the_no_hover_rule_shows_the_controls(self):
        # Chromium in CI cannot emulate a touch (no-hover, coarse-pointer) device, so
        # assert the rule that serves one exists and would show the controls.
        page = self._page()
        applied = page.evaluate("""() => {
          for (const sheet of document.styleSheets) {
            let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
            for (const rule of rules) {
              if (!rule.media || !rule.media.mediaText.includes('pointer: coarse')) continue;
              for (const inner of rule.cssRules) {
                if (inner.selectorText && inner.selectorText.includes('.entry__acts')
                    && inner.style.opacity === '1') return true;
              }
            }
          }
          return false;
        }""")
        self.assertTrue(applied, 'the no-hover rule is missing')
