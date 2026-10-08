"""The service entry model (spec 006, slice 1).

Its rules, its citation, and what it resolves to for the display. The legacy item
model is exercised alongside, because both have to work in the same service.
"""

from django.core.exceptions import ValidationError
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APITestCase

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

        cls.songbook = songs.Book.objects.create(name='Kidung Jemaat',
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

    def test_a_deleted_song_remains_resolvable_and_is_marked_for_warning(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2])
        self.song.delete()
        self.assertEqual(entry.resolve(), ('Kidung Jemaat 152', 'bait 1\n\nbait 2'))
        self.assertTrue(entry.target_deleted)

    def test_a_deleted_included_verse_is_omitted_and_warned(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2])
        songs.Verse.objects.get(song=self.song, number=2).delete()
        self.assertEqual(entry.resolve(), ('Kidung Jemaat 152', 'bait 1'))
        self.assertTrue(entry.target_deleted)

    def test_a_deleted_songbook_is_detected_through_its_song(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1])
        self.songbook.delete()
        self.assertEqual(entry.resolve()[1], 'bait 1')
        self.assertTrue(entry.target_deleted)

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

    def test_a_text_entry_needs_its_text(self):
        # an empty text entry has nothing to show; the header alone is not one
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='   ')

    def test_a_section_break_may_be_unlabelled(self):
        # the owner's correction: a break is a break, its label is optional
        entry = self._entry(kind=tatib.ServiceEntryKind.SECTION_BREAK, title='')
        self.assertEqual(entry.resolve(), ('', ''))

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


class LegacyTatibApiCompatibilityTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = tatib.TataIbadah.objects.create(name='Legacy service')
        cls.first = tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Opening', text='Legacy text', order_number=1)
        cls.second = tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.END_OF_SECTION,
            title='End', text='', order_number=2)

    def test_legacy_tatib_list_keeps_its_route_and_payload_fields(self):
        response = self.client.get('/api/tatib/tatibs')
        self.assertEqual(response.status_code, 200)
        rows = response.json()
        service = next(row for row in rows if row['id'] == self.service.pk)
        self.assertEqual(set(service), {'id', 'name', 'date', 'is_active', 'created_at'})

    def test_legacy_item_list_keeps_its_route_and_payload_fields(self):
        response = self.client.get('/api/tatib/items', {'tatib': self.service.pk})
        self.assertEqual(response.status_code, 200)
        rows = response.json()
        self.assertEqual([row['id'] for row in rows], [self.first.pk, self.second.pk])
        self.assertEqual(set(rows[0]), {
            'id', 'tatib', 'item_type', 'title', 'text', 'order_number',
        })

    def test_legacy_reorder_action_keeps_its_route_and_response(self):
        response = self.client.post('/api/tatib/items/reorder', {
            'items': [
                {'item': self.first.pk, 'order_number': 2},
                {'item': self.second.pk, 'order_number': 1},
            ],
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'items': [
            {'item': self.first.pk, 'order_number': 2},
            {'item': self.second.pk, 'order_number': 1},
        ]})
        self.first.refresh_from_db()
        self.second.refresh_from_db()
        self.assertEqual((self.first.order_number, self.second.order_number), (2, 1))


class UnifiedServiceOrderMigrationTests(TransactionTestCase):
    """The migration preserves today's old-rows-then-entries reading order."""

    migrate_from = [('tatib', '0005_serviceentry')]
    migrate_to = [('tatib', '0006_unified_service_order')]

    def migrate(self, targets):
        executor = MigrationExecutor(connection)
        executor.migrate(targets)
        return executor.loader.project_state(targets).apps

    def setUp(self):
        super().setUp()
        old_apps = self.migrate(self.migrate_from)
        TataIbadah = old_apps.get_model('tatib', 'TataIbadah')
        LegacyItem = old_apps.get_model('tatib', 'TataIbadahItem')
        ServiceEntry = old_apps.get_model('tatib', 'ServiceEntry')
        service = TataIbadah.objects.create(name='Existing service')
        self.service_id = service.pk
        self.old_ids = [
            LegacyItem.objects.create(tatib=service, item_type=0, title='Opening',
                                      text='First legacy row', order_number=4).pk,
            LegacyItem.objects.create(tatib=service, item_type=0, title='Closing',
                                      text='Second legacy row', order_number=9).pk,
        ]
        self.entry_ids = [
            ServiceEntry.objects.create(tatib=service, kind=0, title='Hymn',
                                        text='First entry', order_number=1).pk,
            ServiceEntry.objects.create(tatib=service, kind=0, title='Prayer',
                                        text='Second entry', order_number=3).pk,
        ]
        self.apps = self.migrate(self.migrate_to)

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_existing_legacy_order_is_kept_and_entries_follow_it(self):
        LegacyItem = self.apps.get_model('tatib', 'TataIbadahItem')
        ServiceEntry = self.apps.get_model('tatib', 'ServiceEntry')
        self.assertEqual(
            list(LegacyItem.objects.filter(tatib_id=self.service_id)
                 .order_by('order_number').values_list('pk', 'order_number')),
            [(self.old_ids[0], 1), (self.old_ids[1], 2)],
        )
        self.assertEqual(
            list(ServiceEntry.objects.filter(tatib_id=self.service_id)
                 .order_by('order_number').values_list('pk', 'order_number')),
            [(self.entry_ids[0], 3), (self.entry_ids[1], 4)],
        )