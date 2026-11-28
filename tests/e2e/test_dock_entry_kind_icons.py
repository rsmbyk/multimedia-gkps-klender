"""Spec 250 — every service entry header states its kind in the dock.

The runner already ends each eligible header with an expand chevron. This module
pins the kind mark that sits immediately to its left: one glyph per row, drawn
from the product's own marks, hidden from assistive technology, without moving
the chevron out of its row. A break is a hairline, not a header, and stays bare.
"""

import unittest
from datetime import date

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


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockEntryKindIconE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Ikon', date=date(2026, 11, 29), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita')
        book_translation, song = self._passage_and_song()
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.SCRIPTURE,
            title='Firman', book_translation=book_translation, chapter=5,
            verse_start=1, verse_end=1)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.SONG,
            title='Pujian', song=song,
            verses=[song.verse_set.get(number=1).pk])
        media = tatib.MediaIdentity.objects.create(
            sha256='2' * 64, byte_count=120, family='image', display_filename='slide.png')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=4, kind=tatib.ServiceEntryKind.MEDIA,
            media=media, media_filename='slide.png', title='Gambar')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=5, kind=tatib.ServiceEntryKind.SECTION_BREAK,
            title='PEMUNGKAHNI')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    @staticmethod
    def _passage_and_song():
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=5, verse=1,
                                   text='Ketika Yesus melihat orang banyak itu,')
        songbook = songs.Book.objects.create(
            name='Nyanyian Kidung Baru', short_name='NKB', is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=43, title='Sinar Pagi')
        songs.Verse.objects.create(song=song, number=1, lyric='Sinar matahari pagi')
        return translation, song

    def tearDown(self):
        self._close_browser()
        super().tearDown()

    def _close_browser(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    def _dock(self):
        context = self.browser.new_context(viewport={'width': 420, 'height': 800})
        page = context.new_page()
        page.goto(self.live_server_url + '/obs/dock')
        page.locator(f'.servicerow[data-name="{self.service.name}"]').first.click()
        page.wait_for_selector('.entryrow')
        return context, page

    def test_every_kind_gets_its_own_mark_beside_the_chevron(self):
        """One mark per eligible header, of the right kind, left of the chevron."""
        context, dock = self._dock()
        try:
            rows = dock.evaluate("""() => [...document.querySelectorAll('.entryli')].map(li => {
                const row = li.querySelector('.entryrow');
                const icon = row.querySelector('.entryicon');
                const chev = row.querySelector('.entrychev');
                const box = row.getBoundingClientRect();
                const ib = icon && icon.getBoundingClientRect();
                const cb = chev && chev.getBoundingClientRect();
                return {index: li.dataset.index,
                        kind: icon && icon.dataset.kind,
                        glyphs: icon ? icon.querySelectorAll('svg > *').length : 0,
                        hidden: icon && icon.getAttribute('aria-hidden'),
                        chevron: !!chev && chev.getClientRects().length > 0,
                        gap: ib && cb ? cb.left - ib.right : null,
                        inRow: ib ? ib.left >= box.left - 0.5 && ib.right <= box.right + 0.5
                                    && ib.top >= box.top - 0.5 && ib.bottom <= box.bottom + 0.5
                                 : null};
            })""")
            by_index = {row['index']: row for row in rows if row['index'] != '4'}
            self.assertEqual(
                [row['kind'] for row in by_index.values()],
                ['text', 'passage', 'song', 'media'],
                f'each header should carry its own kind: {rows}')
            for row in by_index.values():
                self.assertGreater(row['glyphs'], 0, f'empty mark: {row}')
                self.assertEqual(row['hidden'], 'true', f'mark is exposed to AT: {row}')
                self.assertTrue(row['chevron'], f'no chevron beside the mark: {row}')
                self.assertIsNotNone(row['gap'], f'mark has no chevron to sit left of: {row}')
                self.assertGreaterEqual(row['gap'], 4, f'mark overlaps the chevron: {row}')
                self.assertLessEqual(row['gap'], 12, f'mark is not beside the chevron: {row}')
                self.assertTrue(row['inRow'], f'mark spills out of the header: {row}')
            break_row = next(row for row in rows if row['index'] == '4')
            self.assertIsNone(break_row['kind'], f'a break gained a mark: {break_row}')
            self.assertFalse(break_row['chevron'], 'a break gained a chevron')
        finally:
            context.close()

    def test_the_live_header_keeps_its_mark_without_a_chevron(self):
        """Projection hides the chevron but the header still states its kind."""
        context, dock = self._dock()
        try:
            dock.locator('.entryrow').first.click()
            dock.locator('.entryli[data-index="0"] .screenerow').first.click()
            dock.wait_for_function(
                """() => document.querySelector('.entryli[data-live="true"]') !== null""")
            live = dock.evaluate("""() => {
                const li = document.querySelector('.entryli[data-live="true"]');
                const icon = li.querySelector('.entryicon');
                const chev = li.querySelector('.entrychev');
                const row = li.querySelector('.entryrow').getBoundingClientRect();
                const ib = icon.getBoundingClientRect();
                return {kind: icon.dataset.kind, glyphs: icon.querySelectorAll('svg > *').length,
                        chevronShown: !!chev && chev.getClientRects().length > 0,
                        rightGap: row.right - ib.right,
                        colour: getComputedStyle(icon).color,
                        ink: getComputedStyle(li.querySelector('.entryrow')).color};
            }""")
            self.assertEqual(live['kind'], 'text', f'wrong live mark: {live}')
            self.assertGreater(live['glyphs'], 0)
            self.assertFalse(live['chevronShown'], 'the live row still shows a chevron')
            self.assertLessEqual(abs(live['rightGap'] - 10), 1,
                                 f'the live mark is no longer at the row edge: {live}')
            self.assertEqual(live['colour'], live['ink'],
                             f'the live mark lost the live ink: {live}')
        finally:
            context.close()
