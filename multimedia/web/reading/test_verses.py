"""Song verse verbs (spec 189): add/edit/delete/reorder + ID references."""
import json

from django.test import TestCase
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


class VerseVerbTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = songs.Book.objects.create(name='Lagu', short_name='LG', is_hymn_book=False)
        cls.song = songs.Song.objects.create(book=cls.book, title='Berdayakan')
        for number in (1, 2, 3):
            songs.Verse.objects.create(song=cls.song, number=number, lyric=f'stanza {number}')

    def _json(self, url, payload):
        return self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='fetch')

    def _live_numbers(self):
        return list(self.song.verse_set.filter(is_deleted=False).order_by('number').values_list('number', flat=True))

    def test_add_verse_appends_last(self):
        response = self._json(reverse('web-verse-new'), {'song': self.song.pk, 'lyric': 'new line'})
        self.assertTrue(response.status_code in (200, 302))
        self.assertEqual(self._live_numbers(), [1, 2, 3, 4])

    def test_edit_verse_keeps_number(self):
        verse = self.song.verse_set.filter(is_deleted=False).order_by('number')[1]
        response = self._json(reverse('web-verse-save', args=[verse.pk]), {'lyric': 'edited'})
        verse.refresh_from_db()
        self.assertEqual(verse.lyric, 'edited')
        self.assertEqual(verse.number, 2)

    def test_reorder_writes_order(self):
        live = list(self.song.verse_set.filter(is_deleted=False).order_by('number'))
        ordered = [live[2].pk, live[0].pk, live[1].pk]
        response = self._json(reverse('web-verse-reorder'), {'song': self.song.pk, 'ordered_ids': ordered})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.song.verse_set.filter(is_deleted=False).order_by('number').values_list('pk', flat=True)), ordered)
        self.assertEqual(self._live_numbers(), [1, 2, 3])

    def test_entry_keeps_lyric_after_reorder(self):
        service = tatib.TataIbadah.objects.create(name='Svc', date='2026-11-09')
        first = self.song.verse_set.filter(is_deleted=False).order_by('number')[0]
        entry = tatib.ServiceEntry.objects.create(
            tatib=service, kind=tatib.ServiceEntryKind.SONG, order_number=1,
            song=self.song, verses=[first.pk])
        live = list(self.song.verse_set.filter(is_deleted=False).order_by('number'))
        ordered = [live[1].pk, live[2].pk, first.pk]
        self._json(reverse('web-verse-reorder'), {'song': self.song.pk, 'ordered_ids': ordered})
        title, body = entry.resolve()
        self.assertIn('stanza 1', body)
        self.assertEqual(entry.verse_numbers(), [3])

    def test_delete_soft_and_renumbers(self):
        verse = self.song.verse_set.filter(is_deleted=False).order_by('number')[1]
        response = self.client.post(reverse('web-verse-delete', args=[verse.pk]),
                                    HTTP_X_REQUESTED_WITH='fetch')
        self.assertEqual(self._live_numbers(), [1, 2])
        self.assertEqual(self.song.verse_set.filter(pk=verse.pk).first().is_deleted, True)

    def test_hymn_song_refuses(self):
        hymn_book = songs.Book.objects.create(name='HKBP', short_name='HK', is_hymn_book=True)
        hymn_song = songs.Song.objects.create(book=hymn_book, number=1, title='Hymn')
        songs.Verse.objects.create(song=hymn_song, number=1, lyric='hymn')
        response = self._json(reverse('web-verse-new'), {'song': hymn_song.pk, 'lyric': 'no'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(hymn_song.verse_set.filter(is_deleted=False).values_list('lyric', flat=True)), ['hymn'])

    def test_reorder_mismatch_refused(self):
        live = list(self.song.verse_set.filter(is_deleted=False).order_by('number'))
        response = self._json(reverse('web-verse-reorder'),
                              {'song': self.song.pk, 'ordered_ids': [live[0].pk]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self._live_numbers(), [1, 2, 3])


class MigrationIdTests(TestCase):
    def test_entry_stores_ids_not_numbers(self):
        verse = self.song = songs.Verse.objects.filter(is_deleted=False).order_by('number')[0] if False else None
        # Sanity: resolve() and picker both go through ids.
        book = songs.Book.objects.create(name='B2', short_name='B2')
        song = songs.Song.objects.create(book=book, title='T')
        v1 = songs.Verse.objects.create(song=song, number=1, lyric='one')
        v2 = songs.Verse.objects.create(song=song, number=2, lyric='two')
        service = tatib.TataIbadah.objects.create(name='S2', date='2026-11-09')
        entry = tatib.ServiceEntry.objects.create(
            tatib=service, kind=tatib.ServiceEntryKind.SONG, order_number=1,
            song=song, verses=[v2.pk, v1.pk])
        self.assertEqual(entry.verse_numbers(), [1, 2])
        _, body = entry.resolve()
        self.assertEqual(body, 'one\n\ntwo')
