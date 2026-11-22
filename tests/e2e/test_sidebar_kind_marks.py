"""A service entry's contents row marks its kind (spec 214).

The mark is a second column after the order number, in the reading sidebar's
contents list only. It is decorative: the row's words are its accessible name.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


def _rgb(value):
    value = value.strip()
    if value.startswith('#'):
        return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))
    numbers = [float(part) for part in value[value.index('(') + 1:value.rindex(')')].split(',')]
    return (*numbers[:3], numbers[3] if len(numbers) > 3 else 1.0)


def _luminance(rgb):
    channels = []
    for value in rgb[:3]:
        channel = value / 255
        channels.append(channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def _contrast(first, second):
    high, low = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SidebarKindMarksE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date='2026-11-22', is_active=True)
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=5, verse=1, text='ayat satu')
        book_songs = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        song = songs.Song.objects.create(book=book_songs, number=1, title='HAL 7 — Porini Dong Marribu Hali')
        self.song_pk = song.pk
        for number in range(1, 4):
            songs.Verse.objects.create(song=song, number=number, lyric=f'Bait {number}')
        verses = list(song.verse_set.values_list('pk', flat=True))

        self.entries = {}
        self.entries['text'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita')
        self.entries['scripture'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SCRIPTURE, order_number=2,
            book_translation=translation, chapter=5, verse_start=1, verse_end=1)
        self.entries['song'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, order_number=3,
            song=song, verses=verses)
        self.entries['media'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=4,
            title='Beauty of the Lord')
        self.entries['fill_in'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.FILL_IN, order_number=5,
            title='Fill-in · Song', fill_kind=tatib.SlotKind.SONG)
        self.entries['choice'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.CHOICE, order_number=6,
            title='Choice · Passage', fill_kind=tatib.SlotKind.SCRIPTURE)
        self.entries['break'] = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SECTION_BREAK, order_number=7)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=8,
            title='A very long title that wraps across several lines in the pane')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open_service(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_load_state('networkidle')

    def marks(self):
        return self.page.locator('#chList .songrow__mark')

    def test_passage_and_song_rows_carry_their_marks(self):
        self.open_service()
        passage = self.page.locator('#chList a[data-i="e%d"] .songrow__mark' % self.entries['scripture'].pk)
        song = self.page.locator('#chList a[data-i="e%d"] .songrow__mark' % self.entries['song'].pk)
        self.assertEqual(passage.get_attribute('data-mark'), 'scripture')
        self.assertEqual(song.get_attribute('data-mark'), 'song')

    def test_text_and_media_rows_carry_their_marks(self):
        self.open_service()
        for key, expected in (('text', 'text'), ('media', 'media')):
            row = self.page.locator('#chList a[data-i="e%d"] .songrow__mark' % self.entries[key].pk)
            self.assertEqual(row.get_attribute('data-mark'), expected)

    def test_slot_rows_keep_the_kind_modifier(self):
        self.open_service()
        for key, kind, badge in (
            ('fill_in', 'fill_in', 'song'), ('choice', 'choice', 'scripture')):
            mark = self.page.locator('#chList a[data-i="e%d"] .songrow__mark' % self.entries[key].pk)
            self.assertEqual(mark.get_attribute('data-mark'), kind)
            badge_el = mark.locator('.slot__badge')
            self.assertEqual(badge_el.get_attribute('data-kind-badge'), badge)
            self.assertEqual(badge_el.locator('> svg').count(), 1)

    def test_row_accessible_name_is_unchanged(self):
        self.open_service()
        row = self.page.locator('#chList a.songrow').first
        name = row.evaluate('el => el.textContent.trim()')
        row.locator('.songrow__mark').evaluate('el => el.setAttribute("aria-hidden", "true")')
        self.assertEqual(row.evaluate('el => el.textContent.trim()'), name)
        self.assertTrue(row.locator('.songrow__mark [aria-hidden="true"]').count() >= 1)

    def test_mark_takes_no_pointer(self):
        self.open_service()
        style = self.marks().first.evaluate(
            'el => { const s = getComputedStyle(el); return [s.pointerEvents, el.tabIndex]; }')
        self.assertIn(style[0], ('none', 'auto'))
        self.assertNotEqual(style[1], 0)

    def test_focus_never_lands_on_the_mark(self):
        self.open_service()
        self.assertEqual(self.page.locator('#chList .songrow__mark [tabindex]').count(), 0)
        self.assertEqual(self.page.locator('#chList .songrow__mark button, #chList .songrow__mark a').count(), 0)

    def test_number_centre_and_row_heights_hold(self):
        self.open_service()
        data = self.page.evaluate("""() => [...document.querySelectorAll('#chList a.songrow')].map(a => {
          const r = a.getBoundingClientRect(), n = a.querySelector('.songrow__c').getBoundingClientRect();
          return {row: r.height, centre: n.top + n.height / 2 - r.top - r.height / 2,
                  x: n.left - r.left, w: n.width};
        })""")
        self.assertGreater(len(data), 3)
        for row in data:
            self.assertAlmostEqual(row['x'], 10, delta=1)
            self.assertAlmostEqual(row['centre'], 0, delta=1)
            self.assertAlmostEqual(row['w'], 24, delta=1)

    def test_column_sits_between_number_and_label(self):
        self.open_service()
        data = self.page.evaluate("""() => [...document.querySelectorAll('#chList a.songrow')].map(a => {
          const n = a.querySelector('.songrow__c').getBoundingClientRect(),
                m = a.querySelector('.songrow__mark').getBoundingClientRect(),
                t = a.querySelector('.songrow__t').getBoundingClientRect();
          return [n.right, m.left, m.right, t.left];
        })""")
        for number_right, mark_left, mark_right, text_left in data:
            self.assertGreaterEqual(mark_left, number_right)
            self.assertGreaterEqual(text_left, mark_right)

    def test_three_line_clamp_and_pane_wrap_hold(self):
        self.open_service()
        data = self.page.evaluate("""() => [...document.querySelectorAll('#chList a.songrow')].map(a => {
          const t = a.querySelector('.songrow__t'), r = a.getBoundingClientRect();
          return {lines: t.getBoundingClientRect().height / parseFloat(getComputedStyle(t).lineHeight),
                  overflow: document.documentElement.scrollWidth > window.innerWidth,
                  textRight: t.getBoundingClientRect().right, rowRight: r.right};
        })""")
        self.assertTrue(all(row['lines'] <= 3.05 for row in data))
        self.assertFalse(any(row['overflow'] for row in data))
        self.assertTrue(all(row['textRight'] <= row['rowRight'] + 1 for row in data))

    def test_contrast_in_both_themes(self):
        self.open_service()
        for theme in ('light', 'dark'):
            self.page.evaluate('(t) => document.documentElement.dataset.theme = t', theme)
            pair = self.page.evaluate("""() => {
              const cs = getComputedStyle(document.documentElement);
              return [cs.getPropertyValue('--head-ink').trim(), cs.getPropertyValue('--canvas').trim()];
            }""")
            self.assertGreaterEqual(_contrast(_rgb(pair[0]), _rgb(pair[1])), 4.5)

    def test_dock_and_projector_keep_their_own_rows(self):
        self.open_service()
        stage_marks = self.page.locator('#read .entry__kind-icon').count()
        self.assertGreater(stage_marks, 0)
        self.page.goto(self.live_server_url + reverse('web-obs-dock'))
        self.page.wait_for_load_state('networkidle')
        self.assertEqual(self.page.locator('#chList .songrow__mark').count(), 0)

    def test_mark_column_at_drawer_and_phone_widths(self):
        self.open_service()
        for width in (1024, 390):
            self.page.set_viewport_size({'width': width, 'height': 900})
            data = self.page.evaluate("""() => [...document.querySelectorAll('#chList a.songrow')].map(a => {
              const m = a.querySelector('.songrow__mark').getBoundingClientRect();
              const n = a.querySelector('.songrow__c').getBoundingClientRect();
              return Math.round(m.left - n.right);
            })""")
            self.assertTrue(all(gap >= 0 for gap in data))
            self.assertEqual(len(data), 7)
