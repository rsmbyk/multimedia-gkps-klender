"""Acceptance pins for the passage entry's search comboboxes (spec 238).

A separate module from test_entry_pickers.py: that suite has a backdrop race on
unmodified develop (ITEM-174), and this slice's pins must not inherit it.
"""
import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PassageSearchPickerE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
        sim_language = bible.Language.objects.create(name='Simalungun')
        sim_version = bible.Version.objects.create(
            lang=sim_language, name='Bible Simalungun', abbreviation='SIM')

        self.mat = bible.Book.objects.create(
            name='Mat', testament='new', number_of_chapters=28)
        self.mat_tb = bible.BookTranslation.objects.create(
            version=version, book=self.mat, translation='Matius')
        self.mat_sim = bible.BookTranslation.objects.create(
            version=sim_version, book=self.mat, translation='Mateus', abbreviation='Mat')
        self.kej = bible.Book.objects.create(
            name='Kej', testament='old', number_of_chapters=5)
        self.kej_tb = bible.BookTranslation.objects.create(
            version=version, book=self.kej, translation='Kejadian')
        self.kej_sim = bible.BookTranslation.objects.create(
            version=sim_version, book=self.kej, translation='1 Musa', abbreviation='1Mu')

        for translation in (self.mat_tb, self.mat_sim):
            for verse in range(1, 6):
                bible.Verse.objects.create(
                    book_translation=translation, chapter=1, verse=verse,
                    text=f'chapter one verse {verse}')
            for verse in range(1, 16):
                bible.Verse.objects.create(
                    book_translation=translation, chapter=12, verse=verse,
                    text=f'chapter twelve verse {verse}')
        for translation in (self.kej_tb, self.kej_sim):
            bible.Verse.objects.create(
                book_translation=translation, chapter=1, verse=1, text='first verse')

        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Picker', date=date(2026, 11, 24), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=self.mat_sim, chapter=1, verse_start=2)

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
        return page

    def _open(self, page, kind='scripture'):
        page.locator(f'[data-entry-open="{kind}"]').first.dispatch_event('click')
        page.wait_for_selector('dialog[open] #entry-book-search')
        page.wait_for_timeout(200)

    def _choose_book(self, page, label='Matius'):
        search = page.locator('#entry-book-search')
        search.focus()
        page.wait_for_timeout(160)
        search.fill(label)
        page.wait_for_timeout(220)
        page.locator('#entry-book-options [data-book]:not([hidden])').first.click()
        page.wait_for_function("document.querySelector('#id_book_translation').value !== ''")
        return search

    def _open_range(self, page, name):
        page.locator(f'#entry-{name}-trigger').click()
        page.wait_for_timeout(120)
        menu = page.locator(f'#entry-{name}-menu')
        expect(menu).to_be_visible()
        return menu.locator('input[type="search"]')

    def _choose_range(self, page, name, value):
        filter_box = self._open_range(page, name)
        filter_box.fill(value)
        page.wait_for_timeout(160)
        page.locator(
            f'#entry-{name}-options [data-picker-option][data-value="{value}"]:not([hidden])'
        ).first.click()

    def test_book_field_is_a_search_combo(self):
        page = self._page()
        self._open(page)
        book = page.locator('#entry-book-search')
        self.assertEqual(book.get_attribute('type'), 'search')
        book.focus()
        page.wait_for_timeout(160)
        expect(page.locator('#entry-book-menu')).to_be_visible()
        expect(page.locator('#entry-book-options [data-picker-group]:not([hidden])')).to_have_count(2)
        expect(page.locator('#entry-book-options [data-book]:not([hidden])')).to_have_count(2)
        expect(page.locator('#entry-book-menu input[type=search]')).to_have_count(0)
        page.locator('#entry-book-options [data-book]:not([hidden])').first.click()
        page.wait_for_timeout(250)
        self.assertEqual(
            page.locator('#id_book_translation').input_value(),
            str(self.mat_tb.pk))
        expect(page.locator('#entry-chapter-trigger')).to_be_enabled()

    def test_book_filter_matches_names_and_codes(self):
        page = self._page()
        self._open(page)
        book = page.locator('#entry-book-search')
        book.focus()
        book.fill('musa')
        page.wait_for_timeout(220)
        expect(page.locator('#entry-book-options [data-book]:not([hidden])')).to_have_count(1)
        book.fill('mat')
        page.wait_for_timeout(220)
        expect(page.locator('#entry-book-options [data-book]:not([hidden])')).to_have_count(1)
        book.fill('zzzz')
        page.wait_for_timeout(220)
        expect(page.locator('#entry-book-options [data-book]:not([hidden])')).to_have_count(0)
        expect(page.locator('#entry-book-options [data-picker-empty]')).to_be_visible()

    def test_choosing_a_book_keeps_the_translation_id_and_cascade(self):
        page = self._page()
        self._open(page)
        book = self._choose_book(page, 'Matius')
        self.assertEqual(book.input_value(), 'Matius')
        self.assertEqual(page.locator('#id_book_translation').input_value(), str(self.mat_tb.pk))
        expect(page.locator('#entry-chapter-trigger')).to_be_enabled()
        expect(page.locator('#entry-chapter-options [data-picker-option]')).to_have_count(28)

    def test_chapter_filter_and_choice_reload_verses(self):
        page = self._page()
        self._open(page)
        self._choose_book(page)
        expect(page.locator('#entry-chapter-trigger')).to_be_enabled()
        filter_box = self._open_range(page, 'chapter')
        filter_box.fill('12')
        page.wait_for_timeout(160)
        expect(page.locator('#entry-chapter-options [data-picker-option]:not([hidden])')).to_have_count(1)
        expect(page.locator('#entry-chapter-options [data-picker-option]:visible')).to_have_count(1)
        page.locator('#entry-chapter-options [data-picker-option][data-value="12"]:not([hidden])').click()
        self.assertEqual(page.locator('#id_chapter').input_value(), '12')
        expect(page.locator('#entry-verse_start-trigger')).to_be_enabled()
        expect(page.locator('#entry-verse_start-options [data-picker-option]')).to_have_count(15)

    def test_from_verse_filter_and_choice(self):
        page = self._page()
        self._open(page)
        self._choose_book(page)
        self._choose_range(page, 'chapter', '12')
        filter_box = self._open_range(page, 'verse_start')
        filter_box.fill('1')
        page.wait_for_timeout(160)
        visible = page.locator('#entry-verse_start-options [data-picker-option]:not([hidden])')
        expect(visible).to_have_count(7)  # 1, 10..15
        expect(page.locator('#entry-verse_start-options [data-picker-option]:visible')).to_have_count(7)
        filter_box.fill('')
        page.wait_for_timeout(160)
        page.locator(
            '#entry-verse_start-options [data-picker-option][data-value="3"]:not([hidden])'
        ).click()
        page.wait_for_timeout(160)
        self.assertEqual(page.locator('#id_verse_start').input_value(), '3')
        expect(page.locator('#entry-verse_end-trigger')).to_be_enabled()

    def test_to_verse_popover_filters_its_own_options(self):
        page = self._page()
        self._open(page)
        self._choose_book(page)
        self._choose_range(page, 'chapter', '12')
        self._choose_range(page, 'verse_start', '3')
        expect(page.locator('#entry-verse_end-trigger')).to_be_enabled()
        filter_box = self._open_range(page, 'verse_end')
        filter_box.fill('1')
        page.wait_for_timeout(160)
        expect(page.locator('#entry-verse_end-options [data-picker-option]:visible')).to_have_count(6)
        page.locator('#entry-verse_end-options [data-picker-option][data-value="10"]:not([hidden])').click()
        self.assertEqual(page.locator('#id_verse_end').input_value(), '10')

    def test_empty_query_restores_all_options(self):
        page = self._page()
        self._open(page)
        self._choose_book(page)
        filter_box = self._open_range(page, 'chapter')
        filter_box.fill('7')
        page.wait_for_timeout(160)
        expect(page.locator('#entry-chapter-options [data-picker-option]:not([hidden])')).to_have_count(3)
        expect(page.locator('#entry-chapter-options [data-picker-empty]')).to_be_hidden()
        filter_box.fill('')
        page.wait_for_timeout(160)
        expect(page.locator('#entry-chapter-options [data-picker-option]:not([hidden])')).to_have_count(28)
        expect(page.locator('#entry-chapter-options [data-picker-empty]')).to_be_hidden()

    def test_edit_shows_stored_values_in_all_three_fields(self):
        page = self._page()
        page.locator('.tatib__item--scripture [data-entry-edit]').dispatch_event('click')
        page.wait_for_selector('dialog[open] #entry-book-search')
        page.wait_for_timeout(300)
        self.assertEqual(page.locator('#entry-book-search').input_value(), 'Mateus')
        self.assertEqual(page.locator('#entry-chapter-trigger [data-picker-label]').inner_text(), '1')
        self.assertEqual(page.locator('#entry-verse_start-trigger [data-picker-label]').inner_text(), '2')
        self.assertEqual(page.locator('#id_book_translation').input_value(), str(self.mat_sim.pk))
        self.assertEqual(page.locator('#id_chapter').input_value(), '1')
        self.assertEqual(page.locator('#id_verse_start').input_value(), '2')

    def test_translation_toggle_keeps_the_cascade(self):
        page = self._page()
        self._open(page)
        self._choose_book(page, 'Matius')
        page.locator('[data-entry-translation-toggle] [data-edition-option="sim"]').click()
        page.wait_for_timeout(240)
        self.assertEqual(page.locator('#entry-book-search').input_value(), 'Mateus')
        self.assertEqual(page.locator('#id_book_translation').input_value(), str(self.mat_sim.pk))
        expect(page.locator('#entry-chapter-options [data-picker-option]')).to_have_count(28)

    def test_only_one_picker_menu_is_open_at_a_time(self):
        page = self._page()
        self._open(page)
        self._choose_book(page)
        open_menus = (".editor__picker-menu:not([hidden])")

        def assert_one(expected_id):
            page.wait_for_timeout(120)
            expect(page.locator(open_menus)).to_have_count(1)
            self.assertEqual(
                page.locator(open_menus).first.get_attribute('id'), expected_id)

        page.locator('#entry-book-search').focus()
        assert_one('entry-book-menu')
        page.locator('#entry-chapter-trigger').dispatch_event('click')
        assert_one('entry-chapter-menu')
        chapter_filter = page.locator('#entry-chapter-menu input[type="search"]')
        chapter_filter.fill('1')
        page.wait_for_timeout(160)
        page.locator('#entry-chapter-options [data-picker-option][data-value="1"]:not([hidden])').click()
        page.locator('#entry-verse_end-trigger').dispatch_event('click')
        assert_one('entry-verse_end-menu')
        page.locator('#entry-verse_start-trigger').dispatch_event('click')
        assert_one('entry-verse_start-menu')
        self.assertEqual(
            page.locator('#entry-verse_end-trigger').get_attribute('aria-expanded'), 'false')

    def test_tab_from_book_chooses_and_moves_focus(self):
        page = self._page()
        self._open(page)
        book = page.locator('#entry-book-search')
        book.focus()
        book.fill('mat')
        page.wait_for_timeout(220)
        book.press('Tab')
        page.wait_for_timeout(300)
        self.assertEqual(page.locator('#id_book_translation').input_value(), str(self.mat_tb.pk))
        expect(page.locator('#entry-chapter-trigger')).to_be_focused()

    def test_tab_from_chapter_filter_chooses_first_visible_and_moves_focus(self):
        page = self._page()
        self._open(page)
        self._choose_book(page)
        filter_box = self._open_range(page, 'chapter')
        filter_box.fill('12')
        page.wait_for_timeout(160)
        filter_box.press('Tab')
        page.wait_for_timeout(300)
        self.assertEqual(page.locator('#id_chapter').input_value(), '12')
        expect(page.locator('#entry-verse_start-trigger')).to_be_focused()

    def test_keyboard_and_dismissal_match_the_song_picker(self):
        page = self._page()
        self._open(page)
        book = page.locator('#entry-book-search')
        book.focus()
        page.wait_for_timeout(160)
        book.press('ArrowDown')
        expect(page.locator('#entry-book-options [data-book].is-active')).to_have_count(1)
        book.press('Enter')
        page.wait_for_timeout(250)
        self.assertNotEqual(page.locator('#id_book_translation').input_value(), '')
        expect(page.locator('#entry-book-menu')).to_be_hidden()
        expect(page.locator('dialog[open]')).to_have_count(1)

        page.locator('#editorTitle').click()   # take focus off the field
        book.focus()
        page.wait_for_timeout(120)
        expect(page.locator('#entry-book-menu')).to_be_visible()
        before = book.input_value()
        book.press('Escape')
        page.wait_for_timeout(80)
        expect(page.locator('#entry-book-menu')).to_be_hidden()
        self.assertEqual(book.input_value(), before)
        expect(page.locator('dialog[open]')).to_have_count(1)

        self._choose_range(page, 'chapter', '1')
        page.locator('#entry-verse_start-trigger').click()
        page.wait_for_timeout(120)
        expect(page.locator('#entry-verse_start-menu')).to_be_visible()
        page.locator('#editorTitle').click()
        page.wait_for_timeout(80)
        expect(page.locator('#entry-verse_start-menu')).to_be_hidden()
        self.assertEqual(page.locator('#entry-verse_start-trigger').get_attribute('aria-expanded'), 'false')
