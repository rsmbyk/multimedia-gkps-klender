"""Spec 185 — the dock's Go To: a passage or a song on air without leaving the service.

The dock's runner opens a find band over itself, answers from the projector's own index,
writes one display state, and shows what is on air as the list's live block; Back puts
the service back exactly where it stood. Every assertion drives the real pages through
Playwright: the dock's own DOM, the stored state, and the two other surfaces.
"""

import json
import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.bible import models as bible
from multimedia.songs import models as songs
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
class DockGotoE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Go To', date=date(2026, 11, 8), is_active=True)
        for order, text in enumerate(
                ['Salam', 'Pujian', 'Firman', 'Doa'], 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                order_number=order, title=text, text=f'{text} umat Tuhan')

        self.songbook = songs.Book.objects.create(
            name='Nyanyian Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.song = songs.Song.objects.create(
            book=self.songbook, number=43, title='Sinar Matahari Pagi')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Sinar matahari pagi')
        songs.Verse.objects.create(song=self.song, number=2, lyric='Bersyukurlah selalu')

        indonesian = bible.Language.objects.create(name='Indonesia')
        simalungun = bible.Language.objects.create(name='Simalungun')
        tb = bible.Version.objects.create(lang=indonesian, name='Terjemahan Baru',
                                          abbreviation='TB')
        sim = bible.Version.objects.create(lang=simalungun, name='Simalungun',
                                           abbreviation='SIM')
        book = bible.Book.objects.create(name='Mat', testament='new',
                                         number_of_chapters=28)
        self.tb = bible.BookTranslation.objects.create(
            version=tb, book=book, translation='Matius')
        self.sim = bible.BookTranslation.objects.create(
            version=sim, book=book, translation='Mateus')
        for number, text in ((1, 'Ketika Yesus melihat orang banyak itu,'),
                             (2, 'dan Ia membuka mulut-Nya serta mengajar mereka,'),
                             (3, 'kata-Nya: Berbahagialah orang yang miskin di hadapan Allah.'),
                             (4, 'Berbahagialah orang yang berdukacita,'),
                             (5, 'karena mereka akan dihibur.')):
            bible.Verse.objects.create(book_translation=self.tb, chapter=5, verse=number,
                                       text=text)
            bible.Verse.objects.create(book_translation=self.sim, chapter=5, verse=number,
                                       text='SIM ' + text)

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

    def _context(self, width=420):
        return self.browser.new_context(viewport={'width': width, 'height': 800})

    def _dock(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector(f'.servicerow[data-service="{self.service.pk}"]')
        page.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        page.wait_for_selector('.entryrow')
        return page

    def _state(self, page):
        return page.evaluate(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")

    def _goto(self, page):
        return (self._state(page) or {}).get('goto')

    def _open_band(self, page):
        page.bring_to_front()
        page.keyboard.press('g')
        page.wait_for_selector('.bandswap.is-find')

    def _choose(self, page, query):
        self._open_band(page)
        page.fill('#findInput', query)
        page.wait_for_timeout(350)
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        page.wait_for_timeout(250)

    def _block(self, page):
        return page.evaluate("""() => ({
          shown: !document.getElementById('offBlock').hidden,
          label: document.getElementById('offLabel').textContent,
          rows: document.querySelectorAll('#offBody .offrow').length,
          listHidden: document.getElementById('entryList').hidden,
          switchDisabled: document.getElementById('switchBtn').disabled,
          band: document.querySelector('.bandswap').classList.contains('is-find'),
          liveEntries: document.querySelectorAll('.entryrow[aria-current="true"]').length,
          pills: [...document.querySelectorAll('.onscreen')].filter(p => !p.hidden).length
        })""")

    # ---------- US1: the dock puts something on air ---------------------------

    def test_g_opens_the_band_and_the_picker_has_no_goto(self):
        context = self._context()
        dock = self._dock(context)
        self.assertEqual(dock.locator('#viewPick #findBtn').count(), 0,
                         'the picker offered a Go To')
        self._open_band(dock)
        dock.wait_for_function(
            """() => {
                 const scrim = document.getElementById('findScrim');
                 return !scrim.hidden && Number(getComputedStyle(scrim).opacity) > 0;
               }""")
        dock.wait_for_function(
            "() => document.getElementById('findLabel').textContent"
            " === 'Start typing to find a match'")
        box = dock.evaluate("""() => ({
          scrim: (() => { const s = document.getElementById('findScrim');
                          return !s.hidden && getComputedStyle(s).opacity !== '0'; })(),
          count: document.getElementById('findCount').textContent,
          label: document.getElementById('findLabel').textContent,
          focused: document.activeElement === document.getElementById('findInput')
        })""")
        self.assertTrue(box['scrim'], 'the layer is not over the dock')
        self.assertEqual(box['count'], '0 / 0')
        self.assertEqual(box['label'], 'Start typing to find a match')
        self.assertTrue(box['focused'], 'the field does not hold the focus')
        context.close()

    def test_typing_makes_no_request(self):
        context = self._context()
        dock = self._dock(context)
        requests = []
        dock.on('request', lambda request: requests.append(request.url))
        self._open_band(dock)
        dock.wait_for_selector('.findresult__label', timeout=6000)
        dock.wait_for_function(
            "() => document.getElementById('findLabel').textContent !== 'Loading search…'")
        settled = len(requests)
        dock.locator('#findInput').type('NKB 4', delay=40)
        dock.wait_for_timeout(350)
        typed = [url for url in requests[settled:] if '/projector/goto/' in url]
        self.assertEqual(typed, [], 'typing fetched something')
        self.assertEqual(dock.evaluate(
            "() => document.getElementById('findLabel').textContent"),
            'NKB 43 Sinar Matahari Pagi')
        context.close()

    def test_no_match_says_so_and_enter_does_nothing(self):
        context = self._context()
        dock = self._dock(context)
        self._open_band(dock)
        dock.wait_for_function(
            "() => document.getElementById('findLabel').textContent !== 'Loading search…'")
        dock.fill('#findInput', 'zzzz')
        dock.wait_for_timeout(300)
        self.assertEqual(dock.evaluate(
            "() => document.getElementById('findLabel').textContent"),
            'No matching passage or song')
        self.assertTrue(dock.evaluate(
            "() => document.getElementById('findResult').disabled"))
        dock.keyboard.press('Enter')
        dock.wait_for_timeout(200)
        self.assertIsNone(self._goto(dock))
        context.close()

    def test_choosing_fetches_once_and_steps_stay_local(self):
        context = self._context()
        dock = self._dock(context)
        requests = []
        dock.on('request', lambda request: requests.append(request.url))
        self._open_band(dock)
        dock.wait_for_function(
            "() => document.getElementById('findLabel').textContent !== 'Loading search…'")
        dock.fill('#findInput', 'NKB 43')
        dock.wait_for_timeout(300)
        dock.keyboard.press('Enter')
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        songs_requested = [url for url in requests if '/projector/goto/song/' in url]
        self.assertEqual(len(songs_requested), 1, songs_requested)
        before = len(requests)
        dock.locator('#nextBtn').click()
        dock.wait_for_timeout(400)
        self.assertEqual([url for url in requests[before:] if '/projector/goto/' in url],
                         [], 'a step fetched something')
        self.assertEqual(self._state(dock)['goto']['index'], 1)
        context.close()

    def test_the_block_replaces_the_service_rows(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'NKB 43')
        block = self._block(dock)
        self.assertTrue(block['shown'])
        self.assertEqual(block['label'], 'NKB 43 Sinar Matahari Pagi')
        self.assertEqual(block['rows'], 4, block)     # two lyrics and two rests
        self.assertTrue(block['listHidden'], 'the service rows were still drawn')
        self.assertEqual(block['liveEntries'], 0, 'a service row still wore the live tint')
        self.assertEqual(block['pills'], 0, 'a picker pill was still drawn')
        context.close()

    def test_the_layer_closes_on_escape_click_and_empty_backspace(self):
        context = self._context()
        dock = self._dock(context)
        for gesture in ('escape', 'click', 'backspace'):
            self._open_band(dock)
            if gesture == 'escape':
                dock.keyboard.press('Escape')
            elif gesture == 'click':
                dock.locator('#findScrim').click(position={'x': 30, 'y': 200})
            else:
                dock.locator('#findInput').fill('')
                dock.keyboard.press('Backspace')
            dock.wait_for_function(
                "() => !document.querySelector('.bandswap').classList.contains('is-find')",
                timeout=4000)
            self.assertFalse(self._block(dock)['band'], gesture)
            self.assertIsNone(self._goto(dock), gesture)
            self.assertEqual(dock.evaluate(
                "() => document.getElementById('findCount').textContent"), '0 / 0', gesture)
        context.close()

    # ---------- US3: Back restores the service exactly ------------------------

    def test_back_restores_the_service_screen_and_edition(self):
        context = self._context()
        dock = self._dock(context)
        dock.locator('.entryrow').nth(2).click()
        dock.wait_for_timeout(400)
        placed = self._state(dock)['screen']
        self._choose(dock, 'Matius 5:3')
        dock.locator('#nextBtn').click()
        dock.wait_for_timeout(300)
        dock.keyboard.press('t')
        dock.wait_for_timeout(300)
        during = self._state(dock)
        self.assertEqual(during['goto']['translation'], 'SIM')
        self.assertEqual(during['screen'], placed, 'the service moved under the go to')
        dock.locator('#offBack').click()
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && !s.goto); }")
        dock.wait_for_timeout(250)
        after = self._state(dock)
        self.assertEqual(after['screen'], placed)
        self.assertIsNone(after['translation'])
        block = self._block(dock)
        self.assertFalse(block['shown'])
        self.assertGreater(block['rows'], 0)
        context.close()

    def test_the_transport_steps_the_goto_not_the_service(self):
        context = self._context()
        dock = self._dock(context)
        dock.locator('.entryrow').nth(1).click()
        dock.wait_for_timeout(300)
        start = self._state(dock)
        self._choose(dock, 'NKB 43')
        dock.locator('#nextBtn').click()
        dock.wait_for_timeout(300)
        stepped = self._state(dock)
        self.assertEqual(stepped['goto']['index'], 1)
        self.assertEqual(stepped['screen'], start['screen'], 'the service was stepped too')
        context.close()

    def test_switch_service_is_disabled_while_a_goto_is_up(self):
        context = self._context()
        dock = self._dock(context)
        self.assertFalse(self._block(dock)['switchDisabled'])
        self._choose(dock, 'NKB 43')
        self.assertTrue(self._block(dock)['switchDisabled'])
        dock.locator('#offBack').click()
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && !s.goto); }")
        dock.wait_for_timeout(200)
        self.assertFalse(self._block(dock)['switchDisabled'])
        context.close()

    def test_a_block_row_moves_the_goto_and_show_ends_it(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'NKB 43')
        dock.locator('#offBody .offrow').nth(2).click()
        dock.wait_for_timeout(300)
        self.assertEqual(self._state(dock)['goto']['index'], 2)
        dock.evaluate("service => window.gkpsDisplay.show(service, 0)", self.service.pk)
        dock.wait_for_timeout(300)
        state = self._state(dock)
        self.assertIsNone(state['goto'])
        self.assertEqual(state['screen'], 0)
        context.close()

    def test_a_goto_can_start_with_nothing_on_air(self):
        context = self._context()
        dock = self._dock(context)
        self.assertIsNone(self._state(dock))
        self._choose(dock, 'NKB 43')
        state = self._state(dock)
        self.assertEqual(state['service'], self.service.pk)
        self.assertEqual(state['screen'], 0)
        self.assertTrue(state['on'])
        self.assertEqual(state['goto']['song_id'], self.song.pk)
        context.close()

    def test_show_ends_the_goto_and_flip_names_what_is_on_air(self):
        context = self._context()
        dock = self._dock(context)
        dock.locator('.entryrow').first.click()
        dock.wait_for_timeout(300)
        self._choose(dock, 'Matius 5:3')
        self.assertEqual(self._state(dock)['goto']['translation'], 'TB')
        dock.keyboard.press('t')
        dock.wait_for_timeout(300)
        flipped = self._state(dock)
        self.assertEqual(flipped['goto']['translation'], 'SIM')
        self.assertIsNone(flipped['translation'], 'the service took the go to\'s edition')
        dock.evaluate("service => window.gkpsDisplay.show(service, 1)", self.service.pk)
        dock.wait_for_timeout(300)
        ended = self._state(dock)
        self.assertIsNone(ended['goto'])
        self.assertEqual(ended['screen'], 1)
        context.close()

    def test_the_same_lookup_answers_both_surfaces(self):
        context = self._context()
        dock = self._dock(context)
        self._open_band(dock)
        dock.wait_for_function(
            "() => document.getElementById('findLabel').textContent !== 'Loading search…'")
        queries = ('NKB 43', 'Matius 5', '43')
        dock_labels = dock.evaluate("""queries => queries.map(q => ({
          q: q, rows: window.GKPSProjectorLibrary.lookup(q).map(r => r.label) }))""",
          list(queries))
        projector = context.new_page()
        projector.goto(self.live_server_url + '/projector?service=' + str(self.service.pk))
        projector.wait_for_function("() => window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready()")
        projector_labels = projector.evaluate(
            """queries => queries.map(q => ({
                 q: q, rows: window.GKPSProjectorLibrary.lookup(q).map(r => r.label) }))""",
            list(queries))
        self.assertEqual(dock_labels, projector_labels)
        context.close()
