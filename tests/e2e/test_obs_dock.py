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
        # Spec 164: one service whose only entry is a picture, so its group's rest is reachable
        # without another kind's screens in the way. Dated oldest, so the picker's order holds.
        self.media_service = tatib.TataIbadah.objects.create(
            name='Media Minggu', date=date(2026, 10, 11), is_active=True)
        self.media = tatib.MediaIdentity.objects.create(
            sha256='1' * 64, byte_count=120, family='image', display_filename='slide.png')
        tatib.ServiceEntry.objects.create(
            tatib=self.media_service, order_number=1, kind=tatib.ServiceEntryKind.MEDIA,
            media=self.media, media_filename='slide.png', title='Opening image')

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
        """The overlay's words, whatever its kind paints them with (spec 165)."""
        overlay.wait_for_selector('.obs-overlay__plate, .obs-overlay__caption')
        return overlay.locator('.obs-overlay__stage').inner_text()

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

    def test_the_picker_answers_the_arrows_and_enter(self):
        context = self._context()
        dock = self._open(context, '/obs/dock')

        # Newest first: 25 Oct (Ibadah Sore), then 18 Oct (Ibadah Minggu). The
        # first row is marked before a key is pressed, so Enter always has a target.
        dock.wait_for_selector('.servicerow.is-cursor')
        self.assertEqual(
            dock.evaluate("document.querySelector('.servicerow.is-cursor').dataset.name"),
            'Ibadah Sore')

        dock.keyboard.press('ArrowDown')
        self.assertEqual(
            dock.evaluate("document.querySelector('.servicerow.is-cursor').dataset.name"),
            'Ibadah Minggu')

        dock.keyboard.press('Enter')
        dock.wait_for_selector('.entryrow')
        self.assertEqual(
            dock.evaluate("document.getElementById('runService').textContent"),
            'Ibadah Minggu')

        # Back in the picker, the mark stays on the service just opened.
        dock.keyboard.press('Escape')
        dock.wait_for_function(
            "() => document.getElementById('dockPanel').dataset.view === 'pick'")
        self.assertEqual(
            dock.evaluate("document.querySelector('.servicerow.is-cursor').dataset.name"),
            'Ibadah Minggu')
        context.close()

    def test_a_media_entry_lists_and_steps_its_rest(self):
        """Spec 164: the media entry's inner list shows its rest and the transport lands on it."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Media Minggu')
        self._project_first_entry(dock)
        self._wait_state(dock, self.media_service.pk)

        rows = dock.evaluate(
            "() => [...document.querySelectorAll('.entryli')].map(li =>"
            " [...li.querySelectorAll('.screenerow')].map(row => row.innerText.trim()))")
        self.assertEqual(rows[0][:2], ['IMAGE', 'Rest'])

        # One press past the picture is the entry's own rest, and the projector paints it blank.
        dock.keyboard.press('ArrowDown')
        dock.wait_for_function(
            "() => JSON.parse(localStorage.getItem('gkps-display')).screen === 1")
        projector = self._open(context, '/projector')
        projector.wait_for_function(
            "() => { const el = document.querySelector('.screen.is-active');"
            " return el && el.classList.contains('is-blank'); }")
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
            "() => document.getElementById('overlayStage').textContent"
            ".includes('Tuhan, dengarkanlah')")

        # Space: words off everywhere, the place kept.
        dock.keyboard.press(' ')
        self._wait_state(dock, self.service.pk, on=False)
        overlay.wait_for_function(
            "() => document.getElementById('overlayStage').children.length === 0")
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

    # ---------- the panel's own width (spec 164) ------------------------------

    def _panel(self, page, widths):
        """The dock's box at each width, and the body's horizontal overflow."""
        boxes = []
        for width in widths:
            page.set_viewport_size({'width': width, 'height': 900})
            boxes.append(page.evaluate("""() => {
                const box = document.querySelector('.dock').getBoundingClientRect();
                return {width: document.documentElement.clientWidth,
                        x: box.x, w: box.width,
                        overflow: document.documentElement.scrollWidth
                                  - document.documentElement.clientWidth};
            }"""))
        return boxes

    def test_the_dock_fills_whatever_width_it_is_given(self):
        # An OBS dock panel is 300px in one layout and a second monitor in another,
        # so the panel is the page at every width: no cap, no centring.
        context = self._context()
        dock = self._open(context, '/obs/dock')
        dock.wait_for_selector('.servicerow')

        for box in self._panel(dock, (320, 420, 560, 720, 900, 1440, 1920, 2560)):
            self.assertAlmostEqual(box['x'], 0, delta=0.5, msg=f"panel starts at {box['x']} at {box['width']}px")
            self.assertAlmostEqual(box['w'], box['width'], delta=0.5,
                                   msg=f"panel is {box['w']} of {box['width']}px")
            self.assertEqual(box['overflow'], 0, f"horizontal overflow at {box['width']}px")
        context.close()

    def test_a_wide_dock_keeps_the_picker_in_one_column(self):
        # One column at every width — the bucket list does not fan out — but the
        # rows fill the panel instead of sitting in a capped, centred strip.
        context = self._context()
        dock = self._open(context, '/obs/dock')
        dock.wait_for_selector('.servicerow')

        for width in (560, 900, 1440, 1920):
            dock.set_viewport_size({'width': width, 'height': 900})
            boxes = dock.evaluate("""() => {
                const body = document.getElementById('pickBody');
                const style = getComputedStyle(body);
                const secs = [...body.querySelectorAll('section')];
                return {display: style.display,
                        contentW: body.clientWidth - parseFloat(style.paddingLeft)
                                  - parseFloat(style.paddingRight),
                        rowW: body.querySelector('.servicerow').getBoundingClientRect().width,
                        xs: secs.map(s => Math.round(s.getBoundingClientRect().x)),
                        head: getComputedStyle(body.querySelector('.group__head')).position};
            }""")
            self.assertEqual(boxes['display'], 'block', f"single column at {width}px")
            self.assertEqual(len(set(boxes['xs'])), 1, f"buckets stacked at {width}px: {boxes['xs']}")
            self.assertAlmostEqual(boxes['rowW'], boxes['contentW'], delta=0.5,
                                   msg=f"row is {boxes['rowW']} of {boxes['contentW']}px at {width}px")
            self.assertAlmostEqual(boxes['rowW'], width - 16, delta=1,
                                   msg=f"row spans {boxes['rowW']} of {width}px")
            self.assertEqual(boxes['head'], 'sticky')
        context.close()
