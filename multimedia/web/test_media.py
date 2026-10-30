import hashlib
import json
import os
from datetime import timedelta
from unittest.mock import patch, Mock

from django.utils import timezone

from django.test import Client, TestCase, override_settings
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
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_service_media_dialog_lists_entries_in_service_order(self):
        service = TataIbadah.objects.create(name='Ibadah Minggu', date=timezone.localdate())
        media = MediaIdentity.objects.create(sha256='e' * 64, byte_count=120,
                                             family='pdf', display_filename='library.pdf')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=media,
                                    media_filename='second.pdf', title='Second')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=media,
                                    media_filename='first.pdf', title='First')
        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertIn('id="serviceMediaDialog"', html)
        self.assertLess(html.index('>First</strong>'), html.index('>Second</strong>'))
        self.assertIn('id="serviceMediaButton"', html)

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

    def test_reference_order_filename_and_protection(self):
        from zoneinfo import ZoneInfo
        today = timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()
        media = MediaIdentity.objects.create(sha256='c' * 64, byte_count=12,
                                             family='pdf', display_filename='library.pdf')
        dated = TataIbadah.objects.create(name='Ibadah Minggu', date=today)
        undated = TataIbadah.objects.create(name='Template')
        ServiceEntry.objects.create(tatib=dated, kind=4, order_number=2, media=media,
                                    media_filename='second.pdf')
        ServiceEntry.objects.create(tatib=dated, kind=4, order_number=1, media=media,
                                    media_filename='first.pdf')
        ServiceEntry.objects.create(tatib=undated, kind=4, order_number=1, media=media,
                                    media_filename='template.pdf')
        payload = self.client.get(reverse('web-media-references')).json()
        self.assertEqual([use['filename'] for use in payload['uses'][media.sha256]],
                         ['first.pdf', 'second.pdf', 'template.pdf'])
        self.assertEqual(payload['protected'], [media.sha256])


class ImageDisplayContractTests(TestCase):
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_powerpoint_entry_has_slide_preview_and_projector_screen(self):
        from multimedia.web.reading.views import _tatib_stage, _projector_data
        service = TataIbadah.objects.create(name='Slides service')
        media = MediaIdentity.objects.create(sha256='f' * 64, byte_count=120,
                                             family='slides', display_filename='deck.pptx')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=media,
                                    media_filename='service.pptx', title='Teaching slides')
        items, _ = _tatib_stage(service)
        self.assertEqual(items[0]['preview'], {'kind': 'slides', 'title': 'Teaching slides',
                                               'sha256': media.sha256})
        screens = _projector_data(service)['screens']
        self.assertEqual(len(screens), 2)                    # the slide, then the entry's rest
        self.assertEqual(screens[0]['slides_sha256'], media.sha256)
        self.assertFalse(screens[0]['blank'])
        self.assertTrue(screens[-1]['blank'])
        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        self.assertContains(response, f'data-preview-slides="{media.sha256}"')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_image_and_pdf_entries_keep_distinct_preview_payloads(self):
        from multimedia.web.reading.views import _tatib_stage
        service = TataIbadah.objects.create(name='Image service')
        image = MediaIdentity.objects.create(sha256='1' * 64, byte_count=120,
                                             family='image', display_filename='picture.png')
        pdf = MediaIdentity.objects.create(sha256='2' * 64, byte_count=120,
                                           family='pdf', display_filename='notes.pdf')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=image,
                                    media_filename='picture.png', title='Opening image')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=pdf,
                                    media_filename='notes.pdf')

        items, _toc = _tatib_stage(service)
        self.assertEqual(items[0]['preview']['kind'], 'image')
        self.assertEqual(items[0]['preview']['sha256'], image.sha256)
        self.assertEqual(items[0]['preview']['title'], 'Opening image')
        self.assertEqual(items[1]['preview'], {'kind': 'pdf', 'title': 'notes.pdf',
                                               'sha256': pdf.sha256})

        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        self.assertContains(response, f'data-preview-image="{image.sha256}"')
        self.assertContains(response, f'data-preview-pdf="{pdf.sha256}"')

    def test_image_and_pdf_each_have_a_screen_and_a_rest(self):
        from multimedia.web.reading.views import _projector_data
        service = TataIbadah.objects.create(name='Image service')
        image = MediaIdentity.objects.create(sha256='3' * 64, byte_count=120,
                                             family='image', display_filename='picture.png')
        pdf = MediaIdentity.objects.create(sha256='4' * 64, byte_count=120,
                                           family='pdf', display_filename='notes.pdf')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=image,
                                    media_filename='picture.png')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=pdf,
                                    media_filename='notes.pdf')

        data = _projector_data(service)
        screens, entries = data['screens'], data['entries']
        image_entry, pdf_entry = entries[-2:]
        self.assertEqual([image_entry['type'], pdf_entry['type']], ['media', 'media'])
        self.assertEqual(image_entry['end'], image_entry['start'] + 1)
        self.assertEqual(screens[image_entry['start']]['image_sha256'], image.sha256)
        self.assertFalse(screens[image_entry['start']]['blank'])
        self.assertTrue(screens[image_entry['end']]['blank'])
        self.assertEqual(screens[pdf_entry['start']]['pdf_sha256'], pdf.sha256)
        self.assertTrue(screens[pdf_entry['end']]['blank'])


