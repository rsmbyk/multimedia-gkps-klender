"""The landing search field sits on the window's middle (spec 139).

The defect is a composition of three offsets — the logo-and-field block being
centred (half of 96 + 26 = 61px), the stage padding 40px above and 64px below
(12px), and, below 720px, a section measured from ``--pad-top`` while the stage
pads for the toolbar (36px of overhang). Only a rect tells them apart, so every
test here measures boxes: the field's centre against the window's middle, the
logo's gap, the document's own height, and the two views that must not move.

The eleven windows are the ones SC-001 names. They straddle both layout switches
(1272px, 720px) and include the pair 721/720, which is the boundary itself.

Run under Django's runner through ``StaticLiveServerTestCase``; skips cleanly
when Playwright is absent.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

# SC-001's eleven windows, in the order the spec's table lists them.
WINDOWS = (
    (1920, 1000), (1440, 900), (1280, 800), (1272, 800), (1024, 768),
    (834, 1112), (721, 900), (720, 900), (600, 800), (390, 844), (320, 568),
)
PHONES = (720, 600, 390, 320)

# Every box the spec talks about, plus the stage's own paddings — the section's
# space is the stage's content box, and only the computed padding says where it is.
BOXES = r"""
() => {
  const rect = (selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const style = getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden') return 'hidden';
    const box = el.getBoundingClientRect();
    return {top: box.top, bottom: box.bottom, left: box.left, right: box.right,
            width: box.width, height: box.height, cy: box.top + box.height / 2};
  };
  const stage = document.querySelector('.stage');
  const stageStyle = getComputedStyle(stage);
  const section = document.querySelector('.search-home');
  return {
    field: rect('.search-home__input'),
    logo: rect('.search-home__logo'),
    section: rect('.search-home'),
    results: rect('.search-results'),
    read: rect('.read'),
    stage: rect('.stage'),
    stagePad: {top: parseFloat(stageStyle.paddingTop),
               right: parseFloat(stageStyle.paddingRight),
               bottom: parseFloat(stageStyle.paddingBottom),
               left: parseFloat(stageStyle.paddingLeft)},
    sectionTransition: getComputedStyle(section).transitionDuration,
    scrollY: window.scrollY,
    docHeight: document.documentElement.scrollHeight,
    docWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    viewportHeight: window.innerHeight,
  };
}
"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class HomeSearchCenterE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        hymn_book = songs.Book.objects.create(name='Buku Ende', short_name='BE',
                                              is_hymn_book=True)
        self.song = songs.Song.objects.create(book=hymn_book, number=1,
                                              title='Sihol Pujionku')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Bait satu')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    # -- helpers ---------------------------------------------------------

    def open(self, path, field=True):
        self.page.goto(self.live_server_url + path)
        self.page.wait_for_load_state('networkidle')
        if field:
            expect(self.page.locator('.search-home__input')).to_be_visible()

    def open_home(self):
        self.open(reverse('web-index'))

    def at(self, width, height):
        self.page.set_viewport_size({'width': width, 'height': height})
        self.page.wait_for_timeout(120)

    def boxes(self):
        return self.page.evaluate(BOXES)

    def assert_field_on_middle(self, width, height, boxes=None):
        boxes = boxes or self.boxes()
        field = boxes['field']
        self.assertNotEqual(field, 'hidden', f'the field is not painted at {width}x{height}')
        middle = boxes['viewportHeight'] / 2
        self.assertLessEqual(abs(field['cy'] - middle), 1,
                             (width, height, 'field centre', field['cy'], 'window middle', middle))

    # -- US1: the field is the page's middle line ------------------------

    def test_the_field_is_on_the_window_middle(self):
        self.open_home()
        for width, height in WINDOWS:
            with self.subTest(window=f'{width}x{height}'):
                self.at(width, height)
                self.assert_field_on_middle(width, height)

    def test_the_logo_stays_whole_above_the_field(self):
        self.open_home()
        for width, height in WINDOWS:
            with self.subTest(window=f'{width}x{height}'):
                self.at(width, height)
                boxes = self.boxes()
                self.assertNotEqual(boxes['logo'], 'hidden', 'the logo is not painted')
                self.assertGreaterEqual(boxes['logo']['top'], 0,
                                        ('the logo is cut off at the top', boxes['logo']))
                self.assertAlmostEqual(boxes['field']['top'] - boxes['logo']['bottom'], 26,
                                       delta=1,
                                       msg=('the gap between the logo and the field', width,
                                            boxes['logo'], boxes['field']))

    def test_the_landing_page_is_one_window_tall(self):
        self.open_home()
        for width, height in WINDOWS:
            with self.subTest(window=f'{width}x{height}'):
                self.at(width, height)
                boxes = self.boxes()
                self.assertEqual(boxes['docHeight'], boxes['viewportHeight'],
                                 ('the landing page grows past the window', width, height))
                self.assertEqual(boxes['docWidth'], boxes['clientWidth'],
                                 ('the landing page scrolls sideways', width, height))

    def test_the_phone_layout_centres_too(self):
        self.open_home()
        for width in PHONES:
            with self.subTest(window=f'{width}x900'):
                self.at(width, 900)
                boxes = self.boxes()
                stage, pad = boxes['stage'], boxes['stagePad']
                # the section must be exactly the stage's content box, or its middle
                # is not the window's however the form is placed inside it
                self.assertAlmostEqual(boxes['section']['top'], stage['top'] + pad['top'],
                                       delta=1, msg=('section top vs the stage content box', width))
                self.assertAlmostEqual(boxes['section']['height'],
                                       stage['height'] - pad['top'] - pad['bottom'],
                                       delta=1, msg=('section height vs the stage content box', width))
                self.assert_field_on_middle(width, 900, boxes)

    def test_the_field_does_not_travel(self):
        self.open_home()
        self.at(1440, 900)
        first = self.boxes()
        self.assertEqual(first['scrollY'], 0, 'the page scrolled itself on load')
        self.assertTrue(first['sectionTransition'].startswith('0s'),
                        ('the section animates', first['sectionTransition']))
        self.page.wait_for_timeout(400)
        later = self.boxes()
        self.assertAlmostEqual(later['field']['cy'], first['field']['cy'], delta=0.5,
                               msg='the field moved after the page had painted')

    # -- US2: the views that are not the landing ------------------------

    def test_the_results_bar_keeps_its_place(self):
        self.open(reverse('web-search') + '?q=kasih')
        for (width, height), field_top, results_top in (((1440, 900), 46, 128),
                                                        ((390, 844), 82, 164)):
            with self.subTest(window=f'{width}x{height}'):
                self.at(width, height)
                boxes = self.boxes()
                self.assertAlmostEqual(boxes['field']['top'], field_top, delta=1,
                                       msg=('the results bar moved', width, boxes['field']))
                self.assertAlmostEqual(boxes['section']['height'], 88, delta=1,
                                       msg=('the results bar changed height', width))
                self.assertAlmostEqual(boxes['results']['top'], results_top, delta=1,
                                       msg=('the results list moved', width, boxes['results']))
        # and it never recentres on a resize
        self.at(1024, 768)
        resized = self.boxes()
        self.assertAlmostEqual(resized['field']['top'], 46, delta=1,
                               msg=('the compact bar recentred on resize', resized['field']))

    def test_the_reading_page_is_unchanged(self):
        self.open(reverse('web-song', args=(self.song.pk,)), field=False)
        expect(self.page.locator('.read__title')).to_be_visible()
        self.at(1440, 900)
        boxes = self.boxes()
        self.assertEqual(boxes['section'], 'hidden', 'the search section is painted on a reading page')
        stage, pad, read = boxes['stage'], boxes['stagePad'], boxes['read']
        self.assertAlmostEqual(read['top'], stage['top'] + pad['top'], delta=1,
                               msg='the reading column moved off the stage content box')
        self.assertAlmostEqual(read['left'], stage['left'] + pad['left'], delta=1,
                               msg='the reading column moved off the stage content box')
        self.assertAlmostEqual(read['width'], stage['width'] - pad['left'] - pad['right'],
                               delta=1, msg='the reading column changed width')
