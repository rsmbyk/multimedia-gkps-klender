from rest_framework.test import APITestCase

from multimedia.songs import models


class SongApiSoftDeleteTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.active_book = models.Book.objects.create(name='Active Book', short_name='AB')
        cls.deleted_book = models.Book.objects.create(name='Deleted Book', short_name='DB')
        cls.active_song = models.Song.objects.create(
            book=cls.active_book, number=1, title='Active Song')
        cls.deleted_song = models.Song.objects.create(
            book=cls.active_book, number=2, title='Deleted Song')
        cls.song_in_deleted_book = models.Song.objects.create(
            book=cls.deleted_book, number=1, title='Song in Deleted Book')
        cls.active_verse = models.Verse.objects.create(
            song=cls.active_song, number=1, lyric='Active verse')
        cls.deleted_verse = models.Verse.objects.create(
            song=cls.active_song, number=2, lyric='Deleted verse')
        cls.verse_in_deleted_song = models.Verse.objects.create(
            song=cls.deleted_song, number=1, lyric='Verse in deleted song')
        cls.deleted_book.delete()
        cls.deleted_song.delete()
        cls.deleted_verse.delete()

    def test_current_song_endpoints_list_only_active_rows_and_active_parents(self):
        books = self.client.get('/api/songs/books').data
        songs = self.client.get('/api/songs/songs').data
        verses = self.client.get('/api/songs/verses').data

        self.assertEqual([row['id'] for row in books], [self.active_book.pk])
        self.assertEqual([row['id'] for row in songs], [self.active_song.pk])
        self.assertEqual([row['id'] for row in verses], [self.active_verse.pk])
        self.assertEqual(set(books[0]), {'id', 'name', 'short_name', 'is_hymn_book'})
        self.assertNotIn('lang', books[0])
        self.assertEqual(set(songs[0]), {
            'id', 'number', 'sub_number', 'title', 'is_untitled', 'key', 'modified', 'book'})
        self.assertEqual(set(verses[0]), {'id', 'song', 'number', 'lyric'})

    def test_verse_create_rejects_deleted_song(self):
        response = self.client.post('/api/songs/verses', {
            'song': self.deleted_song.pk, 'number': 3, 'lyric': 'Cannot attach'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_verse_update_rejects_deleted_song(self):
        response = self.client.patch(f'/api/songs/verses/{self.active_verse.pk}', {
            'song': self.deleted_song.pk}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_direct_deleted_song_and_book_routes_return_not_found(self):
        self.assertEqual(self.client.get(f'/api/songs/songs/{self.deleted_song.pk}').status_code, 404)
        self.assertEqual(self.client.get(f'/api/songs/books/{self.deleted_book.pk}').status_code, 404)
