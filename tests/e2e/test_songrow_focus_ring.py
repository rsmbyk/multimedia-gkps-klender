"""The first song row's focus ring must fit inside the list scrollport (spec 223).

The ring is the browser's UA outline, painted 1px outside a row that used to sit flush with
#chBody. These cases assert the relationship between the painted ring and the scrollport rather
than a hardcoded y coordinate, plus the row states that must not change.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const row = document.querySelector('#chList li > .songrow');
  const host = document.querySelector('#chBody');
  const current = document.querySelector('#chList li > .songrow[aria-current="true"]');
  if (!row || !host) return null;
  const cs = getComputedStyle(row);
  const r = row.getBoundingClientRect(), h = host.getBoundingClientRect();
  const css = getComputedStyle(current || row);
  return {
    gap: r.top - h.top,
    scrollTop: host.scrollTop,
    scrollHeight: host.scrollHeight,
    clientHeight: host.clientHeight,
    height: r.height,
    outlineStyle: cs.outlineStyle,
    outlineWidth: parseFloat(cs.outlineWidth) || 0,
    outlineOffset: parseFloat(cs.outlineOffset) || 0,
    focusVisible: row.matches(':focus-visible'),
    activeOnRow: document.activeElement === row,
    rowCount: document.querySelectorAll('#chList li > .songrow').length,
    currentTitle: current ? current.textContent.trim() : null,
    currentBackground: css.backgroundColor,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongRowFocusRingE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Buku Ende Ring', short_name='', is_hymn_book=False)
        for number in range(1, 9):
            songs.Song.objects.create(book=self.book, number=number, title='Lagu %02d' % number)
        self.song = songs.Song.objects.get(book=self.book, number=3)
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _page(self):
        page = self.browser.new_page(
            viewport={'width': 900, 'height': 700}, color_scheme='dark', device_scale_factor=1)
        page.goto(self.live_server_url + reverse('web-song', args=[self.song.pk]))
        page.wait_for_selector('#chList li > .songrow')
        return page

    @staticmethod
    def _assert_ring_fits(state):
        needed = state['outlineWidth'] + state['outlineOffset']
        assert state['focusVisible'], 'the first row never became :focus-visible'
        assert state['outlineStyle'] != 'none', 'no focus ring was painted'
        assert state['gap'] >= needed, (
            f"the ring needs {needed}px above the row, but only {state['gap']}px is available")

    def test_the_first_rows_ring_fits_inside_the_scrollport(self):
        page = self._page()
        before = page.evaluate(MEASURE)
        self.assertEqual(before['scrollTop'], 0)
        self.assertEqual(before['scrollHeight'], before['clientHeight'])
        page.locator('#chList li > .songrow').first.click()
        page.keyboard.press('a')                     # promotes the held pointer focus
        state = page.evaluate(MEASURE)
        self._assert_ring_fits(state)
        page.close()

    def test_a_tabbed_first_row_gets_the_same_complete_ring(self):
        page = self._page()
        reached = False
        for _ in range(60):
            page.keyboard.press('Tab')
            if page.evaluate("() => document.activeElement.classList.contains('songrow')"):
                reached = True
                break
        self.assertTrue(reached, 'Tab never reached a song row')
        state = page.evaluate(MEASURE)
        self.assertTrue(state['activeOnRow'])
        self._assert_ring_fits(state)
        page.close()

    def test_focus_does_not_change_the_row_box_or_its_states(self):
        page = self._page()
        before = page.evaluate(MEASURE)
        self.assertEqual(before['outlineStyle'], 'none')
        page.locator('#chList li > .songrow').first.click()
        page.keyboard.press('a')
        after = page.evaluate(MEASURE)
        self.assertEqual(after['height'], before['height'])
        self.assertEqual(after['rowCount'], before['rowCount'])
        self.assertEqual(after['currentTitle'], before['currentTitle'])
        self.assertEqual(after['currentBackground'], before['currentBackground'])
        page.close()
