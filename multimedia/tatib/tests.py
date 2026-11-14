"""The service entry model (spec 006, slice 1).

Its rules, its citation, and what it resolves to for the display. The legacy item
model is exercised alongside, because both have to work in the same service.
"""

import importlib
from datetime import date
from types import SimpleNamespace

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APITestCase

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from multimedia.tatib.screen_breaks import default_breaks, single_screen_boundaries, valid_breaks


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

    def test_one_text_kind_stores_either_default_screen_mode(self):
        multi = self._entry(kind=tatib.ServiceEntryKind.TEXT, text='one\ntwo')
        single = self._entry(kind=tatib.ServiceEntryKind.TEXT, text='one\ntwo',
                             default_screen_mode='single_screen', screen_breaks=[1])
        self.assertEqual(multi.default_screen_mode, 'multi_line')
        self.assertEqual(single.default_screen_mode, 'single_screen')
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.TEXT, text='one\ntwo',
                        default_screen_mode='custom')

    def test_screen_breaks_are_validated_against_written_lines_and_blank_boundaries(self):
        text = 'one\ntwo\nthree\n\nfour\nfive'
        self.assertEqual(default_breaks(text), [2])
        self.assertTrue(valid_breaks(text, [1, 5]))
        for breaks in ([3], [4], [1, 1], [2, 1], ['2'], [True], [0]):
            with self.subTest(breaks=breaks):
                self.assertFalse(valid_breaks(text, breaks))
        with self.assertRaises(ValidationError):
            self._entry(kind=tatib.ServiceEntryKind.TEXT, text=text, screen_breaks=[3])

    def test_single_screen_boundaries_can_cross_paragraph_spacing(self):
        text = 'one\ntwo\n\nthree\nfour'
        self.assertEqual(single_screen_boundaries(text), {1, 2, 4})
        self.assertTrue(valid_breaks(text, [2, 4], single_screen=True))
        self._entry(kind=tatib.ServiceEntryKind.TEXT, default_screen_mode='single_screen',
                    text=text, screen_breaks=[2, 4])
        for breaks in ([3], [5], [2, 2], [4, 2], [True]):
            with self.subTest(breaks=breaks):
                self.assertFalse(valid_breaks(text, breaks, single_screen=True))
                with self.assertRaises(ValidationError):
                    self._entry(kind=tatib.ServiceEntryKind.TEXT, default_screen_mode='single_screen',
                                text=text, screen_breaks=breaks)

    def test_a_section_break_resolves_to_nothing(self):
        # A break is a divider, not a titled entry (spec 038): any stored title is unused.
        entry = self._entry(kind=tatib.ServiceEntryKind.SECTION_BREAK, title='PAMUNGKAHNI')
        self.assertEqual(entry.resolve(), ('', ''))

    def test_media_entry_uses_library_filename_and_has_no_projected_body(self):
        media = tatib.MediaIdentity.objects.create(
            sha256='a' * 64, byte_count=1024, family='pdf', display_filename='notes.pdf')
        entry = self._entry(kind=tatib.ServiceEntryKind.MEDIA, media=media,
                            media_filename='notes.pdf')
        self.assertEqual(entry.resolve(), ('notes.pdf', ''))
        self.assertEqual(entry.media.sha256, 'a' * 64)

    def test_media_reference_cannot_be_replaced_after_creation(self):
        first = tatib.MediaIdentity.objects.create(
            sha256='a' * 64, byte_count=1024, family='pdf', display_filename='notes.pdf')
        second = tatib.MediaIdentity.objects.create(
            sha256='b' * 64, byte_count=1024, family='pdf', display_filename='other.pdf')
        entry = self._entry(kind=tatib.ServiceEntryKind.MEDIA, media=first,
                            media_filename='notes.pdf')
        entry.save()
        entry.title = 'New title'
        entry.full_clean()
        entry.save()
        entry.media = second
        with self.assertRaises(ValidationError):
            entry.full_clean()
        entry.media = first
        entry.media_filename = 'renamed.pdf'
        with self.assertRaises(ValidationError):
            entry.full_clean()
        entry.media_filename = 'notes.pdf'
        entry.kind = tatib.ServiceEntryKind.SECTION_BREAK
        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_image_projection_is_one_image_screen(self):
        from multimedia.web.reading.views import _projector_data
        media = tatib.MediaIdentity.objects.create(
            sha256='c' * 64, byte_count=42, family='image', display_filename='photo.png')
        self._entry(kind=tatib.ServiceEntryKind.MEDIA, media=media,
                    media_filename='photo.png').save()
        projector = _projector_data(self.tatib)
        screens, entries = projector['screens'], projector['entries']
        self.assertEqual(len(screens), 1)
        self.assertFalse(screens[0]['blank'])
        self.assertEqual(screens[0]['image_sha256'], media.sha256)
        self.assertEqual(entries[0]['type'], 'media')

    def test_media_edit_form_ignores_replacement_file(self):
        from multimedia.web.reading.entries import build_entry_form
        original = tatib.MediaIdentity.objects.create(
            sha256='a' * 64, byte_count=10, family='pdf', display_filename='notes.pdf')
        replacement = tatib.MediaIdentity.objects.create(
            sha256='b' * 64, byte_count=11, family='pdf', display_filename='other.pdf')
        entry = self._entry(kind=tatib.ServiceEntryKind.MEDIA, media=original,
                            media_filename='notes.pdf')
        entry.save()
        form = build_entry_form('media', data={'kind': str(tatib.ServiceEntryKind.MEDIA),
                                               'title': 'Edited', 'media': replacement.pk,
                                               'media_filename': 'other.pdf'}, instance=entry)
        self.assertTrue(form.is_valid(), form.errors)
        updated = form.save()
        self.assertEqual(updated.media_id, original.pk)
        self.assertEqual(updated.media_filename, 'notes.pdf')
        self.assertEqual(updated.title, 'Edited')

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

    def test_a_hymn_song_cites_its_short_reference_and_title(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1]])
        self.assertEqual(entry.citation(), 'KJ 152 — Ada Kuasa')

    def test_a_title_less_hymn_song_cites_its_short_reference_alone(self):
        song = songs.Song.objects.create(book=self.songbook, number=200, title='')
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=song, verses=[1])
        self.assertEqual(entry.citation(), 'KJ 200')

    def test_a_sub_numbered_hymn_song_keeps_its_sub_number(self):
        song = songs.Song.objects.create(book=self.songbook, number=90, sub_number='b',
                                         title='Nada Baru')
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=song, verses=[1])
        self.assertEqual(entry.citation(), 'KJ 90B — Nada Baru')

    def test_a_non_hymn_numbered_song_keeps_its_long_reference(self):
        book = songs.Book.objects.create(name='Lagu', short_name='LAGU')
        song = songs.Song.objects.create(book=book, number=7, title='Nyanyian')
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=song, verses=[1])
        self.assertEqual(entry.citation(), 'Lagu 7')

    def test_an_unnumbered_hymn_song_keeps_its_title(self):
        song = songs.Song.objects.create(book=self.songbook, number=None, title='Bukan Nomor')
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=song, verses=[1])
        self.assertEqual(entry.citation(), 'Bukan Nomor')

    def test_a_song_entry_resolves_only_the_verses_it_includes(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1, 3]])
        title, body = entry.resolve()
        self.assertEqual(title, 'KJ 152 — Ada Kuasa')        # short reference + title (spec 054)
        self.assertEqual(body, 'bait 1\n\nbait 3')            # verse 2 is left out

    def test_a_verse_added_to_the_song_later_is_not_in_an_existing_entry(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1, 2, 3]])
        songs.Verse.objects.create(song=self.song, number=4, lyric='bait 4')
        self.assertEqual(entry.resolve()[1], 'bait 1\n\nbait 2\n\nbait 3')

    def test_a_lyric_edit_reaches_a_prepared_entry(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1]])
        songs.Verse.objects.filter(song=self.song, number=1).update(lyric='bait satu (baru)')
        self.assertEqual(entry.resolve()[1], 'bait satu (baru)')

    def test_a_deleted_song_remains_resolvable_and_is_marked_for_warning(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1, 2]])
        self.song.delete()
        self.assertEqual(entry.resolve(), ('KJ 152 — Ada Kuasa', 'bait 1\n\nbait 2'))
        self.assertTrue(entry.target_deleted)

    def test_a_deleted_included_verse_is_omitted_and_warned(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1, 2]])
        songs.Verse.objects.get(song=self.song, number=2).delete()
        self.assertEqual(entry.resolve(), ('KJ 152 — Ada Kuasa', 'bait 1'))
        self.assertTrue(entry.target_deleted)

    def test_a_deleted_songbook_is_detected_through_its_song(self):
        entry = self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[self.song.verse_set.get(number=n).pk for n in [1]])
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
            self._entry(kind=tatib.ServiceEntryKind.SONG, verses=[self.song.verse_set.get(number=n).pk for n in [1]])

    def test_a_song_entry_keeps_at_least_one_verse(self):
        with self.assertRaises(ValidationError) as caught:
            self._entry(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[])
        self.assertEqual(caught.exception.message_dict['verses'],
                         ['Keep at least one verse in the service.'])

    def test_a_song_entry_with_no_verses_names_the_song(self):
        """A song that carries no verse is the cause; say so instead of 'keep one' (spec 162)."""
        empty = songs.Song.objects.create(book=self.songbook, number=901, title='Kosong')
        with self.assertRaises(ValidationError) as caught:
            self._entry(kind=tatib.ServiceEntryKind.SONG, song=empty, verses=[])
        self.assertEqual(caught.exception.message_dict['verses'],
                         ['This song has no verses: pick another song.'])

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


