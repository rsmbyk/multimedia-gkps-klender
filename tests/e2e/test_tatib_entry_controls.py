"""The entry box: the controls' home (spec 033, amended by spec 055).

Preview, Edit and Delete float at their item's top-right inside a box that
CONTAINS them -- 56px minimum, words centred on the box's centreline. Each add
row keeps a 20px slot in the flow and draws its 34px bar over that slot on the
seam line, so opening one moves nothing (spec 143); the start bar is the same bar
above the first block; the controls appear while the item is hovered or holds
keyboard focus, and always on a device with no hover.
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
            ['8px', '8px'])
        self.assertAlmostEqual(divider.bounding_box()['height'], 56, delta=0.6)

    def test_the_resting_surface_is_the_canvas_in_both_themes(self):
        # Spec 142 retires the spec 068 fill and inset ring: at rest an entry is
        # the page. What must survive is the box's dimensions -- the 8/8/8/12
        # padding, the 56px floor and the reserved controls column -- because
        # those are what the hover tint turns into a row.
        page = self._page(self.with_break)
        page.mouse.move(1400, 850)
        for theme in ('light', 'dark'):
            page.evaluate('(value) => document.documentElement.dataset.theme = value', theme)
            item = page.locator('.tatib__item--acts').first
            divider = page.locator('.tatib__eos').first
            for box in (item, divider):
                self.assertEqual(box.evaluate('el => getComputedStyle(el).backgroundColor'),
                                 'rgba(0, 0, 0, 0)', theme)
                self.assertEqual(box.evaluate('el => getComputedStyle(el).boxShadow'),
                                 'none', theme)
            self.assertEqual(item.evaluate(
                'el => [getComputedStyle(el).paddingTop, getComputedStyle(el).paddingLeft, '
                'getComputedStyle(el).paddingBottom]'), ['8px', '12px', '8px'])
            self.assertEqual(divider.evaluate('el => getComputedStyle(el).padding'),
                             '8px 8px 8px 12px')
            reserved = float(item.evaluate('el => parseFloat(getComputedStyle(el).paddingRight)'))
            controls = page.locator('.entry__acts').first.bounding_box()['width']
            self.assertGreaterEqual(reserved, controls + 4)
            for box in (item, divider):
                self.assertEqual(box.evaluate('el => getComputedStyle(el).minHeight'), '56px')
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

    def test_opening_a_row_moves_nothing(self):
        """Spec 143: the bar is drawn over the seam, so the page never reflows."""
        page = self._page()
        tops = """() => [].slice.call(
            document.querySelectorAll('#readBody > .tatib__item, #readBody > .tatib__eos'))
          .map(function (block) {
            return Math.round((block.getBoundingClientRect().top + window.scrollY) * 10) / 10;
          })"""
        page.mouse.move(1400, 850)
        page.wait_for_timeout(400)
        resting = page.evaluate(tops)
        height = page.evaluate('document.body.scrollHeight')
        for index in (0, 1, 3):
            page.mouse.move(1400, 850)
            page.wait_for_timeout(400)
            page.locator('.tatib__item').nth(index).hover()
            page.wait_for_timeout(500)
            self.assertEqual(page.evaluate(tops), resting,
                             'hovering entry %d moved the blocks' % index)
            self.assertEqual(page.evaluate('document.body.scrollHeight'), height)
            opened = page.evaluate("""() => [].slice.call(
                document.querySelectorAll('.entry__add-inner, .entry__start-inner'))
              .filter(function (bar) { return getComputedStyle(bar).opacity === '1'; }).length""")
            self.assertEqual(opened, 2, 'entry %d should open both its rows' % index)

    def test_focus_moves_nothing_either(self):
        page = self._page()
        tops = """() => [].slice.call(
            document.querySelectorAll('#readBody > .tatib__item, #readBody > .tatib__eos'))
          .map(function (block) {
            return Math.round((block.getBoundingClientRect().top + window.scrollY) * 10) / 10;
          })"""
        page.mouse.move(1400, 850)
        page.wait_for_timeout(400)
        resting = page.evaluate(tops)
        page.locator('.tatib__item').nth(1).locator('[data-entry-edit]').first.focus()
        page.wait_for_timeout(450)
        self.assertEqual(page.evaluate(tops), resting)

    def test_the_start_bar_opens_without_moving_the_first_entry(self):
        page = self._page()
        page.mouse.move(1400, 850)
        page.wait_for_timeout(400)
        first = page.locator('#readBody > .tatib__item').first
        before = first.bounding_box()['y']
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(450)
        bar = page.locator('#readBody > .entry__start .entry__start-inner')
        self.assertEqual(bar.evaluate('el => getComputedStyle(el).opacity'), '1')
        self.assertAlmostEqual(first.bounding_box()['y'], before, delta=0.5)
        # the bar is centred on its row, and its row is the seam
        centres = page.evaluate("""() => {
          const row = document.querySelector('#readBody > .entry__start');
          const bar = row.querySelector('.entry__start-inner');
          const r = row.getBoundingClientRect(), b = bar.getBoundingClientRect();
          return [r.top + r.height / 2, b.top + b.height / 2];
        }""")
        self.assertAlmostEqual(centres[0], centres[1], delta=1)

    def test_the_row_keeps_its_slot_and_the_bar_floats_over_it(self):
        page = self._page()
        page.mouse.move(1400, 850)
        slots = page.evaluate("""() => [].slice.call(
            document.querySelectorAll('#readBody > .entry__add, #readBody > .entry__start'))
          .map(function (row) { return Math.round(row.getBoundingClientRect().height); })""")
        self.assertTrue(slots)
        for height in slots:
            self.assertEqual(height, 20, 'every row keeps a 20px slot: %r' % (slots,))
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(450)
        bar = page.evaluate("""() => {
          const row = document.querySelector('#readBody > .entry__add');
          const inner = row.querySelector('.entry__add-inner');
          const r = row.getBoundingClientRect(), b = inner.getBoundingClientRect();
          return { position: getComputedStyle(inner).position,
                   height: Math.round(b.height),
                   rowHeight: Math.round(r.height),
                   offCentre: Math.abs((b.left + b.right) / 2 - (r.left + r.right) / 2) };
        }""")
        self.assertEqual(bar['position'], 'absolute')
        self.assertEqual(bar['height'], 34)
        self.assertEqual(bar['rowHeight'], 20)
        self.assertLess(bar['offCentre'], 1, bar)

    def test_the_seam_is_a_hint_at_rest_and_brightens_when_opened(self):
        page = self._page()
        page.mouse.move(1400, 850)
        page.wait_for_timeout(400)
        rest = page.evaluate("""() => {
          const cs = getComputedStyle(document.querySelector('#readBody > .entry__add'), '::before');
          return { opacity: cs.opacity, colour: cs.backgroundColor };
        }""")
        self.assertEqual(rest['opacity'], '0.15')
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(450)
        opened = page.evaluate("""() => getComputedStyle(
            document.querySelector('#readBody > .entry__add'), '::before').opacity""")
        self.assertEqual(opened, '0.6')

    def test_the_bar_does_not_cover_the_entry_controls(self):
        page = self._page()
        page.mouse.move(1400, 850)
        page.locator('.tatib__item').nth(1).hover()
        page.wait_for_timeout(450)
        hits = page.evaluate("""() => {
          const item = document.querySelectorAll('.tatib__item')[1];
          const control = item.querySelector('.entry__acts .entry__ctrl');
          const r = control.getBoundingClientRect();
          return [r.top + 2, r.top + r.height / 2, r.bottom - 2].map(function (y) {
            const hit = document.elementFromPoint(r.left + r.width / 2, y);
            return !!(hit && (hit === control || control.contains(hit)));
          });
        }""")
        self.assertEqual(hits, [True, True, True], 'the open bar covers the controls')

    def test_a_hovered_button_is_solid_and_opaque(self):
        page = self._page()
        page.mouse.move(1400, 850)
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(450)
        target = page.evaluate("""() => {
          const button = document.querySelector('.entry__add.is-revealed .entry__add-btn');
          const r = button.getBoundingClientRect();
          return { x: r.left + r.width / 2, y: r.top + r.height / 2,
                   resting: getComputedStyle(button).borderStyle };
        }""")
        self.assertEqual(target['resting'], 'dashed')
        page.mouse.move(target['x'], target['y'])
        page.wait_for_timeout(300)
        hovered = page.evaluate("""() => {
          const button = document.querySelector('.entry__add-btn:hover');
          if (!button) return null;
          const cs = getComputedStyle(button);
          return { style: cs.borderStyle, background: cs.backgroundColor };
        }""")
        self.assertIsNotNone(hovered, 'no button took the hover')
        self.assertEqual(hovered['style'], 'solid')
        self.assertNotIn('rgba', hovered['background'],
                         'the hover fill must be opaque: %r' % (hovered,))

    def test_the_first_seam_and_the_gaps_between_blocks(self):
        page = self._page()
        page.mouse.move(1400, 850)
        gaps = page.evaluate("""() => {
          const round = n => Math.round(n * 10) / 10;
          const head = document.querySelector('.read__head');
          const blocks = [].slice.call(
            document.querySelectorAll('#readBody > .tatib__item, #readBody > .tatib__eos'));
          return { head: round(blocks[0].getBoundingClientRect().top - head.getBoundingClientRect().bottom),
                   between: round(blocks[2].getBoundingClientRect().top
                                  - blocks[1].getBoundingClientRect().bottom) };
        }""")
        self.assertAlmostEqual(gaps['head'], 34, delta=1, msg=gaps)
        self.assertAlmostEqual(gaps['between'], 20, delta=1, msg=gaps)

    def test_hovering_an_entry_settles_with_both_rows_open(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        page.mouse.move(1400, 850)
        before = second.bounding_box()
        page.mouse.move(before['x'] + before['width'] / 2,
                        before['y'] + before['height'] / 2, steps=4)
        page.wait_for_timeout(600)
        for row in (above, below):
            self.assertEqual(row.locator('.entry__add-inner').evaluate(
                'el => getComputedStyle(el).opacity'), '1')
        expect(second.locator('.entry__acts')).to_have_css('opacity', '1')
        page.wait_for_timeout(400)
        for row in (above, below):
            self.assertEqual(row.locator('.entry__add-inner').evaluate(
                'el => getComputedStyle(el).opacity'), '1')
        self.assertAlmostEqual(second.bounding_box()['y'], before['y'], delta=0.5)
        self.assertLessEqual(second.bounding_box()['y'] + second.bounding_box()['height'],
                             below.bounding_box()['y'] + 21)

    # --- reveal behaviour (specs 036/037; drawn over the seam by spec 143) ----

    def test_the_add_row_is_not_part_of_the_item(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        bar = page.locator('.entry__add').first
        acts = page.locator('.entry__acts').first
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        expect(bar.locator('.entry__add-inner')).to_have_css('opacity', '0')
        item.hover()
        expect(bar.locator('.entry__add-inner')).to_have_css('opacity', '1')
        page.wait_for_timeout(250)
        bar.hover()
        expect(bar.locator('.entry__add-inner')).to_have_css('opacity', '1')
        expect(acts).to_have_css('opacity', '0')
        expect(item).to_have_css('background-color', 'rgba(0, 0, 0, 0)')

    def test_hovering_the_item_still_reveals_its_add_row(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        bar = page.locator('.entry__add').first
        page.mouse.move(1400, 850)
        expect(bar.locator('.entry__add-inner')).to_have_css('opacity', '0')
        item.hover()
        expect(bar.locator('.entry__add-inner')).to_have_css('opacity', '1')

    def test_hovering_an_item_reveals_the_add_rows_around_it(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        page.mouse.move(1400, 850)
        expect(above.locator('.entry__add-inner')).to_have_css('opacity', '0')
        expect(below.locator('.entry__add-inner')).to_have_css('opacity', '0')
        second.hover()
        expect(above.locator('.entry__add-inner')).to_have_css('opacity', '1')
        expect(below.locator('.entry__add-inner')).to_have_css('opacity', '1')

    def test_focus_within_an_item_reveals_the_add_rows_around_it(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        page.mouse.move(1400, 850)
        expect(above.locator('.entry__add-inner')).to_have_css('opacity', '0')
        second.locator('[data-entry-edit]').first.focus()
        expect(above.locator('.entry__add-inner')).to_have_css('opacity', '1')
        expect(below.locator('.entry__add-inner')).to_have_css('opacity', '1')

    def test_moving_onto_an_add_row_shows_only_that_row(self):
        page = self._page()
        second = page.locator('.tatib__item').nth(1)
        above = page.locator('.entry__add').nth(0)
        below = page.locator('.entry__add').nth(1)
        second.hover()
        expect(below.locator('.entry__add-inner')).to_have_css('opacity', '1')
        above.hover()
        expect(above.locator('.entry__add-inner')).to_have_css('opacity', '1')
        expect(below.locator('.entry__add-inner')).to_have_css('opacity', '0')

    def test_tabbing_into_a_row_opens_it(self):
        page = self._page()
        page.mouse.move(1400, 850)
        row = page.locator('#readBody > .entry__add').first
        bar = row.locator('.entry__add-inner')
        expect(bar).to_have_css('opacity', '0')
        row.locator('[data-entry-open]').first.focus()
        expect(bar).to_have_css('opacity', '1')
        expect(bar).to_have_css('pointer-events', 'auto')

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
                if (inner.selectorText && inner.selectorText.includes('.entry__add-inner')
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
                if (inner.selectorText && inner.selectorText.includes('.entry__start-inner')
                    && inner.style.opacity === '1') return true;
              }
            }
          }
          return false;
        }""")
        self.assertTrue(applied, 'the no-hover rule for the start bar is missing')
