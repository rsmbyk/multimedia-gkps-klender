"""Spec 187 — the dock's own keyboard, at parity with the projector's.

One grammar for both surfaces: the held `Esc`, `G` on the picker, a go to that stands
with no service, the projector's go-to steps and unit boundaries, `K` for the dock's
sheet, the fetch guard, and a band that keeps the keyboard when the window returns.

Every assertion drives the real `/obs/dock` page through Playwright and reads the stored
display state, the dock's DOM, or the requests the page made — never a mock.
"""

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


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DockKeyboardE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        # The runner's service: one long text, one song with two baits, one short text.
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Keyboard', date=date(2026, 11, 8), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Salam', text='Salam sejahtera bagi kita semua.\n\n'
                                'Kasih karunia Tuhan beserta kita.\n\n'
                                'Marilah kita beribadah kepada Tuhan.')
        self.songbook = songs.Book.objects.create(
            name='Nyanyian Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.song = songs.Song.objects.create(
            book=self.songbook, number=43, title='Sinar Matahari Pagi')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Sinar matahari pagi')
        songs.Verse.objects.create(song=self.song, number=2, lyric='Bersyukurlah selalu')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, order_number=2,
            song=self.song, verses=[1, 2])
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=3,
            title='Doa', text='Tuhan, dengarkanlah doa kami.\n\nAmin.')

        # Two more services, so the picker's mark has somewhere to move.
        for days, name in ((7, 'Ibadah Dua'), (6, 'Ibadah Tiga')):
            tatib.TataIbadah.objects.create(
                name=name, date=date(2026, 11, days), is_active=True)

        indonesian = bible.Language.objects.create(name='Indonesia')
        simalungun = bible.Language.objects.create(name='Simalungun')
        tb = bible.Version.objects.create(lang=indonesian, name='Terjemahan Baru',
                                          abbreviation='TB')
        sim = bible.Version.objects.create(lang=simalungun, name='Simalungun',
                                           abbreviation='SIM')
        matius = bible.Book.objects.create(name='Mat', testament='new',
                                           number_of_chapters=28)
        self.tb = bible.BookTranslation.objects.create(
            version=tb, book=matius, translation='Matius')
        bible.BookTranslation.objects.create(
            version=sim, book=matius, translation='Mateus')
        markus = bible.Book.objects.create(name='Mrk', testament='new',
                                           number_of_chapters=16)
        bible.BookTranslation.objects.create(
            version=tb, book=markus, translation='Markus')
        for chapter in (5, 6):
            for number in (1, 2, 3):
                bible.Verse.objects.create(
                    book_translation=self.tb, chapter=chapter, verse=number,
                    text=f'Matius {chapter}:{number}')
        markus_tb = bible.BookTranslation.objects.get(version=tb, book=markus)
        for number in (1, 2):
            bible.Verse.objects.create(
                book_translation=markus_tb, chapter=1, verse=number,
                text=f'Markus 1:{number}')

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

    def _context(self):
        return self.browser.new_context(viewport={'width': 420, 'height': 900})

    def _dock(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector(f'.servicerow[data-service="{self.service.pk}"]')
        page.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        page.wait_for_selector('.entryrow')
        page.wait_for_function(
            "() => document.querySelectorAll('.entryrow').length >= 3")
        return page

    def _picker(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector('.servicerow')
        return page

    def _state(self, page):
        return page.evaluate(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")

    def _view(self, page):
        return page.evaluate("() => document.getElementById('dockPanel').dataset.view")

    def _open_band(self, page):
        page.bring_to_front()
        page.keyboard.press('g')
        page.wait_for_selector('.bandswap.is-find')
        page.wait_for_function(
            "() => document.getElementById('findLabel').textContent"
            " !== 'Loading search…'")

    def _choose(self, page, query):
        self._open_band(page)
        page.fill('#findInput', query)
        page.wait_for_timeout(350)
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        page.wait_for_timeout(250)

    def _block_rows(self, page):
        return page.evaluate(
            "() => [...document.querySelectorAll('#offBody .offrow')]"
            ".map(r => Number(r.dataset.pos))")

    def _go_to(self, page):
        return page.evaluate(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s ? s.goto : null; }")

    # ---------- US1: the held Esc --------------------------------------------

    def test_a_tap_of_escape_moves_nothing_and_a_hold_returns_to_the_picker(self):
        context = self._context()
        dock = self._dock(context)
        dock.keyboard.down('Escape')
        dock.wait_for_timeout(300)
        dock.keyboard.up('Escape')
        dock.wait_for_timeout(120)
        self.assertEqual(self._view(dock), 'run', 'a 300 ms tap left the runner')

        dock.keyboard.down('Escape')
        dock.wait_for_timeout(1000)
        dock.keyboard.up('Escape')
        dock.wait_for_timeout(120)
        self.assertEqual(self._view(dock), 'pick', 'a 1000 ms hold did not return')
        self.assertTrue(dock.locator('#viewPick.is-active').count(),
                        'the picker is not the active view')
        context.close()

    def test_escape_closes_the_sheet_and_the_band_on_the_tap(self):
        context = self._context()
        dock = self._dock(context)
        dock.keyboard.press('k')
        dock.wait_for_function("() => !document.getElementById('keysheet').hidden")
        dock.keyboard.press('Escape')
        dock.wait_for_function("() => document.getElementById('keysheet').hidden")
        self.assertEqual(self._view(dock), 'run')

        self._open_band(dock)
        dock.keyboard.press('Escape')
        dock.wait_for_function(
            "() => !document.querySelector('.bandswap').classList.contains('is-find')")
        self.assertEqual(self._view(dock), 'run')
        context.close()

    # ---------- US2: G on the picker, and a go to that stands alone ----------

    def test_g_opens_the_band_on_the_picker(self):
        context = self._context()
        dock = self._picker(context)
        self.assertEqual(self._view(dock), 'pick')
        dock.bring_to_front()
        dock.keyboard.press('g')
        dock.wait_for_selector('.bandswap.is-find')
        dock.wait_for_function(
            "() => document.activeElement === document.getElementById('findInput')")
        focused = True
        self.assertTrue(focused, 'the field does not hold the focus over the picker')
        context.close()

    def test_the_picker_go_to_stands_alone_and_back_returns_to_the_picker(self):
        context = self._context()
        dock = self._picker(context)
        self._choose(dock, 'NKB 43')
        state = self._state(dock)
        self.assertIsNone(state['service'], 'the picker adopted a service')
        self.assertEqual(state['goto']['kind'], 'song')
        self.assertEqual(self._view(dock), 'run', 'the dock did not show the block')

        block = dock.evaluate("""() => ({
          shown: !document.getElementById('offBlock').hidden,
          label: document.getElementById('offLabel').textContent,
          head: document.getElementById('runService').textContent,
          dateShown: getComputedStyle(document.getElementById('runDate')).display,
          switchDisabled: document.getElementById('switchBtn').disabled
        })""")
        self.assertTrue(block['shown'], 'the go to block is not drawn')
        self.assertEqual(block['label'], 'NKB 43 Sinar Matahari Pagi')
        self.assertEqual(block['head'], 'Go To')
        self.assertEqual(block['dateShown'], 'none')
        self.assertFalse(block['switchDisabled'], 'the exit to the picker is disabled')

        dock.locator('#offBack').click()
        dock.wait_for_function(
            "() => !JSON.parse(localStorage.getItem('gkps-display') || 'null').goto")
        state = self._state(dock)
        self.assertIsNone(state['service'])
        self.assertFalse(state['on'], 'Back left something on air')
        dock.wait_for_timeout(120)
        self.assertEqual(self._view(dock), 'pick', 'Back did not return to the picker')
        context.close()

    def test_the_runner_band_still_adopts_the_browsed_service(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'NKB 43')
        state = self._state(dock)
        self.assertEqual(state['service'], self.service.pk,
                         'the runner band stopped adopting the browsed service')
        self.assertEqual(state['goto']['kind'], 'song')
        context.close()

    # ---------- US12: a refresh lands where the operator is -------------------

    def test_a_refresh_opens_the_service_on_air(self):
        context = self._context()
        dock = self._dock(context)
        dock.locator('.entryrow').nth(1).click()
        dock.wait_for_timeout(200)
        live = self._state(dock)['screen']
        dock.reload()
        dock.wait_for_selector('.entryrow')
        dock.wait_for_timeout(300)
        self.assertEqual(self._view(dock), 'run', 'the refresh fell back to the picker')
        self.assertEqual(
            dock.evaluate("() => document.getElementById('runService').textContent"),
            'Ibadah Keyboard')
        self.assertEqual(self._state(dock)['screen'], live,
                         'opening the service moved what is on air')
        context.close()

    def test_a_refresh_with_nothing_on_air_keeps_the_picker(self):
        context = self._context()
        dock = self._picker(context)
        dock.reload()
        dock.wait_for_selector('.servicerow')
        dock.wait_for_timeout(250)
        self.assertEqual(self._view(dock), 'pick')
        context.close()

    def test_a_refresh_brings_back_a_go_to_that_stands_alone(self):
        context = self._context()
        dock = self._picker(context)
        self._choose(dock, 'NKB 43')
        dock.reload()
        dock.wait_for_selector('.servicerow', state='attached')
        dock.wait_for_function(
            "() => !document.getElementById('offBlock').hidden")
        self.assertEqual(self._view(dock), 'run', 'the standing go to was not shown')
        self.assertEqual(
            dock.evaluate("() => document.getElementById('runService').textContent"),
            'Go To')
        self.assertEqual(
            dock.evaluate("() => document.getElementById('runDate')"
                          ".getBoundingClientRect().height"), 0)
        context.close()

    # ---------- US4: the picker's own two keys --------------------------------

    def test_the_picker_moves_on_up_and_down_only(self):
        context = self._context()
        dock = self._picker(context)

        def marked():
            return dock.evaluate(
                "() => [...document.querySelectorAll('.servicerow')]"
                ".findIndex(r => r.classList.contains('is-cursor'))")

        start = marked()
        self.assertGreaterEqual(start, 0)
        dock.keyboard.press('ArrowDown')
        dock.wait_for_timeout(80)
        moved = marked()
        self.assertEqual(moved, start + 1)
        for key in ('ArrowRight', 'PageDown', 'End', 'ArrowLeft', 'PageUp', 'Home'):
            dock.keyboard.press(key)
            dock.wait_for_timeout(60)
            self.assertEqual(marked(), moved, f'{key} moved the pick')
        dock.keyboard.press('ArrowUp')
        dock.wait_for_timeout(80)
        self.assertEqual(marked(), start)
        context.close()

    # ---------- US5: the shortcut sheet ---------------------------------------

    def _sheet(self, page):
        return page.evaluate("""() => {
          const sheet = document.getElementById('keysheet');
          const groups = [...sheet.querySelectorAll('.ksgroup')];
          return {
            hidden: sheet.hidden,
            rows: sheet.querySelectorAll('.ksgroup:not([hidden]) .krow').length,
            groups: groups.length,
            visibleGroups: groups.filter(g => !g.hidden).length,
            titles: groups.filter(g => !g.hidden)
                          .map(g => g.querySelector('h4').textContent.trim()),
            labels: [...sheet.querySelectorAll('.ksgroup:not([hidden]) .kfn')]
                      .map(l => l.textContent.trim()),
            overflow: sheet.querySelector('.keysheet__panel').scrollWidth
                      > sheet.querySelector('.keysheet__panel').clientWidth
          };
        }""")

    def test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view(self):
        context = self._context()
        dock = self._dock(context)
        dock.keyboard.press('k')
        dock.wait_for_function("() => !document.getElementById('keysheet').hidden")
        runner = self._sheet(dock)
        self.assertEqual(runner['rows'], 32, runner['labels'])
        self.assertEqual(runner['groups'], 6)
        self.assertEqual(runner['visibleGroups'], 5)
        self.assertEqual(runner['titles'],
                         ['Service', 'Song', 'Passage', 'Display', 'Find'])
        self.assertNotIn('Move the Pick', runner['labels'])
        self.assertIn('Back to Services (hold)', runner['labels'])
        self.assertFalse(runner['overflow'], 'the sheet overflows its panel')

        dock.keyboard.press('k')
        dock.wait_for_function("() => document.getElementById('keysheet').hidden")
        dock.locator('#switchBtn').click()
        dock.wait_for_function(
            "() => document.getElementById('dockPanel').dataset.view === 'pick'")
        dock.keyboard.press('k')
        dock.wait_for_function("() => !document.getElementById('keysheet').hidden")
        picker = self._sheet(dock)
        self.assertEqual(picker['rows'], 34)
        self.assertEqual(picker['visibleGroups'], 6)
        self.assertEqual(picker['titles'][0], 'Pick a service')
        self.assertIn('Move the Pick', picker['labels'])
        self.assertIn('Open the Service', picker['labels'])
        context.close()

    def test_the_sheet_is_a_layer_and_closes_on_its_frame(self):
        context = self._context()
        dock = self._dock(context)
        dock.locator('.entryrow').nth(2).click()
        dock.wait_for_timeout(150)
        before = self._state(dock)['screen']

        dock.keyboard.press('k')
        dock.wait_for_function("() => !document.getElementById('keysheet').hidden")
        # A click aimed at the transport behind the sheet lands on its 8 px frame.
        dock.mouse.click(4, 4)
        dock.wait_for_function("() => document.getElementById('keysheet').hidden")
        self.assertEqual(self._state(dock)['screen'], before,
                         'a click through the sheet acted on the dock')
        self.assertEqual(self._view(dock), 'run')
        context.close()

    # ---------- US8: Home and End act on the unit on show --------------------

    def _entries(self, page):
        return page.evaluate("""() => [...document.querySelectorAll('.entryli')].map(li => ({
          index: Number(li.dataset.index),
          screens: [...li.querySelectorAll('.screenerow')]
                     .map(r => Number(r.dataset.screen))
        }))""")

    def test_home_and_end_act_on_the_bait_or_entry(self):
        context = self._context()
        dock = self._dock(context)
        entries = self._entries(dock)
        text_screens, song_screens, prayer_screens = (e['screens'] for e in entries)

        # End inside the song takes the live bait's last screen — never the service's.
        dock.locator('.entryrow').nth(1).click()
        dock.wait_for_timeout(150)
        song_start = self._state(dock)['screen']
        self.assertEqual(song_start, song_screens[0])
        dock.keyboard.press('End')
        dock.wait_for_timeout(150)
        bait_one_end = self._state(dock)['screen']
        self.assertIn(bait_one_end, song_screens)
        self.assertLess(bait_one_end, prayer_screens[0],
                        'plain End left the song — the whole service is Ctrl+End')
        # One screen into the bait, End returns to the bait's own last lyric.
        dock.keyboard.press('ArrowRight')
        dock.wait_for_timeout(150)
        self.assertGreater(self._state(dock)['screen'], bait_one_end)
        dock.keyboard.press('End')
        dock.wait_for_timeout(150)
        self.assertEqual(self._state(dock)['screen'], bait_one_end,
                         'End did not come back to the bait’s last lyric')

        dock.keyboard.press('Shift+End')
        dock.wait_for_timeout(150)
        last_bait = self._state(dock)['screen']
        self.assertGreaterEqual(last_bait, song_screens[2],
                                'Shift+End did not take the last bait')
        self.assertIn(last_bait, song_screens)

        # Ctrl takes the service's ends: its first entry and its last entry.
        dock.keyboard.press('Control+Home')
        dock.wait_for_timeout(150)
        self.assertEqual(self._state(dock)['screen'], text_screens[0])
        dock.keyboard.press('Control+End')
        dock.wait_for_timeout(150)
        self.assertEqual(self._state(dock)['screen'], prayer_screens[0])
        context.close()

    def test_shift_home_and_end_take_a_text_entrys_ends(self):
        """The projector's own fall-through (FR-012): on an entry with no baits, `Shift`
        takes that entry's first or last screen, skipping a blank trailing rest."""
        context = self._context()
        dock = self._dock(context)
        rows = dock.evaluate("""() => [...document.querySelectorAll('.entryli')].map(li => ({
          screens: [...li.querySelectorAll('.screenerow')].map(r => ({
            screen: Number(r.dataset.screen),
            rest: r.classList.contains('screenerow--rest')
          }))
        }))""")
        entry = rows[0]['screens']
        expected_end = entry[-2]['screen'] if entry[-1]['rest'] else entry[-1]['screen']

        dock.locator('.entryrow').first.click()
        dock.wait_for_timeout(150)
        dock.keyboard.press('Shift+End')
        dock.wait_for_timeout(150)
        self.assertEqual(self._state(dock)['screen'], expected_end,
                         'Shift+End did not take the entry’s last screen')
        dock.keyboard.press('Shift+Home')
        dock.wait_for_timeout(150)
        self.assertEqual(self._state(dock)['screen'], entry[0]['screen'],
                         'Shift+Home did not take the entry’s first screen')
        context.close()

    # ---------- US3: the go to steps like the projector's --------------------

    def test_the_go_to_steps_a_verse_a_chapter_and_a_book(self):
        context = self._context()
        dock = self._dock(context)
        requests = []
        dock.on('request', lambda request: requests.append(request.url))
        self._choose(dock, 'Matius 5')
        self.assertEqual(self._go_to(dock)['chapter'], 5)
        chapter_requests = [url for url in requests if '/projector/goto/chapter/' in url]

        plain_before = len(chapter_requests)
        dock.keyboard.press('ArrowRight')
        dock.wait_for_timeout(200)
        self.assertEqual(self._go_to(dock)['verse'], 2)
        self.assertEqual(
            len([url for url in requests if '/projector/goto/chapter/' in url]),
            plain_before, 'a verse step inside the loaded chapter fetched')

        dock.keyboard.press('Shift+ArrowRight')
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display'));"
            " return s.goto && s.goto.chapter === 6; }")
        self.assertEqual(self._go_to(dock)['verse'], 1)
        after_chapter = len([url for url in requests if '/projector/goto/chapter/' in url])
        self.assertEqual(after_chapter, plain_before + 1,
                         'a chapter step did not fetch exactly one chapter')

        dock.keyboard.press('Control+ArrowRight')
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display'));"
            " return s.goto && s.goto.book_id !== 0 && s.goto.chapter === 1; }")
        book = self._go_to(dock)
        self.assertEqual(book['chapter'], 1)
        self.assertNotEqual(book['book_id'], self.tb.book_id)
        after_book = len([url for url in requests if '/projector/goto/chapter/' in url])
        self.assertEqual(after_book, after_chapter + 1,
                         'a book step did not fetch exactly one chapter')
        context.close()

    def test_no_key_changes_what_is_on_air_while_a_go_to_fetches(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'Matius 5')
        held = []

        def hold(route):
            held.append(route)

        dock.route('**/projector/goto/chapter/**', hold)
        dock.keyboard.press('Shift+ArrowRight')
        dock.wait_for_timeout(250)
        self.assertEqual(len(held), 1, 'the crossing did not fetch')

        state_before = self._state(dock)
        for _ in range(10):
            dock.keyboard.press('ArrowRight')
            dock.keyboard.press('ArrowDown')
            dock.keyboard.press('PageDown')
            dock.keyboard.press('End')
        for _ in range(3):
            dock.locator('#nextBtn').click(force=True)
        dock.wait_for_timeout(150)
        header = dock.evaluate("() => document.getElementById('offLabel').textContent")
        self.assertEqual(header, 'Loading…')
        self.assertEqual(self._state(dock)['goto'], state_before['goto'],
                         'a key moved the go to while it fetched')
        self.assertEqual(self._state(dock)['screen'], state_before['screen'])

        held[0].continue_()
        dock.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display'));"
            " return s.goto && s.goto.chapter === 6; }")
        self.assertEqual(self._go_to(dock)['verse'], 1,
                         'the crossing did not land where the chord asked')
        context.close()

    # ---------- US11: the band keeps the keyboard ---------------------------

    def test_the_band_keeps_the_keyboard_when_the_window_returns(self):
        context = self._context()
        dock = self._dock(context)
        self._open_band(dock)
        dock.evaluate("""() => {
          document.activeElement.blur();
          document.getElementById('dockPanel').focus();
          window.dispatchEvent(new Event('focus'));
        }""")
        dock.wait_for_timeout(120)
        self.assertTrue(dock.evaluate(
            "() => document.activeElement === document.getElementById('findInput')"),
            'the window returning did not leave the keyboard in the field')

        dock.wait_for_timeout(400)
        dock.locator('#findInput').type('NKB 4', delay=40)
        query = dock.evaluate("() => document.getElementById('findInput').value")
        self.assertEqual(query, 'NKB 4', 'the typing did not append to the query')

        dock.keyboard.press('Escape')
        dock.wait_for_timeout(200)
        self.assertTrue(dock.evaluate(
            "() => document.activeElement === document.getElementById('dockPanel')"),
            'closing the band did not return the focus to the panel')
        context.close()
