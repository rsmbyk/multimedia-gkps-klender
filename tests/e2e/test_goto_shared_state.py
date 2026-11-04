"""Spec 185 — one go to, three surfaces: the dock, the projector and the overlay.

The go to is one field of the display state, written by whichever surface starts it and
read by all three. These tests drive the real pages together and never compare a surface
against an expectation the other two have not already painted.
"""

import io
import json
import unittest
import wave
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
SESSION_COOKIE = 'gkps-session'


def _wav():
    output = io.BytesIO()
    with wave.open(output, 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(1)
        audio.setframerate(8000)
        audio.writeframes(bytes([128, 144, 160, 144]) * 20000)
    return output.getvalue()


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class GotoSharedStateE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Bersama', date=date(2026, 11, 8), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Salam', text='Kasih karunia Tuhan beserta kita')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=2,
            title='Doa', text='Tuhan, dengarkanlah doa kami')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=3,
            title='Pujian', text='Pujilah Tuhan, hai segala bangsa')
        self.media = tatib.MediaIdentity.objects.create(
            sha256='b' * 64, byte_count=len(_wav()), family='audio',
            display_filename='recording.wav')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, order_number=4,
            media=self.media, media_filename='recording.wav', title='Musik persembahan')

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
        self.tb = bible.BookTranslation.objects.create(version=tb, book=book,
                                                       translation='Matius')
        self.sim = bible.BookTranslation.objects.create(version=sim, book=book,
                                                        translation='Mateus')
        for number, text in ((1, 'Ketika Yesus melihat orang banyak itu,'),
                             (2, 'dan Ia membuka mulut-Nya serta mengajar mereka,'),
                             (3, 'kata-Nya: Berbahagialah orang yang miskin di hadapan Allah.')):
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

    def _state(self, page):
        return page.evaluate(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")

    def _goto(self, page):
        return (self._state(page) or {}).get('goto')

    def _dock(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/obs/dock')
        page.wait_for_selector(f'.servicerow[data-service="{self.service.pk}"]')
        page.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        page.wait_for_selector('.entryrow')
        return page

    def _projector(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/projector?service=' + str(self.service.pk))
        page.wait_for_function("() => window.GKPSProjectorLibrary"
                               " && window.GKPSProjectorLibrary.ready()")
        return page

    def _overlay(self, context):
        page = context.new_page()
        page.set_default_timeout(6000)
        page.goto(self.live_server_url + '/obs/source/overlay')
        page.wait_for_selector('#overlayStage')
        return page

    def _choose(self, page, query):
        page.bring_to_front()
        page.keyboard.press('g')
        page.wait_for_selector('.bandswap.is-find')
        page.wait_for_function(
            "() => document.getElementById('findLabel').textContent"
            " !== 'Loading search…'")
        page.fill('#findInput', query)
        page.wait_for_timeout(300)
        page.keyboard.press('Enter')
        page.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        page.wait_for_timeout(350)

    def _projector_view(self, page):
        return page.evaluate("""() => { const s = document.querySelector('.screen.is-active');
          const lines = s ? s.querySelector('.screen__lines') : null;
          return {detour: !!s && s.classList.contains('projector-detour'),
                  head: s && s.querySelector('.screen__head') ? s.querySelector('.screen__head').textContent : '',
                  line: lines && lines.querySelector('.screen__line') ? lines.querySelector('.screen__line').textContent : '',
                  cue: (document.querySelector('#cue-prefix span') || {}).textContent || '',
                  showing: document.body.dataset.showing}; }""")

    def _overlay_view(self, page):
        return page.evaluate("""() => { const stage = document.getElementById('overlayStage');
          const words = stage.querySelector('.obs-overlay__words');
          const line = words || stage.querySelector('.obs-overlay__caption span, .obs-overlay__line');
          return {kind: stage.dataset.kind || '', children: stage.children.length,
                  kicker: stage.querySelector('.obs-overlay__kicker')
                    ? stage.querySelector('.obs-overlay__kicker').textContent : '',
                  line: line ? line.textContent : ''}; }""")

    def _wait_agree(self, dock, projector, overlay, timeout=6000):
        """Wait until all three name the same thing, and return the three readouts."""
        def agreed():
            p = self._projector_view(projector)
            o = self._overlay_view(overlay)
            d = dock.evaluate("() => document.getElementById('offLabel').textContent")
            return bool(p['line']) and p['line'][:18] == o['line'][:18] and bool(d), (d, p, o)

        last = None
        for _ in range(40):
            ok, values = agreed()
            last = values
            if ok:
                return values
            dock.wait_for_timeout(150)
        raise AssertionError('the three surfaces never agreed: %r' % (last,))

    # ---------- US2: one state, three surfaces -------------------------------

    def test_the_three_surfaces_agree_at_every_step(self):
        context = self._context()
        dock = self._dock(context)
        projector = self._projector(context)
        overlay = self._overlay(context)
        self._choose(dock, 'NKB 43')
        label, proj, ovl = self._wait_agree(dock, projector, overlay)
        self.assertTrue(proj['detour'])
        self.assertEqual(proj['cue'], 'NKB 43 Sinar Matahari Pagi ·')
        self.assertEqual(ovl['kind'], 'song')
        self.assertIn(proj['line'][:18], ovl['line'])

        dock.locator('#offBody .offrow').nth(2).click()
        dock.wait_for_timeout(600)
        label, proj, ovl = self._wait_agree(dock, projector, overlay)
        self.assertTrue(proj['line'], 'the second screen is blank, not missing')

        # A passage, then its edition flipped from the dock
        self._choose(dock, 'Matius 5:3')
        dock.wait_for_timeout(400)
        proj = self._projector_view(projector)
        ovl = self._overlay_view(overlay)
        self.assertEqual(proj['head'], 'Matius 5:3')
        self.assertEqual(ovl['kicker'], 'Matius 5:3')
        dock.bring_to_front()
        dock.keyboard.press('t')
        dock.wait_for_timeout(600)
        self.assertEqual(self._projector_view(projector)['head'], 'Mateus 5:3')
        self.assertEqual(self._overlay_view(overlay)['kicker'], 'Mateus 5:3')
        context.close()

    def test_a_surface_opened_mid_goto_catches_up(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'Matius 5:3')
        dock.wait_for_timeout(400)
        # Both surfaces open for the first time while the go to is already on air.
        projector = self._projector(context)
        overlay = self._overlay(context)
        projector.wait_for_function(
            "() => !!document.querySelector('.screen.is-active.projector-detour')")
        overlay.wait_for_selector('.obs-overlay__plate')
        self.assertEqual(self._projector_view(projector)['head'], 'Matius 5:3')
        self.assertEqual(self._overlay_view(overlay)['kicker'], 'Matius 5:3')
        context.close()

    def test_the_dock_follows_a_goto_started_on_the_projector(self):
        context = self._context()
        dock = self._dock(context)
        projector = self._projector(context)
        overlay = self._overlay(context)
        projector.bring_to_front()
        projector.keyboard.press('g')
        projector.wait_for_selector('#projectorFind:not([hidden])')
        projector.fill('#projectorFindInput', 'NKB 43')
        projector.wait_for_timeout(400)
        projector.keyboard.press('Enter')
        projector.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && s.goto); }")
        dock.wait_for_selector('#offBlock:not([hidden])', timeout=6000)
        dock.wait_for_timeout(400)
        self.assertEqual(dock.evaluate(
            "() => document.getElementById('offLabel').textContent"),
            'NKB 43 Sinar Matahari Pagi')
        self.assertEqual(self._state(dock)['goto']['song_id'], self.song.pk)
        overlay.wait_for_selector('.obs-overlay__caption')
        self.assertEqual(self._overlay_view(overlay)['kind'], 'song')
        # The projector's Back returns the service, at the place it stood.
        projector.keyboard.press('Escape')
        projector.evaluate("() => { const cue = document.getElementById('cue-next');"
                           " cue.click(); }")
        projector.wait_for_function(
            "() => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return !!(s && !s.goto); }")
        dock.wait_for_function(
            "() => document.getElementById('offBlock').hidden")
        context.close()

    def test_a_goto_stops_a_playing_recording(self):
        context = self._context()
        projector = context.new_page()
        projector.set_default_timeout(8000)

        def serve(route):
            route.fulfill(status=200,
                          headers={'Access-Control-Allow-Origin':
                                   route.request.headers.get('origin', '*'),
                                   'Content-Type': 'application/octet-stream'},
                          body=_wav())

        projector.route('http://127.0.0.1:63174/v1/files/' + self.media.sha256, serve)
        projector.goto(self.live_server_url + '/projector?service=' + str(self.service.pk))
        projector.keyboard.press('Space')
        for _ in range(3):
            projector.keyboard.press('Control+ArrowRight')
        projector.wait_for_selector('.screen.is-active .screen__audio-player',
                                    state='visible')
        projector.locator('.screen.is-active [data-audio-play]').click()
        projector.wait_for_function(
            "() => { const host = document.querySelector('.screen.is-active [data-media-audio]');"
            " return !!host && !host.classList.contains('is-idle'); }")
        # The recording holds the screen: the projector's own G is refused.
        projector.keyboard.press('g')
        projector.wait_for_timeout(300)
        self.assertTrue(projector.evaluate(
            "() => document.getElementById('projectorFind').hidden"))

        dock = self._dock(context)
        self._choose(dock, 'NKB 43')
        projector.wait_for_function(
            "() => !!document.querySelector('.screen.is-active.projector-detour')")
        # The recording is released: its element is gone or paused (the panel itself
        # lives on the now-inactive screen, which is not painted).
        self.assertTrue(projector.evaluate("""() => {
          const audios = [...document.querySelectorAll('audio')];
          return audios.every(audio => audio.paused);
        }"""), 'the recording kept playing while a go to painted')
        self.assertEqual(self._projector_view(projector)['cue'], 'NKB 43 Sinar Matahari Pagi ·')
        context.close()

    # ---------- US4: the go to lives exactly as long as the state -------------

    def test_restart_paints_no_goto(self):
        context = self._context()
        seed = {'service': self.service.pk, 'screen': 0, 'on': True, 'translation': None,
                'at': 1, 'session': 'a-session-that-is-not-here',
                'goto': {'kind': 'song', 'song_id': self.song.pk, 'index': 1}}
        context.add_init_script(
            "localStorage.setItem(%s, %s);" % (
                json.dumps(STATE_KEY), json.dumps(json.dumps(seed))))
        dock = self._dock(context)
        dock.wait_for_timeout(400)
        self.assertTrue(dock.evaluate("() => document.getElementById('offBlock').hidden"))
        # The stored object still names a go to; the READER must refuse it.
        self.assertTrue(self._goto(dock), 'the seed did not reach storage')
        self.assertIsNone(dock.evaluate("() => window.gkpsDisplay.read().goto"))
        overlay = self._overlay(context)
        overlay.wait_for_timeout(700)
        self.assertEqual(overlay.evaluate(
            "document.getElementById('overlayStage').children.length"), 0)
        projector = self._projector(context)
        projector.wait_for_timeout(700)
        self.assertEqual(projector.locator('.screen.is-active.projector-detour').count(), 0)
        context.close()

    def test_release_ends_the_goto(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'NKB 43')
        dock.evaluate("() => window.gkpsDisplay.release()")
        dock.wait_for_timeout(400)
        state = self._state(dock)
        self.assertIsNone(state['goto'])
        self.assertIsNone(state['service'])
        self.assertTrue(dock.evaluate("() => document.getElementById('offBlock').hidden"))
        context.close()

    def test_hide_during_a_goto_keeps_the_place(self):
        context = self._context()
        dock = self._dock(context)
        projector = self._projector(context)
        overlay = self._overlay(context)
        self._choose(dock, 'NKB 43')
        self._wait_agree(dock, projector, overlay)
        dock.bring_to_front()
        dock.keyboard.press(' ')
        dock.wait_for_timeout(500)
        state = self._state(dock)
        self.assertFalse(state['on'])
        self.assertIsNotNone(state['goto'])
        self.assertEqual(self._projector_view(projector)['showing'], 'false')
        self.assertEqual(self._overlay_view(overlay)['children'], 0)
        self.assertTrue(dock.evaluate("() => document.getElementById('offBlock').hidden") is False)
        dock.keyboard.press(' ')
        dock.wait_for_timeout(500)
        self.assertTrue(self._state(dock)['on'])
        self.assertTrue(self._projector_view(projector)['line'])
        context.close()

    def test_the_stored_state_carries_no_verse_words(self):
        context = self._context()
        dock = self._dock(context)
        self._choose(dock, 'Matius 5:3')
        dock.wait_for_timeout(300)
        stored = dock.evaluate("() => localStorage.getItem('gkps-display')")
        self.assertIn('"goto"', stored)
        for word in ('Berbahagialah', 'miskin', 'Kerajaan'):
            self.assertNotIn(word, stored, 'the state carried verse text')
        context.close()

    def test_a_corrupt_goto_reads_as_no_goto(self):
        context = self._context()
        seed = {'service': self.service.pk, 'screen': 0, 'on': True, 'translation': None,
                'at': 1, 'session': 'x', 'goto': {'kind': 'nonsense'}}
        page = self._dock(context)
        page.evaluate("""state => {
          const marker = document.cookie.match(/(?:^|;\\s*)gkps-session=([^;]+)/);
          state.session = marker ? decodeURIComponent(marker[1]) : state.session;
          localStorage.setItem('gkps-display', JSON.stringify(state));
        }""", seed)
        page.reload()
        page.wait_for_selector(f'.servicerow[data-service="{self.service.pk}"]')
        page.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        page.wait_for_selector('.entryrow')
        page.wait_for_timeout(300)
        self.assertIsNone(page.evaluate("() => window.gkpsDisplay.read().goto"))
        self.assertTrue(page.evaluate("() => document.getElementById('offBlock').hidden"))
        context.close()