class AudioDisplayContractTests(TestCase):
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_audio_preview_uses_immutable_identity_and_saved_filename(self):
        from multimedia.web.reading.views import _tatib_stage
        service = TataIbadah.objects.create(name='Audio service')
        audio = MediaIdentity.objects.create(sha256='5' * 64, byte_count=120,
                                             family='audio', display_filename='library.mp3')
        pdf = MediaIdentity.objects.create(sha256='6' * 64, byte_count=120,
                                           family='pdf', display_filename='notes.pdf')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=audio,
                                    media_filename='service.mp3', title='Offering music')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=audio,
                                    media_filename='untitled.mp3')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=3, media=pdf,
                                    media_filename='notes.pdf')

        items, _toc = _tatib_stage(service)
        self.assertEqual(items[0]['preview'], {'kind': 'audio', 'title': 'Offering music',
                                                'filename': 'service.mp3', 'sha256': audio.sha256})
        self.assertEqual(items[1]['preview'], {'kind': 'audio', 'title': '',
                                                'filename': 'untitled.mp3', 'sha256': audio.sha256})
        self.assertEqual(items[2]['preview']['kind'], 'pdf')
        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        self.assertContains(response, f'data-preview-audio="{audio.sha256}"')

    def test_audio_has_a_screen_and_a_rest_in_order(self):
        from multimedia.web.reading.views import _projector_data
        service = TataIbadah.objects.create(name='Audio service')
        audio = MediaIdentity.objects.create(sha256='7' * 64, byte_count=120,
                                             family='audio', display_filename='service.mp3')
        pdf = MediaIdentity.objects.create(sha256='8' * 64, byte_count=120,
                                           family='pdf', display_filename='notes.pdf')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=audio,
                                    media_filename='service.mp3')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=pdf,
                                    media_filename='notes.pdf')

        data = _projector_data(service)
        screens, entries = data['screens'], data['entries']
        audio_entry, pdf_entry = entries[-2:]
        self.assertEqual(audio_entry['end'], audio_entry['start'] + 1)
        self.assertEqual(screens[audio_entry['start']]['audio_sha256'], audio.sha256)
        self.assertFalse(screens[audio_entry['start']]['blank'])
        self.assertTrue(screens[audio_entry['end']]['blank'])
        self.assertEqual(screens[pdf_entry['start']]['pdf_sha256'], pdf.sha256)


