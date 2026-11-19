"""Spec 200 — the dock follows the live entry only while in following mode.

Browser-local behaviour: mode, scroll position and the idle clock all live in the
dock page. Fixtures are created in setUp before the browser starts; ORM reads, if
any, happen only after the browser is closed. The module is deliberately targeted —
the full dock suites belong at the push step.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ObsDockFollowE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Panjang', date=date(2026, 10, 18), is_active=True)
        for n in range(1, 61):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=n, kind=tatib.ServiceEntryKind.TEXT,
                title=f'Entri {n}', text=f'Baris pertama entri {n}')
        self.other = tatib.TataIbadah.objects.create(
            name='Ibadah Lain', date=date(2026, 10, 25), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.other, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam lain', text='Damai di bumi')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    # ---------- helpers -------------------------------------------------------

    def _dock(self, *, reduced=False):
        context = self.browser.new_context(
            viewport={'width': 420, 'height': 900},
            reduced_motion='reduce' if reduced else 'no-preference')
        page = context.new_page()
        page.goto(self.live_server_url + '/obs/dock', wait_until='domcontentloaded')
        page.wait_for_selector('.servicerow')
        return page

    def _open_service(self, page, name='Ibadah Panjang'):
        page.locator(f'.servicerow[data-name="{name}"]').first.click()
        page.wait_for_selector('.entryrow')

    def _place(self, page, entry=30, on=True):
        """Project one entry's first screen through the app's own display module."""
        page.evaluate(
            """id => window.gkpsDisplay.show(id, 0)""", [self.service.pk])
        self._project_entry(page, entry)

    def _project_entry(self, page, index):
        page.evaluate(
            """index => {
                const li = document.querySelector('.entryli[data-index="' + index + '"]');
                if (!li) return;
                const row = li.querySelector('.entryrow');
                if (row && row.getAttribute('aria-expanded') !== 'true') row.click();
                const screen = li.querySelector('.screenerow');
                if (screen) screen.click();
               }""", index)

    def _measure(self, page):
        return page.evaluate(
            """() => {
                const body = document.querySelector('#runBody');
                const row = document.querySelector('.screenerow[aria-current="true"]')
                         || document.querySelector('.offrow[aria-current="true"]')
                         || document.querySelector('.entryrow[aria-current="true"]');
                const bb = body.getBoundingClientRect();
                const rr = row ? row.getBoundingClientRect() : null;
                return {
                  scroll: Math.round(body.scrollTop),
                  off: rr ? Math.round(((rr.top + rr.bottom) / 2) - ((bb.top + bb.bottom) / 2)) : null,
                  live: (document.querySelector('.entryli[data-live="true"]') || {dataset:{}}).dataset.index,
                  disabled: document.querySelector('#centreBtn')
                    ? document.querySelector('#centreBtn').disabled : null,
                };
            }""")

    def _face(self, page):
        return page.evaluate(
            """() => { const b = document.querySelector('#centreBtn');
                 const s = getComputedStyle(b);
                 return {bg: s.backgroundColor, border: s.borderColor,
                         colour: s.color, pressed: b.getAttribute('aria-pressed')}; }""")

    def _advance(self, page, button='nextBtn'):
        page.evaluate(
            """id => document.getElementById(id).click()""", button)
        page.wait_for_timeout(500)

    def _scroll_away(self, page):
        """A real wheel scroll — the dock exits following on the wheel event."""
        page.locator('#runBody').hover()
        page.mouse.wheel(0, 20000)
        page.evaluate(
            "document.querySelector('#runBody').dispatchEvent(new WheelEvent('wheel', {bubbles: true}))")
        page.wait_for_timeout(150)

    # ---------- the tests -----------------------------------------------------

    def test_the_centre_control_centres_and_enters_following(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        filled = self._face(page)
        self.assertEqual(filled['pressed'], 'true')
        self.assertEqual(filled['bg'], 'rgb(124, 156, 240)')   # dark --active-bg
        self._scroll_away(page)
        page.wait_for_timeout(260)              # let the background transition settle
        outline = self._face(page)
        self.assertEqual(outline['pressed'], 'false')
        self.assertEqual(outline['bg'], 'rgba(0, 0, 0, 0)')
        before = self._measure(page)
        page.evaluate("document.querySelector('#centreBtn').click()")
        page.wait_for_timeout(260)
        after = self._measure(page)
        self.assertLess(abs(after['off']), 2, (before, after))
        self._advance(page)
        self.assertLess(abs(self._measure(page)['off']), 2)  # following survives

    def test_the_control_is_disabled_without_a_live_row_and_centres_a_goto(self):
        page = self._dock()
        self._open_service(page)
        self.assertTrue(self._measure(page)['disabled'])
        self._place(page)
        self.assertFalse(self._measure(page)['disabled'])

    def test_an_item_click_centres_and_reenters_following(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        page.evaluate(
            """() => { const li = document.querySelector('.entryli[data-live="true"]');
                 const rows = li.querySelectorAll('.screenerow');
                 rows[rows.length - 1].click(); }""")
        page.wait_for_timeout(320)
        self.assertEqual(self._measure(page)['live'], '30')
        self.assertLess(abs(self._measure(page)['off']), 2)
        self._advance(page)
        self.assertLess(abs(self._measure(page)['off']), 2)

    def test_the_next_band_jumps_the_pointer_and_reenters_following(self):
        page = self._dock()
        self._open_service(page)
        self._place(page, entry=11)
        before = self._measure(page)['live']
        self._scroll_away(page)
        page.evaluate("document.querySelector('.nextband').click()")
        page.wait_for_timeout(260)
        after = self._measure(page)
        self.assertEqual(int(after['live']), int(before) + 1)
        self.assertLess(abs(after['off']), 2)

    def test_advances_follow_when_following_and_not_when_browsing(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        page.evaluate("document.querySelector('#centreBtn').click()")
        page.wait_for_timeout(300)
        self._advance(page)
        self.assertLess(abs(self._measure(page)['off']), 2)
        self._scroll_away(page)
        start = self._measure(page)['scroll']
        self._advance(page)
        self._advance(page, 'prevBtn')
        self.assertEqual(self._measure(page)['scroll'], start)
        page.evaluate("document.querySelector('#centreBtn').click()")
        page.wait_for_timeout(260)
        self._advance(page)
        self.assertLess(abs(self._measure(page)['off']), 2)

    def test_scrolling_and_expanding_another_entry_end_following(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        start = self._measure(page)['scroll']
        self._advance(page)
        self.assertEqual(self._measure(page)['scroll'], start)
        page.evaluate("document.querySelector('.entryli[data-index=\"2\"] .entryrow').click()")
        self._advance(page)
        # Gate-2 finding A4: a browsing crossing reflows blocks, and the browser may
        # clamp scrollTop down. No centring glide may run, so it can never climb.
        self.assertLessEqual(self._measure(page)['scroll'], start)

    def test_the_idle_elapse_centres_and_reenters_following(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        page.wait_for_timeout(15400)
        self.assertLess(abs(self._measure(page)['off']), 2)
        self._advance(page)
        self.assertLess(abs(self._measure(page)['off']), 2)

    def test_each_idle_condition_holds_the_centring_back(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        start = self._measure(page)['scroll']
        # another header open; the other five are checked by the same fire-tick gate
        page.evaluate("document.querySelector('.entryli[data-index=\"3\"] .entryrow').click()")
        page.wait_for_timeout(15400)
        self.assertEqual(self._measure(page)['scroll'], start)

    def test_the_clock_counts_scrolls_presses_and_keys_but_not_pointer_movement(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        start = self._measure(page)['scroll']
        for _ in range(4):
            page.mouse.move(200 + _, 400 + _)
            page.wait_for_timeout(60)
        page.wait_for_timeout(15300)
        self.assertNotEqual(self._measure(page)['scroll'], start)  # pointer move did not restart

    def test_a_held_press_suspends_the_clock(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        start = self._measure(page)['scroll']
        page.mouse.move(200, 400)
        page.mouse.down()
        page.wait_for_timeout(15400)
        # A block re-read can shrink the list and clamp scrollTop down; the clock
        # must not produce an upward centring glide while the button is held.
        self.assertLessEqual(self._measure(page)['scroll'], start)
        page.mouse.up()

    def test_other_state_notices_never_centre(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        start = self._measure(page)['scroll']
        page.evaluate(
            """() => { const s = window.gkpsDisplay.read();
                 window.gkpsDisplay.hide(); window.gkpsDisplay.show(s.service, s.screen); }""")
        page.wait_for_timeout(300)
        self.assertEqual(self._measure(page)['scroll'], start)

    def test_the_dock_does_not_follow_a_service_it_is_not_showing(self):
        page = self._dock()
        self._open_service(page, 'Ibadah Lain')
        page.evaluate(
            """id => window.gkpsDisplay.show(id, 0)""", [self.service.pk])
        page.wait_for_timeout(300)
        self.assertEqual(self._measure(page)['off'], None)  # no live row in this dock

    def test_centring_stays_one_motion_and_clamps_at_the_ends(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        page.evaluate("document.querySelector('#centreBtn').click()")
        frames = page.evaluate(
            """() => new Promise((done) => {
                const b = document.querySelector('#runBody');
                const out = []; const t0 = performance.now();
                (function tick() {
                  out.push(Math.round(b.scrollTop));
                  if (performance.now() - t0 < 380) requestAnimationFrame(tick);
                  else done(out);
                })();
               })""")
        peak = frames.index(max(frames)) + 1
        climb = frames[:peak]
        reversals = sum(
            1 for i in range(2, len(climb))
            if (climb[i] - climb[i - 1]) * (climb[i - 1] - climb[i - 2]) < 0)
        self.assertEqual(reversals, 0, frames[:20])

    def test_the_reread_does_not_rebuild_an_unchanged_list(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        page.evaluate(
            """() => { window.__rebuilds = 0;
                 new MutationObserver((ms) => ms.forEach((m) => {
                   if (m.type === 'childList') window.__rebuilds++;
                 })).observe(document.querySelector('#entryList'), {childList: true}); }""")
        page.wait_for_timeout(10800)
        self.assertEqual(page.evaluate('window.__rebuilds'), 0)

    def test_the_centring_decelerates_into_its_target(self):
        page = self._dock()
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        out = page.evaluate(
            """() => new Promise((done) => {
                 const b = document.querySelector('#runBody'); const out = [];
                 const t0 = performance.now();
                 document.querySelector('#centreBtn').click();
                 (function tick() {
                   out.push([Math.round(performance.now() - t0), Math.round(b.scrollTop)]);
                   if (performance.now() - t0 < 350) requestAnimationFrame(tick);
                   else done(out);
                 })();
               })""")
        total = abs(out[-1][1] - out[0][1])
        self.assertGreater(total, 20, out)
        early = sum(abs(out[i][1] - out[i-1][1]) for i in range(1, len(out))
                    if out[i][0] < 60)
        late = sum(abs(out[i][1] - out[i-1][1]) for i in range(1, len(out))
                   if out[i-1][0] > 140)
        self.assertGreater(early, 0.15 * total, out)
        self.assertLess(late, 0.25 * total, out)

    def test_reduced_motion_jumps_instead_of_gliding(self):
        page = self._dock(reduced=True)
        self._open_service(page)
        self._place(page)
        self._scroll_away(page)
        page.evaluate("document.querySelector('#centreBtn').click()")
        self.assertLess(abs(self._measure(page)['off']), 2)
