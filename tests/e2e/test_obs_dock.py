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

        # Spec 198: the eligibility matrix — one dated service whose rows cover every
        # FR-001/FR-010 case: an ordinary text, a passage with verses, a song with
        # verses, a verse-less song (start > end → buildInner finds no screen → no
        # inner, no chevron), a section break, and a trailing text to cross into.
        # Dated oldest, so the picker's arrow order above it holds.
        self.matrix_songbook = songs.Book.objects.create(
            name='Nyanyian Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.matrix_song = songs.Song.objects.create(
            book=self.matrix_songbook, number=43, title='Sinar Matahari Pagi')
        songs.Verse.objects.create(song=self.matrix_song, number=1, lyric='Sinar matahari pagi')
        songs.Verse.objects.create(song=self.matrix_song, number=2, lyric='Bersyukurlah selalu')
        indonesian = bible.Language.objects.create(name='Indonesia')
        tb = bible.Version.objects.create(lang=indonesian, name='Terjemahan Baru',
                                          abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        self.matrix_tb = bible.BookTranslation.objects.create(
            version=tb, book=book, translation='Matius')
        for number, text in ((1, 'Ketika Yesus melihat orang banyak itu,'),
                             (2, 'dan Ia membuka mulut-Nya serta mengajar mereka,')):
            bible.Verse.objects.create(book_translation=self.matrix_tb, chapter=5,
                                       verse=number, text=text)

        self.matrix = tatib.TataIbadah.objects.create(
            name='Ibadah Matriks', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.matrix, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.matrix, order_number=2, kind=tatib.ServiceEntryKind.SCRIPTURE,
            title='Firman', book_translation=self.matrix_tb, chapter=5,
            verse_start=1, verse_end=2)
        tatib.ServiceEntry.objects.create(
            tatib=self.matrix, order_number=3, kind=tatib.ServiceEntryKind.SONG,
            title='Pujian', song=self.matrix_song,
            # `verses` holds the verse pks — the form writes value="<pk>" and the
            # payload filters pk__in=... — never the verse numbers.
            verses=[self.matrix_song.verse_set.get(number=1).pk,
                    self.matrix_song.verse_set.get(number=2).pk])
        tatib.ServiceEntry.objects.create(
            tatib=self.matrix, order_number=4, kind=tatib.ServiceEntryKind.SONG,
            title='Pujian kosong', song=self.matrix_song, verses=[])
        tatib.ServiceEntry.objects.create(
            tatib=self.matrix, order_number=5, kind=tatib.ServiceEntryKind.SECTION_BREAK,
            title='PEMUNGKAHNI')
        tatib.ServiceEntry.objects.create(
            tatib=self.matrix, order_number=6, kind=tatib.ServiceEntryKind.TEXT,
            title='Doa', text='Tuhan, dengarkanlah doa kami')

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
        """The header expands its block; the entry's own first screen row projects it."""
        dock.locator('.entryrow').first.click()
        dock.locator('.entryli[data-index="0"] .screenerow').first.click()

    def _raw(self, page):
        """The stored display state exactly as localStorage holds it — bytes."""
        return page.evaluate("() => localStorage.getItem('gkps-display') || 'null'")

    def _block(self, dock, index):
        """One entry's header and block: the state spec 198 pins on them."""
        return dock.evaluate(
            """index => {
                const li = document.querySelector('.entryli[data-index="' + index + '"]');
                const row = li.querySelector('.entryrow');
                const id = row.getAttribute('aria-controls');
                const inner = id ? document.getElementById(id) : li.querySelector('.entryinner');
                return {expanded: row.getAttribute('aria-expanded'),
                        controls: row.getAttribute('aria-controls'),
                        tabindex: row.getAttribute('tabindex'),
                        current: row.getAttribute('aria-current'),
                        rowClass: row.className,
                        open: !!inner && inner.classList.contains('is-open'),
                        morph: !!inner && inner.classList.contains('is-morph'),
                        hidden: inner ? inner.getAttribute('aria-hidden') : null,
                        inert: inner ? !!inner.inert : null,
                        chev: [...li.querySelectorAll('.entrychev')]
                                .filter(c => c.getClientRects().length).length};
            }""", index)

    def _wait_header_act(self, dock, index, before):
        """Wait until the header acted: its morph started — or, on develop's tree
        where the click still projects, the display state moved off `before` (the
        caller's pre-click read; `projectScreen` writes synchronously, so the helper
        must never re-read it). Either arm settles the wait, so a red run fails on
        its own assertion, not a timeout. Returns the raw state after the wait."""
        dock.wait_for_function(
            """([index, before]) => {
                const inner = document.querySelector(
                    '.entryli[data-index="' + index + '"] .entryinner');
                return (inner && inner.classList.contains('is-morph'))
                    || (localStorage.getItem('gkps-display') || 'null') !== before;
            }""", arg=[index, before])
        return self._raw(dock)

    def _caption(self, overlay):
        """The overlay's words, whatever its kind paints them with (spec 165)."""
        overlay.wait_for_selector('.obs-overlay__plate, .obs-overlay__caption')
        return overlay.locator('.obs-overlay__stage').inner_text()

    # ---------- the tests -----------------------------------------------------

    def test_browsing_does_not_project_and_a_screen_row_click_does(self):
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Minggu')

        # Opening a service is browsing: nothing is on air yet.
        self.assertIsNone(self._state(dock))

        projector = self._open(context, '/projector')
        overlay = self._open(context, '/obs/source/overlay')

        # Watch the inter-surface channel alongside localStorage: a header click
        # must issue no write and no broadcast (FR-002, US2/AC4).
        dock.evaluate(
            """() => {
                window.__channelMessages = [];
                const channel = new BroadcastChannel('gkps-service-display');
                channel.onmessage = event => window.__channelMessages.push(event.data);
            }""")
        dock.locator('.entryrow').first.click()
        dock.wait_for_timeout(100)
        self.assertIsNone(self._state(dock), 'a header click wrote gkps-display')
        self.assertEqual(dock.evaluate("() => window.__channelMessages.length"), 0,
                         'a header click broadcast on the display channel')

        # The item inside is the jump target: its screen row puts the entry on air.
        dock.locator('.entryli[data-index="0"] .screenerow').first.click()
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

        # Back in the picker, the mark stays on the service just opened. Since spec 187
        # the return is a hold, not a tap (`Esc` alone leaves the runner).
        dock.keyboard.down('Escape')
        dock.wait_for_timeout(1000)
        dock.keyboard.up('Escape')
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

    # ---------- spec 198: the entry headers toggle; they never project (US1) ---

    def test_the_header_toggles_its_block_and_never_projects(self):
        """US1/AC1-2: the header is a door — it opens its own block and nothing else."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')
        raw_before = self._raw(dock)
        scroll_before = dock.evaluate("() => document.getElementById('runBody').scrollTop")

        # Watch the morph from inside: the 230 ms class can appear and vanish
        # between two polls of the finished state, so a MutationObserver records
        # every window in which the inner really carried `.is-morph`.
        dock.evaluate(
            """() => {
                const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                window.__entryMorphs = 0;
                new MutationObserver(() => {
                    if (inner.classList.contains('is-morph')) window.__entryMorphs += 1;
                }).observe(inner, {attributes: true, attributeFilter: ['class']});
            }""")

        header = dock.locator('.entryli[data-index="1"] .entryrow')
        header.click()
        # Nothing goes on air: the stored state must be byte-identical. On develop's
        # tree this is where the click used to project — the red reason (FR-002).
        self.assertEqual(self._wait_header_act(dock, 1, raw_before), raw_before,
                         'a header click wrote the display state')

        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 return inner.classList.contains('is-open')
                     && !inner.classList.contains('is-morph'); }""")
        self.assertGreater(dock.evaluate("() => window.__entryMorphs"), 0,
                           'the block opened without a morph')

        block = self._block(dock, 1)
        self.assertEqual(block['expanded'], 'true')
        self.assertEqual(block['hidden'], 'false')
        self.assertFalse(block['inert'])

        # Expanding is peeking: no scroll, no selection, no aria-current (FR-007).
        self.assertEqual(
            dock.evaluate("() => document.getElementById('runBody').scrollTop"),
            scroll_before, 'a toggle scrolled the list')
        self.assertEqual(block['current'], 'false', 'a toggle moved aria-current')
        self.assertEqual(
            dock.evaluate(
                "() => document.querySelectorAll('.screenerow[aria-current=\"true\"]').length"),
            0, 'a toggle selected a screen row')

        # The second click closes it with the same flips, and still never writes.
        seen = dock.evaluate("() => window.__entryMorphs")
        header.click()
        self.assertEqual(self._wait_header_act(dock, 1, raw_before), raw_before,
                         'a header click wrote the display state')
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 return !inner.classList.contains('is-open')
                     && !inner.classList.contains('is-morph'); }""")
        self.assertGreater(dock.evaluate("() => window.__entryMorphs"), seen,
                           'the collapse did not morph')
        closed = self._block(dock, 1)
        self.assertEqual(closed['expanded'], 'false')
        self.assertEqual(closed['hidden'], 'true')
        self.assertTrue(closed['inert'])
        self.assertEqual(
            dock.evaluate("() => document.getElementById('runBody').scrollTop"),
            scroll_before, 'a toggle scrolled the list')

        # An entry with nothing to open ignores its header entirely (FR-010):
        # the verse-less song (start > end → no inner at all) and the section break.
        for index in (3, 4):
            before = self._raw(dock)
            dock.locator(f'.entryli[data-index="{index}"] .entryrow').click()
            dock.wait_for_timeout(150)
            self.assertEqual(self._raw(dock), before,
                             f'header {index} has no inner yet wrote state')
            block = self._block(dock, index)
            self.assertFalse(block['open'], f'header {index} opened a block')
            self.assertFalse(block['morph'], f'header {index} started a morph')
        context.close()

    def test_the_live_header_is_locked_open_and_chevronless(self):
        """US1/AC3 and US3/AC3: the live entry cannot be collapsed, shows no chevron."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')
        self._project_first_entry(dock)
        self._wait_state(dock, self.matrix.pk)
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="0"] .entryinner');
                 return inner && inner.classList.contains('is-open')
                     && !inner.classList.contains('is-morph'); }""")

        locked = self._block(dock, 0)
        self.assertEqual(locked['current'], 'true')
        # The live header carries its state but no way to act on it (FR-002/FR-008).
        self.assertEqual(locked['expanded'], 'true')
        self.assertEqual(locked['hidden'], 'false')
        self.assertFalse(locked['inert'])
        raw_before = self._raw(dock)

        dock.locator('.entryli[data-index="0"] .entryrow').click()
        dock.wait_for_timeout(300)     # long enough for any write, class or attribute change

        after = self._block(dock, 0)
        self.assertEqual(self._raw(dock), raw_before, 'the live header wrote the display state')
        self.assertEqual(after['rowClass'], locked['rowClass'], 'the live header changed class')
        self.assertEqual(after['expanded'], locked['expanded'], 'the live header toggled')
        self.assertEqual(after['current'], 'true', 'aria-current left the live row')
        self.assertTrue(after['open'], 'the live block collapsed')
        self.assertEqual(after['hidden'], 'false')
        self.assertFalse(after['inert'])
        self.assertEqual(after['chev'], 0, 'the live row renders a chevron')
        context.close()

    def test_open_blocks_survive_crossings_and_forget_on_reload(self):
        """US1/AC4-5: overrides survive crossings and repaints; a reload forgets them."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')

        # Entry 0 goes on air without its header ever being toggled — its stored
        # state stays unset, so the crossing's departure must paint it closed again.
        dock.evaluate("service => window.gkpsDisplay.show(service, 0)", self.matrix.pk)
        self._wait_state(dock, self.matrix.pk)
        self.assertEqual(self._state(dock)['screen'], 0)
        dock.wait_for_function(
            """() => document.querySelector('.entryli[data-index="0"] .entryrow')
                 .getAttribute('aria-current') === 'true'""")

        # Two non-live blocks open by hand; each toggle is a peek (no write), and
        # opening the second leaves the first standing (multi-open, US1/AC5).
        for index in (1, 5):
            before = self._raw(dock)
            dock.locator(f'.entryli[data-index="{index}"] .entryrow').click()
            self.assertEqual(self._wait_header_act(dock, index, before), before,
                             f'header {index} projected')
            dock.wait_for_function(
                """index => { const inner = document.querySelector(
                     '.entryli[data-index="' + index + '"] .entryinner');
                     return inner.classList.contains('is-open')
                         && !inner.classList.contains('is-morph'); }""", arg=index)
        self.assertTrue(self._block(dock, 1)['open'], 'a second toggle closed the first')

        # Jump inside entry 2: expand its header (a peek), then click its screen row.
        before = self._raw(dock)
        dock.locator('.entryli[data-index="2"] .entryrow').click()
        self.assertEqual(self._wait_header_act(dock, 2, before), before, 'header 2 projected')
        dock.locator('.entryli[data-index="2"] .screenerow').first.click()
        dock.wait_for_function(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null').screen === 5")

        # Through the hand-off, mid-crossing: the overrides hold — sync repaints and
        # the crossing's morph must not clobber them (FR-006, US1/AC4).
        self.assertTrue(self._block(dock, 1)['open'],
                        'an override was clobbered by the crossing')
        self.assertTrue(self._block(dock, 5)['open'],
                        'an override was clobbered by the crossing')

        # Once the crossing settles, the departed entry paints its stored state —
        # unset, so closed — and the arrival is live, open and chevronless. The
        # settle signal is the DEPARTING inner's `.is-morph`: `startMorph` always
        # marks it (this entry has no override to keep it open), while the arriving
        # inner only carries the class when it was closed before the crossing —
        # here it was peeked open first, so waiting on it would pass before the
        # settle paint ever ran (a lost race under load).
        dock.wait_for_function(
            """() => { const li = document.querySelector('.entryli[data-index="2"]');
                 return li.querySelector('.entryrow').getAttribute('aria-current') === 'true'
                     && !document.querySelector('.entryli[data-index="0"] .entryinner')
                            .classList.contains('is-morph'); }""")
        gone = self._block(dock, 0)
        self.assertFalse(gone['open'], "the departed entry's stored state did not apply")
        self.assertEqual(gone['expanded'], 'false')
        live = self._block(dock, 2)
        self.assertEqual(live['chev'], 0, 'the live row renders a chevron')

        # A reload forgets every override: page memory only (FR-006, US3/AC6).
        dock.reload()
        dock.wait_for_selector('.entryli[data-index="2"] .entryrow')
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="2"] .entryinner');
                 return inner && inner.classList.contains('is-open'); }""")
        for index in (0, 1, 5):
            self.assertFalse(self._block(dock, index)['open'],
                             f'block {index} survived the reload')
        context.close()

    def test_the_header_keeps_the_panel_keyboard_and_the_title_name(self):
        """FR-008/A5: the state rides aria-expanded; the name stays the entry's title."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')

        # Every header stays out of the tab order, like every dock control.
        self.assertEqual(
            dock.evaluate(
                "() => [...document.querySelectorAll('.entryrow')]"
                ".map(row => row.getAttribute('tabindex'))"),
            ['-1'] * 6)

        # A header with an inner carries the state pair, pointing at that inner.
        block = self._block(dock, 1)
        self.assertEqual(block['expanded'], 'false')
        self.assertEqual(block['controls'], 'entryinner-1')
        self.assertIsNotNone(dock.evaluate("() => document.getElementById('entryinner-1')"))

        # An entry with nothing to open reports no state (FR-010 scopes the pair).
        for index in (3, 4):
            bare = self._block(dock, index)
            self.assertIsNone(bare['expanded'], f'header {index} carries aria-expanded')
            self.assertIsNone(bare['controls'], f'header {index} carries aria-controls')

        # Activation flips the state and leaves the focus on the panel.
        dock.locator('.entryli[data-index="1"] .entryrow').click()
        dock.wait_for_function(
            """() => document.querySelector('.entryli[data-index="1"] .entryrow')
                 .getAttribute('aria-expanded') === 'true'""")
        self.assertEqual(dock.evaluate("() => document.activeElement.id"), 'dockPanel')

        # The accessible name is the entry's title — no verb rides on it (A5).
        for index, title in ((0, 'Salam'), (1, 'Matius 5:1-2')):
            name = dock.evaluate(
                """index => { const row = document.querySelector(
                     '.entryli[data-index="' + index + '"] .entryrow');
                     return row.getAttribute('aria-label') || row.innerText; }""", index)
            self.assertIn(title, name.replace('\n', ' '), f'header {index} name: {name!r}')
            self.assertNotIn('expand', name.lower())
            self.assertNotIn('collapse', name.lower())
        context.close()

    # ---------- spec 198: the items inside are the jump targets (US2) ----------

    def test_a_screen_row_inside_projects_that_screen(self):
        """US2/AC1-3: expand to peek, click an item to jump, the block stays open."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')

        # A collapsed non-live block is hidden from AT and inert (FR-008 closed half).
        closed = self._block(dock, 1)
        self.assertEqual(closed['hidden'], 'true')
        self.assertTrue(closed['inert'])

        # Expanding is a peek: the display state stays untouched (US2/AC2).
        before = self._raw(dock)
        dock.locator('.entryli[data-index="1"] .entryrow').click()
        self.assertEqual(self._wait_header_act(dock, 1, before), before,
                         'a header click projected')
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 return inner.classList.contains('is-open')
                     && !inner.classList.contains('is-morph'); }""")
        opened = self._block(dock, 1)
        self.assertEqual(opened['hidden'], 'false')
        self.assertFalse(opened['inert'])

        # A middle screen row inside projects exactly that screen (FR-004):
        # entry 1 spans screens 2-4 — verse 1, verse 2, rest.
        dock.locator('.entryli[data-index="1"] .screenerow').nth(1).click()
        dock.wait_for_function(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null').screen === 3")
        self.assertEqual(self._state(dock)['service'], self.matrix.pk)

        # aria-current moves to that row, and the block stays open — the click
        # inside is a jump, not a collapse (edge "screen-row click keeps it open").
        self.assertEqual(
            dock.evaluate(
                """document.querySelector(
                     '.entryli[data-index="1"] .screenerow[data-screen="3"]')
                     .getAttribute('aria-current')"""),
            'true')
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 return inner.classList.contains('is-open')
                     && !inner.classList.contains('is-morph'); }""")
        self.assertTrue(self._block(dock, 1)['open'], 'the jump closed the block')

        # The Next band projects its own screen, unchanged by this spec (FR-004).
        # `updateBand` hides it the moment the live entry's own end is in view, so
        # at full height this entry (end at 250px, fold at 833px) would never show
        # it. Shrink the window to the situation the band exists for — the entry's
        # end below the fold — and refresh the band's state (a resize alone does
        # not re-run `updateBand`; a scroll does).
        dock.set_viewport_size({'width': 1440, 'height': 250})
        dock.evaluate(
            """() => { const rb = document.getElementById('runBody');
                       rb.scrollTop = 1; rb.scrollTop = 0; }""")
        dock.wait_for_function("() => !document.querySelector('.nextband').hidden")
        band = dock.locator('.nextband')
        self.assertTrue(band.is_visible(), 'the Next band is hidden on a live entry')
        band.click()
        dock.wait_for_function(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null').screen === 5")
        context.close()

    # ---------- spec 198: the chevron shows the state (US3) ----------

    def test_the_chevron_marks_the_state_and_the_eligible_rows(self):
        """US3/AC1-4: the presence matrix, the 90° state rotation, the owner's
        vertically centred chevron, the tint over the whole line, the inert rows
        (FR-001/FR-003/FR-010/FR-011, SC-001)."""
        context = self._context()
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')

        def chevrons():
            """Per entry: chevron nodes rendered for it, and how many really show."""
            return dock.evaluate(
                """() => Object.fromEntries(
                     [...document.querySelectorAll('.entryli')].map(li => {
                       const nodes = [...li.querySelectorAll('.entrychev')];
                       return [li.dataset.index, {count: nodes.length,
                                rendered: nodes.filter(n => n.getClientRects().length).length}];
                     }))""")

        def svg_style(index):
            return dock.evaluate(
                """index => { const s = document.querySelector(
                     '.entryli[data-index="' + index + '"] .entrychev svg');
                   if (!s) return null;
                   const cs = getComputedStyle(s);
                   return {transform: cs.transform, duration: cs.transitionDuration,
                           timing: cs.transitionTimingFunction};
                 }""", index)

        def centre_offset(index):
            """Signed px from the chevron's centre to the header line's centre."""
            return dock.evaluate(
                """index => {
                     const li = document.querySelector('.entryli[data-index="' + index + '"]');
                     const row = li.querySelector('.entryrow');
                     const chev = li.querySelector('.entrychev');
                     if (!chev) return null;
                     const r = row.getBoundingClientRect();
                     const c = chev.getBoundingClientRect();
                     return (c.top + c.height / 2) - (r.top + r.height / 2);
                   }""", index)

        def token_color(index, token):
            """The token's own value, canonicalised through the style engine."""
            return dock.evaluate(
                """([index, token]) => {
                     const row = document.querySelector(
                       '.entryli[data-index="' + index + '"] .entryrow');
                     const probe = document.createElement('div');
                     probe.style.cssText = 'position:absolute;visibility:hidden;';
                     probe.style.backgroundColor =
                       getComputedStyle(row).getPropertyValue(token).trim();
                     document.body.appendChild(probe);
                     const value = getComputedStyle(probe).backgroundColor;
                     probe.remove();
                     return value;
                   }""", [index, token])

        # --- presence matrix (FR-001/FR-010, SC-001): nothing is on air, so every
        # header that has a block to show carries exactly one chevron, and the
        # verse-less song and the section break get no node at all.
        state = chevrons()
        for index in ('0', '1', '2', '5'):
            self.assertEqual(state[index], {'count': 1, 'rendered': 1},
                             f'entry {index} chevron: {state[index]}')
        for index in ('3', '4'):
            self.assertEqual(state[index], {'count': 0, 'rendered': 0},
                             f'entry {index} (empty block / break) renders a chevron: '
                             f'{state[index]}')

        # --- a section break's header and an empty entry's header are inert: the
        # click writes nothing, scrolls nothing, gains no state (FR-002/FR-010).
        raw_before = self._raw(dock)
        scroll_before = dock.evaluate("() => document.getElementById('runBody').scrollTop")
        for index in ('3', '4'):
            dock.locator(f'.entryli[data-index="{index}"] .entryrow').click()
            dock.wait_for_timeout(300)   # long enough for a write, a class or a glide
            self.assertEqual(self._raw(dock), raw_before,
                             f'header {index} wrote the display state')
            self.assertEqual(
                dock.evaluate("() => document.getElementById('runBody').scrollTop"),
                scroll_before, f'header {index} scrolled the list')
            gained = dock.evaluate(
                """index => { const row = document.querySelector(
                     '.entryli[data-index="' + index + '"] .entryrow');
                   return {expanded: row.hasAttribute('aria-expanded'),
                            controls: row.hasAttribute('aria-controls'),
                            inner: !!document.getElementById('entryinner-' + index)};
                 }""", index)
            self.assertEqual(gained, {'expanded': False, 'controls': False, 'inner': False},
                             f'header {index} gained state: {gained}')

        # --- collapsed (FR-003): the stroke points right — no transform — with the
        # flip already riding var(--ease) (200 ms on the given curve) for the day
        # the state changes.
        collapsed = svg_style(1)
        self.assertIsNotNone(collapsed, 'a collapsed header renders no chevron svg')
        self.assertIn(collapsed['transform'], ('none', 'matrix(1, 0, 0, 1, 0, 0)'),
                      f"collapsed chevron transform: {collapsed['transform']}")
        self.assertEqual(collapsed['duration'], '0.2s', collapsed)
        self.assertEqual(collapsed['timing'], 'cubic-bezier(0.32, 0.72, 0.28, 1)', collapsed)

        # --- the owner's ask (2026-11-18, research D008): the chevron centred on
        # the header line, collapsed — at most 1 px off its centre.
        offset = centre_offset(1)
        self.assertIsNotNone(offset, 'a collapsed header renders no chevron to centre')
        self.assertLessEqual(abs(offset), 1,
                             f'collapsed chevron {offset:.2f}px off the header centre')

        # --- the tint covers the whole line, chevron inside it (FR-011): the row's
        # own face under the pointer, landing on the token after its own ease.
        resting = dock.evaluate(
            """() => getComputedStyle(document.querySelector(
                 '.entryli[data-index="1"] .entryrow')).backgroundColor""")
        dock.locator('.entryli[data-index="1"] .entryrow').hover()
        hover_tint = token_color(1, '--icon-hover-bg')
        dock.wait_for_function(
            """([index, tint]) => getComputedStyle(document.querySelector(
                 '.entryli[data-index="' + index + '"] .entryrow')).backgroundColor === tint""",
            arg=['1', hover_tint])
        self.assertNotEqual(resting, hover_tint, 'the resting row already wears the hover tint')
        inside = dock.evaluate(
            """() => { const row = document.querySelector(
                 '.entryli[data-index="1"] .entryrow');
                 const chev = row.querySelector('.entrychev');
                 if (!chev) return null;
                 const r = row.getBoundingClientRect();
                 const c = chev.getBoundingClientRect();
                 return c.left >= r.left - 0.5 && c.right <= r.right + 0.5 &&
                        c.top >= r.top - 0.5 && c.bottom <= r.bottom + 0.5;
               }""")
        self.assertIsNotNone(inside, 'the tinted line holds no chevron')
        self.assertTrue(inside, 'the chevron sits outside the tinted line')

        # --- open (FR-003, US3/AC2): the header toggles only, then the chevron
        # lands rotated a full 90° — matrix b=1, c=-1 — after the settle.
        before = self._raw(dock)
        dock.locator('.entryli[data-index="1"] .entryrow').click()
        self.assertEqual(self._wait_header_act(dock, 1, before), before,
                         'a header click projected')
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 const s = document.querySelector('.entryli[data-index="1"] .entrychev svg');
                 if (!inner || !s || inner.classList.contains('is-morph')) return false;
                 const m = getComputedStyle(s).transform;
                 if (!inner.classList.contains('is-open') || m === 'none' ||
                     !m.startsWith('matrix(')) return false;
                 const v = m.slice(7, -1).split(',').map(Number);
                 return Math.abs(v[1] - 1) < 1e-3 && Math.abs(v[2] + 1) < 1e-3;
               }""")

        offset = centre_offset(1)
        self.assertIsNotNone(offset, 'an open header renders no chevron to centre')
        self.assertLessEqual(abs(offset), 1,
                             f'open chevron {offset:.2f}px off the header centre')

        # --- the live row renders no chevron and keeps its selected fill even
        # under the pointer (FR-001/FR-011, US3/AC3).
        self._project_first_entry(dock)
        dock.wait_for_function(
            """() => document.querySelector('.entryli[data-index="0"] .entryrow')
                 .getAttribute('aria-current') === 'true'""")
        state = chevrons()
        self.assertEqual(state['0']['rendered'], 0, f'the live row shows a chevron: {state["0"]}')
        for index in ('1', '2', '5'):
            self.assertEqual(state[index]['rendered'], 1,
                             f'entry {index} lost its chevron when another went live: '
                             f'{state[index]}')
        selected = token_color(0, '--sidebar-selected-bg')
        # At rest the live row is exactly `--sidebar-selected-bg` (FR-011 literal);
        # the face eases into it over the row's own 200 ms, so settle first.
        dock.wait_for_function(
            """([index, tint]) => getComputedStyle(document.querySelector(
                 '.entryli[data-index="' + index + '"] .entryrow')).backgroundColor === tint""",
            arg=['0', selected])

        # Under the pointer the live row never falls back to the generic
        # `.entryrow:hover` face (FR-011's live clause): its state rule outranks
        # `:hover`, so the baseline's own live tone answers instead — the selected
        # bg mixed with ink (obs-dock.css:641). Plan maps FR-011 to
        # `.entryrow:hover` (unchanged) and the owner-approved preview reuses this
        # very sheet, so that tone stands; "keeps the selected tint" = stays in the
        # selected family, never the generic face.
        generic = token_color(0, '--icon-hover-bg')
        live_tone = dock.evaluate(
            """() => { const probe = document.createElement('div');
                 probe.style.cssText = 'position:absolute;visibility:hidden;';
                 probe.style.backgroundColor =
                   'color-mix(in srgb, var(--sidebar-selected-bg) 84%, var(--ink))';
                 document.body.appendChild(probe);
                 const value = getComputedStyle(probe).backgroundColor;
                 probe.remove();
                 return value; }""")
        self.assertNotEqual(generic, live_tone,
                            'the generic hover face equals the live tone — nothing to tell apart')

        dock.locator('.entryli[data-index="0"] .entryrow').hover()
        dock.wait_for_function(
            """([index, tone]) => getComputedStyle(document.querySelector(
                 '.entryli[data-index="' + index + '"] .entryrow')).backgroundColor === tone""",
            arg=['0', live_tone])
        live_hover = dock.evaluate(
            """() => getComputedStyle(document.querySelector(
                 '.entryli[data-index="0"] .entryrow')).backgroundColor""")
        self.assertEqual(live_hover, live_tone,
                         'the live row lost its selected hover tone under the pointer')
        self.assertNotEqual(live_hover, generic,
                            'the live row fell back to the generic hover face')
        context.close()

    def test_an_open_header_tints_at_half_the_hover_face(self):
        """Spec 206: an open header wears the 4 % rail-and-ink wash (FR-001), the
        pointer replaces it rather than blending (FR-004), and the live row keeps
        its selected fill (FR-005) — in both themes, against the same expression."""

        def computed(page, expression):
            """The colour `expression` resolves to, measured in the page."""
            return page.evaluate(
                """expression => { const probe = document.createElement('div');
                     probe.style.cssText = 'position:absolute;visibility:hidden;';
                     probe.style.backgroundColor = expression;
                     document.body.appendChild(probe);
                     const value = getComputedStyle(probe).backgroundColor;
                     probe.remove();
                     return value; }""", expression)

        def background(page, index):
            return page.evaluate(
                """index => getComputedStyle(document.querySelector(
                     '.entryli[data-index="' + index + '"] .entryrow')).backgroundColor""",
                index)

        def settle(page, index, colour):
            page.wait_for_function(
                """([index, colour]) => getComputedStyle(document.querySelector(
                     '.entryli[data-index="' + index + '"] .entryrow')).backgroundColor
                     === colour""", arg=[index, colour])

        def rgb(value):
            """A computed colour as 8-bit channels: hex, rgb(), or color(srgb …)."""
            value = value.strip()
            if value.startswith('#'):
                return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))
            numbers = (value[value.index('(') + 1:value.rindex(')')]
                       .replace('/', ' ').replace(',', ' ').split())
            if value.startswith('color('):
                numbers = numbers[1:]  # drop the colour space
                return tuple(round(float(number) * 255) for number in numbers[:3])
            return tuple(int(round(float(number))) for number in numbers[:3])

        def overlay(rail, face):
            """The hover face as it lands on the rail — its own alpha composited."""
            numbers = (face[face.index('(') + 1:face.rindex(')')]
                       .replace('/', ' ').replace(',', ' ').split())
            alpha = float(numbers[3])
            return tuple(round(alpha * channel + (1 - alpha) * rail[index])
                         for index, channel in enumerate(rgb(face)))

        for theme in ('light', 'dark'):
            with self.subTest(theme=theme):
                context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
                context.add_init_script(
                    "localStorage.setItem('gkps-theme', %r)" % theme)
                dock = self._open(context, '/obs/dock')
                self._open_service(dock, 'Ibadah Matriks')
                self.assertEqual(
                    dock.evaluate("() => document.documentElement.dataset.theme"), theme,
                    'the dock did not start in the theme under test')

                wash = computed(dock, 'color-mix(in srgb, var(--rail-bg) 96%, var(--ink))')
                hover_face = computed(dock, 'var(--icon-hover-bg)')
                self.assertNotEqual(wash, hover_face,
                                    'the wash equals the hover face — nothing to tell apart')

                # FR-002 / SC-001 — a closed header paints no face of its own.
                self.assertEqual(background(dock, 2), 'rgba(0, 0, 0, 0)',
                                 'a closed header already paints a background')

                # SC-002 — the pointer keeps its existing face on a closed header.
                dock.locator('.entryli[data-index="2"] .entryrow').hover()
                settle(dock, 2, hover_face)

                # US1/AC1, FR-001 — opening lands the wash, and only the opened row.
                self.assertEqual(
                    dock.locator('.entryli[data-index="1"] .entryrow')
                        .get_attribute('aria-expanded'), 'false')
                dock.locator('.entryli[data-index="1"] .entryrow').click()
                dock.wait_for_function(
                    """() => document.querySelector(
                         '.entryli[data-index="1"] .entryrow')
                         .getAttribute('aria-expanded') === 'true'""")
                dock.mouse.move(2, 2)  # off the row the click left the pointer on
                settle(dock, 1, wash)
                self.assertEqual(background(dock, 2), 'rgba(0, 0, 0, 0)',
                                 'a closed header picked up the open wash')

                # FR-006 — the wash covers the line, chevron inside it.
                inside = dock.evaluate(
                    """() => { const row = document.querySelector(
                         '.entryli[data-index="1"] .entryrow');
                         const chev = row.querySelector('.entrychev');
                         if (!chev) return null;
                         const r = row.getBoundingClientRect();
                         const c = chev.getBoundingClientRect();
                         return c.left >= r.left - 0.5 && c.right <= r.right + 0.5 &&
                                c.top >= r.top - 0.5 && c.bottom <= r.bottom + 0.5;
                       }""")
                self.assertIsNotNone(inside, 'an open header renders no chevron')
                self.assertTrue(inside, 'the chevron sits outside the tinted line')

                # FR-007 — the wash rides the row's existing transition, adds none.
                timing = dock.evaluate(
                    """() => { const s = getComputedStyle(document.querySelector(
                         '.entryli[data-index="1"] .entryrow'));
                         return [s.transitionProperty, s.transitionDuration]; }""")
                self.assertEqual(timing, ['background', '0.2s'], timing)

                # US2/AC1, FR-004 — on an open header the pointer face replaces
                # the wash; it is never a blend of the two.
                dock.locator('.entryli[data-index="1"] .entryrow').hover()
                settle(dock, 1, hover_face)

                # US2/AC2 — leaving it returns to the wash, not to bare rail.
                dock.mouse.move(2, 2)
                settle(dock, 1, wash)

                # US1/AC3 — closing takes the wash with it.
                dock.locator('.entryli[data-index="1"] .entryrow').click()
                dock.wait_for_function(
                    """() => document.querySelector(
                         '.entryli[data-index="1"] .entryrow')
                         .getAttribute('aria-expanded') === 'false'""")
                dock.mouse.move(2, 2)
                settle(dock, 1, 'rgba(0, 0, 0, 0)')

                # FR-008 — rows that cannot expand carry no attribute and no wash:
                # index 3 is a song with no verses (no block), index 4 a section break.
                for index in (3, 4):
                    state = dock.evaluate(
                        """index => { const row = document.querySelector(
                             '.entryli[data-index="' + index + '"] .entryrow');
                             return {expanded: row.hasAttribute('aria-expanded'),
                                     controls: row.hasAttribute('aria-controls')}; }""",
                        index)
                    self.assertEqual(state, {'expanded': False, 'controls': False},
                                     f'row {index} names a block it cannot open: {state}')
                    self.assertEqual(background(dock, index), 'rgba(0, 0, 0, 0)',
                                     f'row {index} paints the open wash without expanding')

                # US1/AC4, FR-005 — the live entry is always aria-expanded="true",
                # so its selected fill has to outrank the wash at rest...
                self._project_first_entry(dock)
                dock.wait_for_function(
                    """() => { const row = document.querySelector(
                         '.entryli[data-index="0"] .entryrow');
                         return row.getAttribute('aria-current') === 'true' &&
                                row.getAttribute('aria-expanded') === 'true'; }""")
                selected = computed(dock, 'var(--sidebar-selected-bg)')
                dock.mouse.move(2, 2)
                settle(dock, 0, selected)

                # ...and its own hover tone under the pointer, never the generic
                # face and never the wash.
                live_tone = computed(
                    dock,
                    'color-mix(in srgb, var(--sidebar-selected-bg) 84%, var(--ink))')
                self.assertNotEqual(live_tone, wash)
                self.assertNotEqual(live_tone, hover_face)
                dock.locator('.entryli[data-index="0"] .entryrow').hover()
                settle(dock, 0, live_tone)

                # SC-005 — "softer than the pointer" as a measurement, not an
                # adjective: the wash's farthest channel is a smaller step from
                # the rail than the hover face's, in this theme.
                rail = rgb(dock.evaluate(
                    """() => getComputedStyle(document.documentElement)
                         .getPropertyValue('--rail-bg').trim()"""))
                wash_step = max(abs(rail[i] - rgb(wash)[i]) for i in range(3))
                face_step = max(abs(rail[i] - overlay(rail, hover_face)[i])
                                for i in range(3))
                self.assertLess(wash_step, face_step,
                                f'{theme}: wash {wash_step} is not softer than '
                                f'hover {face_step}')
                context.close()

    def test_the_toggle_swaps_instantly_under_reduced_motion(self):
        """US3/AC5: under reduce the block swaps instantly — no morph runs, and the
        chevron flip has no transition of its own (FR-003/FR-005 reduce halves)."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900},
                                           reduced_motion='reduce')
        dock = self._open(context, '/obs/dock')
        self._open_service(dock, 'Ibadah Matriks')
        self.assertTrue(
            dock.evaluate("() => matchMedia('(prefers-reduced-motion: reduce)').matches"),
            'the context is not emulating reduced motion')

        # Watch from inside: a MutationObserver counts every window in which the
        # inner really carried `.is-morph` (a poll of the finished state would miss
        # a morph that opened and closed between two reads), and page-side clocks
        # measure click → open — Python round trips would measure the wire.
        dock.evaluate(
            """() => {
                 const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 const row = document.querySelector('.entryli[data-index="1"] .entryrow');
                 window.__entryMorphs = 0;
                 window.__clickedAt = null;
                 window.__openAt = null;
                 new MutationObserver(() => {
                   if (inner.classList.contains('is-morph')) window.__entryMorphs += 1;
                 }).observe(inner, {attributes: true, attributeFilter: ['class']});
                 row.addEventListener('click', () => {
                   window.__clickedAt = performance.now();
                   const watch = () => {
                     if (window.__openAt !== null) return;
                     if (inner.classList.contains('is-open'))
                       window.__openAt = performance.now();
                     else requestAnimationFrame(watch);
                   };
                   watch();
                 });
               }""")

        before = self._raw(dock)
        dock.locator('.entryli[data-index="1"] .entryrow').click()
        dock.wait_for_function(
            """() => { const inner = document.querySelector('.entryli[data-index="1"] .entryinner');
                 return inner.classList.contains('is-open')
                      && !inner.classList.contains('is-morph'); }""")
        self.assertEqual(self._raw(dock), before, 'a header click projected')

        # The swap lands within a frame of the click (AC5), on the page's clock.
        clicked, opened = dock.evaluate("() => [window.__clickedAt, window.__openAt]")
        self.assertIsNotNone(clicked, 'the header click never reached the row')
        self.assertIsNotNone(opened, 'the block never reported open')
        elapsed = opened - clicked
        self.assertLess(elapsed, 100,
                        f'the block took {elapsed:.0f}ms to open under reduce — past a frame')

        # A 230 ms morph would be over by now either way; count every window it ran.
        dock.wait_for_timeout(400)
        self.assertEqual(dock.evaluate("() => window.__entryMorphs"), 0,
                         'a morph ran under prefers-reduced-motion: reduce (FR-005)')
        self.assertEqual(
            dock.evaluate(
                """() => document.querySelector('.entryli[data-index="1"] .entryinner')
                     .style.gridTemplateRows"""),
            '', 'the reduce toggle left a hand-morph height inline')

        # The chevron flip has no transition under reduce (FR-003), and it points
        # down already: the full 90° matrix, no partial angle.
        svg = dock.evaluate(
            """() => { const s = document.querySelector(
                 '.entryli[data-index="1"] .entrychev svg');
                 if (!s) return null;
                 const cs = getComputedStyle(s);
                 return {duration: cs.transitionDuration, transform: cs.transform,
                         animations: s.getAnimations().length};
               }""")
        self.assertIsNotNone(svg, 'the open header renders no chevron to flip')
        self.assertEqual(svg['duration'], '0s',
                         f'the chevron flip transitions under reduce: {svg}')
        self.assertEqual(svg['animations'], 0,
                         f'an animation runs on the chevron under reduce: {svg}')
        self.assertTrue(svg['transform'].startswith('matrix('),
                        f'the chevron has not flipped down: {svg}')
        vector = [float(x) for x in svg['transform'][7:-1].split(',')]
        self.assertAlmostEqual(vector[1], 1, delta=1e-3, msg=f'not 90°: {svg}')
        self.assertAlmostEqual(vector[2], -1, delta=1e-3, msg=f'not 90°: {svg}')
        context.close()
