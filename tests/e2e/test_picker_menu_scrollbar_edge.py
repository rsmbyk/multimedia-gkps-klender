"""The picker popout's scrollbar reaches the menu edge (spec 244).

The menu's 8px padding used to stand between its border and the options scrollport, so
Chromium painted the 5px bar inside the panel. These pins measure the two boxes and keep
the option and filter content where it was.
"""
import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const box = el => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {
      x: +r.x.toFixed(1), y: +r.y.toFixed(1),
      right: +r.right.toFixed(1), bottom: +r.bottom.toFixed(1),
      h: +r.height.toFixed(1), cw: el.clientWidth, ch: el.clientHeight,
      sh: el.scrollHeight, gutter: el.offsetWidth - el.clientWidth,
    };
  };
  const menu = document.querySelector('.editor__picker-menu:not([hidden])');
  const options = menu && menu.querySelector('.editor__picker-options');
  return {
    menu: box(menu), options: box(options),
    first: box(options && options.querySelector('[role=option]')),
    filter: box(menu && menu.querySelector('input')),
    overflow: menu && getComputedStyle(menu).overflow,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PickerMenuScrollbarEdgeE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=lang, name='Terjemahan Baru', abbreviation='TB')

        # Enough books to overflow the Book menu's viewport-capped box.
        for number in range(30):
            book = bible.Book.objects.create(
                name=f'B{number:02d}', testament='old', number_of_chapters=1)
            bible.BookTranslation.objects.create(
                version=version, book=book, translation=f'Kitab {number:02d}')

        # A long book overflows the Chapter menu; 40 verses overflow the verse menu.
        self.long_book = bible.Book.objects.create(
            name='Kej', testament='old', number_of_chapters=40)
        long_translation = bible.BookTranslation.objects.create(
            version=version, book=self.long_book, translation='Kejadian')
        for chapter in range(1, 41):
            bible.Verse.objects.create(
                book_translation=long_translation, chapter=chapter, verse=1,
                text=f'chapter {chapter} verse 1')
        for number in range(2, 41):
            bible.Verse.objects.create(
                book_translation=long_translation, chapter=1, verse=number,
                text=f'chapter one verse {number}')

        # A one-chapter book gives a menu that cannot draw a bar.
        short_book = bible.Book.objects.create(
            name='Obj', testament='old', number_of_chapters=1)
        short_translation = bible.BookTranslation.objects.create(
            version=version, book=short_book, translation='Obaja')
        bible.Verse.objects.create(
            book_translation=short_translation, chapter=1, verse=1,
            text='only verse')

        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Scrollbar', date=date(2026, 11, 26), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')

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

    def _page(self):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        page.wait_for_load_state('networkidle')
        page.locator('[data-entry-open="scripture"]').first.dispatch_event('click')
        page.wait_for_selector('dialog[open] #entry-book-search')
        page.wait_for_timeout(150)
        return page

    def _open_book_menu(self, page, label=None):
        search = page.locator('#entry-book-search')
        search.click()
        page.wait_for_selector('.editor__picker-menu:not([hidden])')
        if label:
            search.fill(label)
            page.wait_for_timeout(200)
        return search

    def _choose_book(self, page, label):
        self._open_book_menu(page, label)
        page.locator('#entry-book-options [data-book]:not([hidden])').first.click()
        page.wait_for_function("document.querySelector('#id_book_translation').value !== ''")
        page.wait_for_timeout(100)

    def _open_range(self, page, name):
        page.locator(f'#entry-{name}-trigger').click()
        page.wait_for_selector(f'#entry-{name}-menu:not([hidden])')
        page.wait_for_timeout(100)

    def _measure(self, page):
        return page.evaluate(MEASURE)

    def assert_menu_edge(self, measured):
        menu, options = measured['menu'], measured['options']
        self.assertEqual(menu['right'] - options['right'], 1)
        self.assertEqual(round(menu['bottom'] - options['bottom']), 1)

    # --- US1: the bar is the menu's edge -------------------------------------

    def test_scrollport_reaches_menu_edges(self):
        page = self._page()
        self._open_book_menu(page)
        measured = self._measure(page)
        self.assertGreater(measured['options']['sh'], measured['options']['ch'])
        # Base: the 8px padding left the bar 9px (8px + 1px border) inside.
        self.assert_menu_edge(measured)

    def test_scrollport_reaches_menu_edges_for_all_pickers(self):
        page = self._page()
        for name in ('chapter', 'verse_start'):
            page.close()
            page = self._page()
            self._choose_book(page, 'Kejadian')
            self._open_range(page, name)
            measured = self._measure(page)
            self.assertGreater(measured['options']['sh'], measured['options']['ch'])
            self.assert_menu_edge(measured)
            filter_box = measured['filter']
            self.assertAlmostEqual(filter_box['x'], measured['menu']['x'] + 9, delta=1)
            self.assertAlmostEqual(measured['menu']['right'] - filter_box['right'], 9, delta=1)

    # --- US2: nothing but the lane moves -------------------------------------

    def test_option_and_filter_boxes_are_unchanged(self):
        page = self._page()
        self._open_book_menu(page)
        measured = self._measure(page)
        first = measured['first']
        # Frozen at 1440×900 from the unmodified base, before the margin/padding swap.
        self.assertEqual(first['x'], 511)
        self.assertEqual(first['right'], 929)
        self.assertAlmostEqual(first['y'], 464.1, delta=1)
        self.assertAlmostEqual(first['bottom'], 503.1, delta=1)

        # Fresh page for the chapter measurement; Escape-then-reopen is a different path.
        page.close()
        page = self._page()
        self._choose_book(page, 'Kejadian')
        self._open_range(page, 'chapter')
        chapter = self._measure(page)
        self.assertEqual(chapter['filter']['x'], 511)
        self.assertEqual(chapter['filter']['right'], 929)
        self.assertAlmostEqual(chapter['filter']['y'], 510.1, delta=1)
        self.assertAlmostEqual(chapter['filter']['bottom'], 548.1, delta=1)

    def test_one_option_menu_has_no_scrollbar_lane(self):
        page = self._page()
        self._choose_book(page, 'Obaja')
        self._open_range(page, 'chapter')
        measured = self._measure(page)
        self.assertEqual(measured['options']['sh'], measured['options']['ch'])
        self.assertEqual(measured['options']['gutter'], 0)
        self.assert_menu_edge(measured)
