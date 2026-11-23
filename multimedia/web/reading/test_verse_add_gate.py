"""The song page draws one Add verse control, in the header while verses exist (spec 224, 231)."""
from django.test import TestCase, override_settings
from django.urls import reverse

from multimedia.songs import models as songs


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EmptySongAddControlTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = songs.Book.objects.create(
            name='Lagu Gate', short_name='LG', is_hymn_book=False)
        cls.empty = songs.Song.objects.create(book=cls.book, title='No verses')
        cls.deleted_only = songs.Song.objects.create(book=cls.book, title='Deleted only')
        songs.Verse.objects.create(
            song=cls.deleted_only, number=1, lyric='gone', is_deleted=True)
        cls.with_verses = songs.Song.objects.create(book=cls.book, title='Three verses')
        for number in (1, 2, 3):
            songs.Verse.objects.create(
                song=cls.with_verses, number=number, lyric=f'line {number}')
        cls.hymn_book = songs.Book.objects.create(
            name='Kidung Gate', short_name='KG', is_hymn_book=True)
        cls.hymn = songs.Song.objects.create(book=cls.hymn_book, title='Hymn song', number=1)
        songs.Verse.objects.create(song=cls.hymn, number=1, lyric='hymn line')

    def html(self, song):
        return self.client.get(reverse('web-song', args=[song.pk])).content.decode()

    def header(self, song):
        return (self.html(song).split('class="read__head-top"', 1)[1]
                .split('class="read__row"', 1)[0])

    def test_empty_song_has_no_after_verse_row(self):
        for song in (self.empty, self.deleted_only):
            with self.subTest(song=song.title):
                html = self.html(song)
                self.assertNotIn('class="verse-add"', html)
                self.assertIn('class="entry__empty"', html)

    def test_empty_song_has_one_add_verse_button(self):
        for song in (self.empty, self.deleted_only):
            with self.subTest(song=song.title):
                html = self.html(song)
                self.assertEqual(html.count('data-add-verse'), 1)
                invitation = html.split('class="entry__empty"', 1)[1].split('</article>', 1)[0]
                self.assertEqual(invitation.count('data-add-verse'), 1)

    def test_empty_song_has_no_header_actions(self):
        for song in (self.empty, self.deleted_only):
            with self.subTest(song=song.title):
                header = self.header(song)
                self.assertNotIn('data-add-verse', header)
                self.assertNotIn('data-project-goto', header)

    def test_song_with_verses_keeps_single_header_add_control(self):
        html = self.html(self.with_verses)
        self.assertEqual(html.count('class="verse-add"'), 0)
        self.assertEqual(html.count('data-add-verse'), 1)
        self.assertNotIn('class="entry__empty"', html)
        self.assertLess(html.index('data-add-verse'), html.index('data-project-goto'))
        header = self.header(self.with_verses)
        self.assertIn('data-add-verse', header)
        self.assertIn('data-project-goto', header)
        for number in (1, 2, 3):
            self.assertIn(f'data-verse-number="{number}"', html)

    def test_hymn_song_draws_no_add_verse_but_keeps_project(self):
        header = self.header(self.hymn)
        self.assertNotIn('data-add-verse', header)
        self.assertIn('data-project-goto', header)
