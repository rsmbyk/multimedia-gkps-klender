from django.test import TestCase, override_settings
from django.urls import reverse

from multimedia.songs import models


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReadingViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.lang = models.Language.objects.create(name='Indonesian')
        cls.nkb = models.Book.objects.create(
            lang=cls.lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        cls.song = models.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi', key='c')
        models.Verse.objects.create(song=cls.song, number=1, lyric='Di waktu pagi aku bersyukur')
        models.Verse.objects.create(song=cls.song, number=2, lyric='Bersama seluruh ciptaan')
        cls.next_song = models.Song.objects.create(book=cls.nkb, number=13, title='Di Waktu Malam')

    # --- public reading ---

    def test_home_lists_hymn_books_and_search(self):
        response = self.client.get(reverse('web-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nyanyikanlah Kidung Baru')
        self.assertContains(response, 'name="q"')

    def test_book_index_lists_books(self):
        response = self.client.get(reverse('web-books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nyanyikanlah Kidung Baru')

    def test_book_detail_lists_its_songs(self):
        response = self.client.get(reverse('web-book', args=[self.nkb.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertContains(response, reverse('web-song', args=[self.song.id]))

    def test_song_detail_shows_lyrics_and_book_number(self):
        response = self.client.get(reverse('web-song', args=[self.song.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertContains(response, 'NKB 12')
        self.assertContains(response, 'Di waktu pagi aku bersyukur')

    def test_song_detail_links_previous_and_next(self):
        response = self.client.get(reverse('web-song', args=[self.song.id]))
        self.assertContains(response, reverse('web-song', args=[self.next_song.id]))

    def test_unknown_song_is_404(self):
        self.assertEqual(self.client.get(reverse('web-song', args=[9999])).status_code, 404)

    def test_unknown_book_is_404(self):
        self.assertEqual(self.client.get(reverse('web-book', args=[9999])).status_code, 404)

    def test_search_by_title_from_home(self):
        response = self.client.get(reverse('web-home'), {'q': 'waktu pagi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertNotContains(response, 'Haleluya')

    def test_reading_pages_do_not_use_fomantic(self):
        response = self.client.get(reverse('web-home'))
        self.assertNotContains(response, 'semantic.min.css')

    # --- editor relocation ---

    def test_manage_root_serves_editor(self):
        self.assertEqual(self.client.get(reverse('web-root')).status_code, 200)

    def test_legacy_book_list_redirects_to_manage(self):
        response = self.client.get('/songs/books')
        self.assertRedirects(response, reverse('web-songs-books'), status_code=301)

    def test_legacy_song_list_redirects_to_manage(self):
        response = self.client.get(f'/songs/books/{self.nkb.id}')
        self.assertRedirects(response, reverse('web-songs-songs', args=[self.nkb.id]), status_code=301)

    def test_legacy_verse_list_redirects_to_manage(self):
        response = self.client.get(f'/songs/songs/{self.song.id}')
        self.assertRedirects(response, reverse('web-songs-verses', args=[self.song.id]), status_code=301)
