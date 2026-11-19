"""A long word wraps in the dock runner (spec 203).

The reading page has held this rule since spec 137 (`reading/R13`) and the dock's own
picker has held it since spec 119 (`.servicerow__n`). The runner never did: an unbroken
run — a service name with no spaces, a pasted URL, a filename with no hyphens — painted
straight past the box that owns it and gave the body a horizontal scrollbar.

Every fixture is a value the columns allow: ``TataIbadah.name`` and ``ServiceEntry.title``
are 64 characters, ``ServiceEntry.media_filename`` is 255, and a Text entry's body is a
TextField. The measurement is spec 137's own: how far the painted text runs past the box
that owns it, read from range rects rather than from a style assertion.

Run under Django's runner through ``StaticLiveServerTestCase``; skips cleanly when
Playwright is absent.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

# The widest values the columns accept, and the runs the owner met on a real service.
SERVICE_NAME = 'h' * 64
LINK = 'https://drive.google.com/drive/folders/18A0dI3cwJxzSGTxim3ENlj4GwrB2Yatd'
HYPHENATED = ('side-view-silhouette-african-elephant-walking-across-green-ground-'
              'against-light-blue-sky-stately-wild-bull-marching-proudly-481645534.webp')
UNBROKEN_FILE = 'w' * 200
SONG_TITLE = 'a' * 43 + '581. Sangap di Jahowa'      # 64 characters
PLAIN_NAME = 'Ibadah Minggu'

# The rule this slice ships, and its value restored — the same page read twice, so a
# box that already fits can be proved unchanged rather than asserted to be.
RULE = '.serviceline, .entryrow__t, .screenerow'
RESTORE = RULE + ' { overflow-wrap: normal; }'

# Spec 137's measurement: the painted text's right edge against its own box, plus
# whether the document as a whole grew a horizontal scrollbar.
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
    lines: Math.round(box.height / parseFloat(style.lineHeight)),
    overflowWrap: style.overflowWrap,
    docOverflow: Math.round(document.documentElement.scrollWidth
                            - document.documentElement.clientWidth),
  };
}
"""

