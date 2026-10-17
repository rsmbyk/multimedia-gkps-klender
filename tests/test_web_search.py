"""Public search rules (spec 004).

Covers the cross-corpus search module: query normalization, any-non-empty
query policy, reference resolution (Bible + songs, full name = abbreviation),
the ranking ladder, grouping, and what is *not* indexed (End-of-section notes,
inactive or empty services).
"""

from datetime import date

from django.test import SimpleTestCase, TestCase

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from multimedia.web.reading.search import normalize, search, search_page


class QueryRulesTests(SimpleTestCase):
    def test_normalize_folds_case_diacritics_and_space(self):
        self.assertEqual(normalize('  Y\u00e9sus   K\u00c9KASIH! '), 'yesus kekasih!')
        self.assertEqual(normalize(None), '')

    def test_empty_queries_are_not_searched(self):
        for query in ('', '   '):
            with self.subTest(query=query):
                result = search(query)
                self.assertFalse(result.valid)
                self.assertEqual(result.total, 0)
                self.assertEqual(result['bible'], [])
                self.assertEqual(result['songs'], [])
                self.assertEqual(result['tatib'], [])


class CorpusSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # --- Bible ---
        lang_id = bible.Language.objects.create(name='Indonesia')
        lang_sim = bible.Language.objects.create(name='Simalungun')
        cls.tb = bible.Version.objects.create(lang=lang_id, name='Terjemahan Baru', abbreviation='TB')
        sim = bible.Version.objects.create(lang=lang_sim, name='Simalungun', abbreviation='SIM')
        cls.mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        kej = bible.Book.objects.create(name='Kej', testament='old', number_of_chapters=50)
        mat_tb = bible.BookTranslation.objects.create(version=cls.tb, book=cls.mat, translation='Matius')
        mat_sim = bible.BookTranslation.objects.create(version=sim, book=cls.mat, translation='Mateus')
        kej_tb = bible.BookTranslation.objects.create(version=cls.tb, book=kej, translation='Kejadian')
        kej_sim = bible.BookTranslation.objects.create(
            version=sim, book=kej, translation='1 Musa', abbreviation='1Mu')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=13,
                                   text='Kamu adalah garam dunia. Jika garam itu menjadi tawar, dengan apakah ia diasinkan?')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=14,
                                   text='Kamu adalah terang dunia. Kota yang terletak di atas gunung tidak mungkin tersembunyi.')
        bible.Verse.objects.create(book_translation=mat_sim, chapter=5, verse=13,
                                   text='Hamu do garam ni dunia, tapi anggo naung tawar sira i, aha ma bahen paasom?')
        bible.Verse.objects.create(book_translation=kej_tb, chapter=1, verse=1,
                                   text='Pada mulanya Allah menciptakan langit dan bumi.')
        bible.Verse.objects.create(book_translation=kej_sim, chapter=1, verse=1,
                                   text='Bani mula ni mulani itompa Naibata.')

        # --- Songs ---
        song_lang = None
        kj = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        pkj = songs.Book.objects.create(name='Pelengkap Kidung Jemaat', short_name='PKJ', is_hymn_book=True)
        cls.kj120 = songs.Song.objects.create(book=kj, number=120, title='Sebab Kasih-Nya Kekal')
        songs.Verse.objects.create(song=cls.kj120, number=1, lyric='Kasih setia-Mu tak berkesudahan, ya Tuhan')
        songs.Verse.objects.create(song=cls.kj120, number=2, lyric='Pagi hari aku bersyukur pada-Mu')
        cls.kj152 = songs.Song.objects.create(book=kj, number=152, title='Bila Kuperhatikan')
        songs.Verse.objects.create(song=cls.kj152, number=1, lyric='Di dalam Dia ada pengampunan dosa')
        cls.kj100 = songs.Song.objects.create(book=kj, number=100, title='Kasih')
        songs.Verse.objects.create(song=cls.kj100, number=1, lyric='Kasih itu sabar, kasih itu murah hati')
        cls.pkj120 = songs.Song.objects.create(book=pkj, number=120, title='Kasih Jemaat Terpilih')
        songs.Verse.objects.create(song=cls.pkj120, number=1, lyric='Pujilah Tuhan, hai jemaat')
        harian = songs.Book.objects.create(name='Kidung Harian', short_name='', is_hymn_book=False)
        cls.harian_song = songs.Song.objects.create(book=harian, number=None, title='Doa Pagi')
        songs.Verse.objects.create(song=cls.harian_song, number=1, lyric='Kasih setia setiap hari')

        # --- Tata Ibadah ---
        cls.svc = tatib.TataIbadah.objects.create(name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        cls.item_open = tatib.TataIbadahItem.objects.create(
            tatib=cls.svc, item_type=tatib.TataIbadahItemType.TEXT, title='Nyanyian Pembukaan', text='KJ 120', order_number=1)
        cls.item_doa = tatib.TataIbadahItem.objects.create(
            tatib=cls.svc, item_type=tatib.TataIbadahItemType.TEXT, title='Doa Pengampunan',
            text='Tuhan ampunilah dosa kami', order_number=2)
        tatib.TataIbadahItem.objects.create(
            tatib=cls.svc, item_type=tatib.TataIbadahItemType.END_OF_SECTION,
            title='', text='Catatan: hubungi pendeta', order_number=3)
        cls.svc2 = tatib.TataIbadah.objects.create(name='Ibadah Keluarga', date=None, is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=cls.svc2, item_type=tatib.TataIbadahItemType.TEXT, title='Renungan',
            text='Kasih Allah tidak berkesudahan', order_number=1)
        hidden = tatib.TataIbadah.objects.create(name='Ibadah Khusus', date=None, is_active=False)
        tatib.TataIbadahItem.objects.create(
            tatib=hidden, item_type=tatib.TataIbadahItemType.TEXT, title='', text='rahasia', order_number=1)
        tatib.TataIbadah.objects.create(name='Ibadah Tanpa Isi', date=None, is_active=True)

    @staticmethod
    def targets(rows, key='song_id'):
        return [row['target'][key] for row in rows]

    # --- Bible ---

    def test_bible_reference_resolves_first(self):
        result = search('Matius 5:13')
        first = result['bible'][0]
        self.assertEqual(first['title'], 'Matius 5:13')
        self.assertEqual(first['target'],
                         {'book_id': self.mat.id, 'chapter': 5, 'verse': 13, 'end_verse': 13})
        self.assertTrue(result.valid)

    def test_bible_reference_accepts_alias_and_case(self):
        for query in ('mat 5:13', 'MATEUS 5:13'):
            with self.subTest(query=query):
                first = search(query)['bible'][0]
                self.assertEqual(first['target']['book_id'], self.mat.id)
                self.assertEqual(first['target']['verse'], 13)

    def test_bible_reference_range_marks_both_verses(self):
        first = search('Matius 5:13-14')['bible'][0]
        self.assertEqual(first['title'], 'Matius 5:13\u201314')
        self.assertEqual(first['target']['end_verse'], 14)

    def test_bible_chapter_reference(self):
        first = search('Kejadian 1')['bible'][0]
        self.assertEqual(first['title'], 'Kejadian 1')
        self.assertIsNone(first['target']['verse'])

    def test_bible_reference_accepts_sim_abbreviation(self):
        first = search('1Mu 1')['bible'][0]
        self.assertEqual(first['target']['chapter'], 1)
        self.assertEqual(first['target']['book_id'], bible.Book.objects.get(name='Kej').pk)

    def test_bible_book_name_row(self):
        rows = search('matius')['bible']
        self.assertEqual(rows[0]['kind'], 'book')
        self.assertEqual(rows[0]['title'], 'Matius')
        self.assertIn('Mateus', rows[0]['meta'])

    def test_bible_verse_text_dedupes_translations(self):
        rows = [row for row in search('garam')['bible'] if row['target']['verse'] == 13]
        self.assertEqual(len(rows), 1)
        self.assertIn('garam dunia', rows[0]['excerpt'])
        # both translations contain "dunia": still one row per verse, TB preferred
        rows = [row for row in search('dunia')['bible'] if row['target']['verse'] == 13]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['meta'], 'TB')

    # --- Songs ---

    def test_song_reference_full_name_equals_abbreviation(self):
        by_abbr = search('KJ 120')
        by_name = search('Kidung Jemaat 120')
        by_name_lower = search('kidung jemaat 120')
        first = by_abbr['songs'][0]
        self.assertEqual(first['target']['song_id'], self.kj120.id)
        self.assertEqual(first['meta'], 'KJ 120')
        self.assertEqual(self.targets(by_name['songs'])[0], self.kj120.id)
        self.assertEqual(self.targets(by_name_lower['songs'])[0], self.kj120.id)
        self.assertNotIn(self.pkj120.id, self.targets(by_name['songs']))

    def test_song_ranking_title_exact_then_prefix_then_substring(self):
        ids = self.targets(search('kasih')['songs'])
        self.assertEqual(ids[:3], [self.kj100.id, self.pkj120.id, self.kj120.id])

    def test_song_lyric_excerpt(self):
        rows = search('pengampunan dosa')['songs']
        self.assertEqual(rows[0]['target']['song_id'], self.kj152.id)
        self.assertIn('pengampunan dosa', rows[0]['excerpt'])

    def test_non_hymn_songbooks_are_searchable(self):
        rows = search('setia setiap hari')['songs']
        self.assertIn(self.harian_song.id, self.targets(rows))

    def test_multiword_scattered_match(self):
        rows = search('dosa pengampunan')['songs']
        self.assertIn(self.kj152.id, self.targets(rows))

    # --- Tata Ibadah ---

    def test_tatib_item_search(self):
        rows = search('pengampunan')['tatib']
        row = next(r for r in rows if r['title'] == 'Doa Pengampunan')
        self.assertEqual(row['meta'], 'Ibadah Minggu III \u00b7 Section 2')
        self.assertEqual(row['target'], {'tatib_id': self.svc.id, 'item_order': 2})

    def test_tatib_service_name_search_formats_date(self):
        rows = search('ibadah minggu')['tatib']
        self.assertEqual(rows[0]['title'], 'Ibadah Minggu III')
        self.assertEqual(rows[0]['meta'], '23 Agu 2026')

    def test_tatib_excludes_private_inactive_and_empty(self):
        self.assertEqual(search('hubungi pendeta')['tatib'], [])
        self.assertEqual(search('rahasia')['tatib'], [])
        self.assertEqual(search('tanpa isi')['tatib'], [])

    # --- shape ---

    def test_groups_and_total(self):
        result = search('kasih')
        self.assertEqual(list(result.groups.keys()), ['bible', 'songs', 'tatib'])
        self.assertEqual(result.total, sum(len(rows) for rows in result.groups.values()))

    def test_no_results(self):
        result = search('zzzqqq')
        self.assertTrue(result.valid)
        self.assertEqual(result.total, 0)

    def test_short_query_is_searched(self):
        result = search('di')
        self.assertTrue(result.valid)
        self.assertGreater(result.total, 0)


