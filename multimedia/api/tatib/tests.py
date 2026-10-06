from django.test import TestCase

from multimedia.tatib import models


class LegacyTatibApiCompatibilityTests(TestCase):
    def setUp(self):
        self.service = models.TataIbadah.objects.create(name='Ibadah Minggu III')
        self.first = models.TataIbadahItem.objects.create(
            tatib=self.service, item_type=models.TataIbadahItemType.TEXT,
            title='Pembukaan', text='KJ 120', order_number=1)
        self.second = models.TataIbadahItem.objects.create(
            tatib=self.service, item_type=models.TataIbadahItemType.END_OF_SECTION,
            title='', text='Catatan operator', order_number=2)

    def test_old_item_list_keeps_its_route_and_payload_fields(self):
        response = self.client.get('/api/tatib/items', {'tatib': self.service.pk})
        self.assertEqual(response.status_code, 200)
        rows = response.json()
        self.assertEqual(len(rows), 2)
        self.assertEqual(set(rows[0]), {'id', 'tatib', 'item_type', 'title', 'text', 'order_number'})
        self.assertEqual([row['order_number'] for row in rows], [1, 2])

    def test_old_reorder_route_and_response_shape_stay_available(self):
        response = self.client.post('/api/tatib/items/reorder', {
            'items': [
                {'item': self.second.pk, 'order_number': 1},
                {'item': self.first.pk, 'order_number': 2},
            ],
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {'items'})
        self.assertEqual(
            list(self.service.tataibadahitem_set.order_by('order_number')
                 .values_list('pk', flat=True)), [self.second.pk, self.first.pk])
