"""A reading page's text wraps at its pane (spec 137).

Every fixture is a value the columns allow: ``TataIbadah.name`` and ``Song.title``
are 64 characters, a ``BookTranslation``'s translation is 32, a ``Verse``'s title
is 128, and a text entry's body is a TextField. A longer run cannot be stored, so
the tests measure the widest value the product can actually hold — the case the
owner met on a real service.

The measurement is the one thing a style assertion cannot show: how far the
painted text runs past the box that owns it, and whether the document as a whole
has grown a horizontal scrollbar. Run under Django's runner through
``StaticLiveServerTestCase``; skips cleanly when Playwright is absent.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

# The widest values the columns accept — see the module docstring.
SERVICE_NAME = 'h' * 64
SONG_TITLE = 'a' * 43 + '581. Sangap di Jahowa'      # 64 characters
SPACED_NAME = 'Ibadah Minggu Sahabat ' * 2 + 'Ibadah Minggu'   # 57, wraps at its spaces
TRANSLATION = 'K' * 32
PERICOPE = 'P' * 128
LINK = 'https://drive.google.com/drive/folders/18A0dI3cwJxzSGTxim3ENlj4GwrB2Yatd'

PLAIN_SERVICE = 'Ibadah Minggu'
PLAIN_SONG = 'Sihol Pujionku'

# How far the element's painted text runs past its own box, and whether the
# document has a horizontal scrollbar. A negative spill is text that ends inside.
SPILL = r"""
(selector) => {
  const el = document.querySelector(selector);
  if (!el) return null;
  const box = el.getBoundingClientRect();
  const range = document.createRange();
  range.selectNodeContents(el);
  const rects = [...range.getClientRects()];
  const right = rects.length ? Math.max(...rects.map((r) => r.right)) : box.right;
  const style = getComputedStyle(el);
  return {
    spill: Math.round(right - (box.left + el.clientLeft + el.clientWidth)),
    width: Math.round(box.width),
    height: Math.round(box.height),
    lineHeight: parseFloat(style.lineHeight),
    docOverflow: Math.round(document.documentElement.scrollWidth
                            - document.documentElement.clientWidth),
  };
}
"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReadingTextWrapE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        indonesian = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=indonesian, name='Terjemahan Baru',
                                               abbreviation='TB')
        book = bible.Book.objects.create(name='Kej', testament='old', number_of_chapters=50)
        self.translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation=TRANSLATION)
        bible.Verse.objects.create(book_translation=self.translation, chapter=1, verse=1,
                                   title=PERICOPE, text=LINK)
        bible.Verse.objects.create(book_translation=self.translation, chapter=1, verse=2,
                                   title=None, text='Lalu Allah menciptakan langit.')

        self.service = tatib.TataIbadah.objects.create(
            name=SERVICE_NAME, date=date(2026, 10, 25), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1, text=LINK)
        self.spaced_service = tatib.TataIbadah.objects.create(
            name=SPACED_NAME, date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.spaced_service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            text='Nyanyian pembuka.')
        self.plain_service = tatib.TataIbadah.objects.create(
            name=PLAIN_SERVICE, date=date(2026, 10, 11), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.plain_service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            text='Nyanyian pembuka.')

        hymn_book = songs.Book.objects.create(name='Buku Ende', short_name='BE',
                                              is_hymn_book=True)
        self.song = songs.Song.objects.create(book=hymn_book, number=581, title=SONG_TITLE)
        songs.Verse.objects.create(song=self.song, number=1, lyric='Bait satu')
        self.plain_song = songs.Song.objects.create(book=hymn_book, number=1, title=PLAIN_SONG)
        songs.Verse.objects.create(song=self.plain_song, number=1, lyric='Bait satu')

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

    def open(self, view, *args):
        self.page.goto(self.live_server_url + reverse(view, args=args))
        self.page.wait_for_load_state('networkidle')
        expect(self.page.locator('.read__title')).to_be_visible()

    def at(self, width):
        self.page.set_viewport_size({'width': width, 'height': 900})
        self.page.wait_for_timeout(120)

    def measure(self, selector):
        result = self.page.evaluate(SPILL, selector)
        self.assertIsNotNone(result, f'{selector} is not on the page')
        return result

    def assert_wraps(self, selector, widths, document=True):
        """No painted text past the box (and, optionally, no horizontal scrollbar)."""
        for width in widths:
            self.at(width)
            result = self.measure(selector)
            self.assertLessEqual(result['spill'], 1,
                                 (selector, width, 'spill', result))
            if document:
                self.assertEqual(result['docOverflow'], 0,
                                 (selector, width, 'document overflow', result))

    # -- US1: the page title --------------------------------------------

    TITLE_STATE = """() => {
      const title = document.querySelector('.read__title');
      const toggle = document.querySelector('#langTb');
      const titleBox = title.getBoundingClientRect();
      const toggleBox = toggle ? toggle.getBoundingClientRect() : null;
      const style = getComputedStyle(title);
      return {
        width: Math.round(titleBox.width),
        height: Math.round(titleBox.height),
        lineHeight: parseFloat(style.lineHeight),
        titleBottom: Math.round(titleBox.bottom),
        toggleVisible: !!(toggle && toggle.getClientRects().length),
        toggleY: toggleBox ? Math.round(toggleBox.y) : null,
      };
    }"""

    def with_and_without_rule(self, state=None):
        """The same page read twice: as it ships, and with the rule's value restored.

        The scrollbar state is pinned for both reads, or a scrollbar leaving would move
        every box by itself and shadow the difference the rule makes.
        """
        self.page.add_style_tag(content='html { overflow: hidden; }')
        shipped = self.page.evaluate(state or self.TITLE_STATE)
        self.page.add_style_tag(content='.read, .search-results, .preview '
                                       '{ overflow-wrap: normal; }')
        restored = self.page.evaluate(state or self.TITLE_STATE)
        return shipped, restored

    def test_a_long_title_wraps_inside_the_pane(self):
        self.open('web-tatib-service', self.service.pk)
        self.assert_wraps('.read__title', (1440, 1280, 390))
        self.at(1440)
        tall = self.measure('.read__title')
        self.assertGreater(tall['height'], tall['lineHeight'] * 2,
                           'the 64-character title is one line again')
        # FR-009: the rule is inherited, not declared on the title itself.
        inherited = self.page.evaluate(
            "getComputedStyle(document.querySelector('#readName')).overflowWrap")
        self.assertEqual(inherited, 'break-word')

        self.open('web-song', self.song.pk)
        self.assert_wraps('.read__title', (1440, 1280, 390))

    def test_a_short_title_is_unchanged(self):
        for view, args in (('web-tatib-service', (self.plain_service.pk,)),
                           ('web-song', (self.plain_song.pk,))):
            self.open(view, *args)
            for width in (1440, 1280, 390):
                self.at(width)
                self.assertLessEqual(self.measure('.read__title')['spill'], 1, (view, width))
                shipped, restored = self.with_and_without_rule()
                self.assertEqual(shipped['height'], restored['height'],
                                 (view, width, 'a title that fits changed height',
                                  shipped, restored))
                self.assertEqual(shipped['width'], restored['width'], (view, width))
                self.page.reload(wait_until='networkidle')

        # A long title with spaces wraps at its spaces, as it always has.
        self.open('web-tatib-service', self.spaced_service.pk)
        self.at(1440)
        result = self.measure('.read__title')
        self.assertLessEqual(result['spill'], 1, result)
        self.assertGreater(result['height'], result['lineHeight'] * 1.6,
                           ('the 57-character spaced title should wrap', result))

    def test_the_title_keeps_its_box_and_the_toggle_its_line(self):
        """`break-word` leaves min-content alone, so the header lays out as it does today.

        The guard is about which line the toggle takes, not its absolute `y`: a title
        that wraps is taller, and a taller title moves whatever sits under it. With
        `anywhere` the title's min-content collapses, the flex line stops wrapping and
        the toggle would sit beside a title squeezed into the leftover width.
        """
        self.open('web-bible-chapter', self.translation.book_id, 1)
        for width in (1440, 1280, 820, 390):
            self.at(width)
            shipped, restored = self.with_and_without_rule()
            self.assertTrue(shipped['toggleVisible'], (width, shipped))
            self.assertEqual(shipped['width'], restored['width'],
                             (width, 'the title box changed width', shipped, restored))
            self.assertEqual(shipped['toggleY'] < shipped['titleBottom'],
                             restored['toggleY'] < restored['titleBottom'],
                             (width, 'the toggle changed line', shipped, restored))
            self.page.reload(wait_until='networkidle')

    # -- US2: the other reading surfaces --------------------------------

    def test_no_reading_route_scrolls_sideways(self):
        routes = [
            ('web-tatib-service', (self.service.pk,)),
            ('web-song', (self.song.pk,)),
            ('web-book', (self.song.book_id,)),
            ('web-bible-chapter', (self.translation.book_id, 1)),
            ('web-search', ()),
            ('web-media-library', ()),
            ('web-tatib', ()),
            ('web-books', ()),
        ]
        for view, args in routes:
            url = self.live_server_url + reverse(view, args=args)
            self.page.goto(url + ('?q=hhhhhh' if view == 'web-search' else ''))
            self.page.wait_for_load_state('networkidle')
            for width in (1440, 1280, 820, 390):
                self.at(width)
                overflow = self.page.evaluate(
                    'document.documentElement.scrollWidth'
                    ' - document.documentElement.clientWidth')
                self.assertEqual(overflow, 0, (view, width, 'sideways scroll'))

    def test_a_body_paragraph_holding_a_link_wraps(self):
        self.open('web-tatib-service', self.service.pk)
        expect(self.page.locator('.tatib__tx')).to_have_count(1)
        self.assert_wraps('.tatib__tx', (1440, 820, 390))

    def test_a_bible_heading_and_verse_wrap(self):
        self.open('web-bible-chapter', self.translation.book_id, 1)
        self.assert_wraps('.read__sec', (1280, 820, 390))
        self.assert_wraps('.v', (1280, 820, 390))

    def test_a_search_result_title_wraps(self):
        self.page.goto(self.live_server_url + reverse('web-search') + '?q=hhhhhh')
        self.page.wait_for_load_state('networkidle')
        expect(self.page.locator('.result-row__title').first).to_be_visible()
        self.assert_wraps('.result-row__title', (820, 390))

    def test_preview_lines_wrap(self):
        self.open('web-tatib-service', self.service.pk)
        self.page.locator('[data-preview-open]').first.click()
        expect(self.page.locator('#previewModal')).to_be_visible()
        expect(self.page.locator('.preview__line').first).to_be_visible()
        # The dialog is what this row is about; the page behind it is measured by US1.
        self.assert_wraps('.preview__line', (820, 390), document=False)

    # -- US3: what truncates keeps truncating ----------------------------

    def test_a_truncating_row_still_truncates(self):
        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.page.wait_for_load_state('networkidle')
        row = self.page.locator('.book__n', has_text=SERVICE_NAME).first
        expect(row).to_be_visible()
        style = row.evaluate("""(el) => {
          const cs = getComputedStyle(el);
          return {
            whiteSpace: cs.whiteSpace,
            textOverflow: cs.textOverflow,
            lines: Math.round(el.getBoundingClientRect().height / parseFloat(cs.lineHeight)),
            clipped: el.scrollWidth > el.clientWidth,
          };
        }""")
        self.assertEqual(style['whiteSpace'], 'nowrap')
        self.assertEqual(style['textOverflow'], 'ellipsis')
        self.assertEqual(style['lines'], 1, 'a sidebar row grew to a second line')
        self.assertTrue(style['clipped'], 'the long name no longer exceeds its row')

        self.open('web-tatib-service', self.service.pk)
        contents = self.page.locator('.songrow__t').first
        expect(contents).to_be_visible()
        clamp = contents.evaluate("(el) => getComputedStyle(el).webkitLineClamp")
        self.assertEqual(clamp, '3')
