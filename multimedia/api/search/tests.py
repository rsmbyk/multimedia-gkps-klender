from rest_framework.test import APITestCase

from multimedia.songs import models


class SongSearchSoftDeleteTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        active_book = models.Book.objects.create(name='Search book')
        deleted_book = models.Book.objects.create(name='Deleted search book')
        active_song = models.Song.objects.create(book=active_book, title='Search song')
        deleted_song = models.Song.objects.create(book=active_book, title='Deleted search song')
        song_in_deleted_book = models.Song.objects.create(
            book=deleted_book, title='Song in deleted search book')
        cls.active_verse = models.Verse.objects.create(
            song=active_song, number=1, lyric='alpha bravo charlie')
        models.Verse.objects.create(song=active_song, number=2, lyric='alpha bravo charlie').delete()
        models.Verse.objects.create(
            song=deleted_song, number=1, lyric='alpha bravo charlie')
        models.Verse.objects.create(
            song=song_in_deleted_book, number=1, lyric='alpha bravo charlie')
        deleted_book.delete()
        deleted_song.delete()

    def test_search_filters_deleted_targets_without_changing_active_payload(self):
        response = self.client.get('/api/search/songs', {'q': 'alpha bravo charlie'})

        self.assertEqual(response.status_code, 200)
        rows = response.data['results']
        self.assertEqual([row['id'] for row in rows], [self.active_verse.pk])
        self.assertEqual(set(rows[0]), {'id', 'song', 'number', 'lyric'})