class VideoDisplayContractTests(TestCase):
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_video_preview_uses_immutable_identity_and_saved_filename(self):
        from multimedia.web.reading.views import _tatib_stage
        service = TataIbadah.objects.create(name='Video service',
                                            date=timezone.localdate())
        video = MediaIdentity.objects.create(sha256='9' * 64, byte_count=240,
                                             family='video', display_filename='library.webm')
        audio = MediaIdentity.objects.create(sha256='a' * 64, byte_count=120,
                                             family='audio', display_filename='sound.wav')
        pdf = MediaIdentity.objects.create(sha256='b' * 64, byte_count=120,
                                           family='pdf', display_filename='notes.pdf')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=video,
                                    media_filename='service-recording.webm', title='Welcome video')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=audio,
                                    media_filename='sound.wav', title='Music')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=3, media=pdf,
                                    media_filename='notes.pdf')

        items, _toc = _tatib_stage(service)

        self.assertEqual(items[0]['preview'], {'kind': 'video', 'title': 'Welcome video',
                                                'filename': 'service-recording.webm',
                                                'sha256': video.sha256})
        self.assertEqual(items[1]['preview']['kind'], 'audio')
        self.assertEqual(items[2]['preview']['kind'], 'pdf')
        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        self.assertContains(response, f'data-preview-video="{video.sha256}"')

    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_video_has_a_screen_and_a_rest_in_service_order(self):
        from multimedia.web.reading.views import _projector_data
        service = TataIbadah.objects.create(name='Video service',
                                            date=timezone.localdate())
        image = MediaIdentity.objects.create(sha256='c' * 64, byte_count=120,
                                             family='image', display_filename='picture.png')
        video = MediaIdentity.objects.create(sha256='d' * 64, byte_count=240,
                                             family='video', display_filename='recording.webm')
        audio = MediaIdentity.objects.create(sha256='e' * 64, byte_count=120,
                                             family='audio', display_filename='sound.wav')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=image,
                                    media_filename='picture.png')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=video,
                                    media_filename='recording.webm')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=3, media=audio,
                                    media_filename='sound.wav')

        data = _projector_data(service)
        screens, entries = data['screens'], data['entries']
        image_entry, video_entry, audio_entry = entries[-3:]

        self.assertLess(image_entry['start'], video_entry['start'])
        self.assertLess(video_entry['start'], audio_entry['start'])
        self.assertEqual(video_entry['end'], video_entry['start'] + 1)
        self.assertEqual(screens[video_entry['start']]['video_sha256'], video.sha256)
        self.assertFalse(screens[video_entry['start']]['blank'])
        self.assertTrue(screens[video_entry['end']]['blank'])
        self.assertEqual(screens[image_entry['start']]['image_sha256'], image.sha256)
        self.assertEqual(screens[audio_entry['start']]['audio_sha256'], audio.sha256)
        response = self.client.get(f'/projector?service={service.pk}')
        self.assertContains(response, f'data-media-video="{video.sha256}"')
        self.assertContains(response, 'Audio/Video Play/Pause')


