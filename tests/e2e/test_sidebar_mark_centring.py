"""A service entry's kind mark shares its number's vertical centre (spec 237).

The mark is the decorative column after the order number in the reading sidebar's
contents list. Its box centre must match the row's centre exactly as the number's does,
including when the label wraps and on the drag copy's source markup.
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


MEASURE = """() => [...document.querySelectorAll('#chList a.songrow')].map(a => {
  const n = a.querySelector('.songrow__c'), m = a.querySelector('.songrow__mark');
  const t = a.querySelector('.songrow__t'), b = a.querySelector('.slot__badge');
  const r = a.getBoundingClientRect();
  const centre = box => +(box.top + box.height / 2 - r.top - r.height / 2).toFixed(2);
  const mb = m && m.getBoundingClientRect(), nb = n && n.getBoundingClientRect();
  const tb = t && t.getBoundingClientRect(), bb = b && b.getBoundingClientRect();
  const line = t && parseFloat(getComputedStyle(t).lineHeight);
  return {kind: m ? m.dataset.mark : null,
          title: t ? t.innerText.trim().slice(0, 40) : null,
          rowH: +r.height.toFixed(2),
          number: nb ? centre(nb) : null,
          mark: mb ? centre(mb) : null,
          markX: mb ? +(mb.left - r.left).toFixed(2) : null,
          markW: mb ? +mb.width.toFixed(2) : null,
          labelX: tb ? +(tb.left - r.left).toFixed(2) : null,
          lines: tb && line ? +(tb.height / line).toFixed(2) : null,
          badgeBottom: bb ? +(r.bottom - bb.bottom).toFixed(2) : null,
          badgeX: bb ? +(bb.left - r.left).toFixed(2) : null,
          align: m ? getComputedStyle(m).alignSelf : null};
})"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SidebarMarkCentringE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date='2026-11-24', is_active=True)
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=5, verse=1, text='ayat satu')
        book_songs = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        song = songs.Song.objects.create(
            book=book_songs, number=7, title='Ya Tuhan, Kami Puji NamaMu Besar')
        for number in range(1, 4):
            songs.Verse.objects.create(song=song, number=number, lyric=f'Bait {number}')
        verses = list(song.verse_set.values_list('pk', flat=True))

        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1, title='Votum',
            text='Pertolongan kita')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SCRIPTURE, order_number=2,
            book_translation=translation, chapter=5, verse_start=1, verse_end=1)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, order_number=3,
            song=song, verses=verses)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=4,
            title='Beauty of the Lord')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.FILL_IN, order_number=5,
            title='Fill-in · Song', fill_kind=tatib.SlotKind.SONG)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.CHOICE, order_number=6,
            title='Choice · Passage', fill_kind=tatib.SlotKind.SCRIPTURE)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SECTION_BREAK, order_number=7)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=8,
            title='A long service text that wraps across several lines in a pane')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch(
                executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        except Exception as error:
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1366, 'height': 900}, device_scale_factor=1)

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open_service(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_load_state('networkidle')
        self.page.evaluate("() => document.documentElement.dataset.theme = 'dark'")

    def rows(self):
        return self.page.evaluate(MEASURE)

    def row(self, kind):
        return next(row for row in self.rows() if row['kind'] == kind)

    def test_mark_centre_matches_number_on_every_row(self):
        self.open_service()
        rows = [row for row in self.rows() if row['mark'] is not None]
        self.assertGreaterEqual(len(rows), 6)
        for row in rows:
            self.assertAlmostEqual(row['number'], 0, delta=1, msg=row)
            self.assertAlmostEqual(row['mark'], 0, delta=1, msg=row)

    def test_columns_heights_and_clamp_are_unchanged(self):
        self.open_service()
        for row in self.rows():
            if row['mark'] is None:
                continue
            self.assertAlmostEqual(row['markX'], 42, delta=1, msg=row)
            self.assertAlmostEqual(row['labelX'], 66, delta=1, msg=row)
            self.assertAlmostEqual(row['markW'], 16, delta=0.5, msg=row)
            self.assertLessEqual(row['lines'], 3.05, msg=row)
            self.assertAlmostEqual(row['mark'], row['number'], delta=1, msg=row)
        self.assertAlmostEqual(self.row('text')['rowH'], 38, delta=1)
        self.assertAlmostEqual(self.row('song')['rowH'], 53, delta=2)

    def test_wrapped_song_row_keeps_centred_mark(self):
        self.open_service()
        self.page.set_viewport_size({'width': 390, 'height': 900})
        self.page.wait_for_timeout(50)
        song = self.row('song')
        self.assertGreater(song['rowH'], 53, msg=song)
        self.assertAlmostEqual(song['mark'], 0, delta=1, msg=song)
        self.assertAlmostEqual(song['number'], 0, delta=1, msg=song)
        self.assertAlmostEqual(song['markX'], 42, delta=1, msg=song)
        self.assertLessEqual(song['lines'], 3.05, msg=song)

    def test_slot_badge_follows_the_mark(self):
        self.open_service()
        for kind in ('fill_in', 'choice'):
            row = self.row(kind)
            self.assertAlmostEqual(row['badgeBottom'], 9, delta=1, msg=row)
            self.assertAlmostEqual(row['badgeX'], 50, delta=1, msg=row)
