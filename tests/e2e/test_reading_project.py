"""Spec 193 — the reading pages' Project control: the open song or chapter on air.

The song and Bible chapter pages gain the Tata Ibadah page's project button, minus the
toggle: one click writes the Go To pointer (spec 185), never resets a detour it already
opened, and always opens or reuses the named projector window. The projector fetches and
paints a Go To only when it differs from the detour already open (FR-008).

Every assertion drives the real pages through Playwright: the reading pages' DOM, the
stored display state, the named window, and the projector surface.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


STATE_KEY = 'gkps-display'

STATE_IS = ("() => { const s = JSON.parse(localStorage.getItem('%s') || 'null');"
            " return s; }" % STATE_KEY)


def _goto_is():
    return ("() => { const s = JSON.parse(localStorage.getItem('%s') || 'null');"
            " return !!(s && s.goto); }" % STATE_KEY)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ReadingProjectE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Go To', date=date(2026, 11, 8), is_active=True)
        for order, text in enumerate(['Salam', 'Firman'], 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                order_number=order, title=text, text=f'{text} umat Tuhan')

        self.songbook = songs.Book.objects.create(
            name='Nyanyian Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.song = songs.Song.objects.create(
            book=self.songbook, number=43, title='Sinar Matahari Pagi')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Sinar matahari pagi')
        songs.Verse.objects.create(song=self.song, number=2, lyric='Bersyukurlah selalu')
        self.other_song = songs.Song.objects.create(
            book=self.songbook, number=44, title='Fajar Menyingsing')
        songs.Verse.objects.create(
            song=self.other_song, number=1, lyric='Fajar menyingsing')

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
        for number, text in ((1, 'Ketika Yesus melihat orang banyak itu,'),):
            bible.Verse.objects.create(book_translation=self.tb, chapter=5, verse=number,
                                       text=text)
            bible.Verse.objects.create(book_translation=self.sim, chapter=5, verse=number,
                                       text='SIM ' + text)

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            self._playwright = None
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None
        super().tearDown()

    # ---------- helpers -------------------------------------------------------

    def _context(self, width=1440):
        return self.browser.new_context(viewport={'width': width, 'height': 900})

    def _state(self, page):
        return page.evaluate(STATE_IS)

    def _song_page(self, context, song=None):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + reverse('web-song', args=[(song or self.song).pk]))
        page.wait_for_selector('[data-project-goto]')
        return page

    def _chapter_page(self, context, edition='tb'):
        page = context.new_page()
        page.set_default_timeout(6000)
        url = self.live_server_url + reverse('web-bible-chapter',
                                             args=[self.tb.book_id, 5]) + f'?ed={edition}'
        page.goto(url)
        page.wait_for_selector('[data-project-goto]')
        return page

    def _projector(self, context, url='/projector'):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + url)
        page.wait_for_function(
            "() => window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready()")
        return page

    def _click(self, page):
        page.locator('[data-project-goto]').click()
        page.wait_for_function(_goto_is())

    # ---------- US1: the song page --------------------------------------------

    def test_clicking_project_writes_the_song_pointer(self):
        context = self._context()
        page = self._song_page(context)
        self._click(page)
        state = self._state(page)
        self.assertEqual(state['goto'],
                         {'kind': 'song', 'song_id': self.song.pk, 'index': 0})
        self.assertIsNone(state['service'])
        self.assertEqual(state['screen'], 0)
        self.assertIsNone(state['translation'])
        self.assertTrue(state['on'])
        context.close()

    def test_one_click_opens_the_projector_window_once(self):
        context = self._context()
        page = self._song_page(context)

        def projector_pages():
            return [p for p in context.pages if p.url.endswith('/projector')]

        self._click(page)
        for _ in range(50):
            if len(projector_pages()) == 1:
                break
            page.wait_for_timeout(100)
        self.assertEqual(len(projector_pages()), 1)
        projector_pages()[0].wait_for_url('**/projector')
        self._click(page)                       # the same window is reused
        page.wait_for_timeout(400)
        self.assertEqual(len(projector_pages()), 1)
        context.close()

    # ---------- US2: the chapter page ------------------------------------------

    def test_clicking_project_writes_the_chapter_pointer(self):
        context = self._context()
        page = self._chapter_page(context)
        self._click(page)
        state = self._state(page)
        self.assertEqual(state['goto'],
                         {'kind': 'passage', 'book_id': self.tb.book_id, 'chapter': 5,
                          'verse': 1, 'translation': 'TB'})
        self.assertIsNone(state['service'])
        context.close()

    def test_sim_page_projects_sim(self):
        context = self._context()
        page = self._chapter_page(context, edition='sim')
        self._click(page)
        state = self._state(page)
        self.assertEqual(state['goto']['translation'], 'SIM')
        context.close()

    # ---------- the place is never reset ----------------------------------------

    def test_repeat_click_keeps_the_detours_place(self):
        context = self._context()
        page = self._song_page(context)
        self._click(page)                       # the click opens the projector window
        pages = []
        for _ in range(50):
            pages = [p for p in context.pages if p.url.endswith('/projector')]
            if pages:
                break
            page.wait_for_timeout(100)
        self.assertTrue(pages, 'the projector window never opened')
        projector = pages[0]
        projector.wait_for_function(
            "() => window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready()")
        projector.wait_for_selector('.projector-detour.is-active')
        projector.keyboard.press('ArrowRight')          # the detour steps to screen 1
        projector.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('%s') || 'null');"
            " return s && s.goto && s.goto.index === 1; }" % STATE_KEY)
        self._click(page)                               # the button never resets it
        state = self._state(page)
        self.assertEqual(state['goto']['index'], 1)
        self.assertTrue(state['on'])
        context.close()

    def test_repeat_click_makes_no_second_fetch(self):
        context = self._context()
        requests = []
        context.on('request', lambda request: requests.append(request.url))
        page = self._song_page(context)
        self._click(page)                       # boot paints: one content fetch
        pages = []
        for _ in range(50):
            pages = [p for p in context.pages if p.url.endswith('/projector')]
            if pages:
                break
            page.wait_for_timeout(100)
        self.assertTrue(pages, 'the projector window never opened')
        projector = pages[0]
        projector.wait_for_function(
            "() => window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready()")
        projector.wait_for_selector('.projector-detour.is-active')
        projector.keyboard.press('ArrowRight')          # a step stays local
        page.wait_for_timeout(400)
        self._click(page)                               # identical pointer: inert
        page.wait_for_timeout(400)
        fetched = [url for url in requests if '/projector/goto/song/' in url]
        self.assertEqual(len(fetched), 1, fetched)
        context.close()

    # ---------- composition with the service display ------------------------------

    def test_back_returns_to_the_service(self):
        context = self._context()
        page = self._song_page(context)
        page.evaluate(f"() => window.gkpsDisplay.show({self.service.pk}, 0)")
        self._click(page)                       # the detour takes the screen; the window
        pages = []                              # opens adopting the service underneath
        for _ in range(50):
            pages = [p for p in context.pages if p.url.endswith('/projector')]
            if pages:
                break
            page.wait_for_timeout(100)
        self.assertTrue(pages, 'the projector window never opened')
        projector = pages[0]
        projector.set_default_timeout(6000)
        projector.wait_for_function(
            "() => window.GKPSProjectorLibrary && window.GKPSProjectorLibrary.ready()")
        projector.wait_for_selector('.projector-detour.is-active')
        projector.keyboard.press('Escape')               # Back ends the detour
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('%s') || 'null');"
            " return s && s.goto === null && s.service === %d && s.on === true; }"
            % (STATE_KEY, self.service.pk))
        active = projector.locator('#projectorScreens .screen.is-active[data-screen]')
        self.assertEqual(active.count(), 1)
        self.assertEqual(projector.locator('.projector-detour.is-active').count(), 0)
        context.close()

    def test_the_control_survives_in_page_navigation(self):
        context = self._context()
        page = self._song_page(context)
        page.evaluate("() => { window.__sameDocument = 'kept'; }")
        self._click(page)
        page.locator(f'a.songrow[href*="{self.other_song.pk}"]').click()
        page.wait_for_function(
            "() => document.getElementById('readEyebrow').textContent === 'NKB 44'")
        self.assertEqual(page.evaluate("() => window.__sameDocument"), 'kept')
        self._click(page)
        state = self._state(page)
        self.assertEqual(state['goto']['song_id'], self.other_song.pk)
        context.close()
