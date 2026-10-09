"""The entry modal's picker menus (spec 040).

The book and song menus are capped to the VIEWPORT, not the dialog: they may
overlap the dialog's edge, they never leave the window, and they stay anchored to
their trigger while the dialog's content scrolls.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
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
class EntryPickerE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        self.mat_tb = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        sim_language = bible.Language.objects.create(name='Simalungun')
        sim_version = bible.Version.objects.create(
            lang=sim_language, name='Bible Simalungun', abbreviation='SIM')
        self.mat_sim = bible.BookTranslation.objects.create(
            version=sim_version, book=book, translation='Mateus')
        bible.Verse.objects.create(
            book_translation=self.mat_tb, chapter=1, verse=1, text='Pada mulanya')
        bible.Verse.objects.create(
            book_translation=self.mat_sim, chapter=1, verse=7, text='Na parjolo')

        self.songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                                  is_hymn_book=True)
        self.song = songs.Song.objects.create(
            book=self.songbook, number=152, title='Ada Kuasa')
        for number in (1, 2):
            songs.Verse.objects.create(song=self.song, number=number, lyric=f'bait {number}')

        haleluya = songs.Book.objects.create(
            name='Haleluya', short_name='HAL', is_hymn_book=True)
        zeta = songs.Book.objects.create(name='Zeta Songs')
        alpha = songs.Book.objects.create(name='Alpha Songs')
        for number, sub_number, title in (
                (4, 'B', 'Number Four B'), (4, 'a', 'Number Four A'),
                (2, '', 'Number Two'), (None, 'a', 'Unnumbered Z'),
                (None, 'z', 'Unnumbered A')):
            songs.Song.objects.create(
                book=self.songbook, number=number, sub_number=sub_number, title=title)
        songs.Song.objects.create(book=haleluya, number=1, title='Hal Song')
        songs.Song.objects.create(book=zeta, number=1, title='Zulu Song')
        songs.Song.objects.create(book=zeta, number=2, title='Aardvark Song')
        songs.Song.objects.create(book=alpha, number=2, title='Beta Song')
        songs.Song.objects.create(book=alpha, number=1, title='Alpha Song')

        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')
        self.sim_entry = tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=self.mat_sim, chapter=1, verse_start=7)
        if self._testMethodName == 'test_non_tb_fallback_book_remains_selectable_in_tb_state':
            language = bible.Language.objects.create(name='Alternate')
            version = bible.Version.objects.create(
                lang=language, name='Alternate Version', abbreviation='ALT')
            book = bible.Book.objects.create(name='Luk', testament='new', number_of_chapters=1)
            self.fallback_translation = bible.BookTranslation.objects.create(
                version=version, book=book, translation='Lukas Alternatif')
            bible.Verse.objects.create(
                book_translation=self.fallback_translation, chapter=1, verse=1,
                text='Ayat alternatif')
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

    def _page(self, height=900):
        context = self.browser.new_context(viewport={'width': 1200, 'height': height})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def _open_modal(self, page, kind):
        item = page.locator('.tatib__item').first
        item.hover()
        page.locator(f'[data-entry-open="{kind}"]').first.click()
        page.wait_for_selector('dialog[open]')

    def _menu_geometry(self, page, picker):
        return page.evaluate("""pickerName => {
          const menu = document.querySelector(`[data-entry-picker="${pickerName}"] .editor__picker-menu`);
          const trigger = document.querySelector(`[data-entry-picker="${pickerName}"] [data-picker-trigger], [data-entry-picker="${pickerName}"] [data-verses-trigger]`);
          const m = menu.getBoundingClientRect(), t = trigger.getBoundingClientRect();
          const content = document.getElementById('editorContent').getBoundingClientRect();
          return {position: getComputedStyle(menu).position, gap: m.top - t.bottom,
                  top: m.top, bottom: m.bottom, left: m.left, right: m.right,
                  contentBottom: content.bottom,
                  windowWidth: window.innerWidth, windowHeight: window.innerHeight};
        }""", picker)

    def test_book_picker_shows_tb_and_sim_once_and_keeps_primary_translation(self):
        page = self._page()
        self._open_modal(page, 'scripture')
        picker = page.locator('[data-entry-picker="book"]')
        picker.locator('[data-picker-trigger]').click()

        options = picker.locator('[data-picker-options] [data-book]')
        expect(options).to_have_count(1)
        option = options.first
        expect(option.locator('.book__n')).to_have_text('Matius')
        expect(option.locator('.book__s')).to_have_text('Mateus')
        layout = option.evaluate("""button => {
          const main = button.querySelector('.book__n').getBoundingClientRect();
          const secondary = button.querySelector('.book__s').getBoundingClientRect();
          const style = getComputedStyle(button);
          return {mainRight: main.right, secondaryLeft: secondary.left,
                  secondaryRight: secondary.right, optionRight: button.getBoundingClientRect().right,
                  paddingRight: parseFloat(style.paddingRight),
                  mainColor: getComputedStyle(button.querySelector('.book__n')).color,
                  secondaryColor: getComputedStyle(button.querySelector('.book__s')).color};
        }""")
        self.assertLessEqual(layout['mainRight'], layout['secondaryLeft'])
        self.assertAlmostEqual(layout['optionRight'] - layout['secondaryRight'],
                               layout['paddingRight'], delta=3)
        self.assertNotEqual(layout['mainColor'], layout['secondaryColor'])
        filter_box = picker.locator('input[type="search"]')
        filter_box.fill('Mateus')
        expect(option).to_be_visible()
        filter_box.fill('Matius')
        expect(option).to_be_visible()
        filter_box.fill('missing')
        expect(option).to_be_hidden()
        filter_box.fill('')
        option.click()

        expect(page.locator('[name=book_translation]')).to_have_value(str(self.mat_tb.pk))
        expect(page.locator('[name=chapter]')).to_have_value('1')
        expect(page.locator('[name=verse_start]')).to_have_value('1')

    def test_editing_a_sim_passage_keeps_the_saved_translation_in_the_picker(self):
        page = self._page()
        edit = page.locator(f'[data-entry-edit="{self.sim_entry.pk}"]')
        edit.hover()
        edit.click()

        picker = page.locator('[data-entry-picker="book"]')
        option = picker.locator('[data-picker-options] [data-book]')
        expect(option).to_have_count(1)
        expect(option).to_have_attribute('aria-selected', 'true')
        expect(picker.locator('[data-picker-label]')).to_have_text('Mateus')
        expect(page.locator('[name=book_translation]')).to_have_value(str(self.mat_sim.pk))
        expect(page.locator('[name=chapter]')).to_have_value('1')
        expect(page.locator('[name=verse_start] option')).to_have_count(1)
        expect(page.locator('[name=verse_start]')).to_have_value('7')

    def test_translation_toggle_switches_selected_book_without_refetching_verses(self):
        page = self._page()
        edit = page.locator(f'[data-entry-edit="{self.sim_entry.pk}"]')
        edit.hover()
        edit.click()

        toggle = page.locator('[data-entry-translation-toggle]')
        expect(toggle).to_be_visible()
        toggle_box = toggle.bounding_box()
        label_box = page.locator('#entry-book-label').bounding_box()
        head_box = page.locator('.editor__field-head').bounding_box()
        assert toggle_box is not None
        assert label_box is not None
        assert head_box is not None
        self.assertGreaterEqual(toggle_box['x'] - label_box['x'] - label_box['width'], 8)
        self.assertLessEqual(toggle_box['x'] + toggle_box['width'],
                             head_box['x'] + head_box['width'])
        expect(toggle).to_have_attribute('data-edition', 'sim')
        expect(toggle.locator('[data-edition-option="sim"]')).to_have_attribute(
            'aria-pressed', 'true')
        option = page.locator('[data-entry-picker="book"] [data-book][aria-selected="true"]')
        expect(option.locator('.book__n')).to_have_text('Mateus')
        expect(option.locator('.book__s')).to_have_text('Matius')
        before = page.evaluate("""() => ['chapter', 'verse_start', 'verse_end'].map(name => {
          const node = document.querySelector(`[name="${name}"]`);
          return [name, {value: node.value, disabled: node.disabled,
            options: Array.from(node.options, option => [option.value, option.textContent])}];
        })""")
        chapter_requests = []
        page.on('request', lambda request: chapter_requests.append(request.url)
                if '/editor/entry/chapter/' in request.url else None)

        toggle.locator('[data-edition-option="tb"]').click()

        expect(toggle).to_have_attribute('data-edition', 'tb')
        expect(toggle.locator('[data-edition-option="tb"]')).to_have_attribute(
            'aria-pressed', 'true')
        expect(page.locator('[name=book_translation]')).to_have_value(str(self.mat_tb.pk))
        expect(page.locator('[data-picker-label]')).to_have_text('Matius')
        expect(option.locator('.book__n')).to_have_text('Matius')
        expect(option.locator('.book__s')).to_have_text('Mateus')
        after = page.evaluate("""() => ['chapter', 'verse_start', 'verse_end'].map(name => {
          const node = document.querySelector(`[name="${name}"]`);
          return [name, {value: node.value, disabled: node.disabled,
            options: Array.from(node.options, option => [option.value, option.textContent])}];
        })""")
        self.assertEqual(after, before)
        self.assertEqual(chapter_requests, [])

    def test_new_passage_toggle_selects_sim_translation_for_a_book(self):
        page = self._page()
        self._open_modal(page, 'scripture')
        toggle = page.locator('[data-entry-translation-toggle]')
        expect(toggle).to_be_visible()
        expect(toggle).to_have_attribute('data-edition', 'tb')
        toggle.locator('[data-edition-option="sim"]').click()
        expect(toggle).to_have_attribute('data-edition', 'sim')

        picker = page.locator('[data-entry-picker="book"]')
        picker.locator('[data-picker-trigger]').click()
        option = picker.locator('[data-book-name-sim="Mateus"]')
        expect(option.locator('.book__n')).to_have_text('Mateus')
        expect(option.locator('.book__s')).to_have_text('Matius')
        filter_box = picker.locator('input[type="search"]')
        filter_box.fill('Matius')
        expect(option).to_be_visible()
        filter_box.fill('Mateus')
        expect(option).to_be_visible()
        filter_box.fill('')
        option.click()

        expect(page.locator('[name=book_translation]')).to_have_value(str(self.mat_sim.pk))
        expect(page.locator('[data-picker-label]')).to_have_text('Mateus')
        expect(page.locator('[name=chapter]')).to_have_value('1')
        expect(page.locator('[name=verse_start]')).to_have_value('7')

    def test_non_tb_fallback_book_remains_selectable_in_tb_state(self):
        translation = self.fallback_translation
        page = self._page()
        self._open_modal(page, 'scripture')

        picker = page.locator('[data-entry-picker="book"]')
        picker.locator('[data-picker-trigger]').click()
        option = picker.locator(f'[data-book="{translation.pk}"]')
        expect(option).to_be_enabled()
        expect(option.locator('.book__n')).to_have_text('Lukas Alternatif')
        option.click()

        expect(page.locator('[name=book_translation]')).to_have_value(str(translation.pk))
        expect(page.locator('[name=chapter]')).to_have_value('1')
        expect(page.locator('[name=verse_start]')).to_have_value('1')

    def test_song_picker_sorts_and_labels_by_songbook_type(self):
        page = self._page()
        self._open_modal(page, 'song')
        picker = page.locator('[data-entry-picker="song"]')
        picker.locator('[data-picker-trigger]').click()
        options = page.locator('#entry-song-options [data-song]')
        expect(options).to_have_count(11)
        groups = page.locator('#entry-song-options .editor__songgroup-label')
        expect(groups).to_have_text([
            'Kidung Jemaat', 'Haleluya', 'Alpha Songs', 'Zeta Songs'])
        labels = options.evaluate_all(
            "nodes => nodes.map(node => node.innerText.replace(/\\s+/g, ' ').trim())")
        self.assertEqual(labels, [
            'KJ 2 Number Two', 'KJ 4A Number Four A', 'KJ 4B Number Four B',
            'KJ 152 Ada Kuasa', 'KJ Unnumbered A', 'KJ Unnumbered Z',
            'HAL 1 Hal Song', 'Alpha Song', 'Beta Song', 'Aardvark Song', 'Zulu Song',
        ])
        options.first.click()
        expect(picker.locator('[data-picker-label]')).to_have_text('Number Two')

    def test_the_book_menu_is_capped_to_the_viewport_not_the_dialog(self):
        page = self._page()
        self._open_modal(page, 'scripture')
        page.locator('[data-entry-picker="book"] [data-picker-trigger]').click()
        expect(page.locator('[data-entry-picker="book"] .editor__picker-menu')).to_be_visible()
        geometry = self._menu_geometry(page, 'book')
        self.assertEqual(geometry['position'], 'fixed')
        self.assertAlmostEqual(geometry['gap'], 6, delta=2)          # anchored to its trigger
        self.assertGreaterEqual(geometry['left'], -1)
        self.assertLessEqual(geometry['right'], geometry['windowWidth'] + 1)
        self.assertGreaterEqual(geometry['top'], -1)
        self.assertLessEqual(geometry['bottom'], geometry['windowHeight'] + 1)

    def test_the_song_menu_is_capped_to_the_viewport_not_the_dialog(self):
        page = self._page()
        self._open_modal(page, 'song')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()
        expect(page.locator('[data-entry-picker="song"] .editor__picker-menu')).to_be_visible()
        geometry = self._menu_geometry(page, 'song')
        self.assertEqual(geometry['position'], 'fixed')
        self.assertLessEqual(geometry['bottom'], geometry['windowHeight'] + 1)

    def test_the_menu_follows_the_dialog_content_scroll(self):
        page = self._page(height=420)
        self._open_modal(page, 'scripture')
        page.add_style_tag(content='''#editorContent { height: 120px !important;
            max-height: 120px !important; flex: 0 0 120px !important; }''')
        page.locator('[data-entry-picker="book"] [data-picker-trigger]').click()
        menu = page.locator('[data-entry-picker="book"] .editor__picker-menu')
        expect(menu).to_be_visible()
        before = self._menu_geometry(page, 'book')
        page.locator('#editorContent').evaluate('el => { el.scrollTop = el.scrollHeight; }')
        page.wait_for_timeout(200)
        after = self._menu_geometry(page, 'book')
        self.assertAlmostEqual(after['gap'], 6, delta=3)             # still anchored
        self.assertNotAlmostEqual(before['top'], after['top'], places=0)   # it followed
        self.assertLessEqual(after['bottom'], after['windowHeight'] + 1)
