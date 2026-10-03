from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditorViewTests(TestCase):
    """Sidebar editors (spec 005): the forms, the endpoints, and the two gates."""

    @classmethod
    def setUpTestData(cls):
        lang = songs.Language.objects.create(name='Indonesian')
        cls.nkb = songs.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi', key='c')
        songs.Verse.objects.create(song=cls.song, number=1, lyric='Di waktu pagi aku bersyukur')
        songs.Verse.objects.create(song=cls.song, number=2, lyric='Bersama seluruh ciptaan')
        cls.next_song = songs.Song.objects.create(book=cls.nkb, number=13, title='Di Waktu Malam')
        cls.harian = songs.Book.objects.create(
            lang=lang, name='Kidung Harian', short_name='', is_hymn_book=False)
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
        lang = songs.Language.objects.create(name='Uji Bahasa')
        book = songs.Book.objects.create(lang=lang, name='Uji Urutan', is_hymn_book=False)
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
        url = reverse('web-editor-save-new', kwargs={'kind': 'song'})
        post = self.client.post(url, {'book': self.nkb.pk, 'title': 'Diselundupkan',
                                      'number': '', 'sub_number': '', 'key': ''})
        self.assertEqual(post.status_code, 404)
        self.assertFalse(songs.Song.objects.filter(title='Diselundupkan').exists())
        form = self.client.get(reverse('web-editor-new', kwargs={'kind': 'song'}),
                               {'book': self.nkb.pk})
        self.assertEqual(form.status_code, 404)

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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditorViewTests(TestCase):
    """Sidebar editors (spec 005): the forms, the endpoints, and the two gates."""

    @classmethod
    def setUpTestData(cls):
        lang = songs.Language.objects.create(name='Indonesian')
        cls.nkb = songs.Book.objects.create(
            lang=lang, name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        songs.Song.objects.create(book=cls.nkb, number=12, title='Di Waktu Pagi')
        cls.harian = songs.Book.objects.create(
            lang=lang, name='Kidung Harian', short_name='KH', is_hymn_book=False)
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

    def test_new_form_renders_every_field_with_csrf(self):
        response = self.client.get(self.new_url('songbook'))
        self.assertEqual(response.status_code, 200)
        for field in ('name', 'short_name', 'lang', 'is_hymn_book'):
            self.assertContains(response, 'name="%s"' % field)
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'New songbook')

    def test_edit_form_is_prefilled(self):
        response = self.client.get(
            reverse('web-editor-edit', kwargs={'kind': 'songbook', 'pk': self.harian.pk}))
        self.assertContains(response, 'value="Kidung Harian"')
        self.assertContains(response, 'Edit songbook')

    def test_tatib_edit_form_has_no_section_fields(self):
        response = self.client.get(
            reverse('web-editor-edit', kwargs={'kind': 'tatib', 'pk': self.service.pk}))
        self.assertNotContains(response, 'first_title')

    def test_unknown_kind_is_404(self):
        self.assertEqual(self.client.get(self.new_url('bible')).status_code, 404)

    # --- songbooks ---

    def test_create_songbook(self):
        response = self.client.post(self.save_url('songbook'), {
            'name': 'Kidung Baru', 'short_name': 'KB', 'lang': self.harian.lang_id,
            'is_hymn_book': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['ok'])
        self.assertTrue(songs.Book.objects.filter(name='Kidung Baru', short_name='KB').exists())

    def test_duplicate_short_name_is_refused(self):
        response = self.client.post(self.save_url('songbook'), {
            'name': 'Lain', 'short_name': 'KH', 'lang': self.harian.lang_id})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'already been used', status_code=400)
        self.assertFalse(songs.Book.objects.filter(name='Lain').exists())

    def test_editing_a_songbook_keeps_its_own_short_name(self):
        response = self.client.post(
            self.save_url('songbook', self.harian.pk),
            {'name': 'Kidung Harian Baru', 'short_name': 'KH', 'lang': self.harian.lang_id})
        self.assertEqual(response.status_code, 200, response.content[:400])
        self.harian.refresh_from_db()
        self.assertEqual(self.harian.name, 'Kidung Harian Baru')

    def test_hymn_songbook_cannot_be_edited(self):
        self.assertEqual(self.client.get(reverse(
            'web-editor-edit', kwargs={'kind': 'songbook', 'pk': self.nkb.pk})).status_code, 404)
        self.assertEqual(self.client.post(self.save_url('songbook', self.nkb.pk), {
            'name': 'Changed', 'short_name': 'NKB', 'lang': self.nkb.lang_id}).status_code, 404)

    # --- songs ---

    def test_create_song_in_the_open_songbook(self):
        response = self.client.post(self.save_url('song'), {
            'book': self.harian.pk, 'title': 'Lagu Baru', 'number': '', 'sub_number': '',
            'key': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(songs.Song.objects.filter(book=self.harian, title='Lagu Baru').exists())

    def test_a_hymn_book_refuses_new_songs_entirely(self):
        # A hymn corpus is published work: no new songs, with a number or without.
        for number in ('', '13'):
            response = self.client.post(self.save_url('song'), {
                'book': self.nkb.pk, 'title': 'Hymn Baru', 'number': number,
                'sub_number': '', 'key': ''})
            self.assertEqual(response.status_code, 404)
        self.assertFalse(songs.Song.objects.filter(title='Hymn Baru').exists())

    def test_duplicate_song_number_is_refused(self):
        songs.Song.objects.create(book=self.harian, number=12, title='Sudah Ada')
        response = self.client.post(self.save_url('song'), {
            'book': self.harian.pk, 'title': 'Lagu Lain', 'number': '12', 'sub_number': '', 'key': ''})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'already taken', status_code=400)

    def test_song_without_a_songbook_is_404(self):
        self.assertEqual(self.client.get(self.new_url('song')).status_code, 404)

    def test_a_hymn_song_cannot_be_edited(self):
        song = songs.Song.objects.get(book=self.nkb, number=12)
        self.assertEqual(self.client.get(reverse(
            'web-editor-edit', kwargs={'kind': 'song', 'pk': song.pk})).status_code, 404)

    def test_editing_a_free_song(self):
        song = songs.Song.objects.create(book=self.harian, title='Alpha')
        response = self.client.post(self.save_url('song', song.pk), {
            'title': 'Alpha Baru', 'number': '', 'sub_number': '', 'key': 'c'})
        self.assertEqual(response.status_code, 200, response.content[:400])
        song.refresh_from_db()
        self.assertEqual(song.title, 'Alpha Baru')

    # --- Tata Ibadah ---

    def test_create_tatib_with_its_first_section(self):
        response = self.client.post(self.save_url('tatib'), {
            'name': 'Ibadah Baru', 'date': '2026-11-01', 'is_active': 'on',
            'first_title': 'Pembukaan', 'first_text': 'KJ 1'})
        self.assertEqual(response.status_code, 200)
        service = tatib.TataIbadah.objects.get(name='Ibadah Baru')
        self.assertEqual(service.tataibadahitem_set.count(), 1)
        self.assertEqual(service.tataibadahitem_set.first().order_number, 1)

    def test_create_tatib_without_a_section_still_saves(self):
        self.client.post(self.save_url('tatib'), {'name': 'Tanpa Bagian', 'date': ''})
        service = tatib.TataIbadah.objects.get(name='Tanpa Bagian')
        self.assertEqual(service.tataibadahitem_set.count(), 0)

    def test_edit_tatib(self):
        response = self.client.post(self.save_url('tatib', self.service.pk), {
            'name': 'Ibadah Minggu IV', 'date': '2026-08-30', 'is_active': 'on'})
        self.assertEqual(response.status_code, 200, response.content[:400])
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Ibadah Minggu IV')

    # --- the gates ---

    def test_csrf_is_enforced(self):
        strict = Client(enforce_csrf_checks=True)
        response = strict.post(self.save_url('songbook'), {
            'name': 'X', 'short_name': 'X', 'lang': self.harian.lang_id})
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

        s_lang = songs.Language.objects.create(name='Indonesian')
        cls.songbook = songs.Book.objects.create(lang=s_lang, name='Kidung Jemaat',
                                                 short_name='KJ', is_hymn_book=True)
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

    # --- the form fragment per kind ----------------------------------------

    def test_the_new_fragment_offers_the_fields_its_kind_needs(self):
        cases = {
            'text': ['name="title"', 'name="text"'],
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

    def test_the_scripture_fragment_offers_the_books_and_their_chapter_counts(self):
        response = self.client.get(self.new_url('scripture'))
        self.assertContains(response, 'Matius')
        self.assertContains(response, 'data-chapters="28"')

    # --- creating ----------------------------------------------------------

    def test_creating_a_text_entry_appends_it_to_the_service(self):
        response = self.client.post(self.save_new_url(),
                                    {'kind': 'text', 'title': 'Salam', 'text': 'Kasih karunia'})
        self.assertEqual(response.status_code, 200)
        entry = self.tatib.service_entries.get()
        self.assertEqual(response.json()['id'], entry.pk)
        self.assertEqual(entry.order_number, 1)

    def test_creating_a_scripture_entry(self):
        response = self.client.post(self.save_new_url(), {
            'kind': 'scripture', 'book_translation': self.matius.pk, 'chapter': 5,
            'verse_start': 2, 'verse_end': 4})
        self.assertEqual(response.status_code, 200)
        entry = self.tatib.service_entries.get()
        self.assertEqual(entry.resolve(), ('Matius 5:2-4', '2 ayat 2\n\n3 ayat 3\n\n4 ayat 4'))

    def test_creating_a_song_entry_stores_the_verses_it_includes(self):
        response = self.client.post(self.save_new_url(),
                                    {'kind': 'song', 'song': self.song.pk, 'verses': ['1', '3']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tatib.service_entries.get().verses, [1, 3])

    def test_creating_a_section_break_without_a_label(self):
        response = self.client.post(self.save_new_url(), {'kind': 'section_break', 'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tatib.service_entries.get().resolve(), ('', ''))

    def test_the_next_entry_lands_after_the_last_one(self):
        self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=1)
        self.client.post(self.save_new_url(), {'kind': 'text', 'text': 'b'})
        self.assertEqual([e.order_number for e in self.tatib.service_entries.all()], [1, 2])

    # --- refusing ----------------------------------------------------------

    def test_a_song_entry_without_verses_is_refused_and_writes_nothing(self):
        response = self.client.post(self.save_new_url(),
                                    {'kind': 'song', 'song': self.song.pk, 'verses': []})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'at least one verse', status_code=400)
        self.assertFalse(self.tatib.service_entries.exists())

    def test_a_passage_without_a_chapter_is_refused(self):
        response = self.client.post(self.save_new_url(), {
            'kind': 'scripture', 'book_translation': self.matius.pk, 'verse_start': 2})
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
                                    {'kind': 'text', 'title': 'Baru', 'text': 'b'})
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual((entry.order_number, entry.title), (3, 'Baru'))

    def test_deleting_an_entry(self):
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a')
        response = self.client.post(reverse('web-entry-delete', kwargs={'pk': entry.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(tatib.ServiceEntry.objects.filter(pk=entry.pk).exists())

    @override_settings(SIDEBAR_EDITORS_REQUIRE_LOGIN=True)
    def test_the_editor_gate_covers_entries(self):
        self.assertEqual(self.client.get(self.new_url('text')).status_code, 403)
        self.assertEqual(self.client.post(self.save_new_url(), {'kind': 'text'}).status_code, 403)

    # --- what the pickers need ---------------------------------------------

    def test_the_song_options_are_grouped_by_songbook_and_searchable(self):
        response = self.client.get(reverse('web-entry-song-options') + '?q=kuasa')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kidung Jemaat')
        self.assertContains(response, f'data-song="{self.song.pk}"')

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
        self.assertIn('PAMUNGKAHNI', html.split('entry__add')[0])   # nothing injected before it

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
        self.assertIn(reverse('web-song', args=[self.song.pk]), html)
        self.assertIn('Ada Kuasa dalam DarahNya', html)          # the song's title

    def test_the_add_controls_sit_on_each_item(self):
        entry = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a')
        html = self.client.get(reverse('web-tatib-service',
                                       args=[self.tatib.pk])).content.decode()
        for kind in ('scripture', 'song', 'text', 'section_break'):
            self.assertIn(f'data-entry-open="{kind}"', html)
        self.assertIn(f'data-entry-after="e{entry.pk}"', html)

    def test_an_entry_is_inserted_after_the_item_whose_control_was_used(self):
        # after, never before: the new entry takes the next place and the rest move down
        first = self.make(kind=tatib.ServiceEntryKind.TEXT, text='a', order_number=1)
        second = self.make(kind=tatib.ServiceEntryKind.TEXT, text='b', order_number=2)
        response = self.client.post(self.save_new_url(),
                                    {'kind': 'text', 'text': 'c', 'after': first.pk})
        self.assertEqual(response.status_code, 200)
        second.refresh_from_db()
        self.assertEqual([(e.order_number, e.text) for e in self.tatib.service_entries.all()],
                         [(1, 'a'), (2, 'c'), (3, 'b')])

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
        self.assertEqual(html.count('data-entry-open="scripture"'), 2)   # both rows add

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

    def test_the_verses_of_a_song_come_back_all_included(self):
        response = self.client.get(reverse('web-entry-song-verses', kwargs={'pk': self.song.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['verses'], [1, 2, 3])

    def test_the_verse_count_of_a_chapter(self):
        response = self.client.get(reverse('web-entry-chapter-verses',
                                           kwargs={'pk': self.matius.pk, 'chapter': 5}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 5)