class MediaEntryRestTests(TestCase):
    """Spec 164: a media entry ends on the built-in rest every other kind ends on."""

    def _media(self, sha_char, family='image', name='file.png'):
        return MediaIdentity.objects.create(sha256=sha_char * 64, byte_count=120, family=family,
                                            display_filename=name)

    def test_each_family_ends_on_one_rest(self):
        from multimedia.web.reading.views import _projector_data
        families = (('image', 'image_sha256'), ('audio', 'audio_sha256'), ('video', 'video_sha256'),
                    ('pdf', 'pdf_sha256'), ('slides', 'slides_sha256'))
        for index, (family, key) in enumerate(families):
            with self.subTest(family=family):
                media = self._media(str(index), family, f'file.{family}')
                service = TataIbadah.objects.create(name=f'{family} service')
                ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=media,
                                            media_filename=media.display_filename)
                screens = _projector_data(service)['screens']
                self.assertEqual(len(screens), 2)              # the media, then its rest
                self.assertFalse(screens[0]['blank'])
                self.assertEqual(screens[0][key], media.sha256)
                self.assertTrue(screens[1]['blank'])

    def test_a_media_entry_without_a_file_keeps_its_one_rest(self):
        from multimedia.web.reading.views import _projector_data
        service = TataIbadah.objects.create(name='Unattached media service')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=None,
                                    media_filename='gone.png')
        screens = _projector_data(service)['screens']
        self.assertEqual(len(screens), 1)                      # its own screen already rests
        self.assertTrue(screens[0]['blank'])

    def test_the_rest_carries_only_the_built_in_blank(self):
        from multimedia.web.reading.views import _projector_data
        media = self._media('a', 'image', 'slide.png')
        service = TataIbadah.objects.create(name='Rest shape service')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=1, media=media,
                                    media_filename='slide.png')
        rest = _projector_data(service)['screens'][1]
        self.assertEqual(set(rest), {'blank', 'header', 'lines', 'entry_index'})
        self.assertEqual((rest['header'], rest['lines']), ('', []))

    def test_the_entry_range_extends_over_the_rest(self):
        from multimedia.web.reading.views import _projector_data
        service = TataIbadah.objects.create(name='Range service')
        ServiceEntry.objects.create(tatib=service, kind=0, order_number=1, title='Salam',
                                    text='Kasih karunia Tuhan beserta kita')
        media = self._media('b', 'image', 'opening.png')
        ServiceEntry.objects.create(tatib=service, kind=4, order_number=2, media=media,
                                    media_filename='opening.png', title='Opening image')
        text_entry, media_entry = _projector_data(service)['entries']
        self.assertEqual(media_entry['start'], text_entry['end'] + 1)   # the start does not move
        self.assertEqual(media_entry['end'], media_entry['start'] + 1)  # the rest is inside it
        self.assertEqual((media_entry['type'], media_entry['label']), ('media', 'Opening image'))
        self.assertEqual(media_entry['baits'], [])

    def test_four_images_in_a_row_build_ten_screens(self):
        """The service-149 shape: a text row then four pictures, each picture followed by a rest."""
        from multimedia.web.reading.views import _projector_data
        service = TataIbadah.objects.create(name='Images service')
        ServiceEntry.objects.create(tatib=service, kind=0, order_number=1, title='Salam',
                                    text='Kasih karunia Tuhan beserta kita')
        for order, sha in enumerate(('c', 'd', 'e', 'f'), start=2):
            media = self._media(sha, 'image', f'{sha}.png')
            ServiceEntry.objects.create(tatib=service, kind=4, order_number=order, media=media,
                                        media_filename=f'{sha}.png')
        data = _projector_data(service)
        screens, entries = data['screens'], data['entries']
        self.assertEqual(len(screens), 10)
        self.assertEqual([(entry['start'], entry['end']) for entry in entries],
                         [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)])
        self.assertEqual([screen['blank'] for screen in screens],
                         [False, True, False, True, False, True, False, True, False, True])


class MediaLibraryCsrfTests(TestCase):
    def setUp(self):
        self.media = MediaIdentity.objects.create(sha256='f' * 64, byte_count=20,
                                                  family='pdf', display_filename='share.pdf')

    @patch('multimedia.web.reading.views.media_handoff.begin_share',
           return_value=('https://r2.example/upload', None, 'completion-token'))
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_fresh_library_visit_supplies_csrf_token_for_share(self, begin_share):
        client = Client(enforce_csrf_checks=True)
        page = client.get(reverse('web-media-library'))
        self.assertIn('csrftoken', page.cookies)

        response = client.post(reverse('web-media-share', args=[self.media.pk, 'begin']),
                               HTTP_X_CSRFTOKEN=page.cookies['csrftoken'].value)

        self.assertEqual(response.status_code, 200, response.content[:400])
        self.assertEqual(response.json()['sha256'], self.media.pk)
        begin_share.assert_called_once()

    def test_share_still_rejects_requests_without_valid_csrf(self):
        from multimedia.tatib.models import MediaShare

        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse('web-media-share', args=[self.media.pk, 'begin']))

        self.assertEqual(response.status_code, 403)
        self.assertFalse(MediaShare.objects.exists())


