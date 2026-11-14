"""A passage and a song carry their own kind mark (spec 144).

The stage marks a media row with a 42px tinted chip. A passage and a song get a 20px
glyph of their own instead — on the media chip's centre line and on the media title's
column, so one left rail holds every kind — and nothing else on the page may move.

The mark is decorative: it states the kind a second time, in a shape, beside the words
the row already carries.
"""
from datetime import date
import math
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from multimedia.tatib.models import MediaIdentity

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

# The width a 1440px window leaves the stage with both sidebars open; the pane below that
# is where the media column costs a song its line.
TEXT_ROW = ('.tatib__item:not(.tatib__item--media)'
            ':not(.tatib__item--scripture):not(.tatib__item--song)')


def _rgb(value):
    """'rgb(100, 99, 87)' or 'rgba(31, 31, 29, 0.08)' -> (r, g, b, a)."""
    numbers = [float(part) for part in value[value.index('(') + 1:value.rindex(')')].split(',')]
    return (*numbers[:3], numbers[3] if len(numbers) > 3 else 1.0)


def _over(foreground, background):
    """Paint an rgba onto an opaque rgb, the way the browser composites the hover fill."""
    *fg, alpha = foreground
    return tuple(fg[i] * alpha + background[i] * (1 - alpha) for i in range(3))


