"""Spec 197 — the dock picker's bucket head owns the strip above its label.

The defect: the head's `top: 0` resolved inside the scroll body's own 4px top
padding, so the head pinned 4px below the scroller's edge and the row above kept
painting in that strip. The fix moves the strip into the head's own padding, so
the label sits at one height whether the head is at rest or pinned, and the air
between two buckets rides the section instead of the head.

Every assertion here is geometry read from the live page: the numbers are the
spec's (`specs/197-dock-bucket-head-pin/spec.md`), not the stylesheet's.
"""

import unittest
from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.tatib import models as tatib
from multimedia.web.reading.date_buckets import present_day

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


# The picker's scroller, its bucket heads and the rows under them, as boxes.
GEOMETRY = """() => {
  const body = document.getElementById('pickBody');
  const b = body.getBoundingClientRect();
  const heads = [...body.querySelectorAll('.group__head')];
  const box = (el) => { const r = el.getBoundingClientRect();
    return {top: r.top, bottom: r.bottom, height: r.height}; };
  const label = (head) => {
    const range = document.createRange();
    range.selectNodeContents(head);
    return range.getBoundingClientRect().top;
  };
  const sections = [...body.querySelectorAll('section')];
  return {
    scroller: {top: b.top, left: b.left, bottom: b.bottom},
    scrollTop: body.scrollTop,
    groups: sections.length,
    heads: heads.map(h => ({box: box(h), labelTop: label(h)})),
    firstRow: box(body.querySelector('.servicerow')),
    // the air between two buckets: the next label against the previous group's last row
    boundaryAir: sections.slice(1).map(s => {
      const prev = sections[sections.indexOf(s) - 1];
      const rows = prev.querySelectorAll('.servicerow');
      const last = rows[rows.length - 1].getBoundingClientRect();
      return label(s.querySelector('.group__head')) - last.bottom;
    }),
    paintedAtTop: (() => {
      const el = document.elementFromPoint(Math.max(1, b.left + 20), b.top + 2);
      return el ? el.tagName + ' ' + String(el.className) : null;
    })(),
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockBucketHeadE2ETests(StaticLiveServerTestCase):
    """Three services in three age buckets, so the picker draws two boundaries."""

    def setUp(self):
        super().setUp()
        today = present_day()
        for offset, name in ((0, 'Ibadah Hari Ini'), (-5, 'Ibadah Minggu'),
                             (-60, 'Ibadah Lama')):
            service = tatib.TataIbadah.objects.create(
                name=name, date=today + timedelta(days=offset), is_active=True)
            tatib.ServiceEntry.objects.create(
                tatib=service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
                title='Salam', text='Kasih karunia Tuhan beserta kita semua')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self._close_browser()
        super().tearDown()

    def _close_browser(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    # ---------- helpers -------------------------------------------------------

    def _open_dock(self):
        context = self.browser.new_context(viewport={'width': 449, 'height': 604})
        page = context.new_page()
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector('#pickBody .servicerow')
        self.assertGreaterEqual(page.eval_on_selector_all(
            '#pickBody section', 'nodes => nodes.length'), 2,
            'the fixtures must fill two buckets for a boundary to exist')
        return context, page

    def _at(self, page, scroll):
        page.evaluate('(s) => { document.getElementById("pickBody").scrollTop = s; }', scroll)
        page.wait_for_timeout(80)
        return page.evaluate(GEOMETRY)

    def _pinned_offset(self, page):
        """A scroll offset deep enough that the first head is pinned."""
        first_head_bottom = self._at(page, 0)['heads'][0]['box']['bottom']
        scroller_top = self._at(page, 0)['scroller']['top']
        return round(first_head_bottom - scroller_top) + 40

    # ---------- US1 -----------------------------------------------------------

    def test_a_pinned_bucket_head_leaves_no_row_above_it(self):
        context, page = self._open_dock()
        try:
            scroll = self._pinned_offset(page)
            at = self._at(page, scroll)
            head = at['heads'][0]['box']

            self.assertAlmostEqual(
                head['top'], at['scroller']['top'], delta=0.6,
                msg=f"the head starts {head['top'] - at['scroller']['top']:.2f}px below the scroller's top")
            self.assertIn('group__head', at['paintedAtTop'],
                          f"the strip above the label paints {at['paintedAtTop']!r}, not the head")
        finally:
            context.close()

    def test_the_label_holds_its_place_between_rest_and_pinned(self):
        context, page = self._open_dock()
        try:
            rest = self._at(page, 0)
            scroll = self._pinned_offset(page)
            pinned = self._at(page, scroll)

            rest_label = rest['heads'][0]['labelTop'] - rest['scroller']['top']
            pinned_label = pinned['heads'][0]['labelTop'] - pinned['scroller']['top']

            self.assertGreater(rest_label, 0, 'the label must sit below the divider')
            self.assertAlmostEqual(
                pinned_label, rest_label, delta=0.6,
                msg=f'the label moves {pinned_label - rest_label:.2f}px when the head pins')
        finally:
            context.close()

    def test_nothing_below_the_head_moves(self):
        context, page = self._open_dock()
        try:
            rest = self._at(page, 0)
            head = rest['heads'][0]['box']
            row = rest['firstRow']

            self.assertAlmostEqual(
                row['top'], head['bottom'], delta=0.6,
                msg='the first row must start at the head\'s foot at rest')

            scroll = self._pinned_offset(page)
            pinned = self._at(page, scroll)
            self.assertAlmostEqual(
                pinned['heads'][0]['box']['height'], head['height'], delta=0.6,
                msg='the head\'s height must not change when it pins')
            self.assertAlmostEqual(
                pinned['firstRow']['top'], pinned['heads'][0]['box']['bottom'], delta=0.6,
                msg='the row under a pinned head must still start at its foot')
        finally:
            context.close()

    # ---------- US2 -----------------------------------------------------------

    def test_the_cursor_still_parks_below_the_head(self):
        context, page = self._open_dock()
        try:
            page.evaluate('() => document.getElementById("dockPanel").focus()')
            page.keyboard.press('ArrowDown')
            page.wait_for_timeout(60)
            for _ in range(6):
                page.keyboard.press('ArrowDown')
                page.wait_for_timeout(30)

            clearances = []
            for _ in range(12):
                page.keyboard.press('ArrowUp')
                page.wait_for_timeout(40)
                parked = page.evaluate("""() => {
                  const body = document.getElementById('pickBody');
                  const b = body.getBoundingClientRect();
                  const cursor = document.querySelector('.servicerow.is-cursor');
                  if (!cursor) return null;
                  const pinned = [...body.querySelectorAll('.group__head')]
                    .map(h => h.getBoundingClientRect())
                    .filter(r => r.top <= b.top + 6 && r.bottom > b.top + 1);
                  if (!pinned.length) return null;
                  const foot = Math.max(...pinned.map(r => r.bottom));
                  return cursor.getBoundingClientRect().top - foot;
                }""")
                if parked is not None:
                    clearances.append(parked)

            self.assertTrue(clearances, 'the cursor never crossed a pinned head')
            self.assertGreaterEqual(
                min(clearances), -0.6,
                msg=f'a cursor row parks {-min(clearances):.2f}px under the pinned head')
        finally:
            context.close()

    # ---------- US3 -----------------------------------------------------------

    def test_consecutive_buckets_keep_their_air(self):
        context, page = self._open_dock()
        try:
            at = self._at(page, 0)
            first_label = at['heads'][0]['labelTop'] - at['scroller']['top']

            self.assertTrue(at['boundaryAir'], 'no bucket boundary to measure')
            for air in at['boundaryAir']:
                self.assertAlmostEqual(
                    air, first_label + 12, delta=0.6,
                    msg=f'the air above a bucket label is {air:.2f}px, '
                        f'expected {first_label + 12:.2f}px')
        finally:
            context.close()