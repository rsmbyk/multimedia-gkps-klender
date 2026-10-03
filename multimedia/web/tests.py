from datetime import date

from django.test import TestCase, override_settings
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReadingViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        lang = songs.Language.objects.create(name='Indonesian')
        cls.nkb = songs.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi', key='c')
        songs.Verse.objects.create(song=cls.song, number=1, lyric='Di waktu pagi aku bersyukur')
        songs.Verse.objects.create(song=cls.song, number=2, lyric='Bersama seluruh ciptaan')
        cls.next_song = songs.Song.objects.create(book=cls.nkb, number=13, title='Di Waktu Malam')
        songs.Book.objects.create(lang=lang, name='Kidung Harian', short_name='', is_hymn_book=False)

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru', abbreviation='TB')
        cls.mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        mat_tb = bible.BookTranslation.objects.create(version=version, book=cls.mat, translation='Matius')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=13, text='Kamu adalah garam dunia.')
        bible.Verse.objects.create(book_translation=mat_tb, chapter=5, verse=14, text='Kamu adalah terang dunia.')

        cls.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Nyanyian Pembukaan', text='KJ 120\nL. Liturgis memimpin', order_number=1)
        tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.END_OF_SECTION,
            title='', text='Catatan privat', order_number=2)

    # --- shell ---

    def test_home_is_search_first(self):
        response = self.client.get(reverse('web-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'Search Alkitab, Kidung, and Tata Ibadah')
        self.assertContains(response, 'Try Matius 5:13, KJ 152, or pengampunan dosa')
        self.assertContains(response, 'data-tip="Alkitab"')
        self.assertContains(response, 'id="railSearch"')
        self.assertContains(response, 'aria-current="page"')

    def test_reading_pages_do_not_use_fomantic(self):
        self.assertNotContains(self.client.get(reverse('web-home')), 'semantic.min.css')

    # --- search page ---

    def test_search_page_groups_song_hits(self):
        response = self.client.get(reverse('web-search'), {'q': 'waktu pagi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Results for')
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertContains(response, 'result-group__title')
        self.assertContains(response, reverse('web-song', args=[self.song.id]))

    def test_search_page_resolves_bible_reference(self):
        response = self.client.get(reverse('web-search'), {'q': 'Matius 5:13'})
        target = reverse('web-bible-chapter', args=[self.mat.id, 5]) + '?v=13&amp;to=13'
        self.assertContains(response, target)
        self.assertContains(response, 'Kamu adalah garam dunia.')

    def test_search_page_flags_short_queries(self):
        response = self.client.get(reverse('web-search'), {'q': 'ab'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter at least 3 letters or numbers.')
        self.assertContains(response, 'aria-invalid="true"')
        self.assertNotContains(response, 'Results for')

    # --- Alkitab ---

    def test_bible_root_lists_testaments(self):
        response = self.client.get(reverse('web-bible'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perjanjian Baru')
        self.assertContains(response, 'Matius')

    def test_bible_chapter_renders_verses_and_marks_target(self):
        response = self.client.get(
            reverse('web-bible-chapter', args=[self.mat.id, 5]), {'v': 13, 'to': 13})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kamu adalah garam dunia.')
        self.assertContains(response, 'data-search-target="true"')
        self.assertContains(response, 'data-n="5"')

    def test_bible_unknown_chapter_is_404(self):
        response = self.client.get(reverse('web-bible-chapter', args=[self.mat.id, 99]))
        self.assertEqual(response.status_code, 404)

    # --- Kidung ---

    def test_book_index_lists_songbooks(self):
        response = self.client.get(reverse('web-books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nyanyikanlah Kidung Baru')
        self.assertContains(response, 'Kidung Harian')

    def test_book_detail_lists_its_songs(self):
        response = self.client.get(reverse('web-book', args=[self.nkb.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertContains(response, reverse('web-song', args=[self.song.id]))
        self.assertContains(response, 'Song list')

    def test_song_detail_shows_lyrics_and_citation(self):
        response = self.client.get(reverse('web-song', args=[self.song.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertContains(response, 'NKB 12')
        self.assertContains(response, 'Di waktu pagi aku bersyukur')
        self.assertContains(response, 'read__eyebrow')

    def test_unknown_song_is_404(self):
        self.assertEqual(self.client.get(reverse('web-song', args=[9999])).status_code, 404)

    def test_unknown_book_is_404(self):
        self.assertEqual(self.client.get(reverse('web-book', args=[9999])).status_code, 404)

    # --- Tata Ibadah ---

    def test_tatib_service_renders_order(self):
        response = self.client.get(reverse('web-tatib-service', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nyanyian Pembukaan')
        self.assertContains(response, '23 Agu 2026')
        self.assertContains(response, 'tatib__sp')   # speaker marks
        self.assertContains(response, 'tatib__eos')  # quiet end-of-section note

    def test_tatib_list_groups_by_month(self):
        response = self.client.get(reverse('web-tatib'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Agustus 2026')
        self.assertContains(response, 'Ibadah Minggu III')

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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MaintenanceModeTests(TestCase):
    """The site root shows a maintenance notice while MAINTENANCE_MODE is on."""

    @classmethod
    def setUpTestData(cls):
        lang = songs.Language.objects.create(name='Indonesian')
        cls.book = songs.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)

    @override_settings(MAINTENANCE_MODE=True)
    def test_root_shows_maintenance_when_on(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Retry-After', response)
        self.assertContains(response, 'pemeliharaan', status_code=503)
        self.assertContains(response, 'noindex', status_code=503)
        self.assertNotContains(response, 'name="q"', status_code=503)

    @override_settings(MAINTENANCE_MODE=False)
    def test_root_shows_home_when_off(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="q"')
        self.assertContains(response, 'Search Alkitab, Kidung, and Tata Ibadah')

    @override_settings(MAINTENANCE_MODE=True)
    def test_temporary_home_serves_home_when_on(self):
        self.assertEqual(reverse('web-home'), '/home/')
        response = self.client.get(reverse('web-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="q"')

    @override_settings(MAINTENANCE_MODE=True)
    def test_other_surfaces_unaffected(self):
        for url in ('/songs/', '/manage/'):
            with self.subTest(url=url):
                self.assertNotEqual(self.client.get(url).status_code, 503)
