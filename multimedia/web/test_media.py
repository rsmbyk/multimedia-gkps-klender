import hashlib
import json

from django.test import TestCase
from django.urls import reverse

from multimedia.tatib.models import MediaIdentity
from multimedia.tatib.models import ServiceEntry, TataIbadah


class MediaRegistrationTests(TestCase):
    def test_registers_identity_without_binary_data_and_reuses_it(self):
        payload = {'sha256': hashlib.sha256(b'example').hexdigest(),
                   'size': 7, 'family': 'pdf', 'name': 'notes.pdf'}
        url = reverse('web-media-register')
        first = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(first.status_code, 200)
        self.assertEqual(MediaIdentity.objects.count(), 1)
        payload['name'] = 'same bytes, other name.pdf'
        second = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(second.status_code, 200)
        self.assertEqual(MediaIdentity.objects.get().display_filename, 'notes.pdf')

    def test_rejects_invalid_or_conflicting_identity(self):
        url = reverse('web-media-register')
        payload = {'sha256': 'not-a-hash', 'size': 7, 'family': 'pdf', 'name': 'notes.pdf'}
        self.assertEqual(self.client.post(url, data=json.dumps(payload),
                         content_type='application/json').status_code, 400)
        payload['sha256'] = 'a' * 64
        self.assertEqual(self.client.post(url, data=json.dumps(payload),
                         content_type='application/json').status_code, 200)
        payload['family'] = 'image'
        self.assertEqual(self.client.post(url, data=json.dumps(payload),
                         content_type='application/json').status_code, 409)


class MediaEntryFlowTests(TestCase):
    def test_create_form_and_save_reference_without_binary_upload(self):
        service = TataIbadah.objects.create(name='Ibadah Minggu')
        media = MediaIdentity.objects.create(sha256='a' * 64, byte_count=120,
                                             family='pdf', display_filename='notes.pdf')
        form = self.client.get(reverse('web-entry-new'), {'kind': 'media', 'tatib': service.pk})
        self.assertEqual(form.status_code, 200)
        self.assertContains(form, 'Drop a file here')
        saved = self.client.post(reverse('web-entry-save-new') + f'?tatib={service.pk}',
                                 {'kind': 4, 'title': '', 'media': media.pk,
                                  'media_filename': 'notes.pdf'})
        self.assertEqual(saved.status_code, 200)
        entry = ServiceEntry.objects.get()
        self.assertEqual(entry.media_id, media.pk)
        self.assertEqual(entry.resolve(), ('notes.pdf', ''))
        from multimedia.web.reading.views import _tatib_stage
        items, _toc = _tatib_stage(service)
        self.assertEqual(items[0]['media_hash'], media.pk)
        self.assertEqual(items[0]['subtitle'], 'PDF')

    def test_reference_inventory_keeps_entry_link_after_local_file_removal(self):
        service = TataIbadah.objects.create(name='Ibadah Minggu')
        media = MediaIdentity.objects.create(sha256='b' * 64, byte_count=120,
                                             family='pdf', display_filename='notes.pdf')
        entry = ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=media,
                                            media_filename='notes.pdf', title='Sermon')
        response = self.client.get(reverse('web-media-references'))
        self.assertEqual(response.status_code, 200)
        use = response.json()['uses'][media.sha256][0]
        self.assertEqual(use['title'], 'Sermon')
        self.assertIn(f'#ti-e{entry.pk}', use['url'])
