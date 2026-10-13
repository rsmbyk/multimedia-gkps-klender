"""The entry box: the controls' home (spec 033, amended by spec 055).

Preview, Edit and Delete float at their item's top-right inside a box that
CONTAINS them -- 56px minimum, words centred on the box's centreline. Every
revealed add row keeps equal 8px above and below its buttons; the start bar
collapses at rest and reveals with the first block; the controls appear while
the item is hovered or holds keyboard focus, and always on a device with no
hover.
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
        # An untitled entry: its first content is a line of text, which is where
        # floating controls used to land (spec 053).
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=3, kind=tatib.ServiceEntryKind.TEXT,
            title='', text='Kasih karunia beserta kita semua. ' * 12)
        # A one-liner: its box has room for the controls, its words on the
        # box's centreline (spec 055).
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=4, kind=tatib.ServiceEntryKind.TEXT,
            title='', text='Amin.')
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

    def _revealed_gaps(self, page):
        """Each revealed add row: the button block's distance to the box above and below.

        Measured to the inner block, not one button: at test widths the five buttons
        wrap to two lines (spec 055), and the 8px bracket belongs around the block.
        """
        return page.evaluate("""() => {
          const round = n => Math.round(n * 10) / 10;
          const out = [];
          [].slice.call(document.querySelectorAll('#readBody > .entry__add'))
            .forEach(function (row) {
              if (row.getBoundingClientRect().height < 1) return;
              const block = row.querySelector('.entry__add-inner').getBoundingClientRect();
              const prev = row.previousElementSibling, next = row.nextElementSibling;
              out.push({
                above: prev ? round(block.top - prev.getBoundingClientRect().bottom) : null,
                below: next ? round(next.getBoundingClientRect().top - block.bottom) : null,
              });
            });
          return out;
        }""")

    # --- the box contains the controls (spec 055, replacing the 053 band) -----

    def test_the_box_contains_the_controls(self):
        page = self._page()
        page.mouse.move(1400, 850)
        boxes = page.locator('.tatib__item, .tatib__eos')
        self.assertGreater(boxes.count(), 0)
        for index in range(boxes.count()):
            item = boxes.nth(index)
            acts = item.locator('.entry__acts')
            if acts.count() == 0:
                continue
            item_box, acts_box = item.bounding_box(), acts.bounding_box()
            self.assertGreaterEqual(acts_box['y'], item_box['y'] - 1,
                                    'entry %d: controls start above the box' % index)
            self.assertLessEqual(acts_box['y'] + acts_box['height'],
                                 item_box['y'] + item_box['height'] + 1,
                                 'entry %d: controls end below the box' % index)
            self.assertGreaterEqual(acts_box['x'], item_box['x'] - 1,
                                    'entry %d: controls start outside the box' % index)
            right_gap = item_box['x'] + item_box['width'] - acts_box['x'] - acts_box['width']
            self.assertAlmostEqual(right_gap, 8, delta=1,
                                   msg='entry %d: controls are not right-aligned' % index)

    def test_the_box_is_at_least_the_controls_height(self):
        page = self._page()
        page.mouse.move(1400, 850)
        items = page.locator('.tatib__item--acts')
        self.assertGreater(items.count(), 0)
        for index in range(items.count()):
            self.assertGreaterEqual(items.nth(index).bounding_box()['height'], 55.5, index)
        one_liner = page.locator('.tatib__item').nth(3)
        self.assertAlmostEqual(one_liner.bounding_box()['height'], 56, delta=0.6)

    def test_the_words_are_centred_in_the_box(self):
        page = self._page()
        page.mouse.move(1400, 850)
        one_liner = page.locator('.tatib__item').nth(3)
        word = one_liner.locator('.tatib__tx').first.bounding_box()
        box = one_liner.bounding_box()
        top_gap = word['y'] - box['y']
        bottom_gap = (box['y'] + box['height']) - (word['y'] + word['height'])
        self.assertAlmostEqual(top_gap, bottom_gap, delta=1.5,
                               msg='the one-line words sit off the box centre')

    def test_the_box_replaces_the_band(self):
        page = self._page()
        page.mouse.move(1400, 850)
        with_acts = page.locator('.tatib__item:has(.entry__acts)')
        self.assertEqual(with_acts.count(), page.locator('.tatib__item--acts').count())
        for index in range(with_acts.count()):
            item = with_acts.nth(index)
            self.assertEqual(item.evaluate('el => getComputedStyle(el).paddingTop'), '8px')
            self.assertEqual(item.evaluate('el => getComputedStyle(el).minHeight'), '56px')
        rule = self._page(self.with_break).locator('.tatib__eos').first
        self.assertEqual(rule.evaluate('el => getComputedStyle(el).minHeight'), '56px')

    def test_the_divider_takes_the_same_box(self):
        page = self._page(self.with_break)
        page.mouse.move(1400, 850)
        divider = page.locator('.tatib__eos').first
        self.assertEqual(divider.evaluate(
            'el => [getComputedStyle(el).marginTop, getComputedStyle(el).marginBottom]'),
            ['0px', '0px'])
        self.assertAlmostEqual(divider.bounding_box()['height'], 56, delta=0.6)

    def test_the_resting_surface_matches_spec_068_in_both_themes(self):
        page = self._page(self.with_break)
        page.mouse.move(1400, 850)
        for theme, fill, outline in (
            ('light', 'rgba(31, 31, 29, 0.012)', 'rgba(31, 31, 29, 0.08)'),
            ('dark', 'rgba(255, 255, 255, 0.012)', 'rgba(255, 255, 255, 0.09)'),
        ):
            page.evaluate('(value) => document.documentElement.dataset.theme = value', theme)
            root = page.locator('html')
            self.assertEqual(root.evaluate(
                "el => getComputedStyle(el).getPropertyValue('--tatib-entry-fill').trim()"), fill)
            self.assertEqual(root.evaluate(
                "el => getComputedStyle(el).getPropertyValue('--tatib-entry-outline').trim()"), outline)
            for box in (page.locator('.tatib__item--acts').first,
                        page.locator('.tatib__eos').first):
                self.assertEqual(box.evaluate('el => getComputedStyle(el).padding'),
                                 '8px 8px 8px 12px')
                self.assertEqual(box.evaluate('el => getComputedStyle(el).minHeight'), '56px')
                self.assertIn('1px inset', box.evaluate('el => getComputedStyle(el).boxShadow'))
            acts = page.locator('.entry__acts').first
            self.assertEqual(acts.evaluate(
                'el => [getComputedStyle(el).top, getComputedStyle(el).right]'), ['8px', '8px'])

    def test_the_padded_boxes_do_not_overflow_at_narrow_width(self):
        page = self._page()
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(250)
        for box in page.locator('.tatib__item--acts').all():
            self.assertTrue(box.evaluate('el => el.scrollWidth <= el.clientWidth + 1'))
        break_page = self._page(self.with_break)
        break_page.set_viewport_size({'width': 390, 'height': 844})
        self.assertTrue(break_page.locator('.tatib__eos').first.evaluate(
            'el => el.scrollWidth <= el.clientWidth + 1'))

    def test_keyboard_focus_reveals_the_controls(self):
        page = self._page()
        acts = page.locator('.tatib__item .entry__acts').first
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        page.locator('[data-entry-edit]').first.focus()
        expect(acts).to_have_css('opacity', '1')

    # --- the gaps include the buttons (spec 055) ------------------------------

    def test_a_revealed_row_keeps_equal_gaps_above_and_below(self):
        page = self._page()
        for index in (0, 1, 3):          # the first tall entry, the second, the one-liner
            hovered = page.locator('.tatib__item').nth(index)
            page.mouse.move(1400, 850)
            page.wait_for_timeout(400)   # past the hide delay
            hovered.hover()
            page.wait_for_timeout(450)   # past the expand
            hovered.hover()              # a short entry slides once; re-target it
            page.wait_for_timeout(450)
            gaps = self._revealed_gaps(page)
            self.assertGreater(len(gaps), 0, index)
            for gap in gaps:
                if gap['above'] is not None:
                    self.assertAlmostEqual(gap['above'], 8, delta=1, msg=(index, gaps))
                if gap['below'] is not None:
                    self.assertAlmostEqual(gap['below'], 8, delta=1, msg=(index, gaps))

    def test_focus_keeps_the_same_gaps(self):
        page = self._page()
        page.mouse.move(1400, 850)
        page.locator('.tatib__item').nth(1).locator('[data-entry-edit]').first.focus()
        page.wait_for_timeout(450)
        gaps = self._revealed_gaps(page)
        self.assertGreater(len(gaps), 0)
        for gap in gaps:
            if gap['above'] is not None:
                self.assertAlmostEqual(gap['above'], 8, delta=1, msg=gaps)
            if gap['below'] is not None:
                self.assertAlmostEqual(gap['below'], 8, delta=1, msg=gaps)

    def test_the_start_bar_collapses_and_reveals_with_equal_gaps(self):
        page = self._page()
        bar = page.locator('#readBody > .entry__start')
        self.assertEqual(bar.count(), 1)
        page.mouse.move(1400, 850)
        page.wait_for_timeout(450)
        self.assertEqual(bar.bounding_box()['height'], 0)      # collapsed at rest
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(450)
        self.assertGreater(bar.bounding_box()['height'], 30)   # revealed with the first entry
        gaps = page.evaluate("""() => {
          const round = n => Math.round(n * 10) / 10;
          const bar = document.querySelector('#readBody > .entry__start');
          const block = bar.querySelector('.entry__start-inner').getBoundingClientRect();
          const head = document.querySelector('#readBody').previousElementSibling;
          const entry = bar.nextElementSibling;
          const word = entry.querySelector('h2, p');
          return {
            above: round(block.top - head.getBoundingClientRect().bottom),
            below: round(entry.getBoundingClientRect().top - block.bottom),
            wordBelow: round(word.getBoundingClientRect().top - block.bottom),
            margin: getComputedStyle(bar).marginTop,
          };
        }""")
        self.assertAlmostEqual(gaps['above'], 8, delta=1, msg=gaps)
        self.assertAlmostEqual(gaps['below'], 8, delta=1, msg=gaps)
        self.assertAlmostEqual(gaps['wordBelow'], 16, delta=1, msg=gaps)
        self.assertEqual(gaps['margin'], '-30px')

    # --- at rest the rows and the bar reserve nothing (spec 055) --------------

    def test_at_rest_the_rows_and_the_bar_reserve_nothing(self):
        page = self._page()
        page.mouse.move(1400, 850)
        self.assertEqual(page.locator('#readBody > .entry__start').bounding_box()['height'], 0)
        for row in page.locator('#readBody > .entry__add').all():
            self.assertEqual(row.bounding_box()['height'], 0)
        # The resting rhythm is uniform: 12px between the boxes (the rows' 6px
        # margins), not the uneven stack the reserved space used to leave.
        gaps = page.evaluate("""() => {
          const round = n => Math.round(n * 10) / 10;
          const boxes = [].slice.call(document.querySelectorAll(
            '#readBody > .tatib__item, #readBody > .tatib__eos'));
          return boxes.slice(1).map((box, i) => round(
            box.getBoundingClientRect().top - boxes[i].getBoundingClientRect().bottom));
        }""")
        self.assertEqual(len(gaps), 3)
        for gap in gaps:
            self.assertAlmostEqual(gap, 12, delta=0.6)

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

    # --- reveal behaviour (specs 036/037/052; geometry of spec 055) -----------

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
        expect(item).to_have_css('background-color', 'rgba(31, 31, 29, 0.01)')
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

    def test_tabbing_into_a_collapsed_row_expands_it(self):
        page = self._page()
        page.mouse.move(1400, 850)
        row = page.locator('#readBody > .entry__add').first
        self.assertEqual(row.bounding_box()['height'], 0)
        row.locator('[data-entry-open]').first.focus()
        expect(row).to_have_css('opacity', '1')
        self.assertGreater(row.bounding_box()['height'], 0)

    # --- the no-hover device --------------------------------------------------

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

    def test_the_no_hover_rule_shows_the_start_bar(self):
        # Spec 055: the bar joins the rows -- a device with no hover sees it outright.
        page = self._page()
        applied = page.evaluate("""() => {
          for (const sheet of document.styleSheets) {
            let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
            for (const rule of rules) {
              if (!rule.media || !rule.media.mediaText.includes('pointer: coarse')) continue;
              for (const inner of rule.cssRules) {
                if (inner.selectorText && inner.selectorText.includes('.entry__start')
                    && inner.style.opacity === '1') return true;
              }
            }
          }
          return false;
        }""")
        self.assertTrue(applied, 'the no-hover rule for the start bar is missing')
