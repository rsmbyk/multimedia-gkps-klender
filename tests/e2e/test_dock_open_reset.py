"""Spec 204 — opening a service starts its entry blocks shut.

A hand-opened block is page memory keyed by entry index. An explicit open of a service
(picker click, picker Enter, the on-load resume) ends every override, so the opened list
paints shut except the live entry's block. A crossing and a re-read are not opens and keep
what the operator opened (spec 198 R14, spec 195 R13).

Fixtures are created in setUp before the browser starts. The one mid-test write (the re-read
pin) runs in its own thread with the connection closed afterwards, and the update is posted
from a second tab — the pattern the projector suite uses.
"""

import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.test import override_settings, tag

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


STATE_KEY = 'gkps-display'
CHANNEL = 'gkps-service-display'


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockOpenResetE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.long = tatib.TataIbadah.objects.create(
            name='Ibadah Panjang', date=date(2026, 11, 15), is_active=True)
        for order in range(1, 13):
            kind = (tatib.ServiceEntryKind.SECTION_BREAK if order == 6
                    else tatib.ServiceEntryKind.TEXT)
            entry = tatib.ServiceEntry.objects.create(
                tatib=self.long, order_number=order, kind=kind,
                title=f'Entri {order}', text=f'Baris pertama entri {order}')
            if order == 2:
                self.entry_two_pk = entry.pk
        self.short = tatib.TataIbadah.objects.create(
            name='Ibadah Pendek', date=date(2026, 11, 8), is_active=True)
        for order in range(1, 6):
            tatib.ServiceEntry.objects.create(
                tatib=self.short, order_number=order, kind=tatib.ServiceEntryKind.TEXT,
                title=f'Pendek {order}', text=f'Baris pendek {order}')
        self.empty = tatib.TataIbadah.objects.create(
            name='Ibadah Kosong', date=date(2026, 11, 1), is_active=True)

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

    def _dock(self):
        context = self.browser.new_context(viewport={'width': 420, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + '/obs/dock', wait_until='domcontentloaded')
        page.wait_for_selector('.servicerow')
        return page

    def _view(self, page):
        return page.evaluate("() => document.getElementById('dockPanel').dataset.view")

    def _open(self, page, name):
        """An explicit open through the picker, settled past the toggle morph."""
        if self._view(page) != 'pick':
            page.locator('#switchBtn').click()
            page.wait_for_selector('#viewPick.is-active')
        page.locator(f'.servicerow[data-name="{name}"]').first.click()
        page.wait_for_function(
            "() => document.getElementById('dockPanel').dataset.view === 'run'")
        page.wait_for_timeout(650)

    def _header(self, page, index):
        page.locator(f'.entryli[data-index="{index}"] .entryrow').click()
        page.wait_for_function(
            """index => {
                const inner = document.querySelector(
                    '.entryli[data-index="' + index + '"] .entryinner');
                return inner && !inner.classList.contains('is-morph');
            }""", arg=index)
        page.wait_for_timeout(120)

    def _project(self, page, index):
        """The item inside is the jump target: expand, then click its first screen row."""
        inner = page.locator(f'#entryinner-{index}')
        if not inner.evaluate("el => el.classList.contains('is-open')"):
            self._header(page, index)
        page.locator(f'.entryli[data-index="{index}"] .screenerow').first.click()
        page.wait_for_function(
            """index => {
                const li = document.querySelector('.entryli[data-index="' + index + '"]');
                return li && li.dataset.live === 'true';
            }""", arg=index)
        page.wait_for_timeout(650)

    def _opens(self, page):
        """What is PAINTED: open blocks, the non-live ones, and the live one."""
        return page.evaluate(
            """() => {
                const lis = [...document.querySelectorAll('#entryList .entryli')];
                const open = [], nonLive = [], live = [];
                lis.forEach(li => {
                    const inner = li.querySelector('.entryinner');
                    const i = Number(li.dataset.index);
                    if (li.dataset.live === 'true') live.push(i);
                    if (inner && inner.classList.contains('is-open')) {
                        open.push(i);
                        if (li.dataset.live !== 'true') nonLive.push(i);
                    }
                });
                return {open, nonLive, live, rows: lis.length};
            }""")

    def _block(self, page, index):
        return page.evaluate(
            """index => {
                const li = document.querySelector('.entryli[data-index="' + index + '"]');
                if (!li) return null;
                const row = li.querySelector('.entryrow');
                const inner = li.querySelector('.entryinner');
                return {expanded: row ? row.getAttribute('aria-expanded') : null,
                        current: row ? row.getAttribute('aria-current') : null,
                        open: !!inner && inner.classList.contains('is-open'),
                        height: inner ? Math.round(inner.getBoundingClientRect().height) : null,
                        chev: [...li.querySelectorAll('.entrychev')]
                                .filter(c => c.getClientRects().length).length};
            }""", index)

    def _raw(self, page):
        return page.evaluate("() => localStorage.getItem('gkps-display') || 'null'")

    def _listen(self, page):
        page.evaluate(
            """() => { window.__msgs = [];
                const c = new BroadcastChannel('gkps-service-display');
                c.onmessage = e => window.__msgs.push(e.data); }""")

    def _scroll(self, page):
        return page.evaluate("() => Math.round(document.getElementById('runBody').scrollTop)")

    def _mark(self, page, service_id):
        """Walk the picker's cursor to a service with the dock's own keys."""
        for _ in range(20):
            cur = page.evaluate(
                "() => (document.querySelector('.servicerow.is-cursor') || {}).dataset?.service")
            if str(cur) == str(service_id):
                return True
            page.keyboard.press('ArrowDown')
            page.wait_for_timeout(90)
        return False

    # ---------- US1: an open starts every block shut but the live one ----------

    def test_an_open_starts_every_block_shut_in_another_service(self):
        """US1/AC1, FR-001, FR-003 (click), SC-001."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._header(page, 3)
        self.assertEqual(self._opens(page)['nonLive'], [3], 'the hand-open did not take')
        self._open(page, 'Ibadah Pendek')
        state = self._opens(page)
        self.assertEqual(state['nonLive'], [],
                         'a block carried over to the same position of another service')
        self.assertEqual(state['open'], [])
        for index in range(state['rows']):
            block = self._block(page, index)
            self.assertEqual(block['expanded'], 'false')
            self.assertEqual(block['height'], 0)

    def test_reopening_the_same_service_starts_every_block_shut(self):
        """US1/AC2, SC-002 — the open is a fresh start, not a return."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._header(page, 3)
        self.assertEqual(self._opens(page)['nonLive'], [3])
        self._open(page, 'Ibadah Panjang')
        self.assertEqual(self._opens(page)['nonLive'], [],
                         're-opening the same service kept the hand-opened block')

    def test_several_hand_opened_blocks_leak_nothing_into_a_shorter_service(self):
        """US1/AC3, SC-003 — every position, not only the ones the new list has."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        for index in (1, 3, 8):
            self._header(page, index)
        self.assertEqual(self._opens(page)['nonLive'], [1, 3, 8])
        self._open(page, 'Ibadah Pendek')
        self.assertEqual(self._opens(page)['open'], [],
                         'hand-opened positions leaked into the shorter service')

    def test_the_live_entrys_block_stays_open_when_its_service_is_opened(self):
        """US1/AC4, FR-002, SC-004 — the exception is liveness, not a remembered index."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._project(page, 3)
        self._open(page, 'Ibadah Pendek')
        self.assertEqual(self._opens(page)['open'], [], 'a browsed service inherited a live block')
        self._open(page, 'Ibadah Panjang')
        state = self._opens(page)
        self.assertEqual(state['live'], [3])
        self.assertEqual(state['open'], [3], 'the live block did not stay open')
        self.assertEqual(state['nonLive'], [])
        block = self._block(page, 3)
        self.assertEqual(block['current'], 'true')
        self.assertEqual(block['chev'], 0, 'the live row renders a chevron')
        self.assertGreater(block['height'], 0)

    def test_a_browsed_service_has_no_open_block_while_another_is_on_air(self):
        """US1/AC5 — nothing is live in the browsed service, so nothing is open."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._project(page, 3)
        self._open(page, 'Ibadah Pendek')
        state = self._opens(page)
        self.assertEqual(state['live'], [])
        self.assertEqual(state['open'], [])
        self.assertEqual(self._raw(page).find(str(self.long.pk)) > 0, True,
                         'the open changed what is on air')

    def test_the_keyboard_open_resets_like_a_click(self):
        """US1/AC6, FR-003 (Enter) — the picker's keyboard path is the same open."""
        page = self._dock()
        self.assertTrue(self._mark(page, self.long.pk), 'the cursor never reached the service')
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => document.getElementById('dockPanel').dataset.view === 'run'")
        page.wait_for_timeout(650)
        self._header(page, 3)
        self.assertEqual(self._opens(page)['nonLive'], [3])
        page.locator('#switchBtn').click()
        page.wait_for_selector('#viewPick.is-active')
        self.assertTrue(self._mark(page, self.short.pk))
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => document.getElementById('dockPanel').dataset.view === 'run'")
        page.wait_for_timeout(650)
        self.assertEqual(self._opens(page)['open'], [], 'the Enter open kept the override')

    def test_the_on_load_open_keeps_only_the_live_block(self):
        """US1/AC6, FR-003 (resume) — a reload opens the on-air service through the same path."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._project(page, 3)
        self._header(page, 8)
        self.assertEqual(self._opens(page)['nonLive'], [8])
        page.reload()
        page.wait_for_function(
            "() => document.getElementById('dockPanel').dataset.view === 'run'")
        page.wait_for_timeout(800)
        state = self._opens(page)
        self.assertEqual(state['live'], [3], 'the reload did not resume the on-air service')
        self.assertEqual(state['open'], [3])
        self.assertEqual(state['nonLive'], [], 'a hand-opened block survived the reload')

    # ---------- US2: what an open must not reset ----------

    def test_a_reread_keeps_a_hand_opened_block_open(self):
        """US2/AC2, FR-003 (not a re-read), SC-005 — a saved change is not an open."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._project(page, 0)
        for index in (3, 8):
            self._header(page, index)
        before = self._opens(page)
        scroll = self._scroll(page)
        self.assertEqual(before['nonLive'], [3, 8])
        page.evaluate(
            """() => { window.__rebuilds = 0;
                new MutationObserver(ms => ms.forEach(m => {
                    if (m.type === 'childList') window.__rebuilds++;
                })).observe(document.getElementById('entryList'), {childList: true}); }""")

        # A real saved change, so the re-read rebuilds instead of taking the unchanged-list
        # shortcut: written in its own thread with the connection closed afterwards. The pk
        # was read in setUp, before the browser started — an ORM read here would run inside
        # Playwright's event loop.
        entry_id = self.entry_two_pk
        with ThreadPoolExecutor(max_workers=1) as pool:
            def edit():
                try:
                    tatib.ServiceEntry.objects.filter(pk=entry_id).update(
                        text='Baris pertama entri 2 — disunting')
                finally:
                    connections.close_all()
            pool.submit(edit).result()
        sender = page.context.new_page()
        sender.goto(self.live_server_url + '/api/')
        sender.evaluate(
            """() => { const c = new BroadcastChannel('gkps-service-display');
                c.postMessage({type: 'update'}); c.close(); }""")
        sender.close()
        page.wait_for_function("() => window.__rebuilds > 0", timeout=15000)
        page.wait_for_timeout(600)
        after = self._opens(page)
        self.assertEqual(after['nonLive'], before['nonLive'],
                         'a re-read shut the blocks the operator opened')
        self.assertEqual(after['live'], before['live'])
        self.assertEqual(self._scroll(page), scroll, 'a re-read moved the list')

    # ---------- US3: the reset is silent ----------

    def test_an_open_writes_no_display_state_and_broadcasts_nothing(self):
        """US3/AC2, FR-005, SC-006 — the reset touches no state and sends no message."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._project(page, 3)
        self._listen(page)
        before = self._raw(page)
        self._open(page, 'Ibadah Pendek')
        self.assertEqual(self._raw(page), before, 'an open wrote the display state')
        self._open(page, 'Ibadah Panjang')
        self.assertEqual(self._raw(page), before, 'an open wrote the display state')
        self.assertEqual(page.evaluate("() => window.__msgs.length"), 0,
                         'an open broadcast on the display channel')

    def test_an_open_paints_no_morph_in_the_new_list(self):
        """US3/AC1, FR-005, SC-006 — the list is drawn shut, not animated shut."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        for index in (1, 3, 8):
            self._header(page, index)
        page.locator('#switchBtn').click()
        page.wait_for_selector('#viewPick.is-active')
        page.locator('.servicerow[data-name="Ibadah Pendek"]').first.click()
        samples = page.evaluate(
            """() => new Promise(resolve => {
                const out = []; const t0 = performance.now();
                const body = document.getElementById('runBody');
                function tick() {
                    out.push({t: Math.round(performance.now() - t0),
                              morph: document.querySelectorAll(
                                  '#entryList .entryinner.is-morph').length,
                              scroll: Math.round(body.scrollTop)});
                    if (performance.now() - t0 < 600) requestAnimationFrame(tick);
                    else resolve(out);
                }
                requestAnimationFrame(tick);
            })""")
        self.assertTrue(samples, 'no frames were sampled')
        self.assertEqual(sum(1 for s in samples if s['morph'] > 0), 0,
                         'the opened list animated a block shut')
        self.assertEqual(max(s['scroll'] for s in samples), 0,
                         'the open moved the list')
        self.assertEqual(self._opens(page)['open'], [])

    def test_an_empty_service_opens_without_a_block_or_an_error(self):
        """Edge case: nothing to reset, nothing to draw."""
        page = self._dock()
        self._open(page, 'Ibadah Panjang')
        self._header(page, 3)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        self._open(page, 'Ibadah Kosong')
        state = self._opens(page)
        self.assertEqual(state['rows'], 0)
        self.assertEqual(state['open'], [])
        self.assertEqual(errors, [])
