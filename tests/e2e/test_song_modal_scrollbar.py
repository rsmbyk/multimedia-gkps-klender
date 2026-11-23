"""The shared editor dialog's own edge (spec 236).

The dialog used to keep the browser's UA ``overflow: auto``. The collapsed song-entry
Verses panel left 10px of clipped content past the dialog box, so the *dialog* grew a
scrollbar even though ``.editor__content`` was the intended scrollport. These tests
measure the two boxes separately in both entry modes and on tall forms.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const d = document.querySelector('#editorModal');
  const c = d && d.querySelector('.editor__content');
  const box = el => {
    if (!el) return null;
    const s = getComputedStyle(el);
    return {
      clientH: el.clientHeight,
      scrollH: el.scrollHeight,
      gutter: el.offsetWidth - el.clientWidth,
      scrollTop: el.scrollTop,
      overflowY: s.overflowY,
      width: Math.round(el.getBoundingClientRect().width),
    };
  };
  return {dialog: box(d), content: box(c)};
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongModalScrollbarE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        book = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        self.with_verses = songs.Song.objects.create(book=book, number=1, title='With verses')
        for number in range(1, 121):
            songs.Verse.objects.create(song=self.with_verses, number=number,
                                       lyric=f'bait {number}')
        self.no_verses = songs.Song.objects.create(book=book, number=2, title='No verses')
        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Uji', date=date(2026, 11, 24), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.SONG,
            song=self.with_verses)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.SONG,
            song=self.no_verses)
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.contexts = []

    def tearDown(self):
        for context in self.contexts:
            context.close()
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self, width=1366, height=900):
        context = self.browser.new_context(viewport={'width': width, 'height': height})
        self.contexts.append(context)
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        page.wait_for_load_state('networkidle')
        page.evaluate("document.documentElement.dataset.theme = 'dark'")
        return page

    def _open_new_song(self, page):
        page.locator('.entry__add-btn[data-entry-open="song"]').first.dispatch_event('click')
        page.wait_for_selector('#editorModal[open] .editor__form[data-entry-mode="new"]')

    def _open_edit_song(self, page, empty=False):
        row = page.locator('.tatib__item--song').filter(
            has_text='No verses' if empty else 'With verses')
        row.locator('[data-entry-edit]').first.dispatch_event('click')
        page.wait_for_selector('#editorModal[open] .editor__form[data-entry-mode="edit"]')
        if empty:
            page.wait_for_selector('#editorModal [data-verse-panel][hidden]', state='attached')
        else:
            page.wait_for_selector('#editorModal [data-verse-panel][data-settled="true"]')

    def _open_large_text_form(self, page):
        # A song with enough verse tiles makes the form taller than the dialog cap, so
        # .editor__content — not a textarea — has to be the scrollport.
        self._open_edit_song(page, empty=False)

    def _measure(self, page):
        return page.evaluate(MEASURE)

    def _wheel_dialog(self, page):
        box = page.locator('#editorModal').bounding_box()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        page.mouse.wheel(0, 240)
        page.wait_for_timeout(200)

    def _wheel_content(self, page):
        box = page.locator('.editor__content').bounding_box()
        page.mouse.move(box['x'] + box['width'] - 8, box['y'] + box['height'] / 2)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(200)

    # --- US1: New song -------------------------------------------------------

    def test_new_song_dialog_has_no_scrollbar_gutter(self):
        page = self._page()
        self._open_new_song(page)
        measured = self._measure(page)
        self.assertEqual(measured['dialog']['gutter'], 0)
        self.assertEqual(measured['dialog']['overflowY'], 'clip')
        self.assertEqual(measured['dialog']['width'], 480)
        self.assertEqual(measured['content']['overflowY'], 'auto')

    def test_new_song_wheel_does_not_scroll_the_dialog(self):
        page = self._page()
        self._open_new_song(page)
        self._wheel_dialog(page)
        measured = self._measure(page)
        self.assertEqual(measured['dialog']['scrollTop'], 0)
        page.eval_on_selector('#editorModal', 'el => { el.scrollTop = 60; }')
        self.assertEqual(self._measure(page)['dialog']['scrollTop'], 0)

    def test_new_song_results_menu_still_escapes_the_dialog(self):
        page = self._page()
        self._open_new_song(page)
        before = page.locator('#editorModal').bounding_box()
        page.fill('#entry-song-search', 'With')
        page.wait_for_selector('#entry-song-menu:not([hidden])')
        menu = page.locator('#entry-song-menu').bounding_box()
        after = page.locator('#editorModal').bounding_box()
        position = page.eval_on_selector('#entry-song-menu', 'el => getComputedStyle(el).position')
        self.assertEqual(position, 'fixed')
        self.assertGreaterEqual(menu['y'], 0)
        self.assertLessEqual(menu['y'] + menu['height'], 900)
        self.assertEqual(round(after['height']), round(before['height']))
        self.assertEqual(round(after['width']), round(before['width']))

    # --- US2: Edit song ------------------------------------------------------

    def test_edit_song_collapsed_verses_has_no_scrollbar(self):
        page = self._page()
        self._open_edit_song(page, empty=True)
        self._wheel_dialog(page)
        measured = self._measure(page)
        self.assertEqual(measured['dialog']['gutter'], 0)
        self.assertEqual(measured['dialog']['overflowY'], 'clip')
        self.assertEqual(measured['dialog']['scrollTop'], 0)

    def test_edit_song_with_verses_keeps_its_box(self):
        page = self._page()
        self._open_edit_song(page, empty=False)
        measured = self._measure(page)
        self.assertEqual(measured['dialog']['gutter'], 0)
        self.assertEqual(measured['dialog']['clientH'], measured['content']['clientH'])
        self.assertEqual(measured['dialog']['width'], 480)

    # --- US3: the content wrapper still scrolls -------------------------------

    def test_large_form_scrolls_inside_content(self):
        page = self._page()
        self._open_large_text_form(page)
        before = self._measure(page)
        self.assertGreater(before['content']['scrollH'], before['content']['clientH'])
        self._wheel_content(page)
        measured = self._measure(page)
        self.assertGreater(measured['content']['scrollTop'], 0)
        self.assertEqual(measured['dialog']['scrollTop'], 0)
        self.assertEqual(measured['dialog']['gutter'], 0)

    def test_short_viewport_scrolls_inside_content(self):
        page = self._page(width=900, height=600)
        self._open_large_text_form(page)
        before = self._measure(page)
        self.assertGreater(before['content']['scrollH'], before['content']['clientH'])
        self._wheel_content(page)
        measured = self._measure(page)
        self.assertGreater(measured['content']['scrollTop'], 0)
        self.assertEqual(measured['dialog']['scrollTop'], 0)
        self.assertEqual(measured['dialog']['gutter'], 0)
