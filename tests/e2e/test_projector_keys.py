"""Spec 187 — the projector's half of the keyboard parity.

`⌘` is the same modifier as `Ctrl` for the arrows and `Home`/`End`, the shortcut sheet
carries one `Display` group and one `Find` group, the media groups sit together at the
end of the left column, and the sheet follows its tallest column instead of clipping.
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


DISPLAY_ORDER = ['Show or Hide Words', 'Show or Hide Corner', 'Keyboard Shortcuts',
                 'Find in Service', 'Passage or Song', 'Enter or Leave', 'Hold to Leave']
FIND_ORDER = ['Previous Match', 'Next Match', 'Open Match', 'Close When Empty',
              'Close Find']


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProjectorKeyboardE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Proyektor', date=date(2026, 11, 8), is_active=True)
        for order, text in enumerate(('Salam', 'Pujian', 'Firman'), 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=order,
                title=text, text=f'{text} umat Tuhan.\n\nHaleluya.')
        self.songbook = songs.Book.objects.create(
            name='Nyanyian Kidung Baru', short_name='NKB', is_hymn_book=True)
        song = songs.Song.objects.create(
            book=self.songbook, number=43, title='Sinar Matahari Pagi')
        songs.Verse.objects.create(song=song, number=1, lyric='Sinar matahari pagi')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, order_number=4,
            song=song, verses=[1])

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

    def _context(self, width=1920, height=1080):
        return self.browser.new_context(viewport={'width': width, 'height': height})

    def _projector(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + f'/projector?service={self.service.pk}')
        page.wait_for_selector('.screen')
        return page

    def _active(self, page):
        return page.evaluate(
            "() => [...document.querySelectorAll('.screen')]"
            ".findIndex(s => s.classList.contains('is-active'))")

    def _press(self, page, key, meta=False, ctrl=False, shift=False):
        """Dispatch the chord the way Chromium would, and report whether the page took
        the key (its handler called preventDefault) or left it to the browser."""
        return page.evaluate(
            """([key, meta, ctrl, shift]) => {
                 const event = new KeyboardEvent('keydown', {
                   key, metaKey: meta, ctrlKey: ctrl, shiftKey: shift, bubbles: true,
                   cancelable: true});
                 document.dispatchEvent(event);
                 return event.defaultPrevented;
               }""", [key, meta, ctrl, shift])

    def _sheet(self, page):
        page.keyboard.press('k')
        page.wait_for_function("() => document.body.classList.contains('keys-open')")
        return page.evaluate("""() => {
          const stacks = [...document.querySelectorAll('#key-list .stack')];
          const read = (stack) => [...stack.querySelectorAll('.group')].map(g => ({
            title: g.querySelector('h3').textContent.trim(),
            rows: [...g.querySelectorAll('.row .fn')].map(r => r.textContent.trim()),
            height: g.getBoundingClientRect().height
          }));
          const el = document.getElementById('key-list');
          const box = el.getBoundingClientRect();
          const rows = [...el.querySelectorAll('.row')];
          const last = rows[rows.length - 1];
          return {
            columns: stacks.map(read),
            groups: stacks.map(read),
            height: box.height,
            stackX: stacks.map(s => Math.round(s.getBoundingClientRect().x)),
            scrollWidth: el.scrollWidth,
            clientWidth: el.clientWidth,
            overflows: el.scrollHeight > el.clientHeight + 1,
            lastRowBottom: last ? last.getBoundingClientRect().bottom : 0,
            bottom: box.bottom
          };
        }""")

    # ---------- the sheet is the top layer ------------------------------------

    def test_the_corner_cue_stays_out_of_the_sheet(self):
        context = self._context(900, 900)
        projector = self._projector(context)
        projector.mouse.move(450, 400)                  # wake the cue
        projector.wait_for_timeout(300)
        projector.wait_for_function(
            "() => getComputedStyle(document.getElementById('corner-cue')).visibility"
            " === 'visible'", timeout=4000)

        projector.keyboard.press('k')
        projector.wait_for_function("() => document.body.classList.contains('keys-open')")
        projector.wait_for_timeout(300)
        cue = projector.evaluate("""() => {
          const el = document.getElementById('corner-cue');
          const style = getComputedStyle(el);
          return {visibility: style.visibility, opacity: style.opacity,
                  z: style.zIndex};
        }""")
        self.assertEqual(cue['visibility'], 'hidden',
                         f"the cue is still drawn over the sheet: {cue}")
        self.assertEqual(cue['opacity'], '0')

        projector.keyboard.press('k')
        projector.mouse.move(450, 400)
        projector.wait_for_timeout(300)
        projector.wait_for_function(
            "() => getComputedStyle(document.getElementById('corner-cue')).visibility"
            " === 'visible'", timeout=4000)
        context.close()

    # ---------- US7: Meta is a modifier --------------------------------------

    def test_meta_and_control_take_the_same_step(self):
        context = self._context()
        projector = self._projector(context)
        self.assertEqual(self._active(projector), 0)
        self.assertTrue(self._press(projector, 'ArrowRight', ctrl=True),
                        'Ctrl+Right was left to the browser')
        projector.wait_for_timeout(150)
        by_control = self._active(projector)
        self.assertGreater(by_control, 0, 'Ctrl+Right did not step an entry')

        projector.reload()
        projector.wait_for_selector('.screen')
        self.assertTrue(self._press(projector, 'ArrowRight', meta=True),
                        'Meta+Right was left to the browser')
        projector.wait_for_timeout(150)
        self.assertEqual(self._active(projector), by_control,
                         'Meta+Right landed somewhere Ctrl+Right does not')

        projector.reload()
        projector.wait_for_selector('.screen')
        self.assertTrue(self._press(projector, 'End', meta=True))
        projector.wait_for_timeout(150)
        meta_end = self._active(projector)
        projector.reload()
        projector.wait_for_selector('.screen')
        self.assertTrue(self._press(projector, 'End', ctrl=True))
        projector.wait_for_timeout(150)
        self.assertEqual(self._active(projector), meta_end,
                         'Meta+End landed somewhere Ctrl+End does not')
        context.close()

    def test_meta_with_a_letter_leaves_the_browser_its_shortcut(self):
        context = self._context()
        projector = self._projector(context)
        for key in ('t', 'c', 'k', 'f', 'g', ' '):
            self.assertFalse(self._press(projector, key, meta=True),
                             f'Meta+{key!r} was swallowed by the projector')
        corner_hidden = projector.evaluate(
            "() => document.body.classList.contains('corner-hidden')")
        self.assertFalse(corner_hidden, 'Meta+C hid the corner')
        self.assertFalse(projector.evaluate(
            "() => document.body.classList.contains('keys-open')"), 'Meta+K opened the sheet')
        context.close()

    # ---------- US9: one Display group and one Find group --------------------

    def test_the_sheet_carries_one_display_group_and_one_find_group(self):
        context = self._context()
        projector = self._projector(context)
        sheet = self._sheet(projector)
        titles = [group['title'] for column in sheet['columns'] for group in column]
        self.assertEqual(titles.count('Display'), 1, titles)
        self.assertEqual(titles.count('Find'), 1, titles)
        self.assertNotIn('While Finding', titles)
        self.assertNotIn('Fullscreen', titles)

        display = next(group for column in sheet['columns'] for group in column
                       if group['title'] == 'Display')
        self.assertEqual(display['rows'], DISPLAY_ORDER)
        find = next(group for column in sheet['columns'] for group in column
                    if group['title'] == 'Find')
        self.assertEqual(find['rows'], FIND_ORDER)
        context.close()

    def test_audio_and_video_are_one_group_in_the_left_column(self):
        context = self._context()
        projector = self._projector(context)
        sheet = self._sheet(projector)
        left, middle, right = sheet['columns']
        self.assertEqual([group['title'] for group in left],
                         ['Service', 'Song', 'Image and PDF', 'Audio and Video'])
        self.assertEqual([group['title'] for group in middle],
                         ['Passage', 'Library Detour'])
        self.assertEqual([group['title'] for group in right], ['Display', 'Find'])
        self.assertEqual(left[-1]['rows'], ['Play/Pause'])
        context.close()

    def test_the_passage_group_merges_verses_chapters_and_books(self):
        context = self._context()
        projector = self._projector(context)
        sheet = self._sheet(projector)
        middle = sheet['columns'][1]
        self.assertEqual(middle[0]['title'], 'Passage')
        self.assertEqual(middle[0]['rows'], [
            'Flip TB / SIM', 'First Verse', 'Last Verse',
            'Next Chapter', 'Previous Chapter', 'First Chapter', 'Last Chapter',
            'Next Book', 'Previous Book', 'First Book', 'Last Book'])
        titles = [group['title'] for column in sheet['columns'] for group in column]
        self.assertNotIn('Library passage', titles, 'the old group is still drawn')
        self.assertEqual(titles.count('Passage'), 1)
        context.close()

    def test_a_narrow_window_draws_one_scrolling_column(self):
        context = self._context(900, 900)
        projector = self._projector(context)
        sheet = self._sheet(projector)
        self.assertEqual(len(set(sheet['stackX'])), 1,
                         f"the sheet kept its columns at 900 px: {sheet['stackX']}")
        self.assertLessEqual(sheet['scrollWidth'], sheet['clientWidth'] + 1,
                             'the single column was cut at the frame')
        self.assertTrue(sheet['overflows'], 'the one column does not scroll')
        self.assertEqual([group['title'] for column in sheet['columns'] for group in column],
                         ['Service', 'Song', 'Image and PDF', 'Audio and Video',
                          'Passage', 'Library Detour', 'Display', 'Find'])
        # The scrollbar is the app's own, as the dock's sheet draws it (spec 087).
        bar = projector.evaluate("""() => {
          const el = document.getElementById('key-list');
          return {width: getComputedStyle(el, '::-webkit-scrollbar').width,
                  thumb: getComputedStyle(el, '::-webkit-scrollbar-thumb').backgroundColor,
                  standard: getComputedStyle(el).scrollbarWidth};
        }""")
        self.assertEqual(bar['width'], '5px', 'the sheet paints the platform scrollbar')
        self.assertEqual(bar['thumb'], 'rgb(69, 65, 58)', 'the thumb is not the app token')
        self.assertEqual(bar['standard'], 'auto',
                         'the standard property must stay gated off in Blink')
        context.close()

    def test_the_sheet_measures_its_tallest_column_and_scrolls_at_720(self):
        context = self._context(1920, 1080)
        projector = self._projector(context)
        sheet = self._sheet(projector)
        # The frame follows its tallest column: that column's groups, its gaps, and the
        # sheet's own 20 px padding and 1 px border (FR-014).
        tallest = max(sum(group['height'] for group in column) + 24 * (len(column) - 1)
                      for column in sheet['groups'])
        self.assertAlmostEqual(sheet['height'], tallest + 40 + 2, delta=3,
                               msg=f"the sheet is {sheet['height']} px, its tallest column"
                                   f" needs {tallest} px")
        self.assertFalse(sheet['overflows'], 'the sheet scrolls at 1080p')
        context.close()

        context = self._context(1280, 720)
        projector = self._projector(context)
        sheet = self._sheet(projector)
        self.assertLessEqual(sheet['height'], 720 - 32 + 1)
        # A row is never out of reach: the sheet either fits it or scrolls to it.
        self.assertTrue(sheet['overflows'] or sheet['lastRowBottom'] <= sheet['bottom'] + 1,
                        'the sheet clipped a row at 720p')
        context.close()
