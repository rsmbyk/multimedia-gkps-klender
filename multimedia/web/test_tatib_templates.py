"""Tata Ibadah types, slots and generation (spec 167).

The rules this module guards are the ones a single page cannot prove: the type and the date
never disagree, a slot exists only on a template, a generated service is the template's order
with each slot replaced, and generating leaves the template byte-identical.
"""

import json
from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib.models import (MediaIdentity, ServiceEntry, ServiceEntryKind,
                                     SlotKind, TataIbadah, TataIbadahKind)


def make_service(name='Ibadah Minggu', day=None):
    return TataIbadah.objects.create(name=name, date=day or date(2026, 11, 1))


def make_template(name='Ibadah Minggu'):
    return TataIbadah.objects.create(name=name)


def add_text(service, title='Votum', text='Pertolongan kita adalah dalam nama Tuhan.', order=1):
    return ServiceEntry.objects.create(tatib=service, kind=ServiceEntryKind.TEXT,
                                       order_number=order, title=title, text=text)


def add_song(service, song, verses, order, title=''):
    return ServiceEntry.objects.create(tatib=service, kind=ServiceEntryKind.SONG,
                                       order_number=order, song=song, verses=verses,
                                       title=title)


class KindTests(TestCase):
    """FR-001, FR-002, SC-001, SC-005, A10."""

    def test_a_create_with_no_date_is_a_template(self):
        service = TataIbadah.objects.create(name='Skeleton')
        self.assertEqual(service.kind, TataIbadahKind.TEMPLATE)
        self.assertIsNone(service.date)

    def test_a_create_with_a_date_is_a_service(self):
        service = make_service()
        self.assertEqual(service.kind, TataIbadahKind.SERVICE)

    def test_kind_and_date_always_agree(self):
        from django.core.exceptions import ValidationError
        template_with_date = TataIbadah(name='T', date=date(2026, 11, 1),
                                        kind=TataIbadahKind.TEMPLATE)
        with self.assertRaises(ValidationError):
            template_with_date.full_clean()
        service_without_date = TataIbadah(name='S', kind=TataIbadahKind.SERVICE)
        with self.assertRaises(ValidationError):
            service_without_date.full_clean()

    def test_the_type_is_set_once_and_never_changes(self):
        from django.core.exceptions import ValidationError
        service = make_service()
        service.kind = TataIbadahKind.TEMPLATE
        with self.assertRaises(ValidationError):
            service.save()
        service.refresh_from_db()
        self.assertEqual(service.kind, TataIbadahKind.SERVICE)

    def test_the_database_refuses_a_disagreeing_row(self):
        from django.db import IntegrityError, transaction
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                TataIbadah.objects.filter(pk=make_service().pk).update(kind=TataIbadahKind.TEMPLATE)

    def test_the_api_never_writes_the_type(self):
        response = self.client.post('/api/tatib/tatibs', data=json.dumps({'name': 'API template'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TataIbadah.objects.get(pk=response.json()['id']).kind,
                         TataIbadahKind.TEMPLATE)
        service = make_service()
        response = self.client.patch(f'/api/tatib/tatibs/{service.pk}',
                                     data=json.dumps({'kind': TataIbadahKind.TEMPLATE}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        service.refresh_from_db()
        self.assertEqual(service.kind, TataIbadahKind.SERVICE)


STATIC = override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')


@STATIC
class PanelTests(TestCase):
    """FR-005, FR-006, SC-005."""

    def test_panel_lists_by_type(self):
        make_service(name='Dated', day=date(2026, 11, 1))
        make_template(name='Skeleton')
        response = self.client.get(reverse('web-tatib') + '?mode=template')
        groups = response.context['tatib_groups']
        self.assertEqual([row['name'] for group in groups for row in group['services']],
                         ['Skeleton'])
        response = self.client.get(reverse('web-tatib'))
        names = [row['name'] for group in response.context['tatib_groups']
                 for row in group['services']]
        self.assertIn('Dated', names)
        self.assertNotIn('Skeleton', names)

    def test_two_templates_with_one_name_both_list(self):
        make_template(name='Sama')
        make_template(name='Sama')
        response = self.client.get(reverse('web-tatib') + '?mode=template')
        rows = [row for group in response.context['tatib_groups'] for row in group['services']]
        self.assertEqual(len(rows), 2)


@STATIC
class ProjectionTests(TestCase):
    """FR-012, US5/AC3, US5/AC4, SC-002."""

    def test_a_template_is_never_projected(self):
        template = make_template()
        add_text(template)
        response = self.client.get(reverse('web-projector') + f'?service={template.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['service'])
        self.assertEqual(response.context['screens'], [])

    def test_the_dock_lists_no_template(self):
        make_service(name='Dated', day=date(2026, 11, 1))
        make_template(name='Skeleton')
        response = self.client.get(reverse('web-obs-dock'))
        names = [row.name for group in response.context['groups'] for row in group['services']]
        self.assertIn('Dated', names)
        self.assertNotIn('Skeleton', names)

    def test_a_service_page_keeps_its_controls(self):
        service = make_service()
        add_text(service)
        response = self.client.get(reverse('web-tatib-service', args=[service.pk]))
        html = response.content.decode()
        self.assertIn('data-project-window', html)
        self.assertIn('data-project-open', html)
        self.assertNotIn('data-generate-open', html)

    def test_a_template_page_has_no_project_controls(self):
        template = make_template()
        add_text(template)
        response = self.client.get(reverse('web-tatib-service', args=[template.pk]))
        html = response.content.decode()
        self.assertNotIn('data-project-window', html)
        self.assertNotIn('data-project-open', html)
        self.assertIn('data-generate-open', html)


class SlotModelTests(TestCase):
    """FR-008, FR-009, FR-010, US2/AC5, US2/AC7."""

    def slot(self, template, kind=ServiceEntryKind.FILL_IN, fill_kind=SlotKind.SONG,
             title='Nyanyian Pembuka', order=1):
        return ServiceEntry.objects.create(tatib=template, kind=kind, fill_kind=fill_kind,
                                           title=title, order_number=order)

    def test_a_fill_in_carries_a_kind_and_no_content(self):
        from django.core.exceptions import ValidationError
        template = make_template()
        fill_in = self.slot(template)
        fill_in.full_clean()
        fill_in.text = 'something of its own'
        with self.assertRaises(ValidationError):
            fill_in.full_clean()

    def test_a_service_refuses_slots(self):
        from django.core.exceptions import ValidationError
        service = make_service()
        entry = ServiceEntry(tatib=service, kind=ServiceEntryKind.FILL_IN,
                             fill_kind=SlotKind.SONG, order_number=1)
        with self.assertRaises(ValidationError):
            entry.full_clean()
        entry.kind = ServiceEntryKind.CHOICE
        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_an_option_must_match_its_choice_kind(self):
        from django.core.exceptions import ValidationError
        template = make_template()
        choice = self.slot(template, kind=ServiceEntryKind.CHOICE, fill_kind=SlotKind.SONG)
        wrong = ServiceEntry(tatib=template, kind=ServiceEntryKind.TEXT, parent=choice,
                             order_number=2, text='A prayer')
        with self.assertRaises(ValidationError):
            wrong.full_clean()

    def test_options_live_under_their_choice(self):
        template = make_template()
        choice = self.slot(template, kind=ServiceEntryKind.CHOICE, fill_kind=SlotKind.SONG,
                           order=2)
        first = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.SONG,
                                            parent=choice, order_number=3, verses=[1])
        second = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.SONG,
                                             parent=choice, order_number=4, verses=[2])
        self.assertEqual(list(choice.options.order_by('order_number')), [first, second])

    def test_a_choice_with_no_options_is_valid(self):
        template = make_template()
        choice = self.slot(template, kind=ServiceEntryKind.CHOICE, fill_kind=SlotKind.SONG)
        choice.full_clean()
        self.assertEqual(choice.options.count(), 0)


@STATIC
class SlotEndpointTests(TestCase):
    """The slot forms, the validate endpoint, generation and copying (FR-003…FR-021)."""

    @classmethod
    def setUpTestData(cls):
        cls.book = songs.Book.objects.create(name='Nyanyikanlah Kidung Baru', short_name='NKB',
                                             is_hymn_book=True)
        cls.song = songs.Song.objects.create(book=cls.book, number=12,
                                             title='Di Waktu Pagi', key='c')
        songs.Verse.objects.create(song=cls.song, number=1, lyric='Line one')
        songs.Verse.objects.create(song=cls.song, number=2, lyric='Line two')
        cls.other = songs.Song.objects.create(book=cls.book, number=13, title='Di Waktu Malam')

    def test_new_form_offers_both_types(self):
        html = self.client.get(reverse('web-editor-new', args=['tatib'])).content.decode()
        self.assertIn('data-tatib-kind="0"', html)
        self.assertIn('data-tatib-kind="1"', html)
        self.assertIn('Normal', html)
        self.assertIn('Template', html)
        self.assertNotIn('data-date-picker-clear', html)

    def test_edit_refuses_to_clear_a_normal_date(self):
        service = make_service(day=date(2026, 11, 1))
        response = self.client.post(reverse('web-editor-save', args=['tatib', service.pk]),
                                    {'name': service.name, 'date': ''})
        self.assertEqual(response.status_code, 400)
        service.refresh_from_db()
        self.assertEqual(service.date, date(2026, 11, 1))

    def test_a_fill_in_is_a_title_and_a_kind(self):
        template = make_template()
        response = self.client.post(
            reverse('web-entry-save-new') + f'?tatib={template.pk}',
            {'kind': str(int(ServiceEntryKind.FILL_IN)), 'title': 'Nyanyian Pembuka',
             'fill_kind': str(int(SlotKind.SONG))})
        self.assertEqual(response.status_code, 200)
        slot = ServiceEntry.objects.get(pk=response.json()['id'])
        self.assertEqual(slot.kind, ServiceEntryKind.FILL_IN)
        self.assertEqual(slot.fill_kind, SlotKind.SONG)
        self.assertEqual(slot.title, 'Nyanyian Pembuka')

    def test_a_service_refuses_slots_from_every_endpoint(self):
        service = make_service()
        response = self.client.post(
            reverse('web-entry-save-new') + f'?tatib={service.pk}',
            {'kind': str(int(ServiceEntryKind.FILL_IN)), 'title': 'Nope',
             'fill_kind': str(int(SlotKind.SONG))})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ServiceEntry.objects.count(), 0)

    def test_options_live_under_their_choice(self):
        template = make_template()
        choice = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.CHOICE,
                                             fill_kind=SlotKind.SONG, title='Nyanyian',
                                             order_number=1)
        response = self.client.post(
            reverse('web-entry-save-new') + f'?tatib={template.pk}&parent={choice.pk}',
            {'kind': str(int(ServiceEntryKind.SONG)), 'song': str(self.song.pk), 'verses': ['1']})
        self.assertEqual(response.status_code, 200)
        option = ServiceEntry.objects.get(pk=response.json()['id'])
        self.assertEqual(option.parent_id, choice.pk)
        self.assertEqual(option.kind, ServiceEntryKind.SONG)
        self.assertGreater(option.order_number, choice.order_number)
        wrong = self.client.post(
            reverse('web-entry-save-new') + f'?tatib={template.pk}&parent={choice.pk}',
            {'kind': str(int(ServiceEntryKind.TEXT)), 'title': 'Doa', 'text': 'Tuhan, '})
        self.assertEqual(wrong.status_code, 400)

    def test_validate_answers_the_row_and_writes_nothing(self):
        template = make_template()
        slot = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.FILL_IN,
                                           fill_kind=SlotKind.SONG, title='Nyanyian Pembuka',
                                           order_number=1)
        before = ServiceEntry.objects.count()
        response = self.client.post(reverse('web-entry-validate'), {
            'entry': str(slot.pk), 'kind': str(int(ServiceEntryKind.SONG)),
            'song': str(self.song.pk), 'verses': ['1', '2']})
        self.assertEqual(response.status_code, 200)
        value = response.json()['value']
        self.assertIn('NKB 12', value['line'])
        self.assertIn('Bait 1, 2', value['meta'])
        self.assertEqual(response.json()['data']['song'], str(self.song.pk))
        self.assertEqual(ServiceEntry.objects.count(), before)

    def _template_with_slots(self):
        template = make_template(name='Skeleton')
        add_text(template, order=1)
        fill_in = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.FILL_IN,
                                              fill_kind=SlotKind.SONG, title='Nyanyian Pembuka',
                                              order_number=2)
        choice = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.CHOICE,
                                             fill_kind=SlotKind.SONG, title='Nyanyian Penutup',
                                             order_number=3)
        first = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.SONG,
                                            parent=choice, order_number=4, song=self.song,
                                            verses=[1])
        second = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.SONG,
                                             parent=choice, order_number=5, song=self.other,
                                             verses=[1])
        add_text(template, title='Doa', text='Tuhan, sertailah kami.', order=6)
        return template, fill_in, choice, first, second

    def _generate(self, template, slots):
        return self.client.post(
            reverse('web-tatib-generate', args=[template.pk]),
            data=json.dumps({'name': 'Ibadah Minggu', 'date': '2026-11-01', 'slots': slots}),
            content_type='application/json')

    def test_generate_replaces_slots_in_order(self):
        template, fill_in, choice, first, _second = self._template_with_slots()
        response = self._generate(template, [
            {'entry': fill_in.pk, 'data': {'kind': str(int(ServiceEntryKind.SONG)),
                                           'song': str(self.song.pk), 'verses': ['1', '2']}},
            {'entry': choice.pk, 'option': first.pk}])
        self.assertEqual(response.status_code, 201)
        service = TataIbadah.objects.get(pk=response.json()['id'])
        self.assertEqual(service.kind, TataIbadahKind.SERVICE)
        rows = list(service.service_entries.order_by('order_number'))
        self.assertEqual([row.kind for row in rows],
                         [ServiceEntryKind.TEXT, ServiceEntryKind.SONG,
                          ServiceEntryKind.SONG, ServiceEntryKind.TEXT])
        self.assertEqual(rows[1].verses, [1, 2])          # the fill-in's resolution
        self.assertEqual(rows[2].song_id, first.song_id)  # the chosen option
        self.assertEqual([row.order_number for row in rows], [1, 2, 3, 4])
        self.assertFalse(service.service_entries.filter(parent__isnull=False).exists())

    def test_generate_leaves_the_template_untouched(self):
        template, fill_in, choice, first, _second = self._template_with_slots()
        snapshot = [(row.pk, row.kind, row.title, row.fill_kind, row.parent_id,
                     row.order_number, row.song_id, list(row.verses or []))
                    for row in template.service_entries.order_by('order_number')]
        self._generate(template, [
            {'entry': fill_in.pk, 'data': {'kind': str(int(ServiceEntryKind.SONG)),
                                           'song': str(self.song.pk), 'verses': ['1']}},
            {'entry': choice.pk, 'option': first.pk}])
        after = [(row.pk, row.kind, row.title, row.fill_kind, row.parent_id,
                  row.order_number, row.song_id, list(row.verses or []))
                 for row in template.service_entries.order_by('order_number')]
        self.assertEqual(snapshot, after)
        self.assertEqual(template.kind, TataIbadahKind.TEMPLATE)

    def test_an_unsettled_slot_creates_nothing(self):
        template, fill_in, choice, first, _second = self._template_with_slots()
        before = TataIbadah.objects.count()
        response = self._generate(template, [
            {'entry': fill_in.pk, 'data': {'kind': str(int(ServiceEntryKind.SONG)),
                                           'song': str(self.song.pk), 'verses': ['1']}}])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TataIbadah.objects.count(), before)

    def test_a_template_without_slots_copies_straight(self):
        template = make_template(name='Bare skeleton')
        add_text(template)
        response = self._generate(template, [])
        self.assertEqual(response.status_code, 201)
        service = TataIbadah.objects.get(pk=response.json()['id'])
        self.assertEqual(service.service_entries.count(), 1)

    def test_a_deleted_option_refuses_the_create(self):
        template, fill_in, choice, first, _second = self._template_with_slots()
        first.delete()
        response = self._generate(template, [
            {'entry': fill_in.pk, 'data': {'kind': str(int(ServiceEntryKind.SONG)),
                                           'song': str(self.song.pk), 'verses': ['1']}},
            {'entry': choice.pk, 'option': first.pk}])
        self.assertEqual(response.status_code, 400)

    def test_legacy_rows_are_copied_as_legacy_rows(self):
        from multimedia.tatib.models import TataIbadahItem, TataIbadahItemType
        template = make_template()
        TataIbadahItem.objects.create(tatib=template, item_type=TataIbadahItemType.TEXT,
                                      title='Old row', text='Old body', order_number=1)
        response = self._generate(template, [])
        service = TataIbadah.objects.get(pk=response.json()['id'])
        self.assertTrue(service.tataibadahitem_set.filter(title='Old row').exists())

    def test_a_media_slot_keeps_its_identity(self):
        media = MediaIdentity.objects.create(sha256='b' * 64, byte_count=2048, family='pdf',
                                             display_filename='liturgi.pdf')
        template = make_template()
        slot = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.FILL_IN,
                                           fill_kind=SlotKind.MEDIA, title='Liturgi',
                                           order_number=1)
        response = self._generate(template, [
            {'entry': slot.pk, 'data': {'kind': str(int(ServiceEntryKind.MEDIA)),
                                        'title': 'Liturgi', 'media': media.pk,
                                        'media_filename': 'liturgi.pdf'}}])
        self.assertEqual(response.status_code, 201)
        service = TataIbadah.objects.get(pk=response.json()['id'])
        self.assertEqual(service.service_entries.get().media_id, media.pk)

    def test_a_copy_converts_nothing(self):
        service = make_service()
        add_text(service, order=1)
        add_song(service, self.song, [1], order=2)
        response = self.client.post(reverse('web-tatib-copy', args=[service.pk]))
        self.assertEqual(response.status_code, 201)
        copy = TataIbadah.objects.get(pk=response.json()['id'])
        self.assertEqual(copy.kind, TataIbadahKind.TEMPLATE)
        self.assertIsNone(copy.date)
        self.assertEqual([row.kind for row in copy.service_entries.order_by('order_number')],
                         [ServiceEntryKind.TEXT, ServiceEntryKind.SONG])

    def test_a_template_copy_keeps_its_slots(self):
        template, fill_in, choice, first, second = self._template_with_slots()
        response = self.client.post(reverse('web-tatib-copy', args=[template.pk]))
        copy = TataIbadah.objects.get(pk=response.json()['id'])
        self.assertEqual(copy.kind, TataIbadahKind.TEMPLATE)
        self.assertEqual(copy.service_entries.filter(kind=ServiceEntryKind.FILL_IN).count(), 1)
        copied_choice = copy.service_entries.get(kind=ServiceEntryKind.CHOICE)
        self.assertEqual(copied_choice.options.count(), 2)
        self.assertEqual(copied_choice.options.first().parent_id, copied_choice.pk)

    def test_a_choice_moves_with_its_options(self):
        template = make_template()
        first = add_text(template, title='First', order=1)
        choice = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.CHOICE,
                                             fill_kind=SlotKind.SONG, title='Nyanyian',
                                             order_number=2)
        option = ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.SONG,
                                             parent=choice, order_number=3, song=self.song,
                                             verses=[1])
        last = add_text(template, title='Last', order=4)
        response = self.client.post(reverse('web-entry-reorder'),
                                    data=json.dumps({'tatib': template.pk,
                                                     'entries': [{'entry': last.pk},
                                                                 {'entry': choice.pk}]}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order = list(template.service_entries.order_by('order_number')
                     .values_list('pk', flat=True))
        self.assertEqual(order, [last.pk, choice.pk, option.pk, first.pk])


class MediaRuleTests(TestCase):
    """FR-023, FR-024: a template's file is a use and is never auto-downloaded."""

    def test_a_template_only_file_is_never_expired(self):
        media = MediaIdentity.objects.create(sha256='c' * 64, byte_count=10, family='pdf',
                                             display_filename='a.pdf')
        template = make_template()
        ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.MEDIA,
                                    media=media, media_filename='a.pdf', order_number=1)
        payload = self.client.get(reverse('web-media-references')).json()
        self.assertIn(media.pk, payload['uses'])
        self.assertEqual(payload['protected'], [])

    @patch('multimedia.media_handoff.status_for')
    def test_a_template_only_file_is_not_in_the_manifest(self, status_for):
        media = MediaIdentity.objects.create(sha256='d' * 64, byte_count=10, family='pdf',
                                             display_filename='b.pdf')
        template = make_template()
        ServiceEntry.objects.create(tatib=template, kind=ServiceEntryKind.MEDIA,
                                    media=media, media_filename='b.pdf', order_number=1)
        status_for.return_value = {media.pk: '2030-01-01T00:00:00+00:00'}
        payload = self.client.get(reverse('web-media-manifest')).json()
        self.assertEqual(payload['files'], [])
