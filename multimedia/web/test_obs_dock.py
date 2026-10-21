"""Spec 119 — the OBS surfaces: the dock, the projector, and the overlay.

Routes and first paint only: the state behaviour lives in the browser (E2E);
these tests pin the server side — which pages exist, what they carry, and that
the old per-service projector routes are gone.
"""
from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone

from pathlib import Path
import re

from multimedia.tatib.models import TataIbadah
from multimedia.web.reading import search as search_lib


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

    def test_the_dock_groups_the_picker_by_month_in_indonesian(self):
        response = self.client.get('/obs/dock')
        # The product's own month names, not Django's English filter. Built from the
        # fixture's date and the name tables — a literal date here rots at midnight.
        date = self.service.date
        self.assertContains(
            response, f'{search_lib.MONTHS_LONG[date.month - 1]} {date.year}')
        self.assertContains(
            response, f'{date.day} {search_lib.MONTHS_SHORT[date.month - 1]} {date.year}')

    def test_the_dock_lists_only_dated_services(self):
        TataIbadah.objects.create(name='Kerangka Kosong', date=None)
        response = self.client.get('/obs/dock')
        self.assertNotContains(response, 'Kerangka Kosong')

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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class BundledTypefacesTest(TestCase):
    """Spec 119: both display faces ship in the repository; no machine install."""

    def test_the_typefaces_ship_with_their_licences(self):
        root = Path(settings.BASE_DIR) / 'static' / 'assets' / 'fonts'
        for name in ('CMGSans-Bold.ttf', 'SourceSans3.ttf',
                     'CMG-Sans-License-OFL.txt', 'SourceSans3-License-OFL.txt'):
            self.assertTrue((root / name).is_file(), name)

    def test_the_display_surfaces_load_the_bundled_faces(self):
        for path in ('/projector', '/obs/source/overlay'):
            response = self.client.get(path)
            self.assertContains(response, 'styles/design/fonts.css', msg_prefix=path)

    def test_the_projector_balances_a_wrapped_line(self):
        css = (Path(settings.BASE_DIR) / 'static' / 'styles' / 'design'
               / 'projector.css').read_text(encoding='utf-8')
        self.assertIn('text-wrap: balance', css)


class SharedScrollbarTest(TestCase):
    """Spec 087/119: the dock takes the app's scrollbar, not the platform's."""

    def test_the_standard_properties_stay_out_of_blink(self):
        css = (Path(settings.BASE_DIR) / 'static' / 'styles' / 'design'
               / 'obs-dock.css').read_text(encoding='utf-8')
        # In Blink `scrollbar-width` beats ::-webkit-scrollbar and paints the
        # platform's 10px bar with steppers, so it may appear only inside the
        # guard for engines that have no ::-webkit-scrollbar (spec 087).
        without_guard = re.sub(
            r'@supports not selector\(::-webkit-scrollbar\)\s*\{[^}]*\}\s*\}', '', css)
        self.assertNotIn('scrollbar-width: thin', without_guard)
        self.assertIn('.dock__body::-webkit-scrollbar { width: 5px', css)
