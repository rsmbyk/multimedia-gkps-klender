"""End-to-end tests for the empty reading stage after deleting the open record (spec 221).

Same runner and skip behaviour as the other reading suites: Django's test runner via
``StaticLiveServerTestCase``, skipped when Playwright or its browser is missing.
"""

import json
import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DeletedStageE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Kidung Harian', short_name='KH', is_hymn_book=False)
        self.other_book = songs.Book.objects.create(
            name='Lagu Lain', short_name='LL', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=self.book, title='Alpha', number=1)
        self.other_song = songs.Song.objects.create(book=self.book, title='Beta', number=2)
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 8, 23), is_active=True)
        self.other_service = tatib.TataIbadah.objects.create(
            name='Ibadah Rabu', date=date(2026, 8, 26), is_active=True)
        self.template = tatib.TataIbadah.objects.create(
            name='Polos', kind=tatib.TataIbadahKind.TEMPLATE, is_active=True)
        self.other_template = tatib.TataIbadah.objects.create(
            name='Polos Dua', kind=tatib.TataIbadahKind.TEMPLATE, is_active=True)
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self, path, width=1440, height=900):
        page = self.browser.new_page(viewport={'width': width, 'height': height})
        page.goto(self.live_server_url + path)
        page.wait_for_load_state('networkidle')
        return page

    def _delete_row(self, page, scope, kind, pk):
        button = page.locator(
            f'{scope} button[data-editor-delete="{kind}"][data-editor-id="{pk}"]')
        button.locator('xpath=..').hover()
        button.click()
        page.locator('#editorModal [data-editor-delete-form] button[type="submit"]').click()

    def _wait_nothing_open(self, page):
        page.wait_for_function("""() => {
          const d = document.documentElement.dataset;
          const title = document.querySelector('.entry__empty-title');
          return d.read === 'on' && d.home === 'reading' && !!title &&
                 title.textContent === 'Nothing open.' &&
                 !!document.querySelector('.entry__empty-hint') &&
                 !!document.querySelector('.entry__empty-icon svg') &&
                 getComputedStyle(document.getElementById('searchHome')).display === 'none';
        }""", timeout=5000)

    def _shell(self, page):
        return page.evaluate("""() => {
          const d = document.documentElement.dataset;
          const box = (s) => { const e = document.querySelector(s); if (!e) return null;
            const r = e.getBoundingClientRect();
            return {x: Math.round(r.x*10)/10, y: Math.round(r.y*10)/10,
                    w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10}; };
          return {read: d.read, home: d.home, section: d.section,
                  path: location.pathname + location.search,
                  stage: box('.stage'), block: box('.entry__empty'),
                  icon: box('.entry__empty-icon svg'), title: box('.entry__empty-title'),
                  hint: box('.entry__empty-hint'), history: history.length,
                  scroll: document.documentElement.scrollWidth, inner: innerWidth};
        }""")

    # --- US1: the song on stage ---

    def test_deleting_the_open_song_leaves_a_nothing_open_stage(self):
        page = self._page(f'/songs/{self.song.pk}/')
        expect(page.locator('#readName')).to_have_text('Alpha')
        self._delete_row(page, '#chList', 'song', self.song.pk)
        self._wait_nothing_open(page)
        state = self._shell(page)
        self.assertEqual(state['read'], 'on')
        self.assertEqual(state['home'], 'reading')
        self.assertEqual(state['section'], 'kidung')
        self.assertTrue(state['path'].startswith(f'/songs/book/{self.book.pk}/'))
        self.assertIn('stage=empty', state['path'])
        self.assertEqual(page.locator('.entry__empty-hint').inner_text(),
                         'Choose a song or service from the list.')

    def test_reloading_the_empty_stage_keeps_the_reading_view(self):
        page = self._page(f'/songs/book/{self.book.pk}/')
        page.locator(f'#chList .songrow[data-i="{self.song.pk}"]').click()
        expect(page).to_have_url(f'{self.live_server_url}/songs/{self.song.pk}/')
        before = self._shell(page)
        self._delete_row(page, '#chList', 'song', self.song.pk)
        self._wait_nothing_open(page)
        after = self._shell(page)
        self.assertEqual(after['history'], before['history'])
        page.reload()
        self._wait_nothing_open(page)
        self.assertEqual(self._shell(page)['path'], after['path'])
        page.go_back()
        expect(page).to_have_url(f'{self.live_server_url}/songs/book/{self.book.pk}/')

    def test_the_nothing_open_stage_keeps_the_shell_geometry(self):
        page = self._page(f'/songs/{self.song.pk}/')
        self._delete_row(page, '#chList', 'song', self.song.pk)
        self._wait_nothing_open(page)
        page.wait_for_function("() => document.getAnimations().every(a => a.playState === 'finished')")
        wide = self._shell(page)
        self.assertEqual(wide['stage'], {'x': 792, 'y': 0, 'w': 648, 'h': 900})
        self.assertEqual(wide['block']['h'], 108)
        self.assertEqual(wide['block']['y'], 396)
        self.assertEqual(wide['icon']['w'], 38)
        self.assertEqual(wide['icon']['h'], 38)
        self.assertEqual(wide['scroll'], wide['inner'])
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(250)
        narrow = self._shell(page)
        self.assertEqual(narrow['stage'], {'x': 0, 'y': 0, 'w': 390, 'h': 844})
        self.assertEqual(narrow['block']['y'], 368)
        self.assertEqual(narrow['block']['h'], 108)
        self.assertEqual(narrow['scroll'], narrow['inner'])

    # --- US2: the other deletable kinds ---

    def test_deleting_the_open_service_keeps_the_reading_stage(self):
        page = self._page(f'/tatib/{self.service.pk}/')
        self._delete_row(page, '#panelBody', 'tatib', self.service.pk)
        self._wait_nothing_open(page)
        state = self._shell(page)
        self.assertEqual(state['section'], 'tatib')
        self.assertTrue(state['path'].startswith('/tatib/?'))
        self.assertIn('stage=empty', state['path'])
        self.assertGreater(page.locator('#panelBody .book').count(), 0)

    def test_deleting_the_open_template_keeps_its_mode_and_the_stage(self):
        page = self._page(f'/tatib/{self.template.pk}/?mode=template')
        self._delete_row(page, '#panelBody', 'template', self.template.pk)
        self._wait_nothing_open(page)
        state = self._shell(page)
        self.assertEqual(state['section'], 'tatib')
        self.assertIn('mode=template', state['path'])
        self.assertIn('stage=empty', state['path'])

    def test_deleting_the_open_songbook_keeps_the_reading_stage(self):
        page = self._page(f'/songs/{self.song.pk}/')
        self._delete_row(page, '#panelBody', 'songbook', self.book.pk)
        self._wait_nothing_open(page)
        state = self._shell(page)
        self.assertEqual(state['section'], 'kidung')
        self.assertTrue(state['path'].startswith('/songs/?'))
        self.assertIn('stage=empty', state['path'])

    # --- US3: off-stage deletes ---

    def test_deleting_another_row_keeps_the_open_song_on_stage(self):
        page = self._page(f'/songs/{self.song.pk}/')
        before = self._shell(page)
        stage_before = page.locator('#read').inner_text()
        self._delete_row(page, '#chList', 'song', self.other_song.pk)
        page.wait_for_function(
            "!document.querySelector('#chList .songrow[data-i=\\'%d\\']')" % self.other_song.pk)
        after = self._shell(page)
        self.assertEqual(after['read'], before['read'])
        self.assertEqual(after['home'], before['home'])
        self.assertEqual(after['path'], before['path'])
        self.assertEqual(page.locator('#read').inner_text(), stage_before)
