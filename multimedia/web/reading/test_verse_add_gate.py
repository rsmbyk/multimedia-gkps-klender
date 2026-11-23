"""The song page draws one Add verse control, not one per empty-state container (spec 224)."""
from django.test import TestCase
from django.urls import reverse

from multimedia.songs import models as songs


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

    def html(self, song):
        return self.client.get(reverse('web-song', args=[song.pk])).content.decode()

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

    def test_song_with_verses_keeps_its_single_add_row(self):
        html = self.html(self.with_verses)
        self.assertEqual(html.count('class="verse-add"'), 1)
        self.assertEqual(html.count('data-add-verse'), 1)
        self.assertNotIn('class="entry__empty"', html)
        for number in (1, 2, 3):
            self.assertIn(f'data-verse-number="{number}"', html)
