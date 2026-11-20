"""Spec 208 — the live entry header's corners follow its pin state.

The flat top is the `.is-stuck` class on the live `.entryrow`. On develop the
toggle sits inside `updateBand()` behind the NEXT band's motion guard, so a
glide or crossing lands the header pinned with round corners, or in flow with
square ones, until a hand scroll reconciles it. These pins read the geometry
(offset from the scrollport top), the class and the painted radius together,
at rest and per-frame, without a hand scroll after the act being tested.

Clicks that must not pre-scroll the list go through `evaluate` — Playwright's
own click scrolls an off-view target into view first, and that scroll event
reconciles the class on develop, masking the bug. Keyboard acts are the real
operator path and never pre-scroll.

Same runner rules as the other e2e suites: fixtures in setUp, the browser is
closed before any ORM assertion, and Playwright's loop never overlaps Django's
database access.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


GEOM = """(index) => {
    const box = document.getElementById('runBody');
    const li = index == null
        ? document.querySelector('.entryli[data-live="true"]')
        : document.querySelector('.entryli[data-index="' + index + '"]');
    if (!box || !li) return null;
    const row = li.querySelector('.entryrow');
    const b = box.getBoundingClientRect(), r = row.getBoundingClientRect();
    const l = li.getBoundingClientRect();
    return {delta: r.top - b.top, liBottom: l.bottom - b.top,
            stuck: row.classList.contains('is-stuck'),
            radius: getComputedStyle(row).borderTopLeftRadius,
            live: li.dataset.live, scrollTop: box.scrollTop};
}"""

SAMPLER = """() => {
    window.__frames = []; window.__stop = false;
    (function sample() {
        if (window.__stop) return;
        const box = document.getElementById('runBody');
        const li = document.querySelector('.entryli[data-live="true"]');
        if (box && li) {
            const row = li.querySelector('.entryrow');
            const b = box.getBoundingClientRect(), r = row.getBoundingClientRect();
            const l = li.getBoundingClientRect();
            window.__frames.push({d: r.top - b.top, lb: l.bottom - b.top,
                                  c: row.classList.contains('is-stuck')});
        }
        requestAnimationFrame(sample);
    })();
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockStuckCornerE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Haleluya', short_name='HAL', is_hymn_book=True)
        # Two long songs: A (16 verses) stands above B (14 verses) so opening A's
        # block by hand pushes B's pinned header far below the pin line, and B's
        # own block is tall enough that centring a deep screen pins its header.
        self.song_a = songs.Song.objects.create(book=self.book, number=1, title='Sudar A')
        self.song_b = songs.Song.objects.create(book=self.book, number=2, title='Sudar B')
        for n in range(1, 17):
            songs.Verse.objects.create(song=self.song_a, number=n, lyric=f'A line {n}')
        for n in range(1, 15):
            songs.Verse.objects.create(song=self.song_b, number=n, lyric=f'B line {n}')
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Sudut', date=date(2026, 11, 8), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.SONG,
            title='Pujian A', song=self.song_a,
            verses=list(self.song_a.verse_set.values_list('pk', flat=True)))
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.SONG,
            title='Pujian B', song=self.song_b,
            verses=list(self.song_b.verse_set.values_list('pk', flat=True)))
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=4, kind=tatib.ServiceEntryKind.TEXT,
            title='Doa', text='Tuhan, dengarkanlah doa kami')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None
        super().tearDown()

    # ---------- helpers -------------------------------------------------------

    def _dock(self, reduced_motion='no-preference'):
        context = self.browser.new_context(
            viewport={'width': 420, 'height': 860}, color_scheme='dark',
            device_scale_factor=1, reduced_motion=reduced_motion)
        page = context.new_page()
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector('#pickBody .servicerow')
        page.locator('.servicerow[data-name="Ibadah Sudut"]').first.click()
        page.wait_for_selector('#dockPanel[data-view="run"] .entryli')
        page.wait_for_timeout(300)
        return page

    def _click(self, page, selector):
        """A real click through the delegated handler, with no auto-scroll."""
        page.evaluate("sel => document.querySelector(sel).click()", selector)

    def _geom(self, page, index=None):
        return page.evaluate(GEOM, index)

    def _focus_panel(self, page):
        page.evaluate("document.getElementById('dockPanel').focus()")

    def _live_first(self, page, index):
        """Open the block by hand, then project its first screen row."""
        self._click(page, f'.entryli[data-index="{index}"] .entryrow')
        page.wait_for_timeout(350)
        self._click(page, f'.entryli[data-index="{index}"] .screenerow')
        page.wait_for_timeout(400)
        self._focus_panel(page)

    def _deep(self, page):
        """Shift+End: the last bait's last screen — one glide deep into the song."""
        page.keyboard.press('Shift+End')
        page.wait_for_timeout(700)   # 200 ms glide + 300 ms band hold + margin

    def _hand_scroll(self, page, px=24):
        # Scroll UP: the fixture's list clamps at the bottom (the live song is
        # near the list's end), so a downward nudge can be a no-op that fires no
        # scroll event. Upward always moves while pinned deep, and keeps the
        # header pinned (its natural position is far above the edge).
        before = page.evaluate("document.getElementById('runBody').scrollTop")
        page.evaluate("px => document.getElementById('runBody').scrollTop -= px", px)
        page.wait_for_timeout(150)
        after = page.evaluate("document.getElementById('runBody').scrollTop")
        self.assertNotEqual(before, after, 'the establishing scroll must actually move')

    def _assert_pinned_flat(self, g):
        self.assertLessEqual(g['delta'], 0.5, f'header should be pinned: {g}')
        self.assertGreater(g['liBottom'], 0.5, f'block should reach below the edge: {g}')
        self.assertTrue(g['stuck'], f'pinned header must wear .is-stuck: {g}')
        self.assertEqual(g['radius'], '0px', f'pinned header must paint a flat top: {g}')

    def _assert_inflow_round(self, g):
        self.assertGreater(g['delta'], 0.5, f'header should be in flow: {g}')
        self.assertFalse(g['stuck'], f'in-flow header must not wear .is-stuck: {g}')
        self.assertEqual(g['radius'], '9px', f'in-flow header must paint round corners: {g}')

    # ---------- the tests -----------------------------------------------------

    def test_a_pinned_header_wears_a_flat_top_after_advancing(self):
        page = self._dock()
        self._live_first(page, 2)
        self._assert_inflow_round(self._geom(page))   # first screen: header in flow
        self._deep(page)                              # last screen: header pins, list rests
        self._assert_pinned_flat(self._geom(page))

    def test_an_in_flow_header_keeps_round_corners_after_a_crossing(self):
        page = self._dock()
        self._live_first(page, 2)
        self._deep(page)
        self._hand_scroll(page)                       # establish the stuck state
        self.assertTrue(self._geom(page)['stuck'])
        page.keyboard.press('Control+Home')           # cross to the first entry
        page.wait_for_timeout(700)
        g = self._geom(page)
        self.assertEqual(g['live'], 'true')
        self._assert_inflow_round(g)

    def test_a_hand_toggle_above_the_live_header_reconciles_the_corners(self):
        page = self._dock()
        self._live_first(page, 2)
        self._deep(page)
        self._hand_scroll(page)
        self.assertTrue(self._geom(page)['stuck'])
        page.evaluate("window.__sc = 0; document.getElementById('runBody')"
                      ".addEventListener('scroll', () => window.__sc++)")
        # Open the closed block ABOVE the live entry: its height pushes the live
        # header below the pin line. No scroll, no glide — the height change alone.
        self._click(page, '.entryli[data-index="1"] .entryrow')
        page.wait_for_timeout(450)                    # 230 ms toggle morph + margin
        self.assertEqual(page.evaluate('window.__sc'), 0,
                         'the toggle must not need a scroll event to reconcile')
        self._assert_inflow_round(self._geom(page, 2))

    def test_the_corners_track_the_pin_line_during_a_glide(self):
        page = self._dock()
        self._live_first(page, 2)
        page.evaluate(SAMPLER)
        self._deep(page)
        page.evaluate('window.__stop = true')
        frames = page.evaluate('window.__frames')
        pinned = [f for f in frames if f['d'] <= 0.5 and f['lb'] > 0.5]
        self.assertTrue(pinned, 'the glide must cross the pin line')
        bad = [f for f in frames
               if f['c'] != (f['d'] <= 0.5 and f['lb'] > 0.5)]
        self.assertFalse(bad, f'class must equal geometry on every frame: {bad[:5]}')

    def test_only_the_live_header_wears_the_stuck_state(self):
        page = self._dock()
        self._live_first(page, 2)
        self._deep(page)
        self._hand_scroll(page)
        self.assertTrue(self._geom(page, 2)['stuck'])
        page.keyboard.press('Control+Home')
        page.wait_for_timeout(60)                     # sync painted; morph in flight
        self.assertFalse(self._geom(page, 2)['stuck'],
                         'the old live row must lose .is-stuck on the crossing paint')

    def test_the_flat_top_lands_instantly_under_reduced_motion(self):
        page = self._dock(reduced_motion='reduce')
        self._live_first(page, 1)                     # song A live, near the top
        self._click(page, '.entryli[data-index="2"] .entryrow')   # open B, instant
        page.wait_for_timeout(100)
        # Project B's LAST screen row: a crossing under reduced motion lands
        # instantly and pins B's header — the flat top must be in that same paint.
        self._click(page, '.entryli[data-index="2"] .screenerow:last-child')
        page.wait_for_timeout(150)
        self._assert_pinned_flat(self._geom(page))

    # ---------- US4: the live label pins to the bottom (spec 208, folded) ------

    BOTTOM_STATE = """() => {
        const box = document.getElementById('runBody');
        const li = document.querySelector('.entryli[data-live="true"]');
        const row = li && li.querySelector('.entryrow');
        const slot = document.querySelector('.liveband-slot');
        const clone = slot && slot.querySelector('.entryrow');
        const band = document.querySelector('.nextband');
        const b = box.getBoundingClientRect();
        const s = clone && slot && !slot.hidden ? clone.getBoundingClientRect() : null;
        const n = band && !band.hidden ? band.getBoundingClientRect() : null;
        const r = row ? row.getBoundingClientRect() : null;
        return {
            stripVisible: !!s,
            stripBottom: s ? +(s.bottom - b.bottom).toFixed(2) : null,
            stripTop: s ? +(s.top - b.top).toFixed(2) : null,
            stripRadius: clone ? getComputedStyle(clone).borderBottomLeftRadius : null,
            stripTopRadius: clone ? getComputedStyle(clone).borderTopLeftRadius : null,
            copyExact: clone && row ? clone.textContent === row.textContent : null,
            stripText: clone ? clone.textContent.trim() : null,
            bandVisible: !!n,
            bandTop: n ? +(n.top - b.bottom).toFixed(2) : null,
            bandBottom: n ? +(n.bottom - b.bottom).toFixed(2) : null,
            headerTop: r ? +(r.top - b.top).toFixed(2) : null,
            headerBottom: r ? +(r.bottom - b.top).toFixed(2) : null,
            viewportH: b.height, scrollTop: box.scrollTop
        };
    }"""

    BOTTOM_SAMPLER = """() => {
        window.__bframes = []; window.__bstop = false;
        (function sample() {
            if (window.__bstop) return;
            const box = document.getElementById('runBody');
            const li = document.querySelector('.entryli[data-live="true"]');
            const slot = document.querySelector('.liveband-slot');
            if (box && li && slot) {
                const r = li.querySelector('.entryrow').getBoundingClientRect();
                const b = box.getBoundingClientRect();
                const band = document.querySelector('.nextband');
                const clip = band && !band.hidden ? band.getBoundingClientRect().top : b.bottom;
                window.__bframes.push({over: r.bottom - clip, v: !slot.hidden});
            }
            requestAnimationFrame(sample);
        })();
    }"""

    def _bottom(self, page):
        return page.evaluate(self.BOTTOM_STATE)

    def _push_live_below(self, page):
        """Song B live at its first screen, then song A's block opened by hand
        above it — B's header lands far below the bottom edge."""
        self._live_first(page, 2)
        self._click(page, '.entryli[data-index="1"] .entryrow')
        page.wait_for_timeout(450)

    def test_the_bottom_pin_is_the_header_pinned_when_fully_off(self):
        page = self._dock()
        self._push_live_below(page)
        s = self._bottom(page)
        # fully off below: the header's own face pins at the edge, flat bottom
        self.assertGreater(s['headerTop'], s['viewportH'], f'header fully off below: {s}')
        self.assertTrue(s['stripVisible'], f'the bottom pin must stand: {s}')
        self.assertTrue(s['bandVisible'], f'the NEXT band is always shown: {s}')
        self.assertAlmostEqual(s['stripBottom'], s['bandTop'], delta=1,
                               msg=f'the pin abuts directly above NEXT: {s}')
        self.assertEqual(s['stripRadius'], '0px', f'flat bottom corners: {s}')
        self.assertEqual(s['stripTopRadius'], '9px',
                         f'round top corners, mirroring the top pin: {s}')
        self.assertTrue(s['copyExact'], f'a faithful copy of the header, not a caption band: {s}')
        self.assertNotIn('LIVE', (s['stripText'] or '').upper(), f'no LIVE caption: {s}')

    def test_the_bottom_pin_starts_as_soon_as_the_header_goes_off(self):
        # Clip exactly when the header's bottom touches the NEXT band's top — not
        # a row early (that read as too tall). At that point the clone covers the
        # real header exactly, so it takes over with no added height (no doubling).
        page = self._dock()
        self._push_live_below(page)
        s = self._bottom(page)
        header_h = s['headerBottom'] - s['headerTop']
        clip_in_view = s['viewportH'] + s['bandTop']  # band's top, in header coords
        # scroll so the header's bottom is ~8px past the band's top (just touching)
        page.evaluate(
            """s => document.getElementById('runBody').scrollTop += s""",
            s['headerBottom'] - (clip_in_view + 8))
        page.wait_for_timeout(200)
        s = self._bottom(page)
        self.assertGreater(s['headerBottom'], clip_in_view,
                           f'header bottom touching the band: {s}')
        self.assertLess(s['headerBottom'], clip_in_view + header_h,
                        f'header still largely visible, not staged a row early: {s}')
        self.assertTrue(s['stripVisible'], f'the pin clips at the band: {s}')
        self.assertAlmostEqual(s['stripBottom'], s['bandTop'], delta=1,
                               msg=f'the pin abuts directly above NEXT: {s}')
        self.assertTrue(s['copyExact'], f'a faithful copy of the header: {s}')

    def test_the_bottom_pin_tracks_the_header_visibility_per_frame(self):
        page = self._dock()
        self._push_live_below(page)
        self.assertTrue(self._bottom(page)['stripVisible'])
        page.evaluate(self.BOTTOM_SAMPLER)
        page.evaluate("document.querySelector('.liveband-slot').click()")   # the glide home
        page.wait_for_timeout(700)
        page.evaluate('window.__bstop = true')
        frames = page.evaluate('window.__bframes')
        self.assertTrue(any(f['v'] for f in frames), 'the glide starts with the pin up')
        self.assertTrue(any(not f['v'] for f in frames), 'the glide ends with the pin gone')
        bad = [f for f in frames if f['v'] != (f['over'] > -0.5)]
        self.assertFalse(bad, f'pin visibility must equal geometry every frame: {bad[:5]}')

    def test_clicking_the_bottom_pin_performs_the_ruled_act(self):
        page = self._dock()
        self._push_live_below(page)
        before = page.evaluate("() => localStorage.getItem('gkps-display')")
        page.evaluate("document.querySelector('.liveband-slot').click()")
        page.wait_for_timeout(700)
        after = page.evaluate("() => localStorage.getItem('gkps-display')")
        self.assertEqual(after, before, 'the pin click must not change what is on air')
        off = page.evaluate(
            """() => { const box = document.getElementById('runBody');
                 const row = document.querySelector('.screenerow[aria-current="true"]');
                 const b = box.getBoundingClientRect(), r = row.getBoundingClientRect();
                 return ((r.top + r.bottom) / 2) - ((b.top + b.bottom) / 2); }""")
        self.assertLessEqual(abs(off), 2, f'the live row glides back to the centre: {off}')
        self.assertEqual(
            page.evaluate("document.getElementById('centreBtn').getAttribute('aria-pressed')"),
            'true', 'following returns')
        self.assertFalse(self._bottom(page)['stripVisible'], 'the header is back in view')

    def test_the_bottom_pin_lands_instantly_under_reduced_motion(self):
        page = self._dock(reduced_motion='reduce')
        self._push_live_below(page)
        page.wait_for_timeout(100)
        s = self._bottom(page)
        self.assertTrue(s['stripVisible'], f'the pin paints instantly: {s}')
        self.assertEqual(s['stripRadius'], '0px')
        self.assertTrue(s['bandVisible'], f'NEXT is also sticky: {s}')
        self.assertAlmostEqual(s['stripBottom'], s['bandTop'], delta=1,
                               msg=f'pin abuts above NEXT: {s}')

    def test_the_next_band_is_always_visible_even_when_the_list_fits(self):
        # The NEXT band is shown whenever a next entry exists, regardless of
        # whether that row is on screen — and the list fills the scrollport so the
        # band pins at the bottom edge even when all entries fit.
        page = self._dock()
        self._push_live_below(page)
        page.set_viewport_size({'width': 1920, 'height': 1200})
        page.wait_for_timeout(300)
        page.evaluate("document.getElementById('runBody').scrollTop = "
                      "document.getElementById('runBody').scrollHeight")
        page.wait_for_timeout(250)
        s = self._bottom(page)
        self.assertTrue(s['bandVisible'], f'NEXT always visible: {s}')
        self.assertAlmostEqual(s['bandBottom'], 0, delta=2,
                               msg=f'NEXT pinned at the edge even when the list fits: {s}')
