"""Spec 119 — one browser-local display state, three surfaces.

The dock is the writer; the projector and the caption overlay render what it says.
Everything these tests assert lives in the browser (localStorage, the display
channel, the DOM): one CONTEXT is one laptop — its tabs share the state, a second
context would be another laptop and must not see it.

Same runner rules as the other e2e suites: fixtures in setUp, the browser is closed
before any ORM assertion, and Playwright's loop never overlaps Django's database
access.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ObsDockE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Doa', text='Tuhan, dengarkanlah doa kami')
        self.other = tatib.TataIbadah.objects.create(
            name='Ibadah Sore', date=date(2026, 10, 25), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.other, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Damai di bumi bagi manusia')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self._close_browser()
        super().tearDown()

    def _close_browser(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    # ---------- helpers -------------------------------------------------------

    def _context(self):
        return self.browser.new_context(viewport={'width': 1440, 'height': 900})

    def _open(self, context, path):
        page = context.new_page()
        page.goto(self.live_server_url + path)
        return page

    def _state(self, page):
        return page.evaluate(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")

    def _wait_state(self, page, service, on=True):
        page.wait_for_function(
            """([service, on]) => {
                 const state = JSON.parse(localStorage.getItem('gkps-display') || 'null');
                 return state && state.service === service && state.on === on;
               }""",
            arg=[service, on])

    def _open_service(self, dock, name):
        dock.locator(f'.servicerow[data-name="{name}"]').first.click()
        dock.wait_for_selector('.entryrow')

    def _project_first_entry(self, dock):
        dock.locator('.entryrow').first.click()

    def _caption(self, overlay):
        overlay.wait_for_selector('.obs-overlay__caption')
        return overlay.locator('.obs-overlay__caption').inner_text()

    # ---------- the tests -----------------------------------------------------

    def test_browsing_does_not_project_and_an_entry_click_does(self):
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Minggu')

        # Opening a service is browsing: nothing is on air yet.
        self.assertIsNone(self._state(dock))

        projector = self._open(context, '/projector')
        overlay = self._open(context, '/obs/source/overlay')

        self._project_first_entry(dock)
        self._wait_state(dock, self.service.pk)

        projector.wait_for_function(
            "service => document.body.dataset.service === String(service)",
            arg=self.service.pk)
        self.assertEqual(
            projector.evaluate("document.body.classList.contains('words-hidden')"), False)
        self.assertIn(
            'Kasih karunia', projector.locator('.screen.is-active .screen__lines').inner_text())
        self.assertIn('Kasih karunia', self._caption(overlay))
        context.close()

    def test_keyboard_steps_screens_and_space_pauses_and_resumes(self):
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Minggu')
        overlay = self._open(context, '/obs/source/overlay')
        projector = self._open(context, '/projector')

        self._project_first_entry(dock)
        self._wait_state(dock, self.service.pk)
        self.assertIn('Kasih karunia', self._caption(overlay))

        # The entry's own trailing screen is blank; the next entry's words follow it.
        dock.keyboard.press('ArrowDown')
        dock.keyboard.press('ArrowDown')
        dock.wait_for_function(
            "() => JSON.parse(localStorage.getItem('gkps-display')).screen === 2")
        overlay.wait_for_function(
            "() => ((document.querySelector('.obs-overlay__caption') || {}).textContent || '')"
            ".includes('Tuhan, dengarkanlah')")

        # Space: words off everywhere, the place kept.
        dock.keyboard.press(' ')
        self._wait_state(dock, self.service.pk, on=False)
        self.assertEqual(overlay.locator('.obs-overlay__caption').count(), 0)
        self.assertEqual(
            projector.evaluate("document.body.classList.contains('words-hidden')"), True)

        # Space again: the same screen comes back.
        dock.keyboard.press(' ')
        self._wait_state(dock, self.service.pk, on=True)
        self.assertIn('Tuhan, dengarkanlah', self._caption(overlay))
        context.close()

    def test_every_surface_closed_the_display_is_still_there(self):
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Minggu')
        self._project_first_entry(dock)
        self._wait_state(dock, self.service.pk)
        dock.keyboard.press('ArrowDown')
        dock.keyboard.press('ArrowDown')
        dock.wait_for_function(
            "() => JSON.parse(localStorage.getItem('gkps-display')).screen === 2")
        dock.close()                        # every tab is gone; the display is not

        projector = self._open(context, '/projector')
        projector.wait_for_function(
            "service => document.body.dataset.service === String(service)",
            arg=self.service.pk)
        self.assertEqual(
            projector.evaluate("document.body.classList.contains('words-hidden')"), False)
        self.assertIn(
            'Tuhan, dengarkanlah', projector.locator('.screen.is-active .screen__lines').inner_text())

        overlay = self._open(context, '/obs/source/overlay')
        self.assertIn('Tuhan, dengarkanlah', self._caption(overlay))
        context.close()

    def test_naming_a_service_in_the_projector_url_adopts_it_everywhere(self):
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Minggu')
        self._project_first_entry(dock)
        self._wait_state(dock, self.service.pk)

        first = self._open(context, '/projector')
        first.wait_for_function(
            "service => document.body.dataset.service === String(service)",
            arg=self.service.pk)

        # ?service<other> is an act of projection: it replaces the active service,
        # and the page that was already open adopts it in place (no navigation).
        adopted = self._open(context, '/projector?service=%d' % self.other.pk)
        self._wait_state(dock, self.other.pk)
        for page in (first, adopted):
            page.wait_for_function(
                "service => document.body.dataset.service === String(service)",
                arg=self.other.pk)
            self.assertIn(
                'Damai di bumi',
                page.locator('.screen.is-active .screen__lines').inner_text())
        self.assertEqual(adopted.url.split('?')[0], self.live_server_url + '/projector')
        self.assertEqual(first.url.split('?')[0], self.live_server_url + '/projector')
        context.close()
