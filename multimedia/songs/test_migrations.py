from datetime import date

from uuid import uuid4

from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

from multimedia.bookmarks.models import SongBookmark, SongBookmarkItem
from multimedia.tatib.models import ServiceEntry, ServiceEntryKind, TataIbadah


class MergeDuplicateSongbooksMigrationTests(TransactionTestCase):
    migrate_from = ('songs', '0014_book_deleted_at_book_deleted_by_song_deleted_at_and_more')
    migrate_to = ('songs', '0015_merge_duplicate_books_remove_language')

    def setUp(self):
        executor = MigrationExecutor(connection)
        executor.migrate([self.migrate_from])
        old_apps = executor.loader.project_state([self.migrate_from]).apps
        Book = old_apps.get_model('songs', 'Book')
        Language = old_apps.get_model('songs', 'Language')
        Song = old_apps.get_model('songs', 'Song')
        Verse = old_apps.get_model('songs', 'Verse')

        self.run_id = uuid4().hex[:8]
        self.merge_name = f'Mergeable {self.run_id}'
        self.archived_name = f'Archived {self.run_id}'
        self.case_name = f'mergeable {self.run_id}'
        languages = [Language.objects.create(name='L%s%d' % (self.run_id[:7], index))
                     for index in range(1, 8)]
        deleted = Book.objects.create(
            lang=languages[0], name=self.merge_name, short_name='OLD', is_deleted=True)
        keeper = Book.objects.create(
            lang=languages[1], name=self.merge_name, short_name='KEEP', is_hymn_book=True)
        duplicate_a = Book.objects.create(
            lang=languages[2], name=self.merge_name, short_name='DUP-A')
        duplicate_b = Book.objects.create(
            lang=languages[3], name=self.merge_name, short_name='DUP-B')
        self.keeper_id = keeper.pk
        self.duplicate_ids = (deleted.pk, duplicate_a.pk, duplicate_b.pk)

        archived_a = Book.objects.create(
            lang=languages[4], name=self.archived_name, short_name='ARC-A', is_deleted=True)
        archived_b = Book.objects.create(
            lang=languages[5], name=self.archived_name, short_name='ARC-B', is_deleted=True)
        self.archived_keeper_id = archived_a.pk
        self.archived_duplicate_id = archived_b.pk
        case_variant = Book.objects.create(
            lang=languages[6], name=self.case_name, short_name='CASE')
        self.case_variant_id = case_variant.pk

        keeper_song = Song.objects.create(
            book=keeper, number=2, sub_number='a', title='Keeper song', key='c')
        Song.objects.create(book=keeper, number=11, title='Existing maximum')
        moved_collision = Song.objects.create(
            book=duplicate_a, number=2, sub_number='a', title='First collision', key='d')
        Song.objects.create(book=duplicate_a, number=7, title='Non-collision')
        moved_soft_deleted = Song.objects.create(
            book=duplicate_a, number=20, title='Deleted collision', is_deleted=True)
        moved_collision_two = Song.objects.create(
            book=duplicate_b, number=2, sub_number='a', title='Second collision')
        self.song_ids = {
            'keeper': keeper_song.pk,
            'collision_one': moved_collision.pk,
            'soft_deleted': moved_soft_deleted.pk,
            'collision_two': moved_collision_two.pk,
        }
        self.original_modified = moved_collision.modified
        verse = Verse.objects.create(
            song=moved_collision, number=1, lyric='Preserved lyric', is_deleted=True)
        self.verse_id = verse.pk

        service = TataIbadah.objects.create(name='Migration reference service', date=date(2026, 10, 7))
        self.service_entry_id = ServiceEntry.objects.create(
            tatib=service, kind=ServiceEntryKind.SONG, order_number=1,
            song_id=moved_collision.pk, verses=[1]).pk
        bookmark = SongBookmark.objects.create(name='Migration reference bookmark')
        self.bookmark_item_id = SongBookmarkItem.objects.create(
            bookmark=bookmark, song_id=moved_collision.pk, verse='1', order_number=1).pk

        MigrationExecutor(connection).migrate([self.migrate_to])
        self.apps = MigrationExecutor(connection).loader.project_state([self.migrate_to]).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        super().tearDown()

    def test_duplicate_books_merge_without_losing_song_verse_or_reference_ids(self):
        Book = self.apps.get_model('songs', 'Book')
        Song = self.apps.get_model('songs', 'Song')
        Verse = self.apps.get_model('songs', 'Verse')

        merged_books = list(Book.objects.filter(name=self.merge_name))
        self.assertEqual([book.pk for book in merged_books], [self.keeper_id])
        keeper = merged_books[0]
        self.assertEqual(keeper.short_name, 'KEEP')
        self.assertTrue(keeper.is_hymn_book)
        self.assertFalse(Book.objects.filter(pk__in=self.duplicate_ids).exists())
        self.assertEqual(Book.objects.filter(name=self.archived_name).values_list('pk', flat=True).get(),
                         self.archived_keeper_id)
        self.assertFalse(Book.objects.filter(pk=self.archived_duplicate_id).exists())
        self.assertTrue(Book.objects.filter(pk=self.case_variant_id, name=self.case_name).exists())

        songs = {song.pk: song for song in Song.objects.filter(pk__in=self.song_ids.values())}
        self.assertEqual(set(songs), set(self.song_ids.values()))
        self.assertEqual(songs[self.song_ids['keeper']].number, 2)
        self.assertEqual(songs[self.song_ids['collision_one']].number, 21)
        self.assertEqual(songs[self.song_ids['collision_one']].sub_number, 'a')
        self.assertEqual(songs[self.song_ids['collision_two']].number, 22)
        self.assertEqual(songs[self.song_ids['collision_two']].sub_number, 'a')
        self.assertEqual(songs[self.song_ids['soft_deleted']].number, 20)
        self.assertTrue(songs[self.song_ids['soft_deleted']].is_deleted)
        self.assertTrue(all(song.book_id == self.keeper_id for song in songs.values()))
        self.assertEqual(songs[self.song_ids['collision_one']].modified, self.original_modified)

        verse = Verse.objects.get(pk=self.verse_id)
        self.assertEqual(verse.song_id, self.song_ids['collision_one'])
        self.assertEqual(verse.lyric, 'Preserved lyric')
        self.assertTrue(verse.is_deleted)
        self.assertTrue(ServiceEntry.objects.filter(
            pk=self.service_entry_id, song_id=self.song_ids['collision_one']).exists())
        self.assertTrue(SongBookmarkItem.objects.filter(
            pk=self.bookmark_item_id, song_id=self.song_ids['collision_one']).exists())

    def test_songbook_language_model_is_removed_and_names_are_unique(self):
        Book = self.apps.get_model('songs', 'Book')
        with self.assertRaises(LookupError):
            self.apps.get_model('songs', 'Language')
        self.assertNotIn('lang', {field.name for field in Book._meta.get_fields()})
        with self.assertRaises(IntegrityError):
            Book.objects.create(name=self.merge_name)