# Every text box the runner paints, each with its own spill and its own box.
RUNNER = r"""
() => {
  const read = (el) => {
    const box = el.getBoundingClientRect();
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()];
    const right = rects.length ? Math.max(...rects.map((r) => r.right)) : box.right;
    const style = getComputedStyle(el);
    return {
      text: (el.textContent || '').trim().slice(0, 24),
      spill: Math.round(right - (box.left + el.clientLeft + el.clientWidth)),
      width: +box.width.toFixed(1), height: +box.height.toFixed(1),
      lines: Math.round(box.height / parseFloat(style.lineHeight)),
    };
  };
  const body = document.getElementById('runBody');
  return {
    bodyOverflow: body.scrollWidth - body.clientWidth,
    title: read(document.getElementById('runService')),
    headers: [...document.querySelectorAll('#entryList .entryrow__t')].map(read),
    rows: [...document.querySelectorAll('#entryList .entryrow')].map(read),
    screens: [...document.querySelectorAll('#entryList .screenerow__line')].map(read),
    numbers: [...document.querySelectorAll('#entryList .entryrow__c')].map(
      (el) => +el.getBoundingClientRect().width.toFixed(1)),
    chevrons: [...document.querySelectorAll('#entryList .entrychev')]
      .filter((el) => el.getBoundingClientRect().width > 0)   /* the live row renders none */
      .map((el) => {
        const r = el.getBoundingClientRect();
        const row = el.closest('.entryrow').getBoundingClientRect();
        return { offRight: +(row.right - r.right).toFixed(1),
                 offCentre: +((r.top + r.bottom) / 2 - (row.top + row.bottom) / 2).toFixed(1) };
      }),
  };
}
"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockTextWrapE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.long = tatib.TataIbadah.objects.create(
            name=SERVICE_NAME, date=date(2026, 10, 25), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.long, order_number=1, kind=tatib.ServiceEntryKind.TEXT, text=LINK)
        for order, filename in ((2, 'random.jpg'), (3, HYPHENATED), (4, UNBROKEN_FILE)):
            media = tatib.MediaIdentity.objects.create(
                sha256=str(order) * 64, byte_count=120, family='image',
                display_filename=filename)
            tatib.ServiceEntry.objects.create(
                tatib=self.long, order_number=order, kind=tatib.ServiceEntryKind.MEDIA,
                media=media, media_filename=filename)
        # An ordinary songbook: the dock labels a hymn by its number alone ("BE 581"),
        # so a long song title reaches the header only through a non-hymn book.
        book = songs.Book.objects.create(name='Nyanyian Pujian', is_hymn_book=False)
        song = songs.Song.objects.create(book=book, number=581, title=SONG_TITLE)
        songs.Verse.objects.create(song=song, number=1, lyric='Bait satu')
        tatib.ServiceEntry.objects.create(
            tatib=self.long, order_number=5, kind=tatib.ServiceEntryKind.SONG, song=song)

        self.plain = tatib.TataIbadah.objects.create(
            name=PLAIN_NAME, date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.plain, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.plain, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Doa', text='Tuhan, dengarkanlah doa kami')

        # A live block tall enough to run past the scrollport, so the NEXT band is
        # drawn (it yields the moment the live entry's own end is in view), and a
        # following entry whose label is an unbroken URL — the band's own cut.
        self.band = tatib.TataIbadah.objects.create(
            name='Ibadah Panjang', date=date(2026, 10, 11), is_active=True)
        band_book = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                              is_hymn_book=True)
        band_song = songs.Song.objects.create(book=band_book, number=1, title='Nyanyian Pembuka')
        for verse in range(1, 13):
            songs.Verse.objects.create(song=band_song, number=verse, lyric=f'Baris bait {verse}')
        tatib.ServiceEntry.objects.create(
            tatib=self.band, order_number=1, kind=tatib.ServiceEntryKind.SONG, song=band_song,
            verses=list(band_song.verse_set.values_list('pk', flat=True)))
        tatib.ServiceEntry.objects.create(
            tatib=self.band, order_number=2, kind=tatib.ServiceEntryKind.TEXT, text=LINK)

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 456, 'height': 1087})

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    # -- helpers ---------------------------------------------------------

    def open_runner(self, service=None, width=456):
        service = service or self.long
        self.page.set_viewport_size({'width': width, 'height': 1087})
        self.page.goto(self.live_server_url + '/obs/dock', wait_until='networkidle')
        self.page.wait_for_selector('.servicerow')
        self.page.locator(f'.servicerow[data-service="{service.pk}"]').first.click()
        self.page.wait_for_selector('#viewRun.is-active .entryrow')
        self.page.wait_for_timeout(250)

    def at(self, width):
        self.page.set_viewport_size({'width': width, 'height': 1087})
        self.page.wait_for_timeout(150)

    def measure(self, selector):
        result = self.page.evaluate(SPILL, selector)
        self.assertIsNotNone(result, f'{selector} is not on the page')
        return result

    def runner(self):
        return self.page.evaluate(RUNNER)

    def restore_rule(self):
        """Read the same page with the rule's value put back to normal."""
        self.page.add_style_tag(content=RESTORE)
        self.page.wait_for_timeout(120)

    def project_first(self):
        """Put the first entry on air through the list's own projection path.

        Dispatched as the follow suite dispatches it: a tall block's first screen row
        can sit under the pinned live header, where a pointer hit-test never lands.
        """
        self.page.evaluate("""() => {
          const li = document.querySelector('#entryList .entryli[data-index="0"]');
          const row = li.querySelector('.entryrow');
          if (row && row.getAttribute('aria-expanded') !== 'true') row.click();
        }""")
        self.page.wait_for_timeout(300)
        self.page.evaluate("""() => {
          const screen = document.querySelector(
            '#entryList .entryli[data-index="0"] .screenerow');
          if (screen) screen.click();
        }""")
        self.page.wait_for_timeout(300)

    # -- US1: the run wraps inside its own box ---------------------------

    def test_an_unbroken_service_name_wraps_inside_its_column(self):
        self.open_runner()
        for width in (320, 456, 900):
            self.at(width)
            result = self.measure('#runService')
            self.assertLessEqual(result['spill'], 1, (width, 'the title runs past its column', result))
            self.assertEqual(result['overflowWrap'], 'anywhere', (width, result))
        self.at(456)
        tall = self.measure('#runService')
        self.assertGreater(tall['lines'], 1, 'the 64-character name is one line again')

    def test_an_unbroken_entry_header_wraps_inside_its_row(self):
        self.open_runner()
        for width in (320, 456):
            self.at(width)
            state = self.runner()
            for header in state['headers']:
                self.assertLessEqual(header['spill'], 1, (width, header))
            # the URL entry and the 200-character filename are the unbroken runs
            self.assertTrue(any(h['text'].startswith('https://') for h in state['headers']),
                            state['headers'])
            self.assertTrue(any(h['text'].startswith('wwww') for h in state['headers']),
                            state['headers'])

    def test_a_screen_row_wraps_inside_the_open_block(self):
        self.open_runner()
        self.project_first()
        for width in (320, 456):
            self.at(width)
            state = self.runner()
            self.assertTrue(state['screens'], 'the open block painted no screen line')
            for line in state['screens']:
                self.assertLessEqual(line['spill'], 1, (width, line))

    def test_the_runner_body_does_not_scroll_sideways(self):
        self.open_runner()
        self.project_first()
        for width in (320, 456, 900):
            self.at(width)
            state = self.runner()
            self.assertEqual(state['bodyOverflow'], 0, (width, 'the body scrolls sideways', state))
            self.assertEqual(self.measure('#runService')['docOverflow'], 0, (width,))

    # -- US2: what fits is unchanged -------------------------------------

    def test_text_that_fits_is_unchanged(self):
        self.open_runner()
        self.at(456)
        shipped = self.runner()
        self.restore_rule()
        restored = self.runner()
        for index, (before, after) in enumerate(zip(shipped['headers'], restored['headers'])):
            if before['spill'] > 1 or after['spill'] > 1:
                continue                      # a run that overflowed is meant to change
            self.assertEqual(before['height'], after['height'], (index, before, after))
            self.assertEqual(before['width'], after['width'], (index, before, after))
            self.assertEqual(before['lines'], after['lines'], (index, before, after))
        self.assertEqual(shipped['rows'][1]['height'], restored['rows'][1]['height'])

    def test_a_short_service_is_unchanged(self):
        for width in (320, 456, 900):
            self.open_runner(service=self.plain, width=width)
            shipped = self.runner()
            self.restore_rule()
            restored = self.runner()
            self.assertEqual(shipped['title']['height'], restored['title']['height'], (width,))
            self.assertEqual(shipped['title']['width'], restored['title']['width'], (width,))
            self.assertEqual(shipped['bodyOverflow'], restored['bodyOverflow'], (width,))
            for index, (before, after) in enumerate(zip(shipped['rows'], restored['rows'])):
                self.assertEqual(before['height'], after['height'], (width, index))
                self.assertEqual(before['width'], after['width'], (width, index))

    def test_the_row_keeps_its_number_and_chevron(self):
        self.open_runner()
        self.at(456)
        shipped = self.runner()
        self.restore_rule()
        restored = self.runner()
        self.assertEqual(shipped['numbers'], restored['numbers'], 'the number column moved')
        self.assertEqual(shipped['chevrons'], restored['chevrons'], 'the chevron moved')
        self.assertTrue(shipped['chevrons'], 'no chevron was drawn to measure')

    def test_a_wide_panel_renders_as_it_does_today(self):
        """At 900px the 64-character name fits its column, so the rule changes nothing
        there. A run wider than the panel itself (the 200-character filename) still
        wraps — the rule is width-independent, not a narrow-panel special case."""
        self.open_runner(width=900)
        shipped = self.runner()
        self.restore_rule()
        restored = self.runner()
        self.assertEqual(shipped['title']['lines'], restored['title']['lines'])
        self.assertEqual(shipped['title']['height'], restored['title']['height'])
        self.assertEqual(shipped['title']['width'], restored['title']['width'])
        self.assertLessEqual(shipped['title']['spill'], 1, 'the name no longer fits a wide panel')
        for index, (before, after) in enumerate(zip(shipped['headers'], restored['headers'])):
            if before['spill'] > 1 or after['spill'] > 1:
                continue
            self.assertEqual(before['height'], after['height'], (index, before, after))
            self.assertEqual(before['width'], after['width'], (index, before, after))
        self.assertEqual(shipped['bodyOverflow'], 0, 'the body scrolls sideways at 900px')

    # -- US3: what truncates keeps truncating ----------------------------

    def test_a_truncating_label_still_truncates(self):
        self.open_runner(service=self.band, width=456)
        self.project_first()
        band = self.page.locator('.nextband')
        self.assertTrue(band.is_visible(), 'the NEXT band was not drawn for a tall live block')
        label = self.page.locator('.nextband__label')
        style = label.first.evaluate("""(el) => {
          const cs = getComputedStyle(el);
          return { whiteSpace: cs.whiteSpace, textOverflow: cs.textOverflow,
                   text: el.textContent.trim().slice(0, 20),
                   lines: Math.round(el.getBoundingClientRect().height / parseFloat(cs.lineHeight)),
                   clipped: el.scrollWidth > el.clientWidth };
        }""")
        self.assertEqual(style['whiteSpace'], 'nowrap')
        self.assertEqual(style['textOverflow'], 'ellipsis')
        self.assertEqual(style['lines'], 1, 'the next band grew to a second line')
        self.assertTrue(style['clipped'], 'the long label no longer exceeds its band')
        self.assertTrue(style['text'].startswith('https://'), style)

    def test_the_picker_name_still_wraps(self):
        self.page.set_viewport_size({'width': 456, 'height': 1087})
        self.page.goto(self.live_server_url + '/obs/dock', wait_until='networkidle')
        self.page.wait_for_selector('.servicerow')
        row = self.page.locator(f'.servicerow[data-service="{self.long.pk}"] .servicerow__n')
        style = row.first.evaluate("""(el) => {
          const cs = getComputedStyle(el);
          const box = el.getBoundingClientRect();
          return { overflowWrap: cs.overflowWrap,
                   lines: Math.round(box.height / parseFloat(cs.lineHeight)),
                   spill: el.scrollWidth - el.clientWidth };
        }""")
        self.assertEqual(style['overflowWrap'], 'anywhere')
        self.assertLessEqual(style['spill'], 1, style)
        self.assertGreater(style['lines'], 1, 'the picker name stopped wrapping')
