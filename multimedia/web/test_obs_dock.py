"""Spec 119 — the OBS surfaces: the dock, the projector, and the overlay.

Routes and first paint only: the state behaviour lives in the browser (E2E);
these tests pin the server side — which pages exist, what they carry, and that
the old per-service projector routes are gone.
"""
from django.test import TestCase, override_settings
from django.utils import timezone

from multimedia.tatib.models import TataIbadah


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ObsSurfacesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = TataIbadah.objects.create(
            name='Ibadah Minggu', date=timezone.localdate())

    def test_the_projector_renders_without_a_service(self):
        response = self.client.get('/projector')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading/projector.html')

    def test_the_projector_carries_the_service_parameter_as_an_adoption(self):
        response = self.client.get('/projector', {'service': self.service.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'data-adopt="{self.service.pk}"')
        self.assertContains(response, f'data-service="{self.service.pk}"')

    def test_the_dock_lists_the_services(self):
        response = self.client.get('/obs/dock')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading/obs_dock.html')
        self.assertContains(response, 'Ibadah Minggu')

    def test_the_overlay_is_a_control_free_shell(self):
        response = self.client.get('/obs/source/overlay')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reading/obs_overlay.html')
        self.assertNotContains(response, '<button')
        self.assertNotContains(response, '<input')
        self.assertNotContains(response, '<a ')

    def test_the_old_projector_routes_are_gone(self):
        for path in (f'/obs/service/{self.service.pk}/',
                     f'/obs/service/{self.service.pk}/lookup/',
                     f'/obs/service/{self.service.pk}/detour/'):
            self.assertEqual(self.client.get(path).status_code, 404, path)