class UnifiedTextScreenModeMigrationTests(TransactionTestCase):
    migrate_from = [('tatib', '0008_serviceentry_screen_breaks')]
    migrate_to = [('tatib', '0009_unify_text_screen_modes')]

    def migrate(self, targets):
        executor = MigrationExecutor(connection)
        executor.migrate(targets)
        return executor.loader.project_state(targets).apps

    def setUp(self):
        super().setUp()
        old_apps = self.migrate(self.migrate_from)
        service = old_apps.get_model('tatib', 'TataIbadah').objects.create(name='Service')
        Entry = old_apps.get_model('tatib', 'ServiceEntry')
        self.service_id = service.pk
        self.rows = [
            Entry.objects.create(tatib=service, kind=0, order_number=1,
                                 title='Paired', text='one\ntwo\nthree', screen_breaks=[1]),
            Entry.objects.create(tatib=service, kind=4, order_number=2,
                                 title='Fitted', text='alpha\nbeta\n\ngamma', screen_breaks=[2]),
            Entry.objects.create(tatib=service, kind=4, order_number=3,
                                 title='Default fitted', text='first\nsecond', screen_breaks=None),
        ]
        self.ids = [row.pk for row in self.rows]
        self.apps = self.migrate(self.migrate_to)

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_rows_keep_content_order_breaks_and_projector_grouping(self):
        from multimedia.web.reading.views import _projector_screens
        rows = list(self.apps.get_model('tatib', 'ServiceEntry').objects
                    .filter(tatib_id=self.service_id).order_by('order_number'))
        self.assertEqual([row.pk for row in rows], self.ids)
        self.assertEqual([(row.kind, row.default_screen_mode, row.screen_breaks)
                          for row in rows],
                         [(0, 'multi_line', [1]), (0, 'single_screen', [2]),
                          (0, 'single_screen', None)])
        self.assertEqual([row.title for row in rows], ['Paired', 'Fitted', 'Default fitted'])
        # The projector uses the current model, whose media columns arrive in 0010.
        self.migrate(MigrationExecutor(connection).loader.graph.leaf_nodes())
        service = tatib.TataIbadah.objects.get(pk=self.service_id)
        screens = _projector_screens(service)
        self.assertEqual([screen.get('single', False) for screen in screens if not screen['blank']],
                         [False, False, True, True, True])