class PageSearchTests(TestCase):
    """The public search page's matcher (spec 104).

    Only the six listed fields match; book names, songbook names and references, bare
    numbers, dates, section labels, and non-text entry bodies never do. Entry rows are
    indexed for the first time, and a service built only from entries can be found by
    its own name.
    """

    @classmethod
    def setUpTestData(cls):
        # --- Bible ---
        lang_id = bible.Language.objects.create(name='Indonesia')
        cls.tb = bible.Version.objects.create(
            lang=lang_id, name='Terjemahan Baru', abbreviation='TB')
        cls.mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        kej = bible.Book.objects.create(name='Kej', testament='old', number_of_chapters=50)
        mat_tb = bible.BookTranslation.objects.create(
            version=cls.tb, book=cls.mat, translation='Matius')
        kej_tb = bible.BookTranslation.objects.create(
            version=cls.tb, book=kej, translation='Kejadian')
        bible.Verse.objects.create(
            book_translation=mat_tb, chapter=5, verse=13,
            text='Kamu adalah garam dunia. Jika garam itu menjadi tawar, dengan apakah ia diasinkan?')
        bible.Verse.objects.create(
            book_translation=kej_tb, chapter=1, verse=1,
            text='Pada mulanya Allah menciptakan langit dan bumi.')
        bible.Verse.objects.create(
            book_translation=mat_tb, chapter=5, verse=3, title='Ucapan bahagia',
            text='Berbahagialah orang yang miskin di hadapan Allah.')

        # --- Songs ---
        kj = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        pkj = songs.Book.objects.create(
            name='Pelengkap Kidung Jemaat', short_name='PKJ', is_hymn_book=True)
        cls.kj100 = songs.Song.objects.create(book=kj, number=100, title='Kasih')
        songs.Verse.objects.create(song=cls.kj100, number=1, lyric='Kasih itu sabar')
        cls.pkj120 = songs.Song.objects.create(book=pkj, number=120, title='Kasih Jemaat Terpilih')
        songs.Verse.objects.create(song=cls.pkj120, number=1, lyric='Pujilah Tuhan, hai jemaat')
        cls.kj120 = songs.Song.objects.create(book=kj, number=120, title='Sebab Kasih-Nya Kekal')
        songs.Verse.objects.create(
            song=cls.kj120, number=1, lyric='Kasih setia-Mu tak berkesudahan, ya Tuhan')
        cls.kj152 = songs.Song.objects.create(book=kj, number=152, title='Bila Kuperhatikan')
        songs.Verse.objects.create(song=cls.kj152, number=1, lyric='Di dalam Dia ada pengampunan dosa')
        cls.song99 = songs.Song.objects.create(book=kj, number=99, title='Nyanyian Khusus')
        songs.Verse.objects.create(song=cls.song99, number=1, lyric='Sungguh indah kasih Tuhan')

        # --- Tata Ibadah: one legacy service, one entry-only service ---
        cls.svc = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        cls.item = tatib.TataIbadahItem.objects.create(
            tatib=cls.svc, item_type=tatib.TataIbadahItemType.TEXT, title='Doa Pengampunan',
            text='Tuhan ampunilah dosa kami', order_number=2)
        cls.svc_entry_only = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=None, is_active=True)
        cls.votum = tatib.ServiceEntry.objects.create(
            tatib=cls.svc_entry_only, kind=tatib.ServiceEntryKind.TEXT, title='Votum',
            text='Marilah kita bangkit berdiri', order_number=1)
        cls.untitled = tatib.ServiceEntry.objects.create(
            tatib=cls.svc_entry_only, kind=tatib.ServiceEntryKind.TEXT, title='',
            text='Dikuduskanlah nama-Mu', order_number=2)
        cls.song_entry = tatib.ServiceEntry.objects.create(
            tatib=cls.svc, kind=tatib.ServiceEntryKind.SONG, song=cls.song99,
            verses=[1], order_number=3)
        cls.passage_entry = tatib.ServiceEntry.objects.create(
            tatib=cls.svc, kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=mat_tb,
            chapter=5, verse_start=13, verse_end=13, order_number=4)
        tatib.ServiceEntry.objects.create(
            tatib=cls.svc, kind=tatib.ServiceEntryKind.SECTION_BREAK, order_number=5)

    @staticmethod
    def targets(rows, key):
        return [row['target'][key] for row in rows]

    # --- the six fields still match ---

    def test_verse_text_matches(self):
        rows = search_page('garam dunia')['bible']
        self.assertEqual([row['target']['verse'] for row in rows], [13])
        self.assertEqual(rows[0]['kind'], 'verse')

    def test_verse_title_matches(self):
        rows = search_page('ucapan bahagia')['bible']
        self.assertEqual([row['target']['verse'] for row in rows], [3])

    def test_song_title_matches(self):
        rows = search_page('Bila Kuperhatikan')['songs']
        self.assertEqual(rows[0]['target']['song_id'], self.kj152.id)

    def test_song_lyric_matches(self):
        rows = search_page('pengampunan dosa')['songs']
        self.assertEqual(rows[0]['target']['song_id'], self.kj152.id)

    def test_song_ranking_title_exact_then_prefix_then_substring(self):
        ids = self.targets(search_page('kasih')['songs'], 'song_id')
        self.assertEqual(ids[:3], [self.kj100.id, self.pkj120.id, self.kj120.id])

    def test_service_name_matches(self):
        rows = search_page('Ibadah Minggu III')['tatib']
        self.assertEqual(rows[0]['title'], 'Ibadah Minggu III')

    def test_legacy_text_row_title_and_body_match(self):
        rows = search_page('pengampunan')['tatib']
        row = next(row for row in rows if row['title'] == 'Doa Pengampunan')
        self.assertEqual(row['meta'], 'Ibadah Minggu III \u00b7 Section 1')
        self.assertEqual(row['target'], {'tatib_id': self.svc.id, 'item_order': 2})

    def test_entry_title_and_text_match(self):
        rows = search_page('Votum')['tatib']
        row = next(row for row in rows
                   if row['target']['item_order'] == f'e{self.votum.pk}')
        self.assertEqual(row['title'], 'Votum')
        self.assertEqual(row['meta'], 'Ibadah Minggu \u00b7 Section 1')
        body_rows = search_page('bangkit berdiri')['tatib']
        self.assertIn(f'e{self.votum.pk}', self.targets(body_rows, 'item_order'))

    def test_untitled_entry_gets_the_section_fallback(self):
        rows = search_page('dikuduskanlah')['tatib']
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['title'], 'Ibadah Minggu \u00b7 Section 2')
        self.assertEqual(rows[0]['target']['item_order'], f'e{self.untitled.pk}')

    def test_entry_only_service_is_listed_by_its_name(self):
        rows = search_page('Ibadah Minggu')['tatib']
        listed = [row['target']['tatib_id'] for row in rows
                  if row['target']['item_order'] is None]
        self.assertIn(self.svc_entry_only.id, listed)

    def test_service_row_matches_only_its_name(self):
        rows = search_page('Doa Pengampunan')['tatib']
        self.assertTrue(rows)
        self.assertFalse([row for row in rows if row['target']['item_order'] is None])

    # --- excluded fields list nothing ---

    def test_bible_references_list_nothing(self):
        for query in ('Matius 5:13', 'Matius 5', 'Yoh 3:16'):
            with self.subTest(query=query):
                self.assertEqual(search_page(query)['bible'], [])

    def test_bible_book_name_lists_no_row(self):
        self.assertEqual(search_page('matius')['bible'], [])

    def test_songbook_name_lists_no_song(self):
        self.assertEqual(search_page('Kidung Jemaat')['songs'], [])

    def test_song_numbers_and_references_list_no_song(self):
        for query in ('152', 'KJ 152', 'Kidung Jemaat 152', 'HAL 411'):
            with self.subTest(query=query):
                self.assertEqual(search_page(query)['songs'], [])

    def test_service_date_and_section_label_list_nothing(self):
        self.assertEqual(search_page('23 Agu 2026')['tatib'], [])
        self.assertEqual(search_page('Section 2')['tatib'], [])

    def test_non_text_entry_bodies_list_nothing(self):
        # The song entry's lyric and the passage entry's verses are display bodies only.
        self.assertEqual(search_page('Sungguh indah')['tatib'], [])
        self.assertEqual(search_page('garam dunia')['tatib'], [])

    # --- shape ---

    def test_empty_query_is_not_searched(self):
        result = search_page('   ')
        self.assertFalse(result.valid)
        self.assertEqual(result.total, 0)

    def test_no_results(self):
        result = search_page('zzzqqq')
        self.assertTrue(result.valid)
        self.assertEqual(result.total, 0)

