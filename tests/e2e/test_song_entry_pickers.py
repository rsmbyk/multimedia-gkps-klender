"""Acceptance pins for the song entry's two pickers (spec 210).

A separate module from test_entry_pickers.py: that suite has a backdrop race on
unmodified develop, and this slice's pins must not inherit it.
"""
import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

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
class SongEntryPickerE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Picker', date=date(2026, 11, 21), is_active=True)
        self.book = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        self.song = songs.Song.objects.create(book=self.book, number=152, title='Ada Kuasa')
        for number in range(1, 13):
            songs.Verse.objects.create(song=self.song, number=number, lyric=f'bait {number}')
        self.solo = songs.Song.objects.create(book=self.book, number=90, title='Bait Tunggal')
        songs.Verse.objects.create(song=self.solo, number=1, lyric='satu')
        self.void = songs.Song.objects.create(book=self.book, number=901, title='Kosong')
        for number in range(10, 22):
            songs.Song.objects.create(book=self.book, number=number, title=f'Song {number}')

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

    def _page(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def _open_song(self, page):
        page.locator('.entry__empty-btn', has_text='Add Song').first.click()
        page.wait_for_selector('dialog[open]')

    def _pick(self, page, title):
        search = page.locator('#entry-song-search')
        search.fill(title)
        page.wait_for_selector('#entry-song-options [data-song]')
        page.locator('#entry-song-options [data-song]').first.click()
        page.wait_for_function("document.querySelector('#id_song').value !== ''")

    def test_search_is_focused_on_open(self):
        page = self._page()
        self._open_song(page)
        expect(page.locator('#entry-song-search')).to_be_focused()
        page.locator('#entry-song-search').fill('KJ 152')
        options = page.locator('#entry-song-options [data-song]')
        expect(options).to_have_count(1)
        expect(options.first).to_have_attribute('data-song', str(self.song.pk))

    def test_results_overlay_may_pass_dialog_bottom_without_resizing(self):
        page = self._page()
        self._open_song(page)
        page.locator('#entry-song-search').focus()
        page.wait_for_selector('#entry-song-options [data-song]')
        boxes = page.evaluate("""() => {
          const d = document.querySelector('dialog[open]').getBoundingClientRect();
          const m = document.querySelector('#entry-song-menu').getBoundingClientRect();
          return {dialogH: d.height, dialogBottom: d.bottom, menuBottom: m.bottom,
                  position: getComputedStyle(document.querySelector('#entry-song-menu')).position};
        }""")
        self.assertEqual(boxes['position'], 'fixed')
        self.assertGreaterEqual(boxes['menuBottom'], boxes['dialogBottom'] - 1)
        page.locator('#entry-song-search').fill('KJ 152')
        page.wait_for_timeout(250)
        few = page.evaluate("document.querySelector('dialog[open]').getBoundingClientRect().height")
        self.assertAlmostEqual(boxes['dialogH'], few, delta=1)

    def test_fresh_pick_ticks_verse_one_only(self):
        page = self._page()
        self._open_song(page)
        self._pick(page, 'KJ 152')
        expect(page.locator('#entry-verses input[type=checkbox]')).to_have_count(12)
        checked = page.evaluate(
            "[...document.querySelectorAll('#entry-verses input')].filter(i => i.checked).length")
        self.assertEqual(checked, 1)
        expect(page.locator('[data-verses-summary]')).to_have_text('Verses 1')
        self.assertEqual(page.locator('#entry-verses input[type=checkbox]').count(), 12)

    def test_click_and_drag_preview_commit(self):
        page = self._page()
        self._open_song(page)
        self._pick(page, 'KJ 152')
        tiles = page.locator('#entry-verses .editor__verse-tile')
        tiles.nth(2).click()
        expect(tiles.nth(2).locator('input')).to_be_checked()
        expect(tiles.nth(0).locator('input')).to_be_checked()  # fresh pick keeps verse 1
        before = page.evaluate(
            "[...document.querySelectorAll('#entry-verses input')].map(i => i.checked)")
        a, b = tiles.nth(0).bounding_box(), tiles.nth(2).bounding_box()
        page.mouse.move(a['x'] + a['width'] / 2, a['y'] + a['height'] / 2)
        page.mouse.down()
        page.mouse.move(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2, steps=4)
        held = page.evaluate(
            "[...document.querySelectorAll('#entry-verses input')].map(i => i.checked)")
        self.assertEqual(held, before)
        expect(page.locator('#pvReadout, [data-verse-readout]').first).to_contain_text('Preview')
        page.mouse.up()
        checked = page.evaluate(
            "[...document.querySelectorAll('#entry-verses input')].map(i => i.checked)")
        self.assertEqual(checked[:3], [True, True, True])

    def test_hidden_and_muted_states(self):
        page = self._page()
        self._open_song(page)
        panel = page.locator('[data-verse-panel]')
        # nothing picked: the whole section, label included, is collapsed
        self.assertAlmostEqual(panel.bounding_box()['height'], 0, delta=1)
        expect(page.locator('#entry-verses-label')).to_be_hidden()
        self._pick(page, 'Kosong')
        self.assertAlmostEqual(panel.bounding_box()['height'], 0, delta=1)
        expect(page.locator('#entry-verses-label')).to_be_hidden()
        page.locator('#entry-song-search').fill('Bait Tunggal')
        page.locator('#entry-song-options [data-song]').first.click()
        expect(panel).to_be_visible()
        expect(page.locator('#entry-verses input[type=checkbox]')).to_have_count(1)
        self.assertEqual(
            page.evaluate("getComputedStyle(document.querySelector('[data-verse-tiles]')).opacity"),
            '0.45')

    def test_tile_grid_geometry_and_helper_position(self):
        page = self._page()
        self._open_song(page)
        self._pick(page, 'KJ 152')
        expect(page.locator('#entry-verses input[type=checkbox]')).to_have_count(12)
        grid = page.evaluate("""() => {
          const box = document.querySelector('#entry-verses');
          const tiles = [...box.querySelectorAll('.editor__verse-tile')];
          const quick = document.querySelector('.editor__verse-quick');
          return {
            columns: getComputedStyle(box).gridTemplateColumns.split(' ').length,
            width: Math.round(tiles[0].getBoundingClientRect().width),
            height: Math.round(tiles[0].getBoundingClientRect().height),
            row: Math.round(box.getBoundingClientRect().width),
            quickAbove: quick.getBoundingClientRect().top < box.getBoundingClientRect().top,
          };
        }""")
        self.assertEqual(grid['columns'], 5)
        panel_style = page.evaluate("""() => {
          const p = document.querySelector('[data-verse-panel]');
          const s = getComputedStyle(p);
          return { border: s.borderTopWidth, padding: s.paddingTop, radius: s.borderTopLeftRadius };
        }""")
        self.assertEqual(panel_style['border'], '1px')
        self.assertEqual(panel_style['padding'], '10px')
        self.assertEqual(panel_style['radius'], '10px')
        self.assertGreaterEqual(grid['width'], 74)
        self.assertLessEqual(grid['width'], 82)
        self.assertEqual(grid['height'], 40)
        self.assertGreaterEqual(grid['row'], 400)
        self.assertTrue(grid['quickAbove'])
        # the reveal clip is dropped once settled: no tile may be cut at rest
        page.wait_for_timeout(350)
        clip = page.evaluate("""() => {
          const inner = document.querySelector('.editor__verse-panel-inner');
          const tiles = [...document.querySelectorAll('.editor__verse-tile')];
          const last = tiles[tiles.length - 1].getBoundingClientRect();
          return { overflow: getComputedStyle(inner).overflow,
                   cut: Math.round((last.bottom - inner.getBoundingClientRect().bottom) * 10) / 10 };
        }""")
        self.assertEqual(clip['overflow'], 'visible')
        self.assertLessEqual(clip['cut'], 0.5)
        # a mouse click leaves no ring; only keyboard focus draws one
        tiles = page.locator('.editor__verse-tile')
        tiles.nth(2).click()
        ring = page.evaluate("""() => getComputedStyle(
          document.querySelectorAll('.editor__verse-tile')[2]).outlineWidth""")
        self.assertEqual(ring, '0px')
        # keyboard focus does draw one, so a sighted keyboard user can see where they are
        page.locator('#entry-song-search').focus()
        landed = False
        for _ in range(60):
            page.keyboard.press('Tab')
            landed = page.evaluate("""() => !!document.activeElement &&
              document.activeElement.type === 'checkbox' &&
              !!document.activeElement.closest('.editor__verse-tile')""")
            if landed:
                break
        self.assertTrue(landed, 'keyboard never reached a verse tile')
        self.assertEqual(page.evaluate("""() => getComputedStyle(
          document.activeElement.closest('.editor__verse-tile')).outlineWidth"""), '2px')

    def test_summary_inside_section_and_quick_states(self):
        page = self._page()
        self._open_song(page)
        self._pick(page, 'KJ 152')
        summary = page.locator('[data-verses-summary]')
        inside = page.evaluate(
            "!!document.querySelector('[data-verse-panel] [data-verses-summary]')")
        self.assertTrue(inside)
        self.assertEqual(
            summary.evaluate("el => getComputedStyle(el).borderBottomWidth"), '1px')
        all_button = page.locator('[data-verse-all]')
        clear = page.locator('[data-verse-clear]')
        page.locator('[data-verse-all]').click()
        expect(all_button).to_be_disabled()
        expect(summary).to_have_text('All verses')
        page.locator('[data-verse-clear]').click()
        expect(clear).to_be_disabled()
        expect(summary).to_have_text('No verses: keep at least one')