class LegacyBookmarkConversionTests(TransactionTestCase):
    """The old bookmarks become services, and the bookmarks stay for the old dock (spec 188)."""

    migrate_from = [('tatib', '0012_tataibadah_kind_and_slots')]
    migrate_to = [('tatib', '0013_legacy_bookmarks_to_services')]

    def migrate(self, targets):
        executor = MigrationExecutor(connection)
        executor.migrate(targets)
        return executor.loader.project_state(targets).apps

    def setUp(self):
        super().setUp()
        self.migrate(self.migrate_from)
        # The bookmark and song models are untouched by this slice, so they come from the
        # registry; the state this test asserts on is the one the migration leaves behind.
        Song = apps.get_model('songs', 'Song')
        Book = apps.get_model('songs', 'Book')
        TataIbadah = apps.get_model('tatib', 'TataIbadah')
        Bookmark = apps.get_model('bookmarks', 'SongBookmark')
        Item = apps.get_model('bookmarks', 'SongBookmarkItem')

        book = Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        first = Song.objects.create(book=book, number=1, title='First song')
        second = Song.objects.create(book=book, number=2, title='Second song')
        self.song_ids = [first.pk, second.pk]

        # The only bookmark that qualifies: active, dated, and holding songs. Its order
        # numbers hold a gap, which the service numbers over.
        kept = Bookmark.objects.create(name='Ibadah Minggu', date=date(2026, 3, 1))
        Item.objects.create(bookmark=kept, song=first, verse='1,3', order_number=2)
        Item.objects.create(bookmark=kept, song=second, verse='2', order_number=7)
        self.kept_id = kept.pk

        # Three ways to be left out: deleted, undated, and empty.
        deleted = Bookmark.objects.create(name='Deleted service', date=date(2026, 3, 8),
                                          is_active=False)
        Item.objects.create(bookmark=deleted, song=first, verse='1', order_number=1)
        undated = Bookmark.objects.create(name='Doding Galangan')
        Item.objects.create(bookmark=undated, song=first, verse='1', order_number=1)
        Bookmark.objects.create(name='Empty service', date=date(2026, 3, 15))

        # A service already standing under the same name and date is the same service: an
        # empty one takes the songs, one the team filled is left alone.
        service = TataIbadah.objects.create(name='Already a service', kind=0,
                                            date=date(2026, 3, 22))
        self.existing_service_id = service.pk
        already = Bookmark.objects.create(name='Already a service', date=date(2026, 3, 22))
        Item.objects.create(bookmark=already, song=second, verse='1', order_number=1)

        built = TataIbadah.objects.create(name='Built by hand', kind=0,
                                          date=date(2026, 3, 29))
        self.built_service_id = built.pk
        built_entry = apps.get_model('tatib', 'ServiceEntry').objects.create(
            tatib_id=built.pk, kind=0, order_number=1, title='Their own opening')
        self.built_entry_id = built_entry.pk
        hand = Bookmark.objects.create(name='Built by hand', date=date(2026, 3, 29))
        Item.objects.create(bookmark=hand, song=first, verse='1', order_number=1)

        self.apps = self.migrate(self.migrate_to)

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_an_active_dated_bookmark_becomes_a_service_of_song_entries(self):
        TataIbadah = self.apps.get_model('tatib', 'TataIbadah')
        ServiceEntry = self.apps.get_model('tatib', 'ServiceEntry')
        service = TataIbadah.objects.get(name='Ibadah Minggu')

        self.assertEqual((service.kind, service.date, service.is_active),
                         (0, date(2026, 3, 1), True))
        entries = list(ServiceEntry.objects.filter(tatib_id=service.pk)
                       .order_by('order_number'))
        self.assertEqual([entry.kind for entry in entries], [2, 2])
        self.assertEqual([entry.song_id for entry in entries], self.song_ids)
        self.assertEqual([entry.verses for entry in entries], [[1, 3], [2]])
        self.assertEqual([entry.order_number for entry in entries], [1, 2])

    def test_a_deleted_undated_or_empty_bookmark_stays_out(self):
        TataIbadah = self.apps.get_model('tatib', 'TataIbadah')
        self.assertEqual(set(TataIbadah.objects.values_list('name', flat=True)),
                         {'Ibadah Minggu', 'Already a service', 'Built by hand'})

    def test_a_service_of_the_same_name_and_date_gets_a_sibling_service(self):
        TataIbadah = self.apps.get_model('tatib', 'TataIbadah')
        ServiceEntry = self.apps.get_model('tatib', 'ServiceEntry')
        twins = list(TataIbadah.objects.filter(name='Already a service').order_by('pk'))
        self.assertEqual(len(twins), 2)
        self.assertEqual({twin.date for twin in twins}, {date(2026, 3, 22)})

        existing, created = twins
        self.assertEqual(existing.pk, self.existing_service_id)
        self.assertFalse(ServiceEntry.objects.filter(tatib_id=existing.pk).exists())
        entries = list(ServiceEntry.objects.filter(tatib_id=created.pk)
                       .order_by('order_number'))
        self.assertEqual([(entry.kind, entry.song_id, entry.verses) for entry in entries],
                         [(2, self.song_ids[1], [1])])

    def test_a_filled_service_is_left_alone_and_gets_a_sibling(self):
        TataIbadah = self.apps.get_model('tatib', 'TataIbadah')
        ServiceEntry = self.apps.get_model('tatib', 'ServiceEntry')
        twins = list(TataIbadah.objects.filter(name='Built by hand').order_by('pk'))
        self.assertEqual(len(twins), 2)

        existing, created = twins
        self.assertEqual(existing.pk, self.built_service_id)
        self.assertEqual(
            list(ServiceEntry.objects.filter(tatib_id=existing.pk)
                 .values_list('pk', 'title')),
            [(self.built_entry_id, 'Their own opening')])
        self.assertEqual(
            list(ServiceEntry.objects.filter(tatib_id=created.pk)
                 .values_list('kind', 'song_id', 'verses')),
            [(2, self.song_ids[0], [1])])

    def test_the_bookmarks_and_their_items_are_left_untouched(self):
        Bookmark = self.apps.get_model('bookmarks', 'SongBookmark')
        Item = self.apps.get_model('bookmarks', 'SongBookmarkItem')
        self.assertEqual(Bookmark.objects.count(), 6)
        self.assertEqual(
            list(Item.objects.filter(bookmark_id=self.kept_id).order_by('order_number')
                 .values_list('verse', 'order_number')),
            [('1,3', 2), ('2', 7)])

    def test_a_second_run_creates_the_same_services_again(self):
        # Deliberate: the owner's rule is "a service under the same name and date never
        # stops the conversion", so the migration has no exists-guard and no idempotence.
        TataIbadah = self.apps.get_model('tatib', 'TataIbadah')
        ServiceEntry = self.apps.get_model('tatib', 'ServiceEntry')
        before = (TataIbadah.objects.count(), ServiceEntry.objects.count())

        conversion = importlib.import_module(
            'multimedia.tatib.migrations.0013_legacy_bookmarks_to_services')
        conversion.convert_bookmarks(apps, SimpleNamespace(connection=connection))

        self.assertEqual((TataIbadah.objects.count(), ServiceEntry.objects.count()),
                         (before[0] + 3, before[1] + 4))

