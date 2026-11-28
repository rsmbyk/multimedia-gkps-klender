"""Spec 242 — the live entry header's off-screen top pin.

The runner's header is sticky inside its own entry li, so it is carried away once
that whole block is above the scrollport. The pin is a faithful clone in a
list-level slot at the head of the list. Each pin reads the clone's geometry, its
label, its painted corners and the live li's position, with no hand scroll after
the act being tested.

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


TOP_STATE = """() => {
  const box = document.getElementById('runBody');
  const li = document.querySelector('.entryli[data-live="true"]');
  const row = li && li.querySelector('.entryrow');
  const slot = document.querySelector('.topband-slot');
  const clone = slot && slot.querySelector('.entryrow');
  const b = box.getBoundingClientRect();
  const l = li ? li.getBoundingClientRect() : null;
  const r = row ? row.getBoundingClientRect() : null;
  const c = clone && slot && !slot.hidden ? clone.getBoundingClientRect() : null;
  const botSlot = document.querySelector('.liveband-slot');
  return {
    blockTop: l ? +(l.top - b.top).toFixed(2) : null,
    blockBottom: l ? +(l.bottom - b.top).toFixed(2) : null,
    headerTop: r ? +(r.top - b.top).toFixed(2) : null,
    headerHeight: r ? +(r.bottom - r.top).toFixed(2) : null,
    visible: !!(c),
    top: c ? +(c.top - b.top).toFixed(2) : null,
    bottom: c ? +(c.bottom - b.top).toFixed(2) : null,
    radiusTop: clone ? getComputedStyle(clone).borderTopLeftRadius : null,
    radiusBottom: clone ? getComputedStyle(clone).borderBottomLeftRadius : null,
    headerVisibility: row ? getComputedStyle(row).visibility : null,
    headerCovered: !!(row && row.classList.contains('is-covered')),
    copyExact: clone && row ? clone.textContent === row.textContent : null,
    label: clone ? clone.textContent.trim().replace(/\\s+/g, ' ') : null,
    bottomPinVisible: !!(botSlot && !botSlot.hidden),
    live: li ? li.dataset.index : null,
    scrollTop: +box.scrollTop.toFixed(1)
  };
}"""

SAMPLER = """() => {
  window.__tframes = []; window.__tstop = false;
  (function sample() {
    if (window.__tstop) return;
    const box = document.getElementById('runBody');
    const li = document.querySelector('.entryli[data-live="true"]');
    const slot = document.querySelector('.topband-slot');
    if (box && li && slot) {
      window.__tframes.push({
        bt: li.getBoundingClientRect().top - box.getBoundingClientRect().top,
        v: !slot.hidden
      });
    }
    requestAnimationFrame(function () { setTimeout(sample, 1); });
  })();
}"""

CENTRE = """() => {
  const box = document.getElementById('runBody').getBoundingClientRect();
  const row = document.querySelector('.screenerow[aria-current="true"]').getBoundingClientRect();
  return ((row.top + row.bottom) / 2) - ((box.top + box.bottom) / 2);
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockTopPinE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Haleluya', short_name='HAL', is_hymn_book=True)
        self.songs = []
        for n, title, verses in ((1, 'Sudar A', 16), (2, 'Sudar B', 14),
                                 (3, 'Sudar C', 12), (4, 'Sudar D', 12),
                                 (5, 'Sudar E', 12)):
            song = songs.Song.objects.create(book=self.book, number=n, title=title)
            for v in range(1, verses + 1):
                songs.Verse.objects.create(song=song, number=v, lyric=f'{title} line {v}')
            self.songs.append(song)
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Atas', date=date(2026, 11, 15), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita')
        for i, song in enumerate(self.songs, start=2):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=i, kind=tatib.ServiceEntryKind.SONG,
                title=f'Pujian {song.title}', song=song,
                verses=list(song.verse_set.values_list('pk', flat=True)))
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=7, kind=tatib.ServiceEntryKind.TEXT,
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
        page.locator('.servicerow[data-name="Ibadah Atas"]').first.click()
        page.wait_for_selector('#dockPanel[data-view="run"] .entryli')
        page.wait_for_timeout(300)
        return page

    def _click(self, page, selector):
        page.evaluate("sel => document.querySelector(sel).click()", selector)

    def _top(self, page):
        return page.evaluate(TOP_STATE)

    def _push_live_above(self, page):
        """Song B live, one long block opened above and three below, list at the bottom."""
        self._click(page, '.entryli[data-index="2"] .entryrow')
        page.wait_for_timeout(350)
        self._click(page, '.entryli[data-index="2"] .screenerow')
        page.wait_for_timeout(400)
        self._click(page, '.entryli[data-index="1"] .entryrow')   # open above
        page.wait_for_timeout(400)
        for index in (3, 4, 5):                                  # open below
            self._click(page, f'.entryli[data-index="{index}"] .entryrow')
            page.wait_for_timeout(400)
        page.wait_for_timeout(250)
        page.evaluate("() => { const b = document.getElementById('runBody');"
                      " b.scrollTop = b.scrollHeight; }")
        page.wait_for_timeout(350)

    def _push_live_to_edge(self, page):
        """Scroll until the live header's own top crosses the fold (block still straddles)."""
        page.evaluate("""() => {
          const box = document.getElementById('runBody');
          const li = document.querySelector('.entryli[data-live="true"]');
          box.scrollTop += li.getBoundingClientRect().top -
                           box.getBoundingClientRect().top + 2;
        }""")
        page.wait_for_timeout(250)

    # ---------- the tests -----------------------------------------------------

    def test_the_top_pin_stands_when_the_live_block_is_above(self):
        page = self._dock()
        self._click(page, '.entryli[data-index="2"] .entryrow')
        page.wait_for_timeout(350)
        self._click(page, '.entryli[data-index="2"] .screenerow')
        page.wait_for_timeout(400)
        self.assertFalse(self._top(page)['visible'], 'no pin while the header is in view')
        self._push_live_above(page)
        s = self._top(page)
        self.assertLessEqual(s['blockBottom'], 0.5, f'block above the fold: {s}')
        self.assertTrue(s['visible'], f'the top pin must stand: {s}')
        self.assertAlmostEqual(s['top'], 0, delta=1, msg=f'flush at the top edge: {s}')
        self.assertEqual(s['radiusTop'], '0px', f'flat top edge: {s}')
        self.assertEqual(s['radiusBottom'], '9px', f'round bottom corners: {s}')
        self.assertTrue(s['copyExact'], f'a faithful copy of the live header: {s}')
        self.assertLess(abs((s['bottom'] - s['top']) - s['headerHeight']), 2,
                        f'one header-height, not a second band: {s}')
        self.assertFalse(s['bottomPinVisible'], f'the two pins never compete: {s}')

    def test_the_top_pin_takes_over_when_the_header_is_clipped(self):
        page = self._dock()
        self._click(page, '.entryli[data-index="2"] .entryrow')
        page.wait_for_timeout(350)
        self._click(page, '.entryli[data-index="2"] .screenerow')
        page.wait_for_timeout(400)
        self.assertFalse(self._top(page)['visible'], 'no pin while the header is in view')
        self._push_live_to_edge(page)
        s = self._top(page)
        self.assertLessEqual(s['blockTop'], 0.5, f'header has reached the fold: {s}')
        self.assertGreater(s['blockBottom'], 0.5, f'the block still straddles the fold: {s}')
        self.assertTrue(s['visible'], f'the pin must take over at the header edge: {s}')
        self.assertAlmostEqual(s['top'], 0, delta=1, msg=f'flush at the edge: {s}')
        self.assertAlmostEqual(s['headerTop'], 0, delta=1, msg=f'no takeover hop: {s}')
        self.assertEqual(s['radiusTop'], '0px', f'flat top edge: {s}')
        self.assertEqual(s['radiusBottom'], '9px', f'round bottom corners: {s}')
        self.assertTrue(s['copyExact'], f'a faithful copy of the live header: {s}')
        self.assertLess(abs((s['bottom'] - s['top']) - s['headerHeight']), 2,
                        f'one header-height, not a second band: {s}')
        self.assertFalse(s['bottomPinVisible'], f'the two pins never compete: {s}')

    def test_only_one_header_is_painted_while_the_pin_owns_the_edge(self):
        page = self._dock()
        self._click(page, '.entryli[data-index="2"] .entryrow')
        page.wait_for_timeout(350)
        self._click(page, '.entryli[data-index="2"] .screenerow')
        page.wait_for_timeout(400)
        self._push_live_to_edge(page)
        s = self._top(page)
        self.assertTrue(s['visible'])
        self.assertEqual(s['headerVisibility'], 'hidden', f'one painted header: {s}')
        self.assertTrue(s['headerCovered'], f'the source is covered: {s}')
        self.assertLess(abs(s['top'] - s['headerTop']), 0.6,
                        f'clone covers the sticky header without a hop: {s}')
        page.evaluate("() => { document.getElementById('runBody').scrollTop -= 12; }")
        page.wait_for_timeout(250)
        back = self._top(page)
        self.assertGreater(back['blockTop'], 0.5, f'block back in view: {back}')
        self.assertFalse(back['visible'], f'pin yielded: {back}')
        self.assertEqual(back['headerVisibility'], 'visible', f'header restored: {back}')
        self.assertFalse(back['headerCovered'], f'cover cleared: {back}')
        page.evaluate("() => { const b = document.getElementById('runBody');"
                      " b.scrollTop = b.scrollHeight; }")
        page.wait_for_timeout(250)
        s2 = self._top(page)
        self.assertTrue(s2['visible'], f'pin still holds once fully above: {s2}')
        self.assertEqual(s2['headerVisibility'], 'hidden', f'still one painted header: {s2}')

    def test_the_top_pin_tracks_the_block_per_frame(self):
        page = self._dock()
        self._push_live_above(page)
        self.assertTrue(self._top(page)['visible'])
        page.evaluate(SAMPLER)
        page.evaluate("document.querySelector('.topband-slot').click()")
        page.wait_for_timeout(800)
        page.evaluate('window.__tstop = true')
        frames = page.evaluate('window.__tframes')
        self.assertTrue(any(f['v'] for f in frames), 'the glide starts with the pin up')
        self.assertTrue(any(not f['v'] for f in frames), 'the glide ends with the pin gone')
        bad = [f for f in frames if f['v'] != (f['bt'] <= 0.5)]
        self.assertFalse(bad, f'visibility must equal geometry every frame: {bad[:5]}')

    def test_the_real_header_takes_over_when_the_block_returns(self):
        page = self._dock()
        self._push_live_above(page)
        self.assertTrue(self._top(page)['visible'])
        page.evaluate("document.getElementById('runBody').scrollTop = 0")
        page.wait_for_timeout(250)
        s = self._top(page)
        self.assertFalse(s['visible'], f'pin gone once the block is back in view: {s}')
        self.assertGreater(s['headerTop'], 0.5, f'native header in flow: {s}')

    def test_clicking_the_top_pin_performs_the_centre_act(self):
        page = self._dock()
        self._push_live_above(page)
        before = page.evaluate("() => localStorage.getItem('gkps-display')")
        page.evaluate("document.querySelector('.topband-slot').click()")
        page.wait_for_timeout(800)
        after = page.evaluate("() => localStorage.getItem('gkps-display')")
        self.assertEqual(after, before, 'the pin click must not change what is on air')
        off = page.evaluate(CENTRE)
        self.assertLessEqual(abs(off), 2, f'the live row glides back to centre: {off}')
        self.assertEqual(
            page.evaluate("document.getElementById('centreBtn').getAttribute('aria-pressed')"),
            'true', 'following returns')
        self.assertFalse(self._top(page)['visible'], 'the header is back in view')

    def test_the_top_pin_lands_instantly_under_reduced_motion(self):
        page = self._dock(reduced_motion='reduce')
        self._push_live_above(page)
        page.wait_for_timeout(100)
        s = self._top(page)
        self.assertTrue(s['visible'], f'the pin paints in the same paint: {s}')
        self.assertEqual(s['radiusTop'], '0px')
        self.assertEqual(s['radiusBottom'], '9px')
        self.assertTrue(s['copyExact'])
