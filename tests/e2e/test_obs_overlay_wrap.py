"""A long run in the overlay wraps inside the box that owns it (spec 183).

The overlay paints operator-typed text, and any of its text can carry a run with no
space in it -- a pasted link, a compound word, a name typed in a hurry. The rule under
test is `overflow-wrap: break-word` on `.obs-overlay__stage`, declared once and inherited
by every text the surface paints: the plate's body rows and its words column, the
plate's kicker and title, and the song caption.

A speaker's mark is the one exception: it is a label from the mark grammar, keeps
`white-space: nowrap`, and is asserted as such.
"""

import json
import re
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

LONG_RUN = 'lo' + 'o' * 118            # 120 characters: wider than the plate's 90 % cap
LONG_URL = 'https://example.org/' + 'x' * 120

# What a text element's ink does against the plate that owns it.
INK = """(selector) => {
  const plate = document.querySelector('.obs-overlay__plate');
  const root = plate || document.querySelector('.obs-overlay__caption');
  const element = document.querySelector(selector);
  if (!element || !root) return null;
  const range = document.createRange();
  range.selectNodeContents(element);
  const rects = [...range.getClientRects()];
  const style = getComputedStyle(root);
  const plateBox = root.getBoundingClientRect();
  const padRight = parseFloat(style.paddingRight) || 0;
  return {
    columns: rects.length,
    rows: new Set(rects.map(r => Math.round(r.top))).size,
    inkLeft: Math.min(...rects.map(r => r.left)),
    inkRight: Math.max(...rects.map(r => r.right)),
    boxRight: element.getBoundingClientRect().right,
    contentRight: plateBox.right - padRight,
    plateWidth: plateBox.width,
    plateHeight: plateBox.height,
    font: parseFloat(style.fontSize)
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ObsOverlayBodyWrapE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date='2026-11-02', is_active=True)
        # 1 -- the report: a body whose long run has no break opportunity.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Title text',
            text='a very ' + LONG_RUN + ' untitled text')
        # 2 -- a marked row whose words are one pasted link, then a short answer.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Persembahan',
            text='L. Marhite ' + LONG_URL + '\nJ. Amen.')
        # 3 -- the control: both lines fit, so the rule must be inert.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia dan damai sejahtera menyertai kita.\nJ. Amen.')
        # 4 -- a lyric, whose caption carries a 66-character run.
        book = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        song = songs.Song.objects.create(book=book, number=152, title='Ada Kuasa')
        songs.Verse.objects.create(
            song=song, number=1,
            lyric='Kasih setia Tuhan ' + 'mmmm' * 15 + ' sampai selamanya')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=4, kind=tatib.ServiceEntryKind.SONG,
            song=song, verses=[1])
        # 5 -- a passage whose verse title is one long run: the plate's `.title`.
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=lang, name='Terjemahan Baru', abbreviation='TB')
        matius = bible.BookTranslation.objects.create(
            version=version,
            book=bible.Book.objects.create(name='Mat', testament='new',
                                           number_of_chapters=28),
            translation='Matius')
        bible.Verse.objects.create(
            book_translation=matius, chapter=9, verse=3,
            title='Judul ' + LONG_RUN,
            text='ayat uji, ' + LONG_RUN + ' dan sisanya pendek')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=5, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=matius, chapter=9, verse_start=3)
        # 6 -- an entry whose own title is one long run: the plate's `.kicker`.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=6, kind=tatib.ServiceEntryKind.TEXT,
            title=('Judul' + 'o' * 59)[:64],
            text='Jemaat menyanyikan pujian.')
        # 7 -- the second control: the smallest panel the surface paints.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=7, kind=tatib.ServiceEntryKind.TEXT,
            title='Tanpa judul', text='Duduklah, jemaat Tuhan.')

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

    def _context(self):
        return self.browser.new_context(viewport={'width': 1920, 'height': 1080})

    def _project(self, context, entry_index, screen=0):
        """Open the dock, project the entry, step to the screen asked for, hand it back."""
        dock = context.new_page()
        dock.goto(self.live_server_url + '/obs/dock')
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        dock.locator('.entryrow').nth(entry_index).click()
        dock.wait_for_function(
            "service => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s && s.service === service && s.on === true; }",
            arg=self.service.pk)
        if screen:
            # One step of the dock's own transport, so the overlay follows the real state.
            dock.keyboard.press('ArrowRight')
            dock.wait_for_function(
                f"() => {{ const s = JSON.parse(localStorage.getItem('gkps-display'));"
                f" return s && s.screen === {screen}; }}")
        return dock

    def _overlay(self, context, selector):
        overlay = context.new_page()
        overlay.goto(self.live_server_url + '/obs/source/overlay')
        overlay.wait_for_selector(selector)
        return overlay

    def _ink(self, page, selector):
        return page.evaluate(INK, selector)

    def _computed(self, page, selector, *properties):
        return page.evaluate("""([selector, properties]) => {
            const element = document.querySelector(selector);
            if (!element) return null;
            const style = getComputedStyle(element);
            return Object.fromEntries(properties.map(p => [p, style[p]]));
        }""", [selector, list(properties)])

    # ---------- the report ----------------------------------------------------

    def test_a_long_run_wraps_inside_the_plate(self):
        """A 120-character run draws inside the plate instead of across the frame."""
        context = self._context()
        self._project(context, 0)
        overlay = self._overlay(context, '.obs-overlay__plate')
        overlay.wait_for_timeout(300)          # let the panel's arrival settle

        ink = self._ink(overlay, '.obs-overlay__line')
        self.assertIsNotNone(ink)
        # The plate is the 90 % cap at this frame; the run breaks at its content edge.
        self.assertAlmostEqual(ink['plateWidth'], 1728, delta=1)
        self.assertLessEqual(ink['inkRight'], ink['contentRight'] + 0.5,
                             f"body ink ends {ink['inkRight'] - ink['contentRight']:.2f}px "
                             f"past the plate's content edge")
        self.assertGreater(ink['rows'], 1, 'the run did not break to a further row')
        # The words that fit on a row keep their own measure: no side spill.
        self.assertLessEqual(ink['inkRight'], ink['boxRight'] + 0.5)
        context.close()

    def test_a_pasted_link_wraps_in_the_words_column_after_a_mark(self):
        """A marked row's link breaks inside the words column, not out of the plate."""
        context = self._context()
        self._project(context, 1)
        overlay = self._overlay(context, '.obs-overlay__line.has-mark')
        overlay.wait_for_timeout(300)

        ink = self._ink(overlay, '.obs-overlay__words')
        self.assertIsNotNone(ink)
        self.assertLessEqual(ink['inkRight'], ink['contentRight'] + 0.5,
                             f"the link ends {ink['inkRight'] - ink['contentRight']:.2f}px "
                             f"past the plate's content edge")
        self.assertGreater(ink['rows'], 1, 'the link did not break to a further row')
        # The mark still owns the first column, so a wrapped row hangs under the words.
        self.assertEqual(overlay.locator('.obs-overlay__speaker').first.text_content(), 'L.')
        context.close()

    def test_the_wrap_holds_at_three_frame_sizes(self):
        """The rule is size-independent: the same body stays inside at 1280 and 960."""
        for width, height in ((1280, 720), (960, 540)):
            with self.subTest(frame=f'{width}x{height}'):
                context = self.browser.new_context(viewport={'width': width,
                                                             'height': height})
                self._project(context, 0)
                overlay = self._overlay(context, '.obs-overlay__plate')
                overlay.wait_for_timeout(300)
                ink = self._ink(overlay, '.obs-overlay__line')
                # The plate is the frame's 90 % cap at every size.
                self.assertAlmostEqual(ink['plateWidth'], width * 0.9, delta=1)
                self.assertLessEqual(ink['inkRight'], ink['contentRight'] + 0.5,
                                     f"at {width}x{height} body ink ends "
                                     f"{ink['inkRight'] - ink['contentRight']:.2f}px past "
                                     f"the plate's content edge")
                context.close()

    # ---------- what must not move -------------------------------------------

    def test_a_body_that_fits_draws_the_same_box_with_the_rule_removed(self):
        """A short liturgy is laid out exactly as it is with no rule at all."""
        for entry_index, name in ((2, 'two short turns'), (6, 'the smallest panel')):
            with self.subTest(state=name):
                context = self._context()
                self._project(context, entry_index)
                overlay = self._overlay(context, '.obs-overlay__plate')
                overlay.wait_for_timeout(300)

                with_rule = self._ink(overlay, '.obs-overlay__line')
                overlay.evaluate("""() => document
                    .querySelectorAll('.obs-overlay__line, .obs-overlay__words')
                    .forEach(el => el.style.setProperty('overflow-wrap', 'normal', 'important'))""")
                overlay.wait_for_timeout(80)
                without = self._ink(overlay, '.obs-overlay__line')

                self.assertEqual(with_rule['rows'], without['rows'])
                self.assertAlmostEqual(with_rule['plateWidth'], without['plateWidth'], places=2)
                self.assertAlmostEqual(with_rule['plateHeight'], without['plateHeight'], places=2)
                self.assertEqual(with_rule['rows'], 1)
                context.close()

    def test_the_rule_is_inherited_from_the_stage(self):
        """One declaration on the stage reaches every text the overlay paints."""
        context = self._context()
        self._project(context, 1)
        overlay = self._overlay(context, '.obs-overlay__line.has-mark')

        self.assertEqual(self._computed(overlay, '.obs-overlay__stage',
                                       'overflowWrap')['overflowWrap'], 'break-word')
        for selector in ('.obs-overlay__plate', '.obs-overlay__kicker',
                         '.obs-overlay__line', '.obs-overlay__words'):
            with self.subTest(selector=selector):
                self.assertEqual(self._computed(overlay, selector,
                                               'overflowWrap')['overflowWrap'],
                                 'break-word')
        context.close()

    def test_the_mark_keeps_its_own_column(self):
        """A speaker's mark is a label: it never wraps, and it keeps its column."""
        context = self._context()
        self._project(context, 1)
        overlay = self._overlay(context, '.obs-overlay__line.has-mark')
        self.assertEqual(self._computed(overlay, '.obs-overlay__speaker',
                                       'whiteSpace')['whiteSpace'], 'nowrap')
        self.assertEqual(self._computed(overlay, '.obs-overlay__line.has-mark',
                                       'display')['display'], 'grid')
        context.close()

    # ---------- the caption and the heading, added to the scope ------------------

    def test_a_song_caption_wraps_its_long_run(self):
        """A lyric's 66-character run draws inside the caption box, not across the frame."""
        context = self._context()
        self._project(context, 3)
        overlay = self._overlay(context, '.obs-overlay__caption')
        overlay.wait_for_timeout(300)

        ink = self._ink(overlay, '.obs-overlay__caption')
        self.assertIsNotNone(ink)
        # The caption has no panel to grow into: its box is the frame less the 5 % inset.
        self.assertAlmostEqual(ink['plateWidth'], 1728, delta=1)
        self.assertLessEqual(ink['inkRight'], ink['contentRight'] + 0.5,
                             f"caption ink ends {ink['inkRight'] - ink['contentRight']:.2f}px "
                             f"past its box")
        self.assertGreater(ink['rows'], 1, 'the run did not break to a further row')
        # Only the break opportunity changed: the caption keeps its own look.
        look = self._computed(overlay, '.obs-overlay__caption', 'textAlign', 'textWrap',
                              'fontWeight', 'textShadow')
        self.assertEqual(look['textAlign'], 'center')
        self.assertEqual(look['textWrap'], 'balance')
        self.assertEqual(look['fontWeight'], '800')
        self.assertIn('rgb(0, 0, 0)', look['textShadow'])
        context.close()

    def test_a_passage_heading_wraps_its_long_run(self):
        """A verse title that is one run breaks under the reference, inside the plate."""
        context = self._context()
        self._project(context, 4)
        overlay = self._overlay(context, '.obs-overlay__title')
        overlay.wait_for_timeout(300)

        ink = self._ink(overlay, '.obs-overlay__title')
        self.assertIsNotNone(ink)
        self.assertLessEqual(ink['inkRight'], ink['contentRight'] + 0.5,
                             f"the title ends {ink['inkRight'] - ink['contentRight']:.2f}px "
                             f"past the plate's content edge")
        self.assertGreater(ink['rows'], 1, 'the title did not break to a further row')
        # The reference over it is short, so the heading's first line is untouched.
        self.assertEqual(overlay.locator('.obs-overlay__kicker').text_content(), 'Matius 9:3')
        context.close()

    def test_a_long_kicker_stays_inside_the_plate(self):
        """A 64-character entry title grows the plate rather than leaving it.

        The kicker is set at `.5em`, so a title-column run (64 characters at most) is
        never wider than the plate's 90 % cap — the plate's own `fit-content` measure
        absorbs it, and the wrap rule is the belt for a kicker that shares a plate with a
        longer row. The assertion is therefore the ink's, plus the property, not a row
        count: this state has one row by the panel's own arithmetic.
        """
        context = self._context()
        self._project(context, 5)
        overlay = self._overlay(context, '.obs-overlay__kicker')
        overlay.wait_for_timeout(300)

        ink = self._ink(overlay, '.obs-overlay__kicker')
        self.assertIsNotNone(ink)
        self.assertLessEqual(ink['inkRight'], ink['contentRight'] + 0.5,
                             f"the kicker ends {ink['inkRight'] - ink['contentRight']:.2f}px "
                             f"past the plate's content edge")
        self.assertLess(ink['inkRight'] - ink['inkLeft'], ink['plateWidth'],
                        'the plate did not grow to hold the kicker')
        self.assertEqual(self._computed(overlay, '.obs-overlay__kicker',
                                       'overflowWrap')['overflowWrap'], 'break-word')
        context.close()
