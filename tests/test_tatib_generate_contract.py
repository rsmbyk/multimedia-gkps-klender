"""A settled slot must survive the round trip to the generate endpoint (spec 167).

The dialog settles a slot by posting its form to the validate endpoint, which answers the
row's value and echoes back the form data. That echo is what the create request sends, and
the create request re-binds the same form to build the entry -- so a field that arrives with
repeated keys (a song's verses) has to survive both hops. It did not: the echo kept only the
last value of each key, the re-bound form was invalid, and a row the dialog showed as settled
came back as "not settled".
"""

from datetime import date

from django.test import TestCase
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


class GenerateContractTests(TestCase):
    def setUp(self):
        self.book = songs.Book.objects.create(name='Nyanyikanlah Kidung Baru',
                                              short_name='NKB', is_hymn_book=True)
        self.song = songs.Song.objects.create(book=self.book, number=152,
                                              title='Ada Kuasa', key='c')
        for number in (1, 2, 3):
            songs.Verse.objects.create(song=self.song, number=number, lyric=f'bait {number}')

        self.template = tatib.TataIbadah.objects.create(name='Skeleton', is_active=True)
        self.slot = tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.SONG, title='Lagu Pembuka', order_number=1)
        tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.TEXT, order_number=0,
            title='Votum', text='Pertolongan kita adalah dalam nama Tuhan.')

    def settle(self, **overrides):
        payload = {'entry': self.slot.pk, 'kind': tatib.ServiceEntryKind.SONG,
                   'song': self.song.pk, 'verses': [1, 2]}
        payload.update(overrides)
        response = self.client.post(reverse('web-entry-validate') + f'?entry={self.slot.pk}',
                                    payload)
        self.assertEqual(response.status_code, 200, response.content[:400])
        return response.json()

    def generate(self, data):
        payload = {
            'name': 'Ibadah Minggu', 'date': date(2026, 11, 1).isoformat(),
            'slots': [{'entry': self.slot.pk, 'data': data}],
        }
        return self.client.post(
            reverse('web-tatib-generate', args=[self.template.pk]),
            data=payload, content_type='application/json')

    def test_a_songs_verses_survive_the_round_trip(self):
        settled = self.settle()
        self.assertEqual(sorted(settled['data']['verses']), ['1', '2'], settled['data'])
        self.assertIn('Bait 1, 2', settled['value']['meta'], settled['value'])

        response = self.generate(settled['data'])
        self.assertEqual(response.status_code, 201, response.content[:400])
        service = tatib.TataIbadah.objects.get(pk=response.json()['id'])
        entry = service.service_entries.get(kind=tatib.ServiceEntryKind.SONG)
        self.assertEqual(entry.song_id, self.song.pk)
        self.assertEqual(entry.verses, [1, 2])

    def test_a_partial_song_settles_as_little_as_one_verse(self):
        settled = self.settle(verses=[3])
        self.assertEqual(settled['data']['verses'], ['3'], settled['data'])
        response = self.generate(settled['data'])
        self.assertEqual(response.status_code, 201, response.content[:400])
        service = tatib.TataIbadah.objects.get(pk=response.json()['id'])
        self.assertEqual(service.service_entries.get(kind=tatib.ServiceEntryKind.SONG).verses, [3])

    def test_an_unsettled_slot_still_fails(self):
        response = self.generate({})
        self.assertEqual(response.status_code, 400)
        self.assertIn('not settled', response.json()['error'])
