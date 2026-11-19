"""The song caption's type scale is bounded by the stage height (spec 202).

The rest size is 5 % of the stage height. A lyric whose lines wrap shrinks the
type until the block fits two visual rows, but never past 2 % of that height.
At the floor the block may exceed two rows — the accepted edge, not a failure.
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


MEASURE = """() => {
  const node = document.querySelector('.obs-overlay__caption');
  if (!node) return null;
  /* Count ink rows from each line's text, not from a range over the whole caption:
     the caption's spans are blocks, and their boxes add rects that are not rows. */
  const tops = [];
  node.querySelectorAll('span').forEach(span => {
    const range = document.createRange();
    range.selectNodeContents(span);
    [...range.getClientRects()].forEach(rect => tops.push(Math.round(rect.top)));
  });
  return {
    font: parseFloat(getComputedStyle(node).fontSize),
    rows: new Set(tops).size,
    height: node.getBoundingClientRect().height,
    stageHeight: document.getElementById('overlayStage').clientHeight
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ObsCaptionHeightE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 11, 19), is_active=True)
        book = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        song = songs.Song.objects.create(book=book, number=152, title='Ada Kuasa')
        lyrics = (
            'Kasih setia Tuhan\nBait satu baris yang kedua',
            'Kasih setia Tuhan ' + 'mmmm' * 12 + ' sampai selamanya',
            'mmmm' * 400,
        )
        for index, lyric in enumerate(lyrics, 1):
            verse = songs.Verse.objects.create(song=song, number=index, lyric=lyric)
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=index,
                kind=tatib.ServiceEntryKind.SONG, song=song, verses=[verse.pk])

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

    def _project(self, context, entry_index):
        dock = context.new_page()
        dock.goto(self.live_server_url + '/obs/dock')
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        dock.locator('.entryrow').nth(entry_index).click()
        dock.locator(f'.entryli[data-index="{entry_index}"] .screenerow').first.click()
        dock.wait_for_function(
            "service => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s && s.service === service && s.on === true; }", arg=self.service.pk)
        return dock

    def _measure(self, context, entry_index):
        self._project(context, entry_index)
        overlay = context.new_page()
        overlay.goto(self.live_server_url + '/obs/source/overlay')
        overlay.wait_for_selector('.obs-overlay__caption')
        overlay.wait_for_function(
            """sel => { const el = document.querySelector(sel);
                 if (!el) return false;
                 const t = getComputedStyle(el).transform;
                 return t === 'none' || t === 'matrix(1, 0, 0, 1, 0, 0)'; }""",
            arg='.obs-overlay__caption')
        overlay.evaluate("() => document.fonts.ready")
        overlay.wait_for_timeout(250)
        measured = overlay.evaluate(MEASURE)
        context.close()
        return measured

    def test_the_rest_is_five_percent_of_the_stage_height(self):
        for width, height in ((1920, 1080), (1280, 720)):
            with self.subTest(frame=f'{width}x{height}'):
                context = self.browser.new_context(
                    viewport={'width': width, 'height': height})
                measured = self._measure(context, 0)
                self.assertAlmostEqual(measured['font'], height * 0.05, delta=0.5,
                                       msg=f"rest at {width}x{height}: {measured}")
                self.assertLessEqual(measured['rows'], 2, measured)

    def test_a_wrapping_lyric_shrinks_but_stays_above_the_floor(self):
        context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        measured = self._measure(context, 1)
        self.assertLess(measured['font'], 1080 * 0.05, measured)   # it did shrink
        self.assertGreaterEqual(measured['font'], 1080 * 0.02, measured)  # not past the floor
        self.assertLessEqual(measured['rows'], 2, measured)

    def test_the_shrink_step_is_four_percent_of_the_rest_size(self):
        """The type walks a linear ladder: rest minus 4 % of rest per step, 15 steps to the floor."""
        context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        measured = self._measure(context, 1)
        rest = measured['stageHeight'] * 0.05
        step = rest * 0.04
        steps = (rest - measured['font']) / step
        self.assertGreater(round(steps), 0, measured)
        self.assertAlmostEqual(steps, round(steps), delta=0.02,
                               msg=f"font {measured['font']} is not on the linear ladder: {measured}")

    def test_the_fit_stops_at_two_percent_when_two_lines_cannot_fit(self):
        context = self.browser.new_context(viewport={'width': 1920, 'height': 1080})
        measured = self._measure(context, 2)
        self.assertAlmostEqual(measured['font'], 1080 * 0.02, delta=0.5,
                               msg=f"floor at 1080p: {measured}")
        self.assertGreater(measured['rows'], 2,
                           'the accepted edge lets the block exceed two rows')