class MediaHandoffTests(TestCase):
    def setUp(self):
        self.media = MediaIdentity.objects.create(sha256='d' * 64, byte_count=20,
                                                  family='pdf', display_filename='order.pdf')

    @patch('multimedia.media_handoff.client')
    @patch('multimedia.media_handoff.config')
    def test_share_is_offline_until_verified_and_expires_after_seven_days(self, config, client):
        config.return_value = {'prefix': 'temporary-media', 'GKPS_R2_BUCKET': 'bucket'}
        client.return_value.generate_presigned_url.return_value = 'https://r2.example/upload'
        client.return_value.head_object.return_value = {'ContentLength': 20}
        begin = self.client.post(reverse('web-media-share', args=[self.media.pk, 'begin']))
        self.assertEqual(begin.status_code, 200)
        self.assertEqual(self.client.get(reverse('web-media-cloud-status')).json()['online'], {})
        completed = self.client.post(reverse('web-media-complete', args=[self.media.pk]),
                                     HTTP_AUTHORIZATION='Bearer ' + begin.json()['completion_token'])
        self.assertEqual(completed.status_code, 200)
        self.assertIn(self.media.pk, self.client.get(reverse('web-media-cloud-status')).json()['online'])
        from multimedia.tatib.models import MediaShare
        share = MediaShare.objects.get(media=self.media)
        self.assertEqual(share.expires_at - share.uploaded_at, timedelta(days=7))

    def test_missing_configuration_fails_closed(self):
        with patch.dict('os.environ', {}, clear=True):
            response = self.client.post(reverse('web-media-share', args=[self.media.pk, 'begin']))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(self.client.get(reverse('web-media-cloud-status')).json()['online'], {})

    @patch('multimedia.media_handoff.client')
    @patch('multimedia.media_handoff.config')
    def test_missing_r2_object_revokes_download(self, config, client):
        from botocore.exceptions import ClientError
        from multimedia.tatib.models import MediaShare
        config.return_value = {'prefix': 'temporary-media', 'GKPS_R2_BUCKET': 'bucket'}
        MediaShare.objects.create(media=self.media, object_key='temporary-media/' + self.media.pk,
                                  status='available', uploaded_at=timezone.now(),
                                  expires_at=timezone.now() + timedelta(days=7))
        client.return_value.head_object.side_effect = ClientError(
            {'Error': {'Code': '404', 'Message': 'missing'}}, 'HeadObject')
        response = self.client.get(reverse('web-media-download', args=[self.media.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(MediaShare.objects.filter(media=self.media).exists())

    @patch('multimedia.media_handoff.status_for')
    def test_manifest_only_includes_today_and_future_online_references(self, status_for):
        from zoneinfo import ZoneInfo
        today = timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()
        future = TataIbadah.objects.create(name='Future', date=today + timedelta(days=3))
        past = TataIbadah.objects.create(name='Past', date=today - timedelta(days=1))
        ServiceEntry.objects.create(tatib=future, kind=4, order_number=1,
                                    media=self.media, media_filename='order.pdf')
        ServiceEntry.objects.create(tatib=past, kind=4, order_number=1,
                                    media=self.media, media_filename='order.pdf')
        status_for.return_value = {self.media.pk: (timezone.now() + timedelta(days=7)).isoformat()}
        files = self.client.get(reverse('web-media-manifest')).json()['files']
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['eligible_until'], (today + timedelta(days=3)).isoformat())

    @patch('multimedia.media_handoff.client')
    @patch('multimedia.media_handoff.config')
    def test_cleanup_removes_abandoned_pending_upload(self, config, client):
        from multimedia import media_handoff
        from multimedia.tatib.models import MediaShare
        config.return_value = {'prefix': 'temporary-media', 'GKPS_R2_BUCKET': 'bucket'}
        share = MediaShare.objects.create(media=self.media, object_key='temporary-media/' + self.media.pk)
        MediaShare.objects.filter(pk=share.pk).update(created_at=timezone.now() - timedelta(days=2))
        self.assertEqual(media_handoff.cleanup_expired(), 1)
        client.return_value.delete_object.assert_called_once()
        self.assertFalse(MediaShare.objects.exists())

    @patch('multimedia.media_handoff.cleanup_expired', return_value=2)
    def test_cleanup_endpoint_requires_cron_secret(self, cleanup):
        url = reverse('web-media-cleanup')
        with patch.dict(os.environ, {'CRON_SECRET': 'test-cron-secret'}):
            self.assertEqual(self.client.get(url).status_code, 403)
            response = self.client.get(url, HTTP_AUTHORIZATION='Bearer test-cron-secret')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['deleted'], 2)
        cleanup.assert_called_once()
