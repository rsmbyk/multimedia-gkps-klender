"""Spec 092: the public offline library contains complete, revisioned chunks."""

from pathlib import Path

from django.conf import settings
from django.test import TestCase

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


class OfflineLibraryEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=language, name='Terjemahan Baru', abbreviation='TB')
        cls.book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        translation = bible.BookTranslation.objects.create(
            version=version, book=cls.book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=1, verse=1, text='Permulaan')

        cls.songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.songbook, number=12, title='Kasih')
        songs.Verse.objects.create(song=cls.song, number=1, lyric='Kasih Tuhan')
        cls.service = tatib.TataIbadah.objects.create(name='Ibadah Minggu', is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=cls.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Doa', text='Tuhan dengar kami', order_number=1)
        cls.hidden = tatib.TataIbadah.objects.create(name='Hidden', is_active=False)

    def test_manifest_names_complete_public_chunks_and_revisions(self):
        response = self.client.get('/offline/manifest/')
        self.assertEqual(response.status_code, 200)
        chunks = {row['key']: row for row in response.json()['chunks']}
        self.assertIn(f'bible:{self.book.pk}', chunks)
        self.assertIn(f'songs:{self.songbook.pk}', chunks)
        self.assertIn(f'service:{self.service.pk}', chunks)
        self.assertNotIn(f'service:{self.hidden.pk}', chunks)
        self.assertEqual(len(chunks[f'songs:{self.songbook.pk}']['revision']), 64)

    def test_service_worker_uses_the_deployed_version_for_its_shell_cache(self):
        version = (Path(settings.BASE_DIR) / 'VERSION').read_text().strip()
        response = self.client.get('/service-worker.js')
        source = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"gkps-public-shell-{version}", source)
        self.assertNotIn('__VERSION__', source)
        self.assertEqual(response['Service-Worker-Allowed'], '/')
        self.assertIn('no-cache', response['Cache-Control'])

    def test_chunk_has_verses_lyrics_and_projector_screens(self):
        bible_data = self.client.get(f'/offline/chunk/bible/{self.book.pk}/').json()['data']
        self.assertEqual(bible_data['translations'][0]['verses'][0]['text'], 'Permulaan')
        song_data = self.client.get(f'/offline/chunk/songs/{self.songbook.pk}/').json()['data']
        self.assertEqual(song_data['songs'][0]['verses'][0]['lyric'], 'Kasih Tuhan')
        service_data = self.client.get(f'/offline/chunk/service/{self.service.pk}/').json()['data']
        self.assertEqual(service_data['screens'][0]['lines'][0]['text'], 'Tuhan dengar kami')
        self.assertEqual(service_data['rows'][0]['text'], 'Tuhan dengar kami')
        self.assertEqual(service_data['items'][0]['paras'][0]['text'], 'Tuhan dengar kami')
        self.assertEqual(service_data['toc'][0]['label'], 'Doa')

    def test_revision_changes_after_content_change(self):
        before = {row['key']: row['revision'] for row in self.client.get('/offline/manifest/').json()['chunks']}
        verse = self.song.verse_set.get(number=1)
        verse.lyric = 'New lyric'
        verse.save()
        after = {row['key']: row['revision'] for row in self.client.get('/offline/manifest/').json()['chunks']}
        self.assertNotEqual(before[f'songs:{self.songbook.pk}'], after[f'songs:{self.songbook.pk}'])
        self.assertEqual(before[f'bible:{self.book.pk}'], after[f'bible:{self.book.pk}'])

    def test_hidden_service_is_not_downloadable(self):
        response = self.client.get(f'/offline/chunk/service/{self.hidden.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_deleted_public_records_leave_manifest(self):
        songbook = songs.Book.objects.create(name='Temporary songs', short_name='TMP')
        service = tatib.TataIbadah.objects.create(name='Temporary service', is_active=True)
        before = {row['key'] for row in self.client.get('/offline/manifest/').json()['chunks']}
        self.assertIn(f'songs:{songbook.pk}', before)
        self.assertIn(f'service:{service.pk}', before)
        songbook.is_deleted = True
        songbook.save()
        service.is_active = False
        service.save()
        after = {row['key'] for row in self.client.get('/offline/manifest/').json()['chunks']}
        self.assertNotIn(f'songs:{songbook.pk}', after)
        self.assertNotIn(f'service:{service.pk}', after)
