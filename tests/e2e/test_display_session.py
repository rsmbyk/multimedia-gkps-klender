"""Spec 184 — the display state lives only for the browser session.

The state is one object in `localStorage['gkps-display']`, stamped with the session that
wrote it. A state from an earlier session paints nothing, on any surface; inside one
session every surface still catches up and closing every surface changes nothing
(spec 119's rule, kept).

One CONTEXT is one browser session: its pages share cookies and storage. A prior
session is a context with the state seeded and no marker; a real restart is a
persistent Chromium profile launched twice.
"""

import json
import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


STATE_KEY = 'gkps-display'
SESSION_COOKIE = 'gkps-session'


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DisplaySessionE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Sesi', date=date(2026, 11, 1), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Doa', text='Tuhan, dengarkanlah doa kami')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

        self._profiles = []

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
        return self.browser.new_context(viewport={'width': 1280, 'height': 720})

    def _open(self, context, path):
        page = context.new_page()
        page.goto(self.live_server_url + path)
        return page

    def _stored(self, page):
        return page.evaluate(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")

    def _project(self, context):
        """Open the dock, run the first entry, and return the dock, on air."""
        dock = self._open(context, '/obs/dock')
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        dock.locator('.entryrow').first.click()
        dock.wait_for_function(
            """service => {
                 const state = JSON.parse(localStorage.getItem('gkps-display') || 'null');
                 return state && state.service === service && state.on === true;
               }""", arg=self.service.pk)
        return dock

    def _seed(self, context, state, watch=True):
        """Put a display state in the browser before any page script runs.

        No marker is written: this is what a state left by an earlier session looks
        like. With `watch`, an observer records whether the overlay ever painted.
        """
        script = "localStorage.setItem(%s, %s);" % (
            json.dumps(STATE_KEY), json.dumps(json.dumps(state)))
        if watch:
            script += """
                window.__overlayEverPainted = false;
                window.__overlayPaintCount = 0;
                const __checkOverlay = () => {
                    const stage = document.getElementById('overlayStage');
                    if (stage && stage.children.length > 0) {
                        window.__overlayEverPainted = true;
                        if (window.__overlayPaintCount === 0) window.__overlayPaintCount = 1;
                    }
                };
                new MutationObserver(__checkOverlay).observe(
                    document, {childList: true, subtree: true});
                document.addEventListener('DOMContentLoaded', __checkOverlay);
            """
        context.add_init_script(script)

    def _marker(self, page):
        return page.evaluate(
            """() => {
                 const match = document.cookie.match(/(?:^|;\\s*)gkps-session=([^;]+)/);
                 return match ? decodeURIComponent(match[1]) : '';
               }""")

    def _pill_count(self, dock):
        return dock.evaluate(
            "() => [...document.querySelectorAll('.onscreen')].filter(p => !p.hidden).length")

    # ---------- the marker's write path --------------------------------------

    def test_the_state_carries_the_session_of_its_writer(self):
        context = self._context()
        dock = self._project(context)
        stored = self._stored(dock)
        marker = self._marker(dock)
        self.assertTrue(marker, 'no session marker was minted')
        self.assertEqual(stored['session'], marker)
        self.assertEqual(stored['service'], self.service.pk)
        context.close()

    def test_the_marker_carries_no_display_data(self):
        context = self._context()
        dock = self._project(context)
        marker = self._marker(dock)
        self.assertRegex(marker, r'^[A-Za-z0-9._-]{8,64}$')
        self.assertNotIn('service', marker)
        self.assertNotIn('screen', marker)
        self.assertEqual(
            [part.split('=')[0].strip() for part in dock.evaluate('document.cookie').split(';')],
            [SESSION_COOKIE])
        context.close()

    def test_two_surfaces_minting_together_agree_on_one_session(self):
        context = self._context()
        first = self._open(context, '/obs/dock')
        second = self._open(context, '/obs/dock')
        first.wait_for_selector('.servicerow')
        second.wait_for_selector('.servicerow')
        context.clear_cookies()
        first.evaluate(
            "service => window.gkpsDisplay.show(service, 0)", self.service.pk)
        second.evaluate(
            "service => window.gkpsDisplay.show(service, 0)", self.service.pk)
        stored = self._stored(first)
        self.assertEqual(stored['session'], self._marker(first))
        self.assertEqual(stored['session'], self._marker(second))

        # A surface that finds the jar already holding a value takes that value rather
        # than stamping the candidate it generated: the write that follows can never
        # carry an id the session no longer holds.
        context.clear_cookies()
        first.evaluate("""() => {
            document.cookie = 'gkps-session=; path=/; max-age=0';
            document.cookie = 'gkps-session=the-one-the-jar-holds; path=/; SameSite=Lax';
        }""")
        first.evaluate("service => window.gkpsDisplay.show(service, 0)", self.service.pk)
        self.assertEqual(self._stored(first)['session'], 'the-one-the-jar-holds')
        self.assertEqual(self._marker(first), 'the-one-the-jar-holds')
        context.close()

    # ---------- a reader rejects a foreign stamp -----------------------------

    def test_a_state_with_a_foreign_stamp_reads_as_no_state(self):
        context = self._context()
        self._seed(context, {'service': self.service.pk, 'screen': 0, 'on': True,
                             'translation': None, 'at': 1,
                             'session': 'a-session-that-is-not-here'})
        dock = self._open(context, '/obs/dock')
        dock.wait_for_selector('.servicerow')
        read = dock.evaluate("() => window.gkpsDisplay.read()")
        self.assertIsNone(read['service'])
        self.assertFalse(read['on'])
        overlay = self._open(context, '/obs/source/overlay')
        overlay.wait_for_timeout(500)
        self.assertEqual(overlay.evaluate(
            "document.getElementById('overlayStage').children.length"), 0)
        context.close()

    def test_a_state_written_before_this_slice_reads_as_no_state(self):
        context = self._context()
        self._seed(context, {'service': self.service.pk, 'screen': 0, 'on': True,
                             'translation': None, 'at': 1})
        dock = self._open(context, '/obs/dock')
        dock.wait_for_selector('.servicerow')
        read = dock.evaluate("() => window.gkpsDisplay.read()")
        self.assertIsNone(read['service'])
        self.assertFalse(read['on'])
        context.close()

    # ---------- US1: a browser that starts again starts idle -----------------

    def test_a_state_from_an_earlier_session_paints_nothing(self):
        context = self._context()
        self._seed(context, {'service': self.service.pk, 'screen': 0, 'on': True,
                             'translation': None, 'at': 1,
                             'session': 'a-session-that-is-not-here'})
        overlay = self._open(context, '/obs/source/overlay')
        overlay.wait_for_timeout(600)
        self.assertEqual(overlay.evaluate(
            "document.getElementById('overlayStage').children.length"), 0)

        dock = self._open(context, '/obs/dock')
        dock.wait_for_selector('.servicerow')
        dock.wait_for_timeout(200)
        self.assertEqual(self._pill_count(dock), 0)
        control = dock.evaluate(
            "() => document.getElementById('blankBtn').getAttribute('aria-label')")
        self.assertEqual(control, 'Display this service')

        projector = self._open(context, '/projector')
        projector.wait_for_timeout(600)
        self.assertEqual(projector.get_attribute('body', 'data-showing'), 'false')
        self.assertEqual(projector.locator('.screen.is-active').count(), 0)
        context.close()

    def test_first_paint_never_shows_a_prior_session_state(self):
        context = self._context()
        self._seed(context, {'service': self.service.pk, 'screen': 0, 'on': True,
                             'translation': None, 'at': 1,
                             'session': 'a-session-that-is-not-here'})
        overlay = self._open(context, '/obs/source/overlay')
        overlay.wait_for_timeout(700)
        self.assertFalse(overlay.evaluate('window.__overlayEverPainted'),
                         'the overlay painted a prior session state')
        context.close()

    def test_a_browser_restart_ends_the_session(self):
        profile = tempfile.mkdtemp(prefix='gkps-184-')
        self._profiles.append(profile)
        context = self.browser.new_context()  # replaced below; kept for symmetry
        context.close()
        persistent = self._playwright.chromium.launch_persistent_context(
            profile, headless=True, viewport={'width': 1280, 'height': 720})
        try:
            dock = persistent.pages[0] if persistent.pages else persistent.new_page()
            dock.goto(self.live_server_url + '/obs/dock')
            dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
            dock.wait_for_selector('.entryrow')
            dock.locator('.entryrow').first.click()
            dock.wait_for_function(
                """service => {
                     const state = JSON.parse(localStorage.getItem('gkps-display') || 'null');
                     return state && state.service === service && state.on === true;
                   }""", arg=self.service.pk)
            before = self._stored(dock)
            self.assertTrue(before['session'])
        finally:
            persistent.close()

        again = self._playwright.chromium.launch_persistent_context(
            profile, headless=True, viewport={'width': 1280, 'height': 720})
        try:
            names = [cookie['name'] for cookie in again.cookies()]
            self.assertNotIn(SESSION_COOKIE, names, 'the session marker outlived the browser')
            overlay = again.new_page()
            overlay.goto(self.live_server_url + '/obs/source/overlay')
            overlay.wait_for_timeout(700)
            self.assertEqual(overlay.evaluate(
                "document.getElementById('overlayStage').children.length"), 0)
            kept = overlay.evaluate(
                "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")
            self.assertEqual(kept['service'], self.service.pk,
                             'the storage outlived the browser too; the test proves nothing')
        finally:
            again.close()
            shutil.rmtree(profile, ignore_errors=True)

    # ---------- US2: inside one session nothing changes ----------------------

    def test_a_reload_inside_the_session_keeps_the_display(self):
        context = self._context()
        dock = self._project(context)
        overlay = self._open(context, '/obs/source/overlay')
        overlay.wait_for_selector('.obs-overlay__plate')

        overlay.reload()
        overlay.wait_for_selector('.obs-overlay__plate')
        dock.reload()
        dock.wait_for_selector('.servicerow', state='attached')
        dock.wait_for_timeout(200)
        self.assertEqual(self._pill_count(dock), 1)
        # And the dock comes back on the service it was running, not on the picker
        # (spec 187 FR-016).
        self.assertEqual(
            dock.evaluate("() => document.getElementById('dockPanel').dataset.view"),
            'run')
        self.assertEqual(overlay.evaluate(
            "document.getElementById('overlayStage').children.length"), 1)
        context.close()

    def test_every_surface_closed_and_reopened_keeps_the_display(self):
        context = self._context()
        dock = self._project(context)
        overlay = self._open(context, '/obs/source/overlay')
        overlay.wait_for_selector('.obs-overlay__plate')
        dock.close()
        overlay.close()

        overlay = self._open(context, '/obs/source/overlay')
        overlay.wait_for_selector('.obs-overlay__plate')
        dock = self._open(context, '/obs/dock')
        dock.wait_for_selector('.servicerow', state='attached')
        dock.wait_for_timeout(200)
        self.assertEqual(self._pill_count(dock), 1)
        self.assertEqual(
            dock.evaluate("() => document.getElementById('dockPanel').dataset.view"),
            'run')
        context.close()

    # ---------- the browser that cannot hold a session ----------------------

    def test_a_surface_without_cookie_storage_still_paints(self):
        context = self._context()
        errors = []
        context.add_init_script("""
            Object.defineProperty(Document.prototype, 'cookie', {
                configurable: true,
                get() { return ''; },
                set(value) { /* a browser that refuses cookies */ }
            });
        """)
        dock = self._open(context, '/obs/dock')
        dock.on('pageerror', lambda error: errors.append(str(error)))
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        dock.locator('.entryrow').first.click()
        dock.wait_for_function("() => window.gkpsDisplay.read().on === true")
        self.assertEqual(errors, [])

        dock.reload()
        dock.wait_for_selector('.servicerow')
        dock.wait_for_timeout(200)
        read = dock.evaluate("() => window.gkpsDisplay.read()")
        self.assertFalse(read['on'], 'a reload with no session marker resurrected the display')
        context.close()
