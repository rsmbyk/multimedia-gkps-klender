"""The rail says what each section is, and its marks are the stage's own (spec 151).

Four marks are decided here: the rail's Bible (an open book with a Latin cross), the rail's
service order (a clipboard), the note a song wears (the rail's own beamed pair), and an audio
file (a waveform, so a media file stops wearing the song's mark).

A mark is compared as its *drawing*: every child node of its inline SVG, serialised with its
geometry attributes. Two marks that draw the same shape serialise identically at any size, which
is what "the rail and the stage draw one mark" means. The media families this slice must leave
alone are pinned as their shipped strings.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from multimedia.tatib.models import MediaIdentity

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

DESTINATIONS = ('Search', 'Alkitab', 'Kidung', 'Tata Ibadah', 'Media Library')

# The other media families, exactly as `static/web/media-stage.js` ships them at 24a6d6d2.
SHIPPED_FAMILIES = {
    'image': ('<rect x="3" y="4" width="18" height="16" rx="2"/>'
              '<circle cx="8.5" cy="9" r="1.5"/>'
              '<path d="m4 17 5-5 3.5 3.5 2.5-2.5 5 5"/>'),
    'video': ('<rect x="3" y="5" width="18" height="15" rx="2"/><path d="M3 10h18M7 5l3 5m4-5 3 5"/>'
              '<path d="m10 12 5 3-5 3z"/>'),
    'pdf': '<path d="M6 2h8l5 5v15H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM14 2v5h5M8 16h8M8 19h6"/>',
    'slides': ('<rect x="3" y="4" width="18" height="14" rx="2"/>'
               '<path d="M12 18v3m-4 0h8M7 9h10M7 12h7"/>'),
    'missing': ('<path d="M6 2h8l5 5v8M14 2v5h5M4 5v15a2 2 0 0 0 2 2h7"/>'
                '<circle cx="18" cy="18" r="4"/><path d="M18 16v2m0 2h.01"/>'),
}

AUDIO_WAVEFORM = 'M3.6 10.2v3.6M7.2 7.2v9.6M10.8 4.4v15.2M14.4 7.2v9.6M18 10.2v3.6'

# Every child of a mark's <svg>, as `tag|attribute=value,…` — geometry only, so the same path
# serialises identically whether the product draws it at 24px or at 20px.
MARK = ("el => [...el.children].map(node => node.tagName + '|' + "
        "[...node.attributes].map(a => a.name + '=' + a.value).sort().join(','))")

PARSE = ("markup => { const host = document.createElement('div'); "
         "host.innerHTML = /^<svg/i.test(markup.trim()) ? markup : '<svg>' + markup + '</svg>'; "
         "return [...host.querySelectorAll('svg > *')].map(node => node.tagName + '|' + "
         "[...node.attributes].map(a => a.name + '=' + a.value).sort().join(',')); }")


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RailMarksE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Kis', testament='new', number_of_chapters=28)
        kisah = bible.BookTranslation.objects.create(version=version, book=book,
                                                     translation='Kisah Para Rasul')
        for number in (1, 2, 3):
            bible.Verse.objects.create(book_translation=kisah, chapter=1, verse=number,
                                       text=f'ayat {number}')

        hymn_book = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        hymn = songs.Song.objects.create(book=hymn_book, number=1, title='Jahowa Sihol')
        for number in (1, 2):
            songs.Verse.objects.create(song=hymn, number=number, lyric=f'bait {number}')

        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=kisah, chapter=1, verse_start=1, verse_end=1)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.SONG,
            song=hymn, verses=[1])
        media = MediaIdentity.objects.create(sha256='a' * 64, byte_count=2048,
                                             family='audio', display_filename='lagu.mp3')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.MEDIA,
            media=media, title='Lagu')
        self.empty = tatib.TataIbadah.objects.create(
            name='Ibadah Kosong', date=date(2026, 10, 11), is_active=True)

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        # The local media companion is a boundary: answer it so the stage's chip is drawn the same
        # way on every run, instead of waiting on a container that may be busy.
        self.page.route('http://127.0.0.1:63174/**', lambda route: route.fulfill(
            status=200, content_type='application/json',
            body='{"files": [{"sha256": "%s"}]}' % ('a' * 64),
            headers={'Access-Control-Allow-Origin': self.live_server_url}))
        self.open(self.service)
        self.page.wait_for_function(
            "() => document.querySelector('.tatib__item--media .entry__media-icon svg') !== null")

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open(self, service):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[service.pk]))
        self.page.wait_for_load_state('load')

    # -- helpers ---------------------------------------------------------

    def rail(self, destination):
        return self.page.locator(f'.rail__menu .rail__btn[aria-label="{destination}"]')

    def rail_mark(self, destination):
        return self.rail(destination).locator('svg').evaluate(MARK)

    def kind_mark(self, kind):
        return self.page.locator(f'.tatib__item--{kind} .entry__kind-icon').first

    def kind_mark_paths(self, kind):
        return self.kind_mark(kind).locator('svg').evaluate(MARK)

    def tile_mark(self, label):
        return self.page.locator(f'.entry__empty-btn[title="{label}"] svg').evaluate(MARK)

    def family_mark(self, family):
        return self.page.evaluate(PARSE, self.page.evaluate(
            '(family) => window.gkpsMediaIcon(family)', family))

    def chip_mark(self):
        return self.page.locator('.tatib__item--media .entry__media-icon svg').first.evaluate(MARK)

    def token(self, name):
        """The computed colour of a custom property, read off a probe element."""
        return self.page.evaluate(
            """(name) => {
                const probe = document.createElement('span');
                probe.style.color = `var(${name})`;
                document.body.appendChild(probe);
                const colour = getComputedStyle(probe).color;
                probe.remove();
                return colour;
            }""", name)

    @staticmethod
    def drawn(mark):
        """The `d` values inside a serialised mark, for shape assertions."""
        return [node.split('d=', 1)[1] for node in mark if 'd=' in node]

    # -- US1: the Bible, in the rail and on a passage --------------------

    def test_the_rail_bible_and_a_passage_draw_one_path(self):
        bible_mark = self.rail_mark('Alkitab')
        self.assertEqual(len(bible_mark), 3, bible_mark)

        drawn = self.drawn(bible_mark)
        self.assertTrue(drawn[0].startswith('M12 9.6'), drawn[0])     # the open book
        self.assertEqual(drawn[1], 'M12 9.6v10.4')                     # its gutter
        self.assertIn('M12 2.6v4.6', drawn[2])                         # the cross's stem
        self.assertIn('M10.1 4.5h3.8', drawn[2])                       # its bar: a Latin cross

        self.assertEqual(self.kind_mark_paths('scripture'), bible_mark)

        self.open(self.empty)
        self.assertEqual(self.tile_mark('Add Passage'), bible_mark)

    # -- US2: the service order is not a file ----------------------------

    def test_the_rail_service_is_a_clipboard(self):
        board = self.rail_mark('Tata Ibadah')
        self.assertEqual(len(board), 3, board)
        rects = [node for node in board if node.startswith('rect|')]
        self.assertEqual(rects, ['rect|height=17.2,rx=2,width=14.8,x=4.6,y=3.4',
                                 'rect|height=3.4,rx=1.4,width=6.8,x=8.6,y=1.9'])
        self.assertEqual(self.drawn(board), ['M8.2 9.6h7.6M8.2 13h7.6M8.2 16.4h4.8'])

        # the shipped page-with-three-lines is gone, and the mark is not the PDF family's page
        self.assertNotIn('M8.6 8.8h6.8', ' '.join(self.drawn(board)))
        self.assertNotEqual(board, self.family_mark('pdf'))

    # -- US3: one note for a song, a waveform for a file -----------------

    def test_the_rail_note_and_a_song_draw_one_path(self):
        note = self.rail_mark('Kidung')
        self.assertEqual(len(note), 3, note)                           # one stem+beam, two heads
        self.assertTrue(note[0].endswith('M9 17.4V5.6l10.2-2v11.6'), note[0])
        self.assertEqual(self.kind_mark_paths('song'), note)

        self.open(self.empty)
        self.assertEqual(self.tile_mark('Add Song'), note)

    def test_an_audio_file_is_a_waveform_in_every_place_it_is_drawn(self):
        waveform = 'path|d=' + AUDIO_WAVEFORM
        self.assertEqual(self.family_mark('audio'), [waveform])
        self.assertEqual(self.chip_mark(), [waveform])
        self.assertNotEqual(self.family_mark('audio'), self.kind_mark_paths('song'))

        for family, markup in SHIPPED_FAMILIES.items():
            self.assertEqual(self.family_mark(family), self.page.evaluate(PARSE, markup), family)

    # -- US4: five marks, five shapes; nothing else moves -----------------

    def test_the_five_rail_marks_are_five_shapes_and_none_is_a_media_family(self):
        shapes = {destination: tuple(self.rail_mark(destination)) for destination in DESTINATIONS}
        self.assertEqual(len(set(shapes.values())), 5, shapes)
        self.assertTrue(all(shapes.values()), shapes)

        families = set()
        for family in ('image', 'audio', 'video', 'pdf', 'slides', 'missing'):
            families.update(self.family_mark(family))
        for destination, mark in shapes.items():
            self.assertFalse(set(mark) & families,
                             f'{destination} draws a media family\'s own node')

    def test_the_marks_keep_their_boxes(self):
        buttons = self.page.evaluate(
            """() => [...document.querySelectorAll('.rail__menu .rail__btn')]
                .map(b => {
                    const box = b.getBoundingClientRect();
                    const glyph = b.querySelector('svg').getBoundingClientRect();
                    return [Math.round(box.width), Math.round(box.height),
                            Math.round(glyph.width), Math.round(glyph.height),
                            Math.round(glyph.x - box.x)];
                })""")
        self.assertEqual(buttons, [[44, 44, 24, 24, 10]] * 5, buttons)

        row = self.page.locator('.tatib__item--scripture').bounding_box()
        mark = self.kind_mark('scripture').bounding_box()
        title = self.page.locator('.tatib__item--scripture .read__sec').bounding_box()
        self.assertEqual((mark['width'], mark['height']), (20, 20))
        self.assertAlmostEqual(mark['x'] - row['x'], 24, delta=0.5)
        self.assertAlmostEqual(title['x'] - row['x'], 64, delta=0.5)
        self.assertAlmostEqual(row['height'], 56, delta=0.5)

        media = self.page.locator('.tatib__item--media').bounding_box()
        chip = self.page.locator('.tatib__item--media .entry__media-icon').bounding_box()
        glyph = self.page.locator('.tatib__item--media .entry__media-icon svg').bounding_box()
        self.assertEqual((chip['width'], chip['height']), (42, 42))
        self.assertAlmostEqual(chip['x'] - media['x'], 13, delta=0.5)
        self.assertEqual((glyph['width'], glyph['height']), (23, 23))
        self.assertAlmostEqual(media['height'], 80, delta=0.5)

    def test_the_marks_keep_their_ink_in_both_themes(self):
        for theme in ('light', 'dark'):
            self.page.evaluate('(theme) => document.documentElement.dataset.theme = theme', theme)
            # the token transition runs on colour; read after it settles, not during
            self.page.evaluate('() => Promise.all(document.getAnimations()'
                               '.map(a => a.finished.catch(() => null)))')
            for destination in DESTINATIONS:
                svg, button = self.rail(destination).locator('svg'), self.rail(destination)
                self.assertEqual(svg.evaluate('el => getComputedStyle(el).color'),
                                 button.evaluate('el => getComputedStyle(el).color'), destination)
                self.assertEqual(svg.get_attribute('aria-hidden'), 'true')

            self.assertEqual(self.kind_mark('song').evaluate('el => getComputedStyle(el).color'),
                             self.token('--head-ink'))
            chip = self.page.locator('.tatib__item--media .entry__media-icon')
            self.assertEqual(chip.locator('svg').evaluate('el => getComputedStyle(el).color'),
                             self.token('--focus'))

        self.assertEqual(self.page.locator('.entry__kind-icon').count(), 2)
        self.assertEqual(self.page.locator('.entry__kind-icon').first.get_attribute('aria-hidden'),
                         'true')
