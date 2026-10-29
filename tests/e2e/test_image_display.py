"""Image media in the operator Preview and congregation projector (spec 114)."""
import struct
import unittest
import zlib
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


def _png(width=12, height=6):
    def chunk(kind, content):
        return (struct.pack('!I', len(content)) + kind + content
                + struct.pack('!I', zlib.crc32(kind + content) & 0xffffffff))
    rows = b''.join(b'\0' + bytes((33, 93, 65, 255)) * width for _ in range(height))
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('!2I5B', width, height, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ImageDisplayE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Image service', date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=1, title='Opening', text='Welcome')
        self.image = tatib.MediaIdentity.objects.create(
            sha256='a' * 64, byte_count=120, family='image', display_filename='church.png')
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA,
            order_number=2, media=self.image, media_filename='church.png', title='Church image')
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=3, title='Closing', text='Amen')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _page(self, path, available=True, pending=False):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        payload = _png()

        def serve(route):
            headers = {'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                       'Content-Type': 'application/octet-stream'}
            route.fulfill(status=200 if available else 404, headers=headers,
                          body=payload if available else b'')

        self.held_routes = []

        def hold(route):
            # Answered by nothing until the case ends: the request stays in flight, so the
            # screen stays pending. Aborted afterwards, or Playwright cancels the handler
            # mid-close and prints a traceback that reads like a failure.
            self.held_routes.append(route)

        page.route('http://127.0.0.1:63174/v1/files/' + self.image.sha256,
                   hold if pending else serve)
        page.goto(self.live_server_url + path)
        return page

    def test_preview_fits_image_and_escape_closes(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('#previewModal .preview__image img')).to_be_visible()
        self.assertEqual(page.locator('#previewTitle').inner_text(), 'Church image')
        bounds = page.locator('#previewModal').bounding_box()
        self.assertLessEqual(bounds['width'], 1440 - 32)
        self.assertLessEqual(bounds['height'], 900 - 48)
        page.keyboard.press('Escape')
        expect(page.locator('#previewModal')).not_to_be_visible()
        page.close()

    def test_missing_preview_and_projector_icon(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]), available=False)
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.hover()
        row.locator('[data-preview-open]').click()
        expect(page.locator('.preview__image-unavailable')).to_be_visible()
        self.assertIn('Image unavailable on this computer',
                      page.locator('.preview__image-unavailable').inner_text())
        page.close()

        projector = self._page(f'/projector?service={self.service.pk}',
                               available=False)
        projector.keyboard.press('Space')
        projector.keyboard.press('Control+ArrowRight')
        projector.wait_for_function("document.querySelector('.screen.is-active [data-media-image]')")
        expect(projector.locator('.screen.is-active .screen__image-missing')).to_be_visible()
        self.assertEqual(projector.locator('.screen.is-active').inner_text().strip(), '')
        projector.close()

    def test_projector_loaded_image_shows_no_placeholder(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        page.wait_for_function("document.querySelector('.screen.is-active [data-media-image]')")
        screen = page.locator('.screen.is-active')
        expect(screen.locator('.screen__image')).to_be_visible()
        expect(screen.locator('.screen__image-missing')).to_be_hidden()
        page.close()

    def test_a_pending_image_screen_paints_nothing(self):
        page = self._page(f'/projector?service={self.service.pk}', pending=True)
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        page.wait_for_function("document.querySelector('.screen.is-active [data-media-image]')")
        screen = page.locator('.screen.is-active')
        expect(screen.locator('.screen__image')).to_be_hidden()
        expect(screen.locator('.screen__image-missing')).to_be_hidden()
        for route in self.held_routes:
            route.abort()
        page.close()

    def test_projector_displays_image_only_on_its_screen(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__image')).to_be_visible()
        self.assertEqual(page.locator('.screen.is-active .screen__image').evaluate(
            '(img) => [img.naturalWidth, img.naturalHeight]'), [12, 6])
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__image')).to_have_count(0)
        page.close()

    def test_narrow_dark_preview_fits_and_backdrop_closes(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.set_viewport_size({'width': 390, 'height': 700})
        page.evaluate("document.documentElement.dataset.theme = 'dark'")
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('#previewModal .preview__image img')).to_be_visible()
        bounds = page.locator('#previewModal').bounding_box()
        self.assertLessEqual(bounds['width'], 358)
        self.assertLessEqual(bounds['height'], 652)
        page.mouse.click(4, 4)
        expect(page.locator('#previewModal')).not_to_be_visible()
        page.close()
