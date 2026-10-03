"""The service entry model (spec 006, slice 1).

Its rules, its citation, and what it resolves to for the display. The legacy item
model is exercised alongside, because both have to work in the same service.
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


class ServiceEntryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tatib = tatib.TataIbadah.objects.create(name='Ibadah Minggu III')

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        cls.matius = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        for number in (13, 14, 15):
            bible.Verse.objects.create(book_translation=cls.matius, chapter=5, verse=number,
                                       text=f'ayat {number}')

        s_lang = songs.Language.objects.create(name='Indonesian')
        cls.songbook = songs.Book.objects.create(lang=s_lang, name='Kidung Jemaat',
                                                 short_name='KJ', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.songbook, number=152, title='Ada Kuasa')
        for number in (1, 2, 3):
            songs.Verse.objects.create(song=cls.song, number=number, lyric=f'bait {number}')

    def _entry(self, **fields):
        entry = tatib.ServiceEntry(tatib=self.tatib, order_number=1, **fields)
        entry.full_clean()
        return entry

    # --- each kind resolves to a title and a body ---------------------------

    def test_a_text_entry_resolves_to_its_title_and_text(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='Kasih karunia')
        self.assertEqual(entry.resolve(), ('Salam', 'Kasih karunia'))

    def test_a_section_break_resolves_to_its_label_and_no_body(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SECTION_BREAK, title='PAMUNGKAHNI')
        self.assertEqual(entry.resolve(), ('PAMUNGKAHNI', ''))

    def test_a_scripture_entry_cites_its_range_and_joins_its_verses(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                            chapter=5, verse_start=13, verse_end=14)
        title, body = entry.resolve()
        self.assertEqual(title, 'Matius 5:13-14')
        self.assertEqual(body, '13 ayat 13\n\n14 ayat 14')

    def test_a_single_verse_passage_cites_one_number(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                            chapter=5, verse_start=13)
        self.assertEqual(entry.citation(), 'Matius 5:13')
        self.assertEqual(entry.resolve()[1], '13 ayat 13')

    def test_a_song_entry_resolves_only_the_verses_it_includes(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 3])
        title, body = entry.resolve()
        self.assertEqual(title, 'Kidung Jemaat 152')
        self.assertEqual(body, 'bait 1\n\nbait 3')            # verse 2 is left out

    def test_a_verse_added_to_the_song_later_is_not_in_an_existing_entry(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2, 3])
        songs.Verse.objects.create(song=self.song, number=4, lyric='bait 4')
        self.assertEqual(entry.resolve()[1], 'bait 1\n\nbait 2\n\nbait 3')

    def test_a_lyric_edit_reaches_a_prepared_entry(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1])
        songs.Verse.objects.filter(song=self.song, number=1).update(lyric='bait satu (baru)')
        self.assertEqual(entry.resolve()[1], 'bait satu (baru)')

    # --- the rules ----------------------------------------------------------

    def test_a_passage_needs_a_book_a_chapter_and_a_starting_verse(self):
        cases = [
            {'book_translation': self.matius, 'chapter': None, 'verse_start': 13},
            {'book_translation': self.matius, 'chapter': 5, 'verse_start': None},
            {'book_translation': None, 'chapter': 5, 'verse_start': 13},
        ]
        for fields in cases:
            with self.subTest(fields=fields):
                with self.assertRaises(ValidationError):
                    self._entry(kind=tatib.ServiceEntryKind.SCRIPTURE, **fields)

    def test_an_ending_verse_cannot_precede_the_starting_one(self):
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                        chapter=5, verse_start=14, verse_end=13)

    def test_a_song_entry_needs_a_song(self):
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.SONG, verses=[1])

    def test_a_song_entry_keeps_at_least_one_verse(self):
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[])

    def test_a_section_break_needs_a_label(self):
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.SECTION_BREAK, title='')

    # --- ordering, and living beside the legacy rows ------------------------

    def test_entries_are_ordered_within_their_service(self):
        second = tatib.ServiceEntry.objects.create(tatib=self.tatib, order_number=2,
                                                   kind=tatib.ServiceEntryKind.TEXT, text='b')
        first = tatib.ServiceEntry.objects.create(tatib=self.tatib, order_number=1,
                                                  kind=tatib.ServiceEntryKind.TEXT, text='a')
        self.assertEqual([e.pk for e in self.tatib.service_entries.all()], [first.pk, second.pk])

    def test_a_service_can_hold_both_legacy_items_and_entries(self):
        tatib.TataIbadahItem.objects.create(tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
                                            title='lama', text='teks lama', order_number=1)
        self._entry(kind=tatib.ServiceEntryKind.TEXT, title='baru', text='teks baru').save()
        self.assertEqual(self.tatib.tataibadahitem_set.count(), 1)
        self.assertEqual(self.tatib.service_entries.count(), 1)