def _luminance(rgb):
    channels = []
    for value in rgb:
        channel = value / 255
        channels.append(channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def _contrast(first, second):
    high, low = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class StageKindMarksE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        matius = bible.BookTranslation.objects.create(version=version, book=book, translation='Matius')
        for number in (2, 3):
            bible.Verse.objects.create(book_translation=matius, chapter=5, verse=number,
                                       text=f'ayat {number}')

        hymn_book = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                              is_hymn_book=True)
        short_song = songs.Song.objects.create(book=hymn_book, number=152,
                                               title='Jahowa Sihol Pujionku')
        long_song = songs.Song.objects.create(book=hymn_book, number=7,
                                              title='Porini Dong Marribu Hali')
        for song in (short_song, long_song):
            for number in (1, 2, 3):
                songs.Verse.objects.create(song=song, number=number, lyric=f'bait {number}')

        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=matius, chapter=5, verse_start=2, verse_end=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia beserta kita semua.')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.SONG,
            song=short_song, verses=[1, 2])
        media = MediaIdentity.objects.create(sha256='b' * 64, byte_count=2048,
                                             family='pdf', display_filename='service.pdf')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=4, kind=tatib.ServiceEntryKind.MEDIA,
            media=media, title='Tingting')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=5, kind=tatib.ServiceEntryKind.SONG,
            song=long_song, verses=[1, 3])

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        self.open()

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open(self):
        self.page.goto(self.live_server_url
                       + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_load_state('networkidle')

    # -- helpers ---------------------------------------------------------

    def rows(self):
        return self.page.locator('.tatib__item')

    def row(self, kind):
        return self.page.locator(f'.tatib__item--{kind}').first

    def mark(self, kind):
        return self.row(kind).locator('.entry__kind-icon')

    def glyph(self, kind):
        """The path data a row's mark draws, so two marks can be compared as shapes."""
        return self.mark(kind).evaluate(
            "el => [...el.querySelectorAll('svg *')]"
            ".map(node => node.getAttribute('d') || '')"
            ".join('|')")

    def tops(self):
        return self.page.evaluate(
            "() => [...document.querySelectorAll('.tatib__item, .tatib__eos')]"
            ".map(el => Math.round((el.getBoundingClientRect().top + window.scrollY) * 10) / 10)")

    # -- US1: the kinds are told apart by the mark -----------------------

    def test_a_passage_row_carries_the_passage_mark(self):
        mark = self.mark('scripture')
        expect(mark).to_have_count(1)
        self.assertEqual(mark.get_attribute('data-kind-icon'), 'scripture')
        self.assertEqual(mark.evaluate('el => getComputedStyle(el).display'), 'grid')

    def test_a_song_row_carries_the_song_mark(self):
        marks = self.rows().locator('.entry__kind-icon')
        self.assertEqual(self.page.locator('.tatib__item--song .entry__kind-icon').count(), 2)
        self.assertNotEqual(self.glyph('scripture'), self.glyph('song'))
        self.assertTrue(self.glyph('song'))
        expect(marks.first).to_be_visible()

    def test_only_passage_and_song_rows_are_marked(self):
        self.assertEqual(self.page.locator('.entry__kind-icon').count(), 3)
        self.assertEqual(self.page.locator('.tatib__item--media .entry__kind-icon').count(), 0)
        self.assertEqual(self.page.locator(TEXT_ROW + ' .entry__kind-icon').count(), 0)

    def test_a_text_row_carries_no_mark(self):
        text_row = self.page.locator(TEXT_ROW)
        expect(text_row).to_have_count(1)
        self.assertEqual(text_row.locator('.entry__kind-icon').count(), 0)
        # and its own body keeps the row's 12px edge, so a text row is untouched
        self.assertEqual(text_row.evaluate('el => getComputedStyle(el).paddingLeft'), '12px')

    # -- US2: a media file is never mistaken for a passage or a song -----

    def test_the_mark_is_not_a_media_chip(self):
        # The chip's family ink is --focus only while the local library answers; with the
        # library down it turns neutral, and its size and fill are then the whole difference.
        # So the library is made to answer here, and the comparison is made in that state.
        self.page.route('http://127.0.0.1:63174/**', lambda route: route.fulfill(
            status=200, content_type='application/json',
            body='{"files": [{"sha256": "%s"}]}' % ('b' * 64),
            headers={'Access-Control-Allow-Origin': self.live_server_url}))
        self.open()
        self.page.wait_for_function(
            "() => !document.querySelector('.tatib__item--media')"
            ".classList.contains('is-unavailable')")
        mark = self.mark('scripture')
        chip = self.row('media').locator('.entry__media-icon')
        expect(chip).to_have_count(1)
        mark_box, chip_box = mark.bounding_box(), chip.bounding_box()
        self.assertEqual((mark_box['width'], mark_box['height']), (20, 20))
        self.assertEqual((chip_box['width'], chip_box['height']), (42, 42))
        self.assertEqual(mark.evaluate('el => getComputedStyle(el).backgroundColor'),
                         'rgba(0, 0, 0, 0)')
        self.assertNotEqual(chip.evaluate('el => getComputedStyle(el).backgroundColor'),
                            'rgba(0, 0, 0, 0)')
        self.assertNotEqual(mark.evaluate('el => getComputedStyle(el).color'),
                            chip.evaluate('el => getComputedStyle(el).color'))

    def test_the_mark_holds_contrast_in_both_themes(self):
        canvas = {'light': (247, 245, 241), 'dark': (20, 19, 15)}
        for theme, background in canvas.items():
            self.page.evaluate('(theme) => document.documentElement.dataset.theme = theme', theme)
            colour = _rgb(self.mark('scripture').evaluate('el => getComputedStyle(el).color'))
            self.assertGreaterEqual(_contrast(colour, background), 4.5, (theme, 'on the canvas'))
            # the hover fill the row takes while pointed at
            self.page.evaluate(
                "(id) => document.querySelector(id).classList.add('is-modal-origin')",
                '#ti-' + self.row('scripture').get_attribute('id').split('-')[-1])
            fill = _rgb(self.row('scripture').evaluate('el => getComputedStyle(el).backgroundColor'))
            hovered = _over(fill, background) if fill[3] < 1 else fill[:3]
            self.assertGreaterEqual(_contrast(colour, hovered), 4.5, (theme, 'on the hover fill'))

    def test_the_sidebar_and_dock_keep_their_own_rows(self):
        self.assertEqual(self.page.locator('#chList .entry__kind-icon').count(), 0)
        dock = self.browser.new_page()
        try:
            dock.goto(self.live_server_url + reverse('web-obs-dock'))
            dock.wait_for_load_state('networkidle')
            self.assertEqual(dock.locator('.entry__kind-icon').count(), 0)
        finally:
            dock.close()

    # -- US3: the stage keeps its rhythm and its text column -------------

    def test_a_passage_row_keeps_its_56px_box(self):
        row = self.row('scripture')
        box = row.bounding_box()
        self.assertAlmostEqual(box['height'], 56, delta=0.5)
        heading = row.locator('.read__sec').bounding_box()
        self.assertAlmostEqual(box['y'] + box['height'] / 2,
                               heading['y'] + heading['height'] / 2, delta=1)
        # the heading's margin is still flattened: a mark in the section's first seat
        # would give it the 30px pericope margin back and the row would measure 69.8px
        self.assertEqual(row.locator('.read__sec').evaluate('el => getComputedStyle(el).marginTop'),
                         '0px')

    def test_no_other_block_moves(self):
        with_mark = self.tops()
        self.page.add_style_tag(content='.entry__kind-icon{display:none} '
                                         '.tatib__item--scripture,.tatib__item--song{padding-left:12px}')
        without_mark = self.tops()
        self.assertEqual(len(with_mark), len(without_mark))
        # The only permitted difference is a song title wrapping: the media column is
        # 250px where the row's own padding left 302px, so the long hymn gains one line.
        for before, after in zip(without_mark, with_mark):
            self.assertIn(round(after - before, 1), (0.0, 23.8), (before, after))

    def test_the_declared_wraps_at_the_400px_pane(self):
        pane = self.page.locator('.read__body').bounding_box()
        self.assertAlmostEqual(pane['width'], 400, delta=2)
        for kind in ('scripture', 'song'):
            self.assertEqual(self.row(kind).evaluate('el => getComputedStyle(el).paddingLeft'),
                             '64px', kind)
        heading = self.row('song').locator('.read__sec').bounding_box()
        self.assertAlmostEqual(heading['height'], 47.6, delta=1, msg='the long hymn wraps')
        passage = self.row('scripture').locator('.read__sec').bounding_box()
        self.assertAlmostEqual(passage['height'], 23.8, delta=1, msg='the passage stays one line')

        wide = self.browser.new_page(viewport={'width': 1920, 'height': 900})
        try:
            wide.goto(self.live_server_url
                      + reverse('web-tatib-service', args=[self.service.pk]))
            wide.wait_for_load_state('networkidle')
            self.assertEqual(wide.locator('.read__body').evaluate('el => el.clientWidth'), 880)
            one_line = wide.locator('.tatib__item--song .read__sec').first.bounding_box()
            self.assertAlmostEqual(one_line['height'], 23.8, delta=1, msg='no wrap at 1920')
        finally:
            wide.close()

    def test_the_mark_is_decorative(self):
        mark = self.mark('scripture')
        self.assertEqual(mark.get_attribute('aria-hidden'), 'true')
        self.assertEqual(mark.inner_text(), '')
        self.assertEqual(mark.evaluate('el => getComputedStyle(el).pointerEvents'), 'none')
        heading = self.row('scripture').locator('.read__sec')
        self.assertEqual(heading.inner_text().strip(), 'Matius 5:2-3')
