from datetime import date
import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReadingViewTests(TestCase):
    """The public reading pages (spec 004): the search-first shell, Alkitab, Kidung, Tata
    Ibadah, and the manage redirects.

    Named for what it tests on purpose. It was called `EditorViewTests` -- the same name as
    the sidebar editors' class further down this module -- so Python kept only the later
    binding and these 23 tests had not run since spec 005 landed (the file's 100 tests
    collected as 77). Two test classes in one module must never share a name.
    """

    @classmethod
    def setUpTestData(cls):
        cls.nkb = songs.Book.objects.create(
            name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi', key='c')
        songs.Verse.objects.create(song=cls.song, number=1, lyric='Di waktu pagi aku bersyukur')
        songs.Verse.objects.create(song=cls.song, number=2, lyric='Bersama seluruh ciptaan')
        cls.next_song = songs.Song.objects.create(book=cls.nkb, number=13, title='Di Waktu Malam')
        cls.harian = songs.Book.objects.create(
            name='Kidung Harian', short_name='', is_hymn_book=False)
        songs.Song.objects.create(book=cls.harian, title='Alpha')
        songs.Song.objects.create(book=cls.harian, title='Zebra')

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
        self.assertContains(response, 'class="field-clear"')          # the clear control
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

    def test_search_field_has_a_clear_control(self):
        response = self.client.get(reverse('web-search'), {'q': 'kasih'})
        self.assertContains(response, 'field-clear')
        self.assertContains(response, 'type="button" aria-label="Clear the filter" hidden')

    def test_search_page_searches_short_queries(self):
        response = self.client.get(reverse('web-search'), {'q': 'di'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Results for')
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertNotContains(response, 'at least 3')

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
        self.assertFalse(response.context['show_song_sort'])   # hymns keep number order

    def test_hymn_songs_are_ordered_by_number_then_casefolded_sub_number(self):
        songs.Song.objects.create(book=self.nkb, number=10, title='Ten')
        songs.Song.objects.create(book=self.nkb, number=12, sub_number='B', title='Suffix B')
        songs.Song.objects.create(book=self.nkb, number=12, sub_number='a', title='Suffix a')
        songs.Song.objects.create(book=self.nkb, number=2, title='Two')
        songs.Song.objects.create(book=self.nkb, number=None, title='Legacy')

        response = self.client.get(reverse('web-book', args=[self.nkb.id]))

        self.assertEqual(
            [row['title'] for row in response.context['songs']],
            ['Two', 'Ten', 'Di Waktu Pagi', 'Suffix a', 'Suffix B',
             'Di Waktu Malam', 'Legacy'],
        )
        self.assertFalse(response.context['show_song_sort'])

    def test_non_hymn_book_offers_the_sort_toggle(self):
        response = self.client.get(reverse('web-book', args=[self.harian.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['show_song_sort'])
        self.assertContains(response, 'data-m="')              # the default's key
        self.assertContains(response, 'data-o="')              # its tiebreak
        self.assertEqual(response.context['songs'][0]['sort_title'], 'zebra')   # newest first

    def test_song_rows_carry_last_modified_and_an_az_key_without_the_number(self):
        # The corpus titles carry their own "435. ", which must not decide A-Z: every
        # song imports with one `modified` timestamp, so with that prefix in the key
        # the alphabetical order would be identical to the last-modified one and the
        # toggle could not be observed to do anything (spec 005).
        book = songs.Book.objects.create(name='Uji Urutan', is_hymn_book=False)
        songs.Song.objects.create(book=book, number=2, title='15. Alfabet')
        songs.Song.objects.create(book=book, number=1, title='9. Zebra')
        response = self.client.get(reverse('web-book', args=[book.pk]))
        rows = response.context['songs']
        self.assertEqual([r['title'] for r in rows], ['9. Zebra', '15. Alfabet'])   # newest first
        self.assertEqual([r['sort_title'] for r in rows], ['zebra', 'alfabet'])     # A-Z
        self.assertContains(response, 'data-m="')               # the default's key
        self.assertContains(response, 'data-o="0"')             # and the tiebreak

    def test_a_hymn_book_offers_no_add_song_button_and_refuses_the_create(self):
        # The first round's rule: a hymn', and a hymn's songs, are never editable.
        page = self.client.get(reverse('web-book', args=[self.nkb.pk]))
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, 'id="songAdd"')
        # (#panelAdd is the songbook section's, which stays available: a new songbook
        # is not a hymn-book write)
        url = reverse('web-editor-save-new', kwargs={'kind': tatib.ServiceEntryKind.SONG})
        post = self.client.post(url, {'book': self.nkb.pk, 'title': 'Diselundupkan'})
        self.assertEqual(post.status_code, 404)
        self.assertFalse(songs.Song.objects.filter(title='Diselundupkan').exists())
        form = self.client.get(reverse('web-editor-new', kwargs={'kind': tatib.ServiceEntryKind.SONG}),
                               {'book': self.nkb.pk})
        self.assertEqual(form.status_code, 404)

    def test_song_detail_shows_lyrics_and_citation(self):
        response = self.client.get(reverse('web-song', args=[self.song.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Di Waktu Pagi')
        self.assertContains(response, 'NKB 12')
        self.assertContains(response, 'Di waktu pagi aku bersyukur')
        self.assertContains(response, 'read__eyebrow')

    def test_deleted_song_is_hidden_from_song_detail_and_search(self):
        self.next_song.delete()
        detail = self.client.get(reverse('web-song', args=[self.next_song.pk]))
        search = self.client.get(reverse('web-search'), {'q': 'Di Waktu Malam'})
        self.assertEqual(detail.status_code, 404)
        self.assertFalse(any(
            row['url'] == reverse('web-song', args=[self.next_song.pk])
            for group in search.context['result_groups'] for row in group['rows']))

    def test_deleted_songbook_is_hidden_with_its_songs(self):
        self.nkb.delete()
        self.assertNotContains(self.client.get(reverse('web-books')), 'Nyanyikanlah Kidung Baru')
        self.assertEqual(self.client.get(reverse('web-book', args=[self.nkb.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('web-song', args=[self.song.pk])).status_code, 404)

    def test_deleted_verse_is_hidden_from_song_detail_and_search(self):
        self.song.verse_set.get(number=1).delete()
        detail = self.client.get(reverse('web-song', args=[self.song.pk]))
        search = self.client.get(reverse('web-search'), {'q': 'aku bersyukur'})
        self.assertNotContains(detail, 'Di waktu pagi aku bersyukur')
        self.assertNotContains(search, 'Di Waktu Pagi')

    def test_legacy_song_pages_hide_deleted_books_and_songs(self):
        self.harian.delete()
        self.next_song.delete()
        book_page = self.client.get(reverse('web-songs-songs', args=[self.harian.pk]))
        song_page = self.client.get(reverse('web-songs-verses', args=[self.next_song.pk]))
        self.assertEqual(book_page.status_code, 404)
        self.assertEqual(song_page.status_code, 404)

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

    def test_tatib_service_header_uses_full_indonesian_month_name(self):
        response = self.client.get(reverse('web-tatib-service', args=[self.service.id]))
        self.assertContains(response,
                            '<p class="read__eyebrow" id="readEyebrow">23 Agustus 2026</p>',
                            html=True)

    def test_undated_tatib_header_keeps_its_label(self):
        service = tatib.TataIbadah.objects.create(name='Recurring service', date=None)
        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        self.assertContains(response,
                            '<p class="read__eyebrow" id="readEyebrow">Tata Ibadah</p>',
                            html=True)

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
        cls.book = songs.Book.objects.create(
            name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)

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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditorViewTests(TestCase):
    """Sidebar editors (spec 005): the forms, the endpoints, and the two gates."""

    @classmethod
    def setUpTestData(cls):
        cls.nkb = songs.Book.objects.create(
            name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        songs.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi')
        cls.harian = songs.Book.objects.create(
            name='Kidung Harian', short_name='KH', is_hymn_book=False)
        cls.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Nyanyian Pembukaan', text='KJ 120', order_number=1)

    def new_url(self, kind):
        return reverse('web-editor-new', kwargs={'kind': kind})

    def save_url(self, kind, pk=None):
        if pk:
            return reverse('web-editor-save', kwargs={'kind': kind, 'pk': pk})
        return reverse('web-editor-save-new', kwargs={'kind': kind})

    # --- the form fragment ---

    def test_new_songbook_form_omits_language_and_hidden_metadata(self):
        response = self.client.get(self.new_url('songbook'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        for field in ('lang', 'short_name', 'is_hymn_book'):
            self.assertNotContains(response, 'name="%s"' % field)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'New songbook')

    def test_edit_form_is_prefilled(self):
        response = self.client.get(
            reverse('web-editor-edit', kwargs={'kind': 'songbook', 'pk': self.harian.pk}))
        self.assertContains(response, 'value="Kidung Harian"')
        self.assertNotContains(response, 'name="lang"')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_song_form_carries_its_songbook_id_to_save(self):
        response = self.client.get(self.new_url('song'), {'book': self.harian.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'name="book" value="{self.harian.pk}"')

    def test_tatib_forms_render_hidden_iso_value_and_custom_date_picker(self):
        response = self.client.get(self.new_url('tatib'))
        self.assertContains(response, 'name="date"')
        self.assertContains(response, 'data-date-picker-value')
        self.assertContains(response, 'data-date-picker-trigger')
        self.assertContains(response, 'data-date-picker-calendar')
        self.assertNotContains(response, 'type="date"')

    def test_tatib_create_and_edit_forms_omit_legacy_and_activation_fields(self):
        for url in (self.new_url('tatib'), reverse(
                'web-editor-edit', kwargs={'kind': 'tatib', 'pk': self.service.pk})):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'name="name"')
                self.assertContains(response, 'name="date"')
                for field in ('first_title', 'first_text', 'is_active'):
                    self.assertNotContains(response, 'name="%s"' % field)

    def test_unknown_kind_is_404(self):
        self.assertEqual(self.client.get(self.new_url('bible')).status_code, 404)

    # --- songbooks ---

    def test_create_songbook_ignores_hidden_metadata_and_forged_language(self):
        response = self.client.post(self.save_url('songbook'), {
            'name': 'Kidung Baru', 'short_name': 'KB', 'lang': 'forged',
            'is_hymn_book': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['kind'], 'songbook')
        book = songs.Book.objects.get(name='Kidung Baru')
        self.assertEqual(book.short_name, '')
        self.assertFalse(book.is_hymn_book)

    def test_editing_a_songbook_ignores_forged_language_and_hidden_values(self):
        response = self.client.post(
            self.save_url('songbook', self.harian.pk),
            {'name': 'Kidung Harian Baru', 'short_name': 'FORGED',
             'is_hymn_book': 'on', 'lang': 'forged'})
        self.assertEqual(response.status_code, 200, response.content[:400])
        self.harian.refresh_from_db()
        self.assertEqual(self.harian.name, 'Kidung Harian Baru')
        self.assertEqual(self.harian.short_name, 'KH')
        self.assertFalse(self.harian.is_hymn_book)

    def test_deleted_songbook_and_song_targets_cannot_be_edited_or_created_into(self):
        deleted_book = songs.Book.objects.create(
            name='Deleted editor book', short_name='DEB')
        deleted_song = songs.Song.objects.create(book=self.harian, title='Deleted editor song')
        deleted_book_song = songs.Song.objects.create(book=deleted_book, title='Child song')
        deleted_book.delete()
        deleted_song.delete()

        self.assertEqual(self.client.get(reverse(
            'web-editor-edit', kwargs={'kind': 'songbook', 'pk': deleted_book.pk})).status_code, 404)
        self.assertEqual(self.client.post(self.save_url('songbook', deleted_book.pk), {
            'name': 'Restored by edit', 'short_name': 'DEB', 'lang': 'forged',
        }).status_code, 404)
        self.assertEqual(self.client.get(reverse(
            'web-editor-edit', kwargs={'kind': 'song', 'pk': deleted_song.pk})).status_code, 404)
        self.assertEqual(self.client.post(self.save_url('song', deleted_song.pk), {
            'title': 'Restored by edit',
        }).status_code, 404)
        self.assertEqual(self.client.post(self.save_url('song'), {
            'book': deleted_book.pk, 'title': 'Created under deleted book',
        }).status_code, 404)
        self.assertFalse(songs.Song.objects.filter(title='Created under deleted book').exists())
        self.assertTrue(songs.Song.objects.filter(pk=deleted_book_song.pk).exists())

    def test_hymn_songbook_cannot_be_edited(self):
        self.assertEqual(self.client.get(reverse(
            'web-editor-edit', kwargs={'kind': 'songbook', 'pk': self.nkb.pk})).status_code, 404)
        self.assertEqual(self.client.post(self.save_url('songbook', self.nkb.pk), {
            'name': 'Changed', 'short_name': 'NKB', 'lang': 'forged'}).status_code, 404)

    # --- songs ---

    def test_create_song_in_the_open_songbook(self):
        response = self.client.post(self.save_url('song'), {
            'book': self.harian.pk, 'title': 'Lagu Baru'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(songs.Song.objects.filter(book=self.harian, title='Lagu Baru').exists())

    def test_a_hymn_book_refuses_new_songs_entirely(self):
        # A hymn corpus is published work: no new songs, with a number or without.
        response = self.client.post(self.save_url('song'), {
            'book': self.nkb.pk, 'title': 'Hymn Baru'})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(songs.Song.objects.filter(title='Hymn Baru').exists())

    def test_song_without_a_songbook_is_404(self):
        self.assertEqual(self.client.get(self.new_url('song')).status_code, 404)

    def test_a_hymn_song_cannot_be_edited(self):
        song = songs.Song.objects.get(book=self.nkb, number=12)
        self.assertEqual(self.client.get(reverse(
            'web-editor-edit', kwargs={'kind': tatib.ServiceEntryKind.SONG, 'pk': song.pk})).status_code, 404)

    def test_editing_a_free_song(self):
        song = songs.Song.objects.create(book=self.harian, title='Alpha')
        response = self.client.post(self.save_url('song', song.pk), {
            'title': 'Alpha Baru'})
        self.assertEqual(response.status_code, 200, response.content[:400])
        song.refresh_from_db()
        self.assertEqual(song.title, 'Alpha Baru')

    # --- Tata Ibadah ---

    def test_create_tatib_ignores_legacy_fields_and_uses_active_default(self):
        response = self.client.post(self.save_url('tatib'), {
            'name': 'Ibadah Baru', 'date': '2026-11-01', 'is_active': '',
            'first_title': 'Pembukaan', 'first_text': 'KJ 1'})
        self.assertEqual(response.status_code, 200, response.content[:400])
        service = tatib.TataIbadah.objects.get(name='Ibadah Baru')
        self.assertTrue(service.is_active)
        self.assertEqual(service.tataibadahitem_set.count(), 0)

    def test_edit_tatib_ignores_activation_post_and_preserves_existing_state(self):
        inactive_service = tatib.TataIbadah.objects.create(
            name='Inactive service', date=date(2026, 8, 30), is_active=False)
        response = self.client.post(self.save_url('tatib', self.service.pk), {
            'name': 'Ibadah Minggu IV', 'date': '2026-08-30', 'is_active': ''})
        self.assertEqual(response.status_code, 200, response.content[:400])
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Ibadah Minggu IV')
        self.assertTrue(self.service.is_active)

        response = self.client.post(self.save_url('tatib', inactive_service.pk), {
            'name': 'Inactive service edited', 'date': '', 'is_active': 'on'})
        self.assertEqual(response.status_code, 200, response.content[:400])
        inactive_service.refresh_from_db()
        self.assertEqual(inactive_service.name, 'Inactive service edited')
        self.assertFalse(inactive_service.is_active)

    # --- the gates ---

    def test_csrf_is_enforced(self):
        strict = Client(enforce_csrf_checks=True)
        response = strict.post(self.save_url('songbook'), {
            'name': 'X', 'short_name': 'X', 'lang': 'forged'})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(songs.Book.objects.filter(name='X').exists())

    def test_endpoints_are_post_only(self):
        response = self.client.get(self.save_url('tatib'))
        self.assertEqual(response.status_code, 405)

    def test_login_hook_hides_the_controls_and_refuses_writes(self):
        with self.settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True):
            page = self.client.get(reverse('web-tatib'))
            self.assertContains(page, 'data-panel="tatib"')       # the sidebar itself
            self.assertNotContains(page, 'editor-add')
            self.assertNotContains(page, 'row-edit')
            self.assertEqual(self.client.get(self.new_url('tatib')).status_code, 403)
            self.assertEqual(self.client.post(self.save_url('tatib'), {'name': 'X'}).status_code, 403)
            self.assertFalse(tatib.TataIbadah.objects.filter(name='X').exists())

    def test_login_hook_lets_staff_through(self):
        staff = User.objects.create_user('editor', password='secret', is_staff=True)
        self.client.force_login(staff)
        with self.settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True):
            self.assertContains(self.client.get(reverse('web-tatib')), 'editor-add')
        self.assertEqual(self.client.get(self.new_url('tatib')).status_code, 200)

    # --- what the shell renders by default ---

    def test_controls_appear_for_editable_rows_only(self):
        free = self.client.get(reverse('web-book', args=[self.harian.pk]))
        self.assertContains(free, 'data-editor-open="songbook"')
        self.assertContains(free, 'data-editor-open="song"')
        hymn = self.client.get(reverse('web-book', args=[self.nkb.pk]))
        # no row control for its songs (the add button is allowed and carries no id)
        self.assertNotContains(hymn, 'data-editor-open="song" data-editor-id')
        self.assertNotContains(hymn, 'data-editor-id="%d"' % self.nkb.pk)  # its own row

    def test_add_buttons_render_per_section(self):
        self.assertContains(self.client.get(reverse('web-books')),
                            'data-editor-open="songbook"')
        self.assertContains(self.client.get(reverse('web-tatib')),
                            'data-editor-open="tatib"')
        self.assertNotContains(self.client.get(reverse('web-bible')), 'data-editor-open')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ServiceEntryViewTests(TestCase):
    """The service entry endpoints (spec 006, slice 2).

    Written before the endpoints exist: every one names the URL it expects, so the
    red run is a page of NoReverseMatch until the wiring lands.
    """

    @classmethod
    def setUpTestData(cls):
        cls.tatib = tatib.TataIbadah.objects.create(name='Ibadah Minggu III')

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        cls.matius = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.BookTranslation.objects.create(
            version=version, book=bible.Book.objects.create(
                name='Mrk', testament='new', number_of_chapters=16), translation='Markus')
        for number in range(1, 6):
            bible.Verse.objects.create(book_translation=cls.matius, chapter=5, verse=number,
                                       text=f'ayat {number}')

        cls.songbook = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.songbook, number=152,
                                             title='Ada Kuasa dalam DarahNya')
        for number in (1, 2, 3):
            songs.Verse.objects.create(song=cls.song, number=number, lyric=f'bait {number}')

    def new_url(self, kind):
        return reverse('web-entry-new') + f'?kind={kind}&tatib={self.tatib.pk}'

    def save_new_url(self):
        return reverse('web-entry-save-new') + f'?tatib={self.tatib.pk}'

    def make(self, **fields):
        fields.setdefault('order_number', 1)
        return tatib.ServiceEntry.objects.create(tatib=self.tatib, **fields)

    def html(self):
        return self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()

    def pane(self):
        return self.html().split('id="readBody"')[1]

    # --- the form fragment per kind ----------------------------------------

    def test_the_new_fragment_offers_the_fields_its_kind_needs(self):
        cases = {
            'text': ['name="title"', 'name="text"'],
            'single_screen_text': ['name="title"', 'name="text"'],
            'scripture': ['name="book_translation"', 'name="chapter"', 'name="verse_start"',
                          'name="verse_end"'],
            'song': ['name="song"', 'id="entry-verses"'],
            'section_break': [],
        }
        for kind, needles in cases.items():
            with self.subTest(kind=kind):
                response = self.client.get(self.new_url(kind))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'data-entry-form="{kind}"')   # the kind is the form's
                for needle in needles:
                    self.assertContains(response, needle)

    def test_the_scripture_fragment_groups_searchable_books_by_testament(self):
        response = self.client.get(self.new_url('scripture'))
        self.assertContains(response, 'Matius')
        self.assertContains(response, 'data-chapters="28"')
        self.assertContains(response, 'Perjanjian Baru')
        self.assertContains(response, 'data-entry-picker="book"')
        self.assertContains(response, 'placeholder="Filter books..."')

    def test_the_chapter_endpoint_returns_actual_verse_numbers(self):
        response = self.client.get(reverse('web-entry-chapter-verses',
                                           kwargs={'pk': self.matius.pk, 'chapter': 5}))
        self.assertEqual(response.json()['verses'], [1, 2, 3, 4, 5])

    def test_song_picker_and_verse_checkboxes_live_in_dropdowns(self):
        response = self.client.get(self.new_url('song'))
        self.assertContains(response, 'data-entry-picker="song"')
        self.assertContains(response, 'placeholder="Search songs..."')
        self.assertContains(response, 'data-verses-trigger')
        self.assertContains(response, 'data-verses-summary')

    def test_text_and_break_titles_say_optional(self):
        self.assertContains(self.client.get(self.new_url('text')), 'Title <span class="editor__hint">(optional)</span>')
        self.assertContains(self.client.get(self.new_url('section_break')),
                            'Label <span class="editor__hint">(optional)</span>')

    def test_empty_text_is_rejected_and_field_marked(self):
        for kind in (tatib.ServiceEntryKind.TEXT, tatib.ServiceEntryKind.SINGLE_SCREEN_TEXT):
            with self.subTest(kind=kind):
                response = self.client.post(self.save_new_url(), {
                    'kind': kind, 'title': 'Heading', 'text': '   ',
                })
                self.assertEqual(response.status_code, 400)
                self.assertContains(response, 'is-invalid', status_code=400)
                self.assertContains(response, 'aria-invalid="true"', status_code=400)
        self.assertFalse(self.tatib.service_entries.exists())

    def test_shared_dialog_has_cancel_but_no_x_button(self):
        html = self.client.get(reverse('web-tatib-service', args=[self.tatib.pk])).content.decode()
        self.assertNotIn('class="editor__close"', html)
        self.assertIn('data-editor-close', self.client.get(self.new_url('text')).content.decode())

    # --- creating ----------------------------------------------------------

    def test_creating_a_text_entry_appends_it_to_the_service(self):
        response = self.client.post(self.save_new_url(),
                                    {'kind': tatib.ServiceEntryKind.TEXT, 'title': 'Salam', 'text': 'Kasih karunia'})
        self.assertEqual(response.status_code, 200)
        entry = self.tatib.service_entries.get()
        self.assertEqual(response.json()['id'], entry.pk)
        self.assertEqual(entry.order_number, 1)

    def test_creating_a_scripture_entry(self):
        response = self.client.post(self.save_new_url(), {
            'kind': tatib.ServiceEntryKind.SCRIPTURE, 'book_translation': self.matius.pk, 'chapter': 5,
            'verse_start': 2, 'verse_end': 4})
        self.assertEqual(response.status_code, 200)
        entry = self.tatib.service_entries.get()
        self.assertEqual(entry.resolve(), ('Matius 5:2-4', '2 ayat 2\n\n3 ayat 3\n\n4 ayat 4'))

    def test_creating_a_song_entry_stores_the_verses_it_includes(self):
        response = self.client.post(self.save_new_url(),
                                    {'kind': tatib.ServiceEntryKind.SONG, 'song': self.song.pk, 'verses': ['1', '3']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tatib.service_entries.get().verses, [1, 3])

    def test_creating_a_section_break_without_a_label(self):
        response = self.client.post(self.save_new_url(), {'kind': tatib.ServiceEntryKind.SECTION_BREAK, 'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tatib.service_entries.get().resolve(), ('', ''))

    def test_deleted_song_cannot_be_added_as_a_new_service_entry(self):
        deleted_song = songs.Song.objects.create(
            book=self.songbook, number=153, title='Deleted entry target')
        songs.Verse.objects.create(song=deleted_song, number=1, lyric='Do not include')
        deleted_song.delete()
        response = self.client.post(self.save_new_url(), {
            'kind': tatib.ServiceEntryKind.SONG, 'song': deleted_song.pk, 'verses': ['1'],
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.tatib.service_entries.filter(song=deleted_song).exists())

    def test_the_next_entry_lands_after_the_last_one(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=1)
        self.client.post(self.save_new_url(), {'kind': tatib.ServiceEntryKind.TEXT, 'text': 'b'})
        self.assertEqual([e.order_number for e in self.tatib.service_entries.all()], [1, 2])

    def test_a_new_entry_can_be_inserted_at_the_beginning(self):
        legacy = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, order_number=1, item_type=tatib.TataIbadahItemType.TEXT,
            title='Old', text='old')
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=2)
        self.client.post(self.save_new_url(),
                         {'kind': tatib.ServiceEntryKind.TEXT, 'text': 'b', 'after': 'start'})
        legacy.refresh_from_db()
        self.assertEqual(self.tatib.service_entries.get(text='b').order_number, 1)
        self.assertEqual(legacy.order_number, 2)              # the legacy row shifted up too
        self.assertEqual(self.tatib.service_entries.get(text='a').order_number, 3)
        order = sorted([legacy.order_number]
                       + [e.order_number for e in self.tatib.service_entries.all()])
        self.assertEqual(order, [1, 2, 3])                    # still contiguous

    # --- refusing ----------------------------------------------------------

    def test_a_song_entry_without_verses_is_refused_and_writes_nothing(self):
        response = self.client.post(self.save_new_url(),
                                    {'kind': tatib.ServiceEntryKind.SONG, 'song': self.song.pk, 'verses': []})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'at least one verse', status_code=400)
        self.assertFalse(self.tatib.service_entries.exists())

    def test_a_passage_without_a_chapter_is_refused(self):
        response = self.client.post(self.save_new_url(), {
            'kind': tatib.ServiceEntryKind.SCRIPTURE, 'book_translation': self.matius.pk, 'verse_start': 2})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.tatib.service_entries.exists())

    def test_the_endpoints_are_post_only(self):
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a')
        self.assertEqual(self.client.get(reverse('web-entry-save-new')).status_code, 405)
        self.assertEqual(self.client.get(reverse('web-entry-save',
                                                 kwargs={'pk': entry.pk})).status_code, 405)

    def test_editing_an_entry_keeps_its_place(self):
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=3)
        response = self.client.post(reverse('web-entry-save', kwargs={'pk': entry.pk}),
                                    {'kind': tatib.ServiceEntryKind.TEXT, 'title': 'Baru', 'text': 'b'})
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual((entry.order_number, entry.title), (3, 'Baru'))

    def test_deleting_an_entry_closes_the_gap_across_both_tables(self):
        first = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Opening', text='First', order_number=1)
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=2)
        last = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Closing', text='Last', order_number=3)
        response = self.client.post(reverse('web-entry-delete', kwargs={'pk': entry.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(tatib.ServiceEntry.objects.filter(pk=entry.pk).exists())
        first.refresh_from_db()
        last.refresh_from_db()
        self.assertEqual((first.order_number, last.order_number), (1, 2))

    @override_settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True)
    def test_the_editor_gate_covers_entries(self):
        self.assertEqual(self.client.get(self.new_url('text')).status_code, 403)
        self.assertEqual(self.client.post(self.save_new_url(), {'kind': tatib.ServiceEntryKind.TEXT}).status_code, 403)

    # --- what the pickers need ---------------------------------------------

    def test_a_deleted_saved_song_remains_available_when_editing_its_existing_entry(self):
        entry = self.make(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2, 3])
        self.song.delete()
        form = self.client.get(reverse('web-entry-edit', kwargs={'pk': entry.pk}))
        self.assertEqual(form.status_code, 200)
        response = self.client.post(reverse('web-entry-save', kwargs={'pk': entry.pk}), {
            'kind': tatib.ServiceEntryKind.SONG, 'song': self.song.pk, 'verses': ['1', '2', '3'],
        })
        self.assertEqual(response.status_code, 200, response.content[:500])
        entry.refresh_from_db()
        self.assertEqual(entry.song_id, self.song.pk)

    def test_the_song_options_are_grouped_by_songbook_and_searchable(self):
        response = self.client.get(reverse('web-entry-song-options') + '?q=kuasa')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kidung Jemaat')
        self.assertContains(response, f'data-song="{self.song.pk}"')

    def test_song_picker_and_verse_picker_exclude_deleted_rows_and_parents(self):
        deleted_song = songs.Song.objects.create(
            book=self.songbook, number=154, title='Deleted picker song')
        deleted_book = songs.Book.objects.create(
            name='Deleted picker book', short_name='DPB')
        child_song = songs.Song.objects.create(book=deleted_book, title='Child of deleted book')
        deleted_verse = self.song.verse_set.get(number=2)
        deleted_song.delete()
        deleted_book.delete()
        deleted_verse.delete()

        options = self.client.get(reverse('web-entry-song-options'))
        verses = self.client.get(reverse('web-entry-song-verses', kwargs={'pk': self.song.pk}))
        self.assertNotContains(options, f'data-song="{deleted_song.pk}"')
        self.assertNotContains(options, f'data-song="{child_song.pk}"')
        self.assertEqual(verses.json()['verses'], [1, 3])

    def test_the_song_fragment_checks_every_verse_of_its_song(self):
        entry = self.make(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2, 3])
        response = self.client.get(reverse('web-entry-edit', kwargs={'pk': entry.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="verses"')
        html = response.content.decode()
        for number in (1, 2, 3):                       # checked, whatever the attribute order
            self.assertRegex(html, rf'value="{number}"[^>]*checked')

    # --- the pane: entries in the service's own stage ----------------------

    def test_the_service_stage_renders_its_entries_after_its_legacy_items(self):
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='PAMUNGKAHNI', text='Paragenda: ...', order_number=1)
        self.make(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='Kasih karunia')
        response = self.client.get(reverse('web-tatib-service', args=[self.tatib.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('PAMUNGKAHNI', html)                       # the legacy item, untouched
        self.assertIn('Kasih karunia', html)
        self.assertIn('tatib__item--entry', html)
        self.assertLess(html.index('PAMUNGKAHNI'), html.index('Kasih karunia'))

    def test_a_service_without_entries_renders_as_it_did_before(self):
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='PAMUNGKAHNI', text='Paragenda: ...', order_number=1)
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertIn('PAMUNGKAHNI', html)
        self.assertNotIn('tatib__item--entry', html)
        pane = html.split('id="readBody"')[1]
        self.assertIn('data-entry-start', pane)              # the start bar rides above it
        self.assertLess(pane.index('data-entry-start'), pane.index('PAMUNGKAHNI'))

    def test_a_scripture_entry_offers_a_jump_to_its_passage(self):
        self.make(kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                  chapter=5, verse_start=2, verse_end=4)
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertIn(f'/bible/{self.matius.book_id}/5/', html)
        self.assertIn('?v=2&amp;to=4', html)

    def test_a_song_entry_offers_a_jump_to_its_song(self):
        self.make(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2, 3])
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        pane = html.split('id="readBody"')[1]
        self.assertIn(reverse('web-song', args=[self.song.pk]), pane)
        self.assertIn('Kidung Jemaat 152', pane)                 # its reference, as the jump
        self.assertNotIn('bait 1', pane)                         # no lyrics: the display has those

    def test_a_song_entry_warns_when_its_target_has_been_soft_deleted(self):
        self.make(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2, 3])
        self.song.verse_set.get(number=2).delete()
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertIn('entry__deleted-warning', html)
        self.assertIn('This song, songbook, or an included verse was deleted.', html)

    def test_the_add_controls_sit_on_each_item(self):
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a')
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        for kind in ('scripture', 'song', 'text', 'section_break'):
            self.assertIn(f'data-entry-open="{kind}"', html)
        self.assertIn(f'data-entry-after="e{entry.pk}"', html)

    # --- clamping a text in the pane (spec 031) -----------------------------

    def test_a_long_text_is_clamped_to_three_lines_with_an_ellipsis(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='satu\ndua\ntiga\nempat\nlima')
        pane = self.pane()
        self.assertIn('satu', pane)
        self.assertIn('dua', pane)
        self.assertIn('tiga…', pane)                          # the kept third line, marked
        self.assertNotIn('empat', pane)
        self.assertNotIn('lima', pane)
        self.assertIn('data-clipped="true"', pane)

    def test_blank_lines_count_toward_the_pane_clamp(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='satu\n\ntiga\nempat')
        pane = self.pane()
        self.assertIn('data-clipped="true"', pane)
        self.assertIn('tiga…', pane)
        self.assertNotIn('empat', pane)

    def test_a_short_text_is_not_clamped(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='satu\ndua\ntiga')
        pane = self.pane()
        self.assertNotIn('tiga…', pane)
        self.assertNotIn('data-clipped', pane)

    def test_a_legacy_text_row_is_clamped_too(self):
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT, order_number=1,
            title='Old', text='satu\ndua\ntiga\nempat')
        pane = self.pane()
        self.assertIn('tiga…', pane)
        self.assertNotIn('empat', pane)
        self.assertIn('data-clipped="true"', pane)

    # --- the entry preview (spec 032) ---------------------------------------

    def test_a_passage_offers_a_preview_with_its_reference_and_full_text(self):
        self.make(kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                  chapter=5, verse_start=2, verse_end=3)
        html = self.html()
        self.assertIn('data-preview-open', html)
        self.assertIn('preview__ref', html)
        self.assertIn('Matius 5:2-3', html)
        self.assertIn('ayat 2', html)
        self.assertIn('ayat 3', html)

    def test_a_song_preview_lists_its_book_title_and_verse_tabs(self):
        self.make(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 3])
        html = self.html()
        self.assertIn('data-preview-open', html)
        self.assertIn('Kidung Jemaat', html)
        self.assertIn('preview__tab', html)
        self.assertIn('>1<', html)
        self.assertIn('>3<', html)

    def test_a_song_preview_has_no_tabs_for_a_single_verse(self):
        self.make(kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[2])
        html = self.html()
        self.assertIn('data-preview-open', html)
        self.assertNotIn('preview__tab', html)

    def test_only_a_clipped_text_offers_a_preview(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='satu\ndua\ntiga')
        self.assertNotIn('data-preview-open', self.html())
        self.make(kind=tatib.ServiceEntryKind.TEXT, order_number=2, text='satu\ndua\ntiga\nempat')
        self.assertIn('data-preview-open', self.html())

    def test_a_section_break_offers_no_preview(self):
        self.make(kind=tatib.ServiceEntryKind.SECTION_BREAK, title='Doa')
        self.assertNotIn('data-preview-open', self.html())

    # --- the entry controls live in the item (spec 033) ---------------------

    def test_the_entry_controls_live_in_the_item_not_the_add_bar(self):
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a')
        html = self.html()
        item = html.split(f'data-entry-pk="{entry.pk}"')[1].split('</section>')[0]
        self.assertIn(f'data-entry-edit="{entry.pk}"', item)
        self.assertIn(f'data-entry-delete="{entry.pk}"', item)
        bar = html.split(f'data-entry-after="e{entry.pk}"')[1].split('</div>')[0]
        self.assertNotIn('entry__ctrl', bar)
        self.assertNotIn('data-entry-edit', bar)

    def test_invalid_insertion_form_keeps_its_after_marker(self):
        first = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a')
        response = self.client.post(self.save_new_url(), {
            'kind': tatib.ServiceEntryKind.SONG, 'song': self.song.pk,
            'verses': [], 'after': f'e{first.pk}',
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, f'name="after" value="e{first.pk}"', status_code=400)

    def test_an_entry_is_inserted_after_the_item_whose_control_was_used(self):
        # after, never before: the new entry takes the next place and the rest move down
        first = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=1)
        second = self.make(kind=tatib.ServiceEntryKind.TEXT, text='b', order_number=2)
        response = self.client.post(self.save_new_url(),
                                    {'kind': tatib.ServiceEntryKind.TEXT, 'text': 'c', 'after': f'e{first.pk}'})
        self.assertEqual(response.status_code, 200)
        second.refresh_from_db()
        self.assertEqual([(e.order_number, e.text) for e in self.tatib.service_entries.all()],
                         [(1, 'a'), (2, 'c'), (3, 'b')])

    def test_text_entry_is_inserted_after_a_legacy_row_and_shifts_later_rows(self):
        first = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Opening', text='Legacy one', order_number=1)
        second = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Hymn', text='Legacy two', order_number=2)
        third = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Prayer', text='Legacy three', order_number=3)
        existing = self.make(kind=tatib.ServiceEntryKind.TEXT, title='Later entry',
                             text='Entry after the old rows', order_number=4)

        response = self.client.post(self.save_new_url(), {
            'kind': tatib.ServiceEntryKind.TEXT, 'title': 'Inserted', 'text': 'New entry',
            'after': f'l{second.pk}',
        })

        self.assertEqual(response.status_code, 200)
        inserted = tatib.ServiceEntry.objects.get(title='Inserted')
        third.refresh_from_db()
        existing.refresh_from_db()
        self.assertEqual(
            sorted([(item.order_number, item.text) for item in
                    tatib.TataIbadahItem.objects.filter(tatib=self.tatib)] +
                   [(entry.order_number, entry.text) for entry in
                    tatib.ServiceEntry.objects.filter(tatib=self.tatib)]),
            [(1, 'Legacy one'), (2, 'Legacy two'), (3, 'New entry'),
             (4, 'Legacy three'), (5, 'Entry after the old rows')],
        )
        self.assertEqual((first.order_number, inserted.order_number), (1, 3))

    # --- an empty service, and what the sidebar lists -----------------------

    def test_an_empty_service_invites_its_first_item(self):
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertIn('This Tata Ibadah is empty', html)
        for label in ('Add Passage', 'Add Song', 'Add Text', 'Add Break'):
            self.assertIn(label, html)
        self.assertIn('entry__empty-btn', html)

    def test_a_service_built_only_from_entries_is_listed_in_the_sidebar(self):
        # the sidebar used to keep only services with a legacy text item, which would
        # have made a service of entries invisible
        self.make(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='a')
        response = self.client.get(reverse('web-tatib') + '?mode=template')
        self.assertContains(response, reverse('web-tatib-service', args=[self.tatib.pk]))

    def test_an_empty_service_is_listed_so_it_can_be_filled(self):
        # the owner's call: an empty service has to be reachable, and its page says so
        response = self.client.get(reverse('web-tatib') + '?mode=template')
        self.assertContains(response, reverse('web-tatib-service', args=[self.tatib.pk]))

    def test_every_entry_carries_its_own_edit_and_delete(self):
        first = self.make(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='a')
        second = self.make(kind=tatib.ServiceEntryKind.TEXT, title='Doa', text='b',
                           order_number=2)
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        for entry in (first, second):
            self.assertIn(f'data-entry-edit="{entry.pk}"', html)
            self.assertIn(f'data-entry-delete="{entry.pk}"', html)

    def test_the_legacy_items_themselves_carry_no_edit_or_delete(self):
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='PAMUNGKAHNI', text='a', order_number=1)
        self.make(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='b')
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertEqual(html.count('data-entry-edit="'), 1)      # the entry's, not the item's
        self.assertEqual(html.count('data-entry-open="scripture"'), 3)   # the start bar and both rows

    def test_a_service_with_only_entries_is_not_empty(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='a')
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertNotIn('This Tata Ibadah is empty', html)
        self.assertIn('entry__add-btn', html)             # the per-item controls, instead

    def test_the_contents_list_carries_the_entries_too(self):
        entry = self.make(kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                          chapter=5, verse_start=2)
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        toc = html.split('id="chList"')[1]
        self.assertIn('Matius 5:2', toc)
        self.assertIn(f'href="#ti-e{entry.pk}"', toc)            # the row points at its block
        self.assertIn(f'id="ti-e{entry.pk}"', html)

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_the_pane_and_contents_list_follow_the_shared_order(self):
        legacy = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Legacy second', text='Old words', order_number=2)
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, title='Entry first',
                          text='New words', order_number=1)

        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        pane = html.split('id="readBody"', 1)[1]
        toc = html.split('id="chList"', 1)[1]
        self.assertLess(pane.index('Entry first'), pane.index('Legacy second'))
        self.assertLess(toc.index('Entry first'), toc.index('Legacy second'))
        self.assertIn(f'href="#ti-e{entry.pk}"', toc)
        self.assertIn(f'href="#ti-{legacy.order_number}"', toc)

    def test_the_verses_of_a_song_come_back_all_included(self):
        response = self.client.get(reverse('web-entry-song-verses', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['verses'], [1, 2, 3])

    def test_the_verse_count_of_a_chapter(self):
        response = self.client.get(reverse('web-entry-chapter-verses',
                                           kwargs={'pk': self.matius.pk, 'chapter': 5}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 5)


class ServiceEntryReorderTests(TestCase):
    """The reorder endpoint (spec 006, slice 3).

    It follows the conventions the current item API already uses: one POST of
    `{entry, order_number}` pairs to a `/reorder` URL, answering with the order it left
    behind, rather than a per-row endpoint. Written before the endpoint exists, so the
    red run is a page of NoReverseMatch.
    """

    @classmethod
    def setUpTestData(cls):
        cls.tatib = tatib.TataIbadah.objects.create(name='Ibadah Minggu III')
        cls.other = tatib.TataIbadah.objects.create(name='Ibadah Sore')
        # This fixture is one valid shared sequence: entries can move in their slots,
        # while a legacy row between them keeps its place.
        cls.legacy = tatib.TataIbadahItem.objects.create(
            tatib=cls.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pujian', text='KJ 120', order_number=2)

    def setUp(self):
        self.first = self.make(1, 'Pembukaan', 'Kasih karunia')
        self.second = self.make(3, 'Penutup', 'Amin')
        self.third = self.make(4, 'Doa', 'Bersyukurlah')
        self.elsewhere = tatib.ServiceEntry.objects.create(
            tatib=self.other, kind=tatib.ServiceEntryKind.TEXT,
            title='Sore', text='Selamat sore', order_number=1)

    def make(self, order, title, text):
        return tatib.ServiceEntry.objects.create(
            tatib=self.tatib, kind=tatib.ServiceEntryKind.TEXT, title=title, text=text,
            order_number=order)

    def url(self):
        return reverse('web-entry-reorder')

    def post(self, entries, service=None):
        payload = {'tatib': (service or self.tatib).pk,
                   'entries': [{'entry': entry.pk, 'order_number': number}
                               for number, entry in enumerate(entries, 1)]}
        return self.client.post(self.url(), data=json.dumps(payload),
                                content_type='application/json')

    def order_now(self, service=None):
        return list((service or self.tatib).service_entries
                    .order_by('order_number').values_list('pk', 'order_number'))

    # --- what a reorder does ------------------------------------------------

    def test_a_reorder_renumbers_the_entries_in_the_posted_order(self):
        response = self.post([self.third, self.first, self.second])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order_now(),
                         [(self.third.pk, 1), (self.first.pk, 3), (self.second.pk, 4)])

    def test_the_reorder_answers_with_the_order_it_left(self):
        response = self.post([self.third, self.first, self.second])
        self.assertEqual([row['entry'] for row in response.json()['entries']],
                         [self.third.pk, self.first.pk, self.second.pk])
        self.assertEqual([row['order_number'] for row in response.json()['entries']], [1, 3, 4])

    def test_the_numbers_stay_contiguous_from_one(self):
        # a list that names only one entry: it goes first, the rest follow in the order
        # they were in, and nothing is left with a hole or a duplicate
        response = self.post([self.second])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order_now(),
                         [(self.second.pk, 1), (self.first.pk, 3), (self.third.pk, 4)])

    def test_a_reorder_leaves_the_legacy_items_alone(self):
        self.post([self.third, self.first, self.second])
        self.legacy.refresh_from_db()
        self.assertEqual(self.legacy.order_number, 2)
        self.assertEqual(self.legacy.text, 'KJ 120')

    def test_reorder_repairs_the_shared_order_after_the_old_api_renumbers_only_old_rows(self):
        old_response = self.client.post('/api/tatib/items/reorder',
                                        data=json.dumps({'items': [
                                            {'item': self.legacy.pk, 'order_number': 1}]}),
                                        content_type='application/json')
        self.assertEqual(old_response.status_code, 200)
        response = self.post([self.third, self.first, self.second])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order_now(),
                         [(self.third.pk, 2), (self.first.pk, 3), (self.second.pk, 4)])
        self.legacy.refresh_from_db()
        self.assertEqual(self.legacy.order_number, 1)
        self.assertEqual([row['order_number'] for row in response.json()['entries']], [2, 3, 4])

    # --- what it refuses ----------------------------------------------------

    def test_an_entry_from_another_service_is_refused(self):
        response = self.post([self.first, self.elsewhere])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.order_now(),
                         [(self.first.pk, 1), (self.second.pk, 3), (self.third.pk, 4)])

    def test_a_reorder_without_its_service_is_refused(self):
        response = self.client.post(self.url(),
                                    data=json.dumps({'entries': [{'entry': self.first.pk,
                                                                  'order_number': 1}]}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_a_service_that_is_not_there_is_refused(self):
        response = self.post([self.first], service=self.tatib)
        self.assertEqual(response.status_code, 200)          # the real one still works
        missing = self.client.post(self.url(),
                                   data=json.dumps({'tatib': 99999, 'entries': []}),
                                   content_type='application/json')
        self.assertEqual(missing.status_code, 400)

    def test_a_reorder_is_post_only(self):
        self.assertEqual(self.client.get(self.url()).status_code, 405)

    @override_settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True)
    def test_a_reorder_is_refused_when_editors_need_a_login(self):
        self.assertEqual(self.post([self.first, self.second, self.third]).status_code, 403)
        self.assertEqual(self.order_now(),
                         [(self.first.pk, 1), (self.second.pk, 3), (self.third.pk, 4)])


class ServiceReorderPaneTests(TestCase):
    """Where the reorder chrome lives (spec 006, slice 3).

    The order is arranged in the SIDEBAR, where the order is listed: each entry's row carries
    its handle and arrows, and the Save/Discard strip sits below the sections filter, in the
    part of the sidebar that never scrolls. The pane keeps the entries themselves and the
    question before leaving. There is no Reorder button: the first drag starts the mode.
    """

    @classmethod
    def setUpTestData(cls):
        cls.tatib = tatib.TataIbadah.objects.create(name='Ibadah Minggu III')
        cls.empty = tatib.TataIbadah.objects.create(name='Ibadah Sore')

    def setUp(self):
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, kind=tatib.ServiceEntryKind.TEXT, title='Pembukaan',
            text='Kasih karunia', order_number=1)
        self.second = tatib.ServiceEntry.objects.create(
            tatib=self.tatib, kind=tatib.ServiceEntryKind.TEXT, title='Penutup',
            text='Amin', order_number=2)

    def page(self, service):
        return self.client.get(reverse('web-tatib-service', args=[service.pk]))

    def test_every_entry_carries_its_own_handle(self):
        response = self.page(self.tatib)
        for entry in self.tatib.service_entries.order_by('order_number'):
            self.assertContains(response, 'data-move-grip="%s"' % entry.pk)
        # only the grip: no arrows beside it, and nothing wrapped around it
        self.assertNotContains(response, 'data-move-up')
        self.assertNotContains(response, 'data-move-down')
        self.assertNotContains(response, 'toc__move')
        self.assertNotContains(response, 'toc__arrow')

    def test_a_section_break_carries_a_handle_too(self):
        """A break is an entry like any other: it can be moved in the order."""
        break_ = tatib.ServiceEntry.objects.create(
            tatib=self.tatib, kind=tatib.ServiceEntryKind.SECTION_BREAK, title='Doa',
            order_number=3)
        response = self.page(self.tatib)
        self.assertContains(response, 'data-move-grip="%s"' % break_.pk)
        # and it is not announced as hidden: it now holds a focusable control
        self.assertContains(response, 'aria-label="Reorder this break')

    def test_the_reorder_endpoint_sits_below_the_filter(self):
        response = self.page(self.tatib)
        self.assertContains(response, 'ch__reorder')
        self.assertContains(response, 'data-reorder-group')
        self.assertContains(response, 'data-reorder-endpoint="%s"' % reverse('web-entry-reorder'))
        self.assertContains(response, 'data-reorder-for="%s"' % self.tatib.pk)
        # spec 026: a change is written at once -- no Save and no Discard
        self.assertNotContains(response, 'data-reorder-save')
        self.assertNotContains(response, 'data-reorder-discard')

    def test_there_is_no_reorder_button(self):
        # the mode is entered by dragging: a button would be a second way in
        self.assertNotContains(self.page(self.tatib), 'data-reorder-start')

    def test_there_is_no_question_before_leaving(self):
        # spec 026: nothing is ever unsaved, so there is nothing to ask about
        self.assertNotContains(self.page(self.tatib), 'data-reorder-confirm')

    def test_a_service_with_no_entries_offers_no_reorder_chrome(self):
        response = self.page(self.empty)
        self.assertNotContains(response, 'data-reorder-group')
        self.assertNotContains(response, 'data-reorder-confirm')
        self.assertNotContains(response, 'data-move-grip')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ServiceProjectorTests(TestCase):
    """The new service projector (spec 006, slice 4).

    Written before the page exists: the URL it names does not resolve yet, so the
    first run is a page of NoReverseMatch.
    """

    @classmethod
    def setUpTestData(cls):
        cls.tatib = tatib.TataIbadah.objects.create(name='Ibadah Minggu III',
                                                    date=date(2026, 7, 12))

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru',
                                               abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        cls.matius = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=cls.matius, chapter=5, verse=2, text='ayat 2')
        bible.Verse.objects.create(book_translation=cls.matius, chapter=5, verse=3,
                                   text='ayat 3', title='Berbahagia')

        cls.songbook = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.songbook, number=152,
                                             title='Ada Kuasa dalam DarahNya')
        for number in (1, 2):
            songs.Verse.objects.create(song=cls.song, number=number, lyric=f'bait {number}')

    def projector_url(self):
        return reverse('web-service-projector', args=[self.tatib.pk])

    def make(self, order, **fields):
        return tatib.ServiceEntry.objects.create(tatib=self.tatib, order_number=order, **fields)

    def html(self):
        response = self.client.get(self.projector_url())
        self.assertEqual(response.status_code, 200)
        return response.content.decode()

    # --- the page and its path --------------------------------------------

    def test_the_projector_lives_on_a_path_of_its_own(self):
        self.assertEqual(self.projector_url(), f'/obs/service/{self.tatib.pk}/')

    def test_an_unknown_service_is_a_404(self):
        response = self.client.get(reverse('web-service-projector', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_it_is_a_page_of_its_own_with_nothing_but_the_words(self):
        html = self.html()
        self.assertIn('styles/design/tokens.css', html)      # the product's own dark palette
        self.assertIn('styles/design/projector.css', html)   # the display's own stylesheet
        self.assertIn('data-theme="dark"', html)             # pinned: a display is not a page
        self.assertNotIn('rail__menu', html)                 # not the reading shell
        self.assertNotIn('panelBody', html)
        self.assertIn('gkps-service-display', html)          # its own channel
        self.assertNotIn('<button', html)                    # no controls on screen
        self.assertNotIn('data-projector', html)

    # --- what it shows ----------------------------------------------------

    def screens(self, html=None):
        return (html or self.html()).split('<section class="screen')[1:]

    def test_a_passage_is_one_verse_a_screen_headed_by_its_reference_and_title(self):
        self.make(1, kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                  chapter=5, verse_start=2, verse_end=3)
        screens = self.screens()
        self.assertEqual(len(screens), 2)                    # one verse at a time
        self.assertIn('Matius 5:2', screens[0])
        self.assertIn('ayat 2', screens[0])
        self.assertNotIn('ayat 3', screens[0])
        self.assertIn('Matius 5:3', screens[1])
        self.assertIn('Berbahagia', screens[1])              # the verse's own title, when it has one
        self.assertIn('ayat 3', screens[1])

    def test_a_text_shows_two_lines_at_a_time_under_its_own_header(self):
        self.make(1, kind=tatib.ServiceEntryKind.TEXT, title='Salam',
                  text='satu\ndua\ntiga\nempat\nlima')
        screens = self.screens()
        self.assertEqual(len(screens), 3)                    # two, two, then the last alone
        for block in screens:
            self.assertIn('Salam', block)
        self.assertIn('satu', screens[0])
        self.assertIn('dua', screens[0])
        self.assertNotIn('tiga', screens[0])
        self.assertIn('tiga', screens[1])
        self.assertIn('empat', screens[1])
        self.assertIn('lima', screens[2])

    def test_a_single_screen_text_shows_the_whole_body_on_one_screen(self):
        self.make(1, kind=tatib.ServiceEntryKind.SINGLE_SCREEN_TEXT, title='Doa',
                  text='baris satu\nbaris dua\n\nbaris empat')
        screens = self.screens()
        self.assertEqual(len(screens), 1)                    # the whole body, one screen
        self.assertIn('data-fit="single"', screens[0])
        self.assertIn('Doa', screens[0])
        self.assertIn('baris satu', screens[0])
        self.assertIn('baris dua', screens[0])
        self.assertIn('baris empat', screens[0])

    def test_a_song_shows_its_lyrics_alone_in_pairs(self):
        self.make(1, kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2])
        screens = self.screens()
        self.assertEqual(len(screens), 2)                    # a verse to a screen
        self.assertIn('bait 1', screens[0])
        self.assertNotIn('bait 2', screens[0])
        self.assertIn('bait 2', screens[1])
        self.assertNotIn('Kidung Jemaat', screens[0])         # the words alone: no citation
        self.assertNotIn('screen__head', screens[0])

    def test_a_blank_line_holds_a_line_alone(self):
        self.make(1, kind=tatib.ServiceEntryKind.TEXT, text='satu\ndua\n\ntiga')
        screens = self.screens()
        self.assertEqual(len(screens), 2)
        self.assertIn('dua', screens[0])
        self.assertNotIn('tiga', screens[0])
        self.assertIn('tiga', screens[1])

    def test_a_section_break_shows_nothing(self):
        self.make(1, kind=tatib.ServiceEntryKind.SECTION_BREAK, title='Persembahan')
        screens = self.screens()
        self.assertEqual(len(screens), 1)
        self.assertIn('is-blank', screens[0])
        self.assertNotIn('Persembahan', screens[0])          # the operator's note stays off screen
        self.assertNotIn('screen__head', screens[0])
        self.assertNotIn('screen__line', screens[0])

    def test_the_legacy_rows_ride_along_before_the_entries(self):
        """A service built before spec 006 still displays: the pane's order is the
        display's order, and its rows take the same shape."""
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, order_number=1, item_type=tatib.TataIbadahItemType.TEXT,
            title='Nas', text='Tuhan adalah gembalaku')
        self.make(2, kind=tatib.ServiceEntryKind.TEXT, title='Salam', text='Tuhan beserta kita')
        screens = self.screens()
        self.assertEqual(len(screens), 2)
        self.assertIn('Nas', screens[0])
        self.assertIn('Tuhan adalah gembalaku', screens[0])
        self.assertIn('Salam', screens[1])

    def test_projector_follows_the_shared_order_not_the_model_type(self):
        tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, order_number=2, item_type=tatib.TataIbadahItemType.TEXT,
            title='Legacy second', text='Old words')
        self.make(1, kind=tatib.ServiceEntryKind.TEXT, title='Entry first', text='New words')

        screens = self.screens()

        self.assertEqual(len(screens), 2)
        self.assertIn('Entry first', screens[0])
        self.assertIn('Legacy second', screens[1])

    def test_a_lyric_change_reaches_a_fresh_projection(self):
        """What Update fetches is resolved at request time: the lyrics are the song's
        own, so an edit reaches every service that uses it."""
        self.make(1, kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1])
        self.assertIn('bait 1', self.html())
        songs.Verse.objects.filter(song=self.song, number=1).update(lyric='bait satu yang baru')
        self.assertIn('bait satu yang baru', self.html())

    def test_the_display_starts_at_its_first_screen_and_off(self):
        html = self.html()
        self.assertIn('data-current-screen="0"', html)
        self.assertIn('data-showing="false"', html)

    # --- the shell's project button ---------------------------------------

    def test_the_reading_page_offers_the_project_button_with_its_icon(self):
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        self.assertIn('data-project-open', html)
        self.assertIn(f'data-projector-url="/obs/service/{self.tatib.pk}/"', html)
        self.assertIn('data-project-service="', html)        # which service it would display
        self.assertIn('gkps-service-display', html)          # the same channel
        self.assertIn('data-project-label', html)            # the icon rides beside a label
        self.assertIn('Stop projecting', html)               # the label it takes while displaying
        # it rides with the date, at the top right, above the service's own words
        self.assertLess(html.index('read__head-top'), html.index('data-project-open'))
        self.assertLess(html.index('data-project-open'), html.index('readBody'))

    def test_the_reading_page_shows_only_the_reference_for_a_passage_and_a_song(self):
        """The pane is the running order: the words belong on the display."""
        self.make(1, kind=tatib.ServiceEntryKind.SCRIPTURE, book_translation=self.matius,
                  chapter=5, verse_start=2, verse_end=3)
        self.make(2, kind=tatib.ServiceEntryKind.SONG, song=self.song, verses=[1, 2])
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        pane = html.split('id="readBody"')[1]
        self.assertIn('Matius 5:2-3', pane)
        self.assertIn('Kidung Jemaat 152', pane)
        self.assertNotIn('ayat 2', pane)
        self.assertNotIn('bait 1', pane)

    def test_the_project_button_is_only_on_a_service(self):
        for name, args in (('web-home', []), ('web-tatib', []), ('web-search', [])):
            with self.subTest(url=name):
                response = self.client.get(reverse(name, args=args))
                self.assertNotIn('data-project-open', response.content.decode())


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LegacyObsRouteCompatibilityTests(TestCase):
    def test_existing_obs_pages_keep_their_paths_and_render(self):
        routes = {
            'obs-bible-dock': '/obs/bible/dock',
            'obs-bible-source': '/obs/bible/source',
            'obs-songs-dock': '/obs/songs/dock',
            'obs-songs-source': '/obs/songs/source',
            'obs-tatib-dock': '/obs/tatib/dock',
            'obs-tatib-source': '/obs/tatib/source',
            'obs-project-source': '/obs/project/source',
            'obs-project-settings': '/obs/project/settings',
        }
        for name, path in routes.items():
            with self.subTest(route=name):
                self.assertEqual(reverse(name), path)
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LegacyTatibItemEditorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = tatib.TataIbadah.objects.create(name='Ibadah Minggu III')
        cls.first = tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembukaan', text='KJ 120', order_number=1)
        cls.break_item = tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.END_OF_SECTION,
            title='', text='Catatan operator', order_number=2)
        cls.last = tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Penutup', text='Doa', order_number=3)

    def test_old_rows_render_edit_and_delete_controls(self):
        html = self.client.get(reverse('web-tatib-service', args=[self.service.pk])).content.decode()
        for item in (self.first, self.break_item, self.last):
            self.assertIn(f'data-old-item-edit="{item.pk}"', html)
            self.assertIn(f'data-old-item-delete="{item.pk}"', html)

    def test_old_row_add_controls_carry_a_stable_insertion_marker(self):
        html = self.client.get(reverse('web-tatib-service', args=[self.service.pk])).content.decode()
        for item in (self.first, self.break_item, self.last):
            self.assertIn(f'data-entry-after="l{item.pk}"', html)

    def test_text_item_form_prefills_its_title_and_text(self):
        response = self.client.get(reverse('web-old-item-edit', args=[self.first.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-old-item-form="text"')
        self.assertContains(response, 'value="Pembukaan"')
        self.assertContains(response, 'KJ 120')

    def test_text_item_update_changes_only_its_title_and_text(self):
        response = self.client.post(reverse('web-old-item-save', args=[self.first.pk]), {
            'title': 'Nyanyian Pembukaan', 'text': 'KJ 152',
            'item_type': tatib.TataIbadahItemType.END_OF_SECTION,
        })
        self.assertEqual(response.status_code, 200)
        self.first.refresh_from_db()
        self.break_item.refresh_from_db()
        self.assertEqual((self.first.item_type, self.first.title, self.first.text),
                         (tatib.TataIbadahItemType.TEXT, 'Nyanyian Pembukaan', 'KJ 152'))
        self.assertEqual(self.break_item.text, 'Catatan operator')

    def test_text_item_rejects_blank_text_without_saving(self):
        response = self.client.post(reverse('web-old-item-save', args=[self.first.pk]), {
            'title': 'Pembukaan', 'text': '   ',
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'aria-invalid="true"', status_code=400)
        self.first.refresh_from_db()
        self.assertEqual(self.first.text, 'KJ 120')

    def test_end_of_section_form_edits_its_note(self):
        form = self.client.get(reverse('web-old-item-edit', args=[self.break_item.pk]))
        self.assertContains(form, 'data-old-item-form="end_of_section"')
        self.assertNotContains(form, 'name="title"')
        response = self.client.post(reverse('web-old-item-save', args=[self.break_item.pk]), {
            'text': 'A moment of silence',
        })
        self.assertEqual(response.status_code, 200)
        self.break_item.refresh_from_db()
        self.assertEqual(self.break_item.text, 'A moment of silence')

    def test_delete_removes_the_old_row_and_keeps_the_remaining_order(self):
        entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
            title='Later', text='Entry', order_number=4)
        response = self.client.post(reverse('web-old-item-delete', args=[self.break_item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(tatib.TataIbadahItem.objects.filter(pk=self.break_item.pk).exists())
        self.assertEqual(list(self.service.tataibadahitem_set.order_by('order_number')
                              .values_list('pk', flat=True)), [self.first.pk, self.last.pk])
        self.last.refresh_from_db()
        entry.refresh_from_db()
        self.assertEqual((self.first.order_number, self.last.order_number, entry.order_number),
                         (1, 2, 3))

    def test_old_row_writes_are_post_only(self):
        self.assertEqual(self.client.get(reverse('web-old-item-save', args=[self.first.pk])).status_code,
                         405)
        self.assertEqual(self.client.get(reverse('web-old-item-delete', args=[self.first.pk])).status_code,
                         405)

    @override_settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True)
    def test_old_row_writes_respect_the_editor_login_mitigation(self):
        save = self.client.post(reverse('web-old-item-save', args=[self.first.pk]),
                                {'title': 'Changed', 'text': 'Changed'})
        delete = self.client.post(reverse('web-old-item-delete', args=[self.first.pk]))
        self.assertEqual((save.status_code, delete.status_code), (403, 403))
        self.first.refresh_from_db()
        self.assertEqual((self.first.title, self.first.text), ('Pembukaan', 'KJ 120'))

    def test_old_row_writes_reject_a_missing_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        page = client.get(reverse('web-tatib-service', args=[self.service.pk]))
        self.assertEqual(page.status_code, 200)
        response = client.post(reverse('web-old-item-delete', args=[self.first.pk]))
        self.assertEqual(response.status_code, 403)
