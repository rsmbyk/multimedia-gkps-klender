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
    STAGE = {'w': 1376, 'h': 804}          # a 1440×900 window minus the screen's 32/32/64 padding

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
        # spec 158: one media entry per shape the fit has to answer for
        self.files = {self.image.sha256: _png()}
        self.entries = {'image': self.entry}
        for order, (slug, sha, size) in enumerate((
                ('landscape', 'b' * 64, (24, 6)),
                ('large', 'c' * 64, (600, 300)),
                ('portrait', 'd' * 64, (300, 400))), start=4):
            media = tatib.MediaIdentity.objects.create(
                sha256=sha, byte_count=120, family='image', display_filename=f'{slug}.png')
            self.files[sha] = _png(*size)
            self.entries[slug] = tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=order,
                media=media, media_filename=f'{slug}.png', title=slug.title())
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

        def serve(route):
            sha = route.request.url.rsplit('/', 1)[-1]
            headers = {'Access-Control-Allow-Origin': route.request.headers.get('origin', '*'),
                       'Content-Type': 'application/octet-stream'}
            route.fulfill(status=200 if available else 404, headers=headers,
                          body=self.files.get(sha, b'') if available else b'')

        self.held_routes = []

        def hold(route):
            # Answered by nothing until the case ends: the request stays in flight, so the
            # screen stays pending. Aborted afterwards, or Playwright cancels the handler
            # mid-close and prints a traceback that reads like a failure.
            self.held_routes.append(route)

        for sha in self.files:
            page.route('http://127.0.0.1:63174/v1/files/' + sha,
                       hold if pending and sha == self.image.sha256 else serve)
        page.goto(self.live_server_url + path)
        return page

    def _projector(self, entry_slug, available=True):
        """The projector, stepped to one media entry (Space shows, Ctrl+→ steps entries)."""
        page = self._page(f'/projector?service={self.service.pk}', available=available)
        page.keyboard.press('Space')
        for _ in range(self.entries[entry_slug].order_number - 1):
            page.keyboard.press('Control+ArrowRight')
        return page

    def _painted(self, page, selector='.screen.is-active .screen__image'):
        page.wait_for_function(
            "([selector]) => { const el = document.querySelector(selector);"
            " return Boolean(el) && el.getBoundingClientRect().width > 0; }", arg=[selector])
        box = page.locator(selector).bounding_box()
        return {'w': box['width'], 'h': box['height']}

    def _assert_painted(self, page, width, height, selector='.screen.is-active .screen__image'):
        painted = self._painted(page, selector)
        self.assertAlmostEqual(painted['w'], width, delta=1.5,
                               msg=f'painted width {painted["w"]} != {width}')
        self.assertAlmostEqual(painted['h'], height, delta=1.5,
                               msg=f'painted height {painted["h"]} != {height}')
        return painted

    def test_projector_enlarges_a_small_image_to_the_stage(self):
        """FR-001/FR-006, SC-001/SC-003: the 12×6 image fills the stage, and follows a resize."""
        page = self._projector('image')
        self._assert_painted(page, self.STAGE['w'], 688)          # 1376/12 < 804/6
        page.set_viewport_size({'width': 1024, 'height': 768})
        page.wait_for_function(
            "() => { const el = document.querySelector('.screen.is-active .screen__image');"
            " return el && Math.round(el.getBoundingClientRect().height) < 600; }")
        self._assert_painted(page, 960, 480)                       # 960/12 < 672/6
        page.close()

    def test_a_landscape_image_fits_by_its_width(self):
        """FR-001 AC3, SC-006: the width is the smaller ratio, so the width is what it fills."""
        page = self._projector('landscape')
        self._assert_painted(page, self.STAGE['w'], 344)          # 1376/24 < 804/6
        page.close()

    def test_a_large_image_still_shrinks(self):
        """US1 AC2: the same rule below 1 — a 600×300 image is capped by the stage."""
        page = self._projector('large')
        self._assert_painted(page, self.STAGE['w'], 688)          # 1376/600 < 804/300
        page.close()

    def test_projector_t_toggles_fit_width_and_height(self):
        """FR-003/FR-004, SC-004: the fit is one of the two states, so T offers the other."""
        page = self._projector('image')
        self._assert_painted(page, 1376, 688)                     # the fit: width-bound
        page.keyboard.press('t')
        self._assert_painted(page, 1608, 804)                     # fit height: 804/6, cut 116 each side
        page.keyboard.press('t')
        self._assert_painted(page, 1376, 688)                     # back to fit width
        page.close()

    def test_projector_pans_the_overflow_by_drag_and_wheel(self):
        """FR-009/FR-010/FR-012, SC-008/SC-009: drag and wheel pan, clamped, and say so."""
        page = self._projector('portrait')
        self._assert_painted(page, 603, 804)                      # the 300×400 image at its fit
        page.keyboard.press('t')                                  # fit width: 1376×1834
        self._assert_painted(page, 1376, 1834)
        image = '.screen.is-active .screen__image'
        screen_before = page.get_attribute('body', 'data-current-screen')

        def transform():
            return page.locator(image).evaluate('el => el.style.transform')

        # the pointer says the page can be dragged, and the first press only enters fullscreen
        page.locator('.mouse-zone--display').click(position={'x': 200, 'y': 200})
        page.wait_for_function('document.fullscreenElement !== null')
        self.assertEqual(page.locator('.mouse-zone--display').evaluate(
            'el => getComputedStyle(el).cursor'), 'grab')

        page.mouse.move(688, 400)
        page.mouse.down()
        page.mouse.move(688, 200, steps=8)                        # drag up 200
        page.mouse.up()
        self.assertEqual(transform(), 'translate(0px, -200px)')

        page.mouse.move(688, 100)
        page.mouse.down()
        page.mouse.move(688, 850, steps=10)                       # drag down past the end
        page.mouse.up()
        self.assertEqual(transform(), 'translate(0px, 515px)')    # (1834 − 804) / 2

        page.mouse.move(688, 400)                                 # back over the stage
        page.mouse.wheel(0, 300)                                  # the wheel pans the same axis
        self.assertEqual(transform(), 'translate(0px, 215px)')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), screen_before)

        page.keyboard.press('t')                                  # back to the fit: no overflow
        self._assert_painted(page, 603, 804)
        self.assertEqual(transform(), '')
        page.mouse.wheel(0, 300)                                  # nothing to pan: the wheel is inert
        self.assertEqual(transform(), '')
        page.close()

    def test_projector_press_without_drag_still_steps(self):
        """FR-011, SC-010: a press that does not move is still the corner's click."""
        page = self._projector('portrait')
        page.keyboard.press('t')
        page.locator('.mouse-zone--display').click(position={'x': 200, 'y': 200})
        page.wait_for_function('document.fullscreenElement !== null')
        image = '.screen.is-active .screen__image'

        page.mouse.move(1200, 400)
        page.mouse.down()
        page.mouse.move(1202, 401)                                # 2 px: under the threshold
        self.assertEqual(page.locator(image).evaluate('el => el.style.transform'), '')
        page.mouse.up()

        before = page.get_attribute('body', 'data-current-screen')
        page.mouse.click(100, 400)                                # the left third: previous
        page.wait_for_timeout(250)
        self.assertNotEqual(page.get_attribute('body', 'data-current-screen'), before)
        page.close()

    def test_shortcut_sheet_lists_the_fit_key(self):
        """FR-007, SC-007: the sheet names the key, and still fits a 1024×768 window."""
        page = self._projector('image')
        page.keyboard.press('k')
        group = page.locator('#key-list .group', has=page.locator('h3:text-is("Image and PDF")'))
        self.assertEqual(group.locator('.row .fn').inner_text().strip(), 'Fit Width / Fit Height')
        self.assertEqual(group.locator('.row .k').inner_text().strip(), 'T')
        page.set_viewport_size({'width': 1024, 'height': 768})
        page.keyboard.press('k')
        page.wait_for_timeout(250)
        page.keyboard.press('k')
        page.wait_for_timeout(400)
        sheet = page.locator('#key-list').bounding_box()
        self.assertLessEqual(sheet['y'] + sheet['height'], 768 + 1)
        self.assertGreaterEqual(sheet['y'], -1)
        page.close()

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
