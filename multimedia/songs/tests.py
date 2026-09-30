from django.test import TestCase

from multimedia.songs import models
from multimedia.songs.search import search_songs


class SearchSongsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        lang = models.Language.objects.create(name='Indonesian')
        cls.nkb = models.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        cls.other = models.Book.objects.create(
            lang=lang, name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
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
