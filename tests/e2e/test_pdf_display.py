"""PDF pages in Tata Ibadah Preview and projector (spec 117)."""
import hashlib
import unittest
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


def _pdf():
    """A three-page PDF with a landscape middle page; no external fixture."""
    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Count 3 /Kids [3 0 R 4 0 R 5 0 R] >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 400] /Contents 6 0 R >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 500 300] /Contents 6 0 R >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 400] /Contents 6 0 R >>',
        b'<< /Length 0 >>\nstream\n\nendstream',
    ]
    data = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f'{number} 0 obj\n'.encode() + body + b'\nendobj\n')
    start = len(data)
    data.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]:
        data.extend(f'{offset:010d} 00000 n \n'.encode())
    data.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode())
    return bytes(data)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PDFDisplayE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.payload = _pdf()
        self.sha = hashlib.sha256(self.payload).hexdigest()
        self.service = tatib.TataIbadah.objects.create(
            name='PDF service', date=date(2026, 10, 19), is_active=True)
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=1, title='Opening', text='Welcome')
        media = tatib.MediaIdentity.objects.create(sha256=self.sha, byte_count=len(self.payload),
                                                  family='pdf', display_filename='order.pdf')
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=2,
            media=media, media_filename='order.pdf', title='Order of service')
        tatib.ServiceEntry.objects.create(tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                                          order_number=3, title='Closing', text='Amen')
        self.untitled = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=4,
            media=media, media_filename='order.pdf')
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

    def _page(self, path, available=True, payload=None):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        def serve(route):
            route.fulfill(status=200 if available else 404,
                          headers={'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                                   'Content-Type': 'application/octet-stream'},
                          body=(self.payload if payload is None else payload) if available else b'')
        page.route('http://127.0.0.1:63174/v1/files/' + self.sha, serve)
        page.goto(self.live_server_url + path)
        return page

    def test_preview_turns_pages_and_follows_landscape_size(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        count = page.locator('[data-pdf-count]')
        expect(count).to_have_text('1 / 3')
        expect(page.locator('#previewTitle')).to_have_text('Order of service')
        page.wait_for_timeout(250)
        first = page.locator('#previewModal').bounding_box()
        page.locator('[data-pdf-next]').click()
        expect(count).to_have_text('2 / 3')
        page.wait_for_timeout(250)
        second = page.locator('#previewModal').bounding_box()
        self.assertGreater(second['width'], first['width'])
        page.keyboard.press('ArrowRight')
        expect(count).to_have_text('3 / 3')
        expect(page.locator('[data-pdf-next]')).to_be_disabled()
        page.keyboard.press('Escape')
        expect(page.locator('#previewModal')).not_to_be_visible()
        page.close()

    def test_projector_steps_within_pdf_before_adjacent_entry(self):
        page = self._page(f'/projector?service={self.service.pk}')
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        expect(page.locator('.screen.is-active .screen__pdf-page')).to_be_visible()
        expect(page.locator('#cue-progress')).to_have_text('1/3')
        page.keyboard.press('ArrowRight')
        expect(page.locator('#cue-progress')).to_have_text('2/3')
        page.keyboard.press('ArrowRight')
        expect(page.locator('#cue-progress')).to_have_text('3/3')
        page.keyboard.press('ArrowRight')
        expect(page.locator('.screen.is-active [data-media-pdf]')).to_have_count(0)
        page.keyboard.press('ArrowLeft')
        expect(page.locator('#cue-progress')).to_have_text('3/3')
        page.close()

    def test_missing_pdf_is_quiet(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]), available=False)
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.preview__pdf-unavailable')).to_be_visible()
        page.close()
        projector = self._page(f'/projector?service={self.service.pk}', available=False)
        projector.keyboard.press('Space')
        projector.keyboard.press('Control+ArrowRight')
        expect(projector.locator('.screen.is-active .screen__pdf-missing')).to_be_visible()
        expect(projector.locator('#corner-cue')).not_to_be_visible()
        projector.close()

    def test_corrupt_pdf_is_unavailable_without_replacing_entry(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]), payload=b'%PDF-invalid')
        row = page.locator('#ti-e' + str(self.entry.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('.preview__pdf-unavailable')).to_be_visible()
        expect(page.locator('#previewTitle')).to_have_text('Order of service')
        page.close()

    def test_untitled_pdf_uses_filename_in_preview_header(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        row = page.locator('#ti-e' + str(self.untitled.pk))
        row.scroll_into_view_if_needed()
        row.locator('[data-preview-open]').evaluate('(button) => button.click()')
        expect(page.locator('#previewTitle')).to_have_text('order.pdf')
        expect(page.locator('[data-pdf-count]')).to_have_text('1 / 3')
        page.close()

