from rest_framework.test import APITestCase

from multimedia.bookmarks import models as bookmark_models
from multimedia.songs import models as song_models


class SongBookmarkSoftDeleteTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        language = song_models.Language.objects.create(name='Bookmark')
        book = song_models.Book.objects.create(lang=language, name='Bookmark book')
        deleted_book = song_models.Book.objects.create(lang=language, name='Deleted bookmark book')
        active_song = song_models.Song.objects.create(book=book, title='Bookmarked active song')
        deleted_song = song_models.Song.objects.create(book=book, title='Bookmarked deleted song')
        song_in_deleted_book = song_models.Song.objects.create(
            book=deleted_book, title='Song in deleted bookmark book')
        song_models.Verse.objects.create(song=active_song, number=1, lyric='Visible lyric')
        deleted_verse = song_models.Verse.objects.create(
            song=active_song, number=2, lyric='Soft-deleted lyric')
        song_models.Verse.objects.create(song=deleted_song, number=1, lyric='Deleted song lyric')
        song_models.Verse.objects.create(
            song=song_in_deleted_book, number=1, lyric='Deleted book lyric')
        cls.bookmark = bookmark_models.SongBookmark.objects.create(name='Saved songs')
        bookmark_models.SongBookmarkItem.objects.create(
            bookmark=cls.bookmark, song=active_song, verse='1,2', order_number=1)
        bookmark_models.SongBookmarkItem.objects.create(
            bookmark=cls.bookmark, song=deleted_song, verse='1', order_number=2)
        bookmark_models.SongBookmarkItem.objects.create(
            bookmark=cls.bookmark, song=song_in_deleted_book, verse='1', order_number=3)
        deleted_verse.delete()
        deleted_song.delete()
        deleted_book.delete()

    def test_reorder_api_rejects_items_for_deleted_songs(self):
        item = bookmark_models.SongBookmarkItem.objects.get(song__title='Bookmarked deleted song')
        response = self.client.post('/api/bookmarks/songs/items/reorder', {
            'items': [{'item': item.pk, 'order_number': 1}],
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_bookmark_api_hides_deleted_songs_and_does_not_project_deleted_verses(self):
        response = self.client.get(
            '/api/bookmarks/songs/items', {'bookmark': self.bookmark.pk})

        self.assertEqual(response.status_code, 200)
        rows = response.json()
        self.assertEqual(len(rows), 1)
        self.assertEqual(set(rows[0]), {
            'id', 'bookmark', 'song', 'verse', 'order_number', 'created_at',
            'verse_info', 'song_info',
        })
        self.assertEqual(rows[0]['song_info']['title'], 'Bookmarked active song')
        self.assertEqual(rows[0]['verse_info'], [
            {'number': 1, 'lyric': 'Visible lyric'},
            {'number': 2, 'lyric': ''},
        ])
        deleted_song = song_models.Song.objects.get(title='Bookmarked deleted song')
        response = self.client.post('/api/bookmarks/songs/items', {
            'bookmark': self.bookmark.pk, 'song': deleted_song.pk, 'verse': '1',
        }, format='json')
        self.assertEqual(response.status_code, 400)
