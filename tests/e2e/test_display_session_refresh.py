"""Spec 186 — a surface re-reads the session it is showing.

The display state is refused when its session stamp is not this browser's (spec 184). That
refusal only happened when a surface read again, and an open tab reads again only when
something writes — so a dock or projector that outlived the browser session kept painting
a display every new surface refused. The re-read on focus/visibility/pageshow closes it.
"""

import json
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


STATE_KEY = 'gkps-display'


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DisplaySessionRefreshE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Sesi Ulang', date=date(2026, 11, 15), is_active=True)
        for order, text in enumerate(['Salam', 'Pujian', 'Firman'], 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                order_number=order, title=text, text=f'{text} umat Tuhan')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None
        super().tearDown()

    # ---------- helpers -------------------------------------------------------

    def _context(self, width=900):
        return self.browser.new_context(viewport={'width': width, 'height': 800})

    def _dock(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector(f'.servicerow[data-service="{self.service.pk}"]')
        page.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        page.wait_for_selector('.entryrow')
        return page

    def _project(self, page, index=1):
        page.locator('.entryrow').nth(index).click()
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.service && s.on === true); }")
        page.wait_for_timeout(300)

    def _focus(self, page):
        page.evaluate("() => window.dispatchEvent(new Event('focus'))")
        page.wait_for_timeout(250)

    def _visibility(self, page):
        page.evaluate("() => document.dispatchEvent(new Event('visibilitychange'))")
        page.wait_for_timeout(250)

    def _dock_paint(self, page):
        return page.evaluate("""() => ({
          liveRows: document.querySelectorAll('.entryrow[aria-current="true"]').length,
          liveScreens: document.querySelectorAll('.screenerow[aria-current="true"]').length,
          block: !document.getElementById('offBlock').hidden,
          eye: document.getElementById('blankBtn').title,
          read: window.gkpsDisplay.read(),
          chip: document.getElementById('transChip').hidden
        })""")

    def _projector_paint(self, page):
        return page.evaluate("""() => ({
          active: document.querySelectorAll('.screen.is-active').length,
          showing: document.body.dataset.showing,
          detour: !!document.querySelector('.projector-detour.is-active')
        })""")

    # ---------- US1: the dock stops claiming what it can no longer see ----------

    def test_a_focused_dock_stops_painting_a_refused_state(self):
        context = self._context()
        dock = self._dock(context)
        self._project(dock, 1)
        painted = self._dock_paint(dock)
        self.assertEqual(painted['liveRows'], 1)
        self.assertEqual(painted['eye'], 'Hide words')

        context.clear_cookies()                 # the browser session ends
        self.assertEqual(dock.evaluate("() => window.gkpsDisplay.read().service"), None,
                         'the module did not refuse the state')
        self.assertEqual(self._dock_paint(dock)['liveRows'], 1,
                         'the stale paint is the defect; this assertion is the premise')

        self._focus(dock)
        after = self._dock_paint(dock)
        self.assertEqual(after['liveRows'], 0)
        self.assertEqual(after['liveScreens'], 0)
        self.assertFalse(after['block'])
        self.assertEqual(after['eye'], 'Display this service')
        self.assertIsNone(after['read']['service'])
        context.close()

    def test_a_visibility_change_stops_painting_a_refused_state(self):
        context = self._context()
        dock = self._dock(context)
        self._project(dock, 1)
        context.clear_cookies()
        self._visibility(dock)
        after = self._dock_paint(dock)
        self.assertEqual(after['liveRows'], 0)
        self.assertEqual(after['eye'], 'Display this service')
        context.close()

    def test_a_refused_state_leaves_every_control_idle(self):
        context = self._context()
        dock = self._dock(context)
        self._project(dock, 1)
        context.clear_cookies()
        self._focus(dock)
        controls = dock.evaluate("""() => ({
          eyePressed: document.getElementById('blankBtn').getAttribute('aria-pressed'),
          prev: document.getElementById('prevBtn').disabled,
          next: document.getElementById('nextBtn').disabled,
          chip: document.getElementById('transChip').hidden,
          switchDisabled: document.getElementById('switchBtn').disabled
        })""")
        self.assertEqual(controls['eyePressed'], 'true')
        self.assertTrue(controls['prev'])
        self.assertTrue(controls['next'])
        self.assertTrue(controls['chip'])
        self.assertFalse(controls['switchDisabled'])
        context.close()

    def test_the_projector_stops_painting_a_refused_state(self):
        context = self._context()
        dock = self._dock(context)
        projector = context.new_page()
        projector.set_default_timeout(6000)
        projector.goto(self.live_server_url + '/projector?service=' + str(self.service.pk))
        projector.wait_for_timeout(600)
        self._project(dock, 1)
        projector.wait_for_function(
            "() => document.querySelectorAll('.screen.is-active').length === 1")
        self.assertEqual(self._projector_paint(projector)['showing'], 'true')

        context.clear_cookies()
        self._focus(projector)
        after = self._projector_paint(projector)
        self.assertEqual(after['active'], 0, 'a screen was still active after the session ended')
        self.assertEqual(after['showing'], 'false')
        context.close()

    # ---------- US2: one read, and nothing repainted without a change ----------

    def test_a_focus_with_the_state_unchanged_repaints_nothing(self):
        context = self._context()
        dock = self._dock(context)
        self._project(dock, 1)
        dock.evaluate("""() => {
          window.__mutations = 0;
          const list = document.getElementById('entryList');
          window.__observer = new MutationObserver(records => {
            window.__mutations += records.length;
          });
          window.__observer.observe(list, {childList: true, subtree: true,
                                           attributes: true, characterData: true});
        }""")
        for _ in range(3):
            self._focus(dock)
            self._visibility(dock)
        self.assertEqual(dock.evaluate("() => window.__mutations"), 0,
                         'a focus with nothing changed repainted the list')
        self.assertEqual(self._dock_paint(dock)['liveRows'], 1)
        context.close()

    def test_a_changed_reread_notifies_a_subscriber_once(self):
        context = self._context()
        dock = self._dock(context)
        self._project(dock, 1)
        dock.evaluate("() => { window.__notices = 0;"
                      " window.gkpsDisplay.subscribe(() => { window.__notices += 1; });"
                      # subscribe() hands the state over at once; the count starts after that.
                      " window.__notices = 0; }")
        context.clear_cookies()
        self._focus(dock)
        self.assertEqual(dock.evaluate("() => window.__notices"), 1)
        self._focus(dock)               # nothing changed this time
        self.assertEqual(dock.evaluate("() => window.__notices"), 1)
        context.close()

    def test_the_stored_shape_and_the_messages_are_unchanged(self):
        context = self._context()
        dock = self._dock(context)
        self._project(dock, 1)
        stored = json.loads(dock.evaluate("() => localStorage.getItem('gkps-display')"))
        self.assertEqual(sorted(stored),
                         sorted(['service', 'screen', 'on', 'translation', 'at', 'session', 'goto']))
        exports = dock.evaluate("() => Object.keys(window.gkpsDisplay).sort()")
        self.assertEqual(exports, sorted([
            'back', 'changed', 'channel', 'flip', 'goTo', 'hide', 'live', 'read', 'reread',
            'release', 'resume', 'screen', 'show', 'state', 'stepGoto', 'subscribe', 'update']))
        context.close()
