from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from multimedia.bookmarks.models import SongBookmark, SongBookmarkItem
from multimedia.songs import models
from multimedia.songs.search import search_songs
from multimedia.tatib.models import ServiceEntry, ServiceEntryKind, TataIbadah


class SearchSongsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nkb = models.Book.objects.create(
            name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        cls.other = models.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        cls.pagi = models.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi', key='c')
        cls.malam = models.Song.objects.create(book=cls.nkb, number=13, title='Di Waktu Malam', key='d')
        cls.kj = models.Song.objects.create(book=cls.other, number=12, title='Haleluya', key='g')

    def test_empty_query_returns_no_songs(self):
        self.assertFalse(search_songs('').exists())
        self.assertFalse(search_songs('   ').exists())
        self.assertFalse(search_songs(None).exists())

    def test_matches_title_case_insensitively(self):
        results = search_songs('waktu pagi')
        self.assertIn(self.pagi, results)
        self.assertNotIn(self.malam, results)

    def test_matches_book_number(self):
        results = search_songs('NKB 12')
        self.assertEqual(list(results), [self.pagi])

    def test_matches_hymn_book_short_name(self):
        results = search_songs('NKB')
        self.assertCountEqual(list(results), [self.pagi, self.malam])

    def test_search_skips_soft_deleted_songs_and_songbooks(self):
        self.malam.delete()
        self.nkb.delete()
        self.assertNotIn(self.malam, search_songs('waktu malam'))
        self.assertNotIn(self.pagi, search_songs('waktu pagi'))


class BookContractTests(TestCase):
    def test_songbook_has_no_language_field(self):
        self.assertNotIn('lang', {field.name for field in models.Book._meta.get_fields()})

    def test_songbook_names_are_globally_unique(self):
        models.Book.objects.create(name='One name')
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.Book.objects.create(name='One name')


class SoftDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = models.Book.objects.create(name='Ende-Enden', short_name='EE')
        cls.song = models.Song.objects.create(book=cls.book, number=1, title='Ende')
        cls.verse = models.Verse.objects.create(song=cls.song, number=1, lyric='Lirik')

    def test_delete_marks_songbook_song_and_verse_without_removing_rows(self):
        for record in (self.verse, self.song, self.book):
            with self.subTest(record=type(record).__name__):
                record.delete()
                record.refresh_from_db()
                self.assertTrue(record.is_deleted)
                self.assertIsNotNone(record.deleted_at)
                self.assertIsNone(record.deleted_by_id)
        self.assertEqual(models.Book.objects.filter(pk=self.book.pk).count(), 1)
        self.assertEqual(models.Song.objects.filter(pk=self.song.pk).count(), 1)
        self.assertEqual(models.Verse.objects.filter(pk=self.verse.pk).count(), 1)


class SoftDeleteAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.admin = User.objects.create(
            username='soft-delete-admin', is_staff=True, is_superuser=True)
        cls.book = models.Book.objects.create(name='Admin songbook')
        cls.song = models.Song.objects.create(book=cls.book, title='Referenced song')
        models.Verse.objects.create(song=cls.song, number=1, lyric='A verse')
        service = TataIbadah.objects.create(name='Admin service')
        ServiceEntry.objects.create(
            tatib=service, kind=ServiceEntryKind.SONG, order_number=1,
            song=cls.song, verses=[1])

    def setUp(self):
        self.client.force_login(self.admin)

    def test_songbook_admin_delete_soft_deletes_without_removing_children_or_references(self):
        bookmark = SongBookmark.objects.create(name='Admin saved song')
        item = SongBookmarkItem.objects.create(
            bookmark=bookmark, song=self.song, verse='1', order_number=1)
        delete_url = reverse('admin:songs_book_delete', args=[self.book.pk])
        confirmation = self.client.get(delete_url)
        self.assertEqual(confirmation.status_code, 200)
        self.assertContains(confirmation, 'Are you sure?')
        response = self.client.post(delete_url, {'post': 'yes'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_deleted)
        self.assertEqual(self.book.deleted_by_id, self.admin.pk)
        self.assertIsNotNone(self.book.deleted_at)
        self.assertTrue(models.Song.objects.filter(pk=self.song.pk).exists())
        self.assertTrue(item.__class__.objects.filter(pk=item.pk).exists())
        self.assertTrue(ServiceEntry.objects.filter(song=self.song).exists())

    def test_single_admin_delete_keeps_references_and_records_actor_and_time(self):
        delete_url = reverse('admin:songs_song_delete', args=[self.song.pk])
        confirmation = self.client.get(delete_url)
        self.assertEqual(confirmation.status_code, 200)
        self.assertContains(confirmation, 'Are you sure?')
        response = self.client.post(delete_url, {'post': 'yes'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.song.refresh_from_db()
        self.assertTrue(self.song.is_deleted)
        self.assertEqual(self.song.deleted_by_id, self.admin.pk)
        self.assertIsNotNone(self.song.deleted_at)
        self.assertTrue(ServiceEntry.objects.filter(song=self.song).exists())

    def test_bulk_admin_delete_keeps_references_and_records_actor_and_time(self):
        url = reverse('admin:songs_song_changelist')
        selection = {'action': 'delete_selected', '_selected_action': str(self.song.pk)}
        confirm = self.client.post(url, selection)
        self.assertEqual(confirm.status_code, 200)
        self.assertContains(confirm, 'Are you sure?')
        response = self.client.post(url, {**selection, 'post': 'yes'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.song.refresh_from_db()
        self.assertTrue(self.song.is_deleted)
        self.assertEqual(self.song.deleted_by_id, self.admin.pk)
        self.assertIsNotNone(self.song.deleted_at)
        self.assertTrue(ServiceEntry.objects.filter(song=self.song).exists())