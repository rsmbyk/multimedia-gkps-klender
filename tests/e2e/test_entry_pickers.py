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
            version=sim_version, book=book, translation='Mateus', abbreviation='Mat')
        if self._testMethodName in {
                'test_book_picker_accepts_tb_and_sim_codes_and_updates_testament_labels',
                'test_edit_passage_picker_accepts_sim_code_and_testament_labels'}:
            self.kej = bible.Book.objects.create(
                name='Kej', testament='old', number_of_chapters=50)
            self.kej_tb = bible.BookTranslation.objects.create(
                version=version, book=self.kej, translation='Kejadian')
            self.kej_sim = bible.BookTranslation.objects.create(
                version=sim_version, book=self.kej, translation='1 Musa', abbreviation='1Mu')
            bible.Verse.objects.create(
                book_translation=self.kej_tb, chapter=1, verse=1, text='TB first verse')
            bible.Verse.objects.create(
                book_translation=self.kej_sim, chapter=1, verse=1, text='SIM first verse')
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
        if self._testMethodName in {
                'test_song_picker_searches_by_short_and_full_songbook_reference',
                'test_song_picker_reference_can_include_the_title',
                'test_song_picker_searches_by_reference_when_editing'}:
            self.short_reference_song = songs.Song.objects.create(
                book=self.songbook, number=123, title='Short Reference Target')
            self.full_reference_song = songs.Song.objects.create(
                book=self.songbook, number=235, title='Reference Title Target')
            other_book = songs.Book.objects.create(
                name='Other Hymns', short_name='OH', is_hymn_book=True)
            self.same_title_other_song = songs.Song.objects.create(
                book=other_book, number=9, title='Reference Title Target')

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
        if self._testMethodName == 'test_song_picker_filters_songs_by_songbook_name':
            self.hal_song = songs.Song.objects.get(book=haleluya, title='Hal Song')
            self.titled_song = songs.Song.objects.create(
                book=zeta, number=3, title='Kidung Malam')
            self.kj_songs = list(songs.Song.objects.filter(book=self.songbook))

        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia')
        self.sim_entry = tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=2, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=self.mat_sim, chapter=1, verse_start=7)
        if self._testMethodName == 'test_edit_passage_picker_accepts_sim_code_and_testament_labels':
            self.kej_entry = tatib.ServiceEntry.objects.create(
                tatib=self.tatib, order_number=3, kind=tatib.ServiceEntryKind.SCRIPTURE,
                book_translation=self.kej_sim, chapter=1, verse_start=1)
        if self._testMethodName == 'test_song_picker_searches_by_reference_when_editing':
            self.reference_entry = tatib.ServiceEntry.objects.create(
                tatib=self.tatib, order_number=3, kind=tatib.ServiceEntryKind.SONG,
                song=self.full_reference_song, verses=[1, 2])
        if self._testMethodName == 'test_song_picker_reference_number_prefix_includes_sub_number':
            self.kj_prefix_songs = {
                number: songs.Song.objects.create(
                    book=self.songbook, number=number, title=f'KJ Number {number}')
                for number in (12, 120, 123, 129, 130)}
            self.kj_subnumber_a = songs.Song.objects.create(
                book=self.songbook, number=12, sub_number='a', title='KJ Twelve A')
            self.kj_subnumber_b = songs.Song.objects.create(
                book=self.songbook, number=12, sub_number='b', title='KJ Twelve B')
            self.pkj = songs.Book.objects.create(
                name='Pelengkap Kidung Jemaat', short_name='PKJ', is_hymn_book=True)
            self.pkj_prefix_songs = {
                number: songs.Song.objects.create(
                    book=self.pkj, number=number, title=f'PKJ Number {number}')
                for number in (12, 123)}
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
        if self._testMethodName == 'test_book_picker_filter_hides_nonmatching_books_and_restores_all':
            markus = bible.Book.objects.create(name='Mrk', testament='new', number_of_chapters=16)
            bible.BookTranslation.objects.create(
                version=version, book=markus, translation='Markus')
            bible.BookTranslation.objects.create(
                version=sim_version, book=markus, translation='Markus Simalungun')
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

    def _wait_for_song_options(self, page, songs):
        expected_ids = sorted(str(song.pk) for song in songs)
        page.wait_for_function(
            """expected => {
              const actual = Array.from(document.querySelectorAll('#entry-song-options [data-song]'))
                .map(option => option.dataset.song).sort();
              return JSON.stringify(actual) === JSON.stringify(expected);
            }""",
            arg=expected_ids,
            timeout=5000)

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

    def test_passage_form_layout_fits_modal_at_narrow_viewport(self):
        home_url = self.live_server_url + reverse('web-index')
        service_path = reverse('web-tatib-service', args=[self.tatib.pk])

        for width, height, range_stacks in ((536, 426, False), (320, 720, True),
                                            (1200, 900, False)):
            with self.subTest(width=width, height=height):
                context = self.browser.new_context(viewport={'width': width, 'height': height})
                page = context.new_page()
                try:
                    page.goto(home_url)
                    page.wait_for_load_state('networkidle')
                    page.locator('[data-panel="tatib"]').click()
                    page.locator(f'.book[href="{service_path}"]').click()
                    page.wait_for_function(
                        "document.querySelector('#readName').textContent.trim() === 'Ibadah Minggu'")
                    page.locator('[data-panel="tatib"]').click()
                    page.wait_for_function(
                        "document.documentElement.dataset.nav === 'closed'")
                    self._open_modal(page, 'scripture')

                    for name in ('Book', 'Chapter', 'From verse', 'To verse'):
                        expect(page.get_by_role('button', name=name)).to_be_visible()

                    layout = page.evaluate("""() => {
                      const rect = element => {
                        const r = element.getBoundingClientRect();
                        return {left: r.left, right: r.right, top: r.top, bottom: r.bottom,
                                width: r.width, height: r.height};
                      };
                      const content = document.querySelector('#editorContent');
                      const contentRect = rect(content);
                      const style = getComputedStyle(content);
                      const left = contentRect.left + content.clientLeft +
                        parseFloat(style.paddingLeft);
                      const right = contentRect.right - parseFloat(style.paddingRight);
                      const byId = id => rect(document.getElementById(id));
                      return {
                        innerLeft: left,
                        innerRight: right,
                        contentScrollWidth: content.scrollWidth,
                        contentClientWidth: content.clientWidth,
                        contentScrollHeight: content.scrollHeight,
                        contentClientHeight: content.clientHeight,
                        modalScrollWidth: document.querySelector('#editorModal').scrollWidth,
                        modalClientWidth: document.querySelector('#editorModal').clientWidth,
                        pageScrollWidth: document.documentElement.scrollWidth,
                        windowWidth: window.innerWidth,
                        toggle: rect(document.querySelector('[data-entry-translation-toggle]')),
                        bookLabel: byId('entry-book-label'),
                        bookTrigger: byId('entry-book-trigger'),
                        chapterLabel: byId('entry-chapter-label'),
                        chapterTrigger: byId('entry-chapter-trigger'),
                        chapterField: rect(document.querySelector('.editor__row .editor__field')),
                        fromLabel: byId('entry-verse_start-label'),
                        fromTrigger: byId('entry-verse_start-trigger'),
                        toLabel: byId('entry-verse_end-label'),
                        toTrigger: byId('entry-verse_end-trigger')
                      };
                    }""")

                    toggle, book_label, book = (layout['toggle'], layout['bookLabel'],
                                                layout['bookTrigger'])
                    self.assertLessEqual(toggle['bottom'], book_label['top'])
                    self.assertLessEqual(book_label['bottom'], book['top'])
                    self.assertAlmostEqual((toggle['left'] + toggle['right']) / 2,
                                           (book['left'] + book['right']) / 2, delta=1)
                    self.assertEqual(page.locator('#entry-book-label').get_attribute('for'),
                                     'entry-book-trigger')
                    self.assertAlmostEqual(layout['chapterField']['width'],
                                           layout['innerRight'] - layout['innerLeft'], delta=1)

                    for control in ('chapterLabel', 'chapterTrigger', 'fromLabel', 'fromTrigger',
                                    'toLabel', 'toTrigger'):
                        self.assertGreaterEqual(layout[control]['left'], layout['innerLeft'] - 1)
                        self.assertLessEqual(layout[control]['right'], layout['innerRight'] + 1)

                    self.assertLessEqual(layout['contentScrollWidth'],
                                         layout['contentClientWidth'] + 1)
                    self.assertLessEqual(layout['modalScrollWidth'],
                                         layout['modalClientWidth'] + 1)
                    self.assertLessEqual(layout['pageScrollWidth'], layout['windowWidth'] + 1)
                    if width == 536:
                        self.assertGreater(layout['contentScrollHeight'],
                                           layout['contentClientHeight'])

                    from_box, to_box = layout['fromTrigger'], layout['toTrigger']
                    if range_stacks:
                        self.assertGreater(to_box['top'], from_box['top'])
                    else:
                        self.assertAlmostEqual(from_box['top'], to_box['top'], delta=1)
                        self.assertGreaterEqual(to_box['left'], from_box['right'])

                    page.locator('#editorContent').evaluate(
                        'element => { element.scrollTop = element.scrollHeight; }')
                    actions = page.locator('.editor__actions').bounding_box()
                    save = page.locator('.editor__save').bounding_box()
                    cancel = page.locator('.editor__cancel').bounding_box()
                    content_viewport = page.locator('#editorContent').evaluate("""element => {
                      const r = element.getBoundingClientRect();
                      return {top: r.top + element.clientTop,
                              bottom: r.top + element.clientTop + element.clientHeight};
                    }""")
                    assert actions is not None and save is not None and cancel is not None
                    self.assertGreaterEqual(actions['y'], content_viewport['top'] - 1)
                    self.assertLessEqual(actions['y'] + actions['height'],
                                         content_viewport['bottom'] + 1)
                    self.assertGreaterEqual(save['y'], content_viewport['top'] - 1)
                    self.assertLessEqual(save['y'] + save['height'], content_viewport['bottom'] + 1)
                    self.assertGreaterEqual(cancel['y'], content_viewport['top'] - 1)
                    self.assertLessEqual(cancel['y'] + cancel['height'],
                                         content_viewport['bottom'] + 1)
                finally:
                    context.close()

    def test_book_picker_filter_hides_nonmatching_books_and_restores_all(self):
        page = self._page()
        self._open_modal(page, 'scripture')
        picker = page.locator('[data-entry-picker="book"]')
        picker.locator('[data-picker-trigger]').click()
        options = picker.locator('[data-picker-options] [data-book]')
        expect(options).to_have_count(2)
        matius_option = picker.locator('[data-book-name-tb="Matius"]')
        markus_option = picker.locator('[data-book-name-tb="Markus"]')
        filter_box = picker.locator('input[type="search"]')

        filter_box.fill('Matius')
        expect(matius_option).to_be_visible()
        expect(markus_option).to_be_hidden()
        expect(picker.locator('[data-book]:visible')).to_have_count(1)

        filter_box.fill('Mateus')
        expect(matius_option).to_be_visible()
        expect(markus_option).to_be_hidden()
        expect(picker.locator('[data-book]:visible')).to_have_count(1)

        filter_box.fill('missing')
        expect(picker.locator('[data-book]:visible')).to_have_count(0)
        expect(picker.locator('[data-picker-group]')).to_be_hidden()
        expect(picker.locator('[data-picker-empty]')).to_be_visible()

        filter_box.fill('')
        expect(picker.locator('[data-book]:visible')).to_have_count(2)
        expect(picker.locator('[data-picker-group]')).to_be_visible()
        expect(picker.locator('[data-picker-empty]')).to_be_hidden()

    def test_book_picker_accepts_tb_and_sim_codes_and_updates_testament_labels(self):
        page = self._page()
        self._open_modal(page, 'scripture')
        picker = page.locator('[data-entry-picker="book"]')
        picker.locator('[data-picker-trigger]').click()
        old_group = picker.locator('[data-picker-group][data-testament="old"]')
        new_group = picker.locator('[data-picker-group][data-testament="new"]')
        option = picker.locator('[data-book-name-tb="Kejadian"]')
        filter_box = picker.locator('input[type="search"]')

        expect(old_group.locator('[data-testament-label]')).to_have_text('Perjanjian Lama')
        expect(new_group.locator('[data-testament-label]')).to_have_text('Perjanjian Baru')
        filter_box.fill('Kej')
        expect(option).to_be_visible()
        filter_box.fill('1Mu')
        expect(option).to_be_visible()
        page.locator('[data-entry-translation-toggle] [data-edition-option="sim"]').click()
        expect(old_group.locator('[data-testament-label]')).to_have_text('Padan na Basaia')
        expect(new_group.locator('[data-testament-label]')).to_have_text('Padan na Baru')
        expect(option.locator('.book__n')).to_have_text('1 Musa')
        picker.locator('[data-picker-trigger]').click()
        expect(filter_box).to_be_visible()
        filter_box.fill('Kej')
        expect(option).to_be_visible()
        filter_box.fill('1Mu')
        expect(option).to_be_visible()

    def test_edit_passage_picker_accepts_sim_code_and_testament_labels(self):
        page = self._page()
        edit = page.locator(f'[data-entry-edit="{self.kej_entry.pk}"]')
        edit.hover()
        edit.click()

        picker = page.locator('[data-entry-picker="book"]')
        picker.locator('[data-picker-trigger]').click()
        option = picker.locator(f'[data-book-tb="{self.kej_tb.pk}"]')
        filter_box = picker.locator('input[type="search"]')
        old_group = picker.locator('[data-picker-group][data-testament="old"]')
        expect(old_group.locator('[data-testament-label]')).to_have_text('Padan na Basaia')
        expect(option).to_have_attribute('aria-selected', 'true')
        filter_box.fill('1Mu')
        expect(option).to_be_visible()
        page.locator('[data-entry-translation-toggle] [data-edition-option="tb"]').click()
        expect(old_group.locator('[data-testament-label]')).to_have_text('Perjanjian Lama')
        picker.locator('[data-picker-trigger]').click()
        expect(filter_box).to_be_visible()
        filter_box.fill('Kej')
        expect(option).to_be_visible()
        filter_box.fill('1Mu')
        expect(option).to_be_visible()

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

    def test_translation_toggle_fills_the_hovered_option(self):
        """The passage picker's TB/SIM switch answers the pointer like the screen-mode one
        (spec 083)."""
        page = self._page()
        edit = page.locator(f'[data-entry-edit="{self.sim_entry.pk}"]')
        edit.hover()
        edit.click()

        toggle = page.locator('[data-entry-translation-toggle]')
        expect(toggle).to_be_visible()
        unselected = toggle.locator('[data-edition-option="tb"]')      # SIM is selected here
        selected = toggle.locator('[data-edition-option="sim"]')

        resting = unselected.evaluate('el => getComputedStyle(el).backgroundColor')
        unselected.hover()
        page.wait_for_timeout(260)             # the fill fades in over --ease
        hovered = unselected.evaluate('el => getComputedStyle(el).backgroundColor')

        self.assertNotEqual(hovered, resting, 'the unselected option took no fill on hover')
        self.assertEqual(hovered, 'rgba(31, 31, 29, 0.08)')     # --icon-hover-bg, light theme

        selected.hover()
        page.wait_for_timeout(260)
        self.assertEqual(selected.evaluate('el => getComputedStyle(el).backgroundColor'),
                         'rgba(0, 0, 0, 0)', 'the selected option filled over its thumb')

    def test_translation_toggle_switches_selected_book_without_refetching_verses(self):
        page = self._page()
        edit = page.locator(f'[data-entry-edit="{self.sim_entry.pk}"]')
        edit.hover()
        edit.click()

        toggle = page.locator('[data-entry-translation-toggle]')
        expect(toggle).to_be_visible()
        toggle_box = toggle.bounding_box()
        label_box = page.locator('#entry-book-label').bounding_box()
        book_box = page.locator('#entry-book-trigger').bounding_box()
        assert toggle_box is not None
        assert label_box is not None
        assert book_box is not None
        self.assertLessEqual(toggle_box['y'] + toggle_box['height'], label_box['y'])
        self.assertLessEqual(label_box['y'] + label_box['height'], book_box['y'])
        self.assertAlmostEqual(toggle_box['x'] + toggle_box['width'] / 2,
                               book_box['x'] + book_box['width'] / 2, delta=1)
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
        expect(page.locator('[data-entry-picker="book"] [data-picker-label]')).to_have_text('Matius')
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
        expect(page.locator('[data-entry-picker="book"] [data-picker-label]')).to_have_text('Mateus')
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
        self.assertEqual(picker.locator('[data-picker-label]').inner_text(), 'KJ 2 Number Two')

        picker.locator('[data-picker-trigger]').click()
        page.fill('#entry-song-search', 'Alpha Song')
        page.wait_for_function("document.querySelectorAll('#entry-song-options [data-song]').length === 1")
        non_hymn = page.locator('#entry-song-options [data-song]')
        self.assertEqual(non_hymn.count(), 1)
        non_hymn.click()
        self.assertEqual(picker.locator('[data-picker-label]').inner_text(), 'Alpha Song')

    def test_song_picker_searches_by_songbook_short_name(self):
        page = self._page()
        self._open_modal(page, 'song')
        picker = page.locator('[data-entry-picker="song"]')
        picker.locator('[data-picker-trigger]').click()
        page.fill('#entry-song-search', 'kj')
        page.wait_for_function("document.querySelectorAll('#entry-song-options [data-song]').length === 6",
                               timeout=5000)
        options = page.locator('#entry-song-options [data-song]')
        self.assertEqual(options.count(), 6)
        matching_song = page.locator(f'#entry-song-options [data-song="{self.song.pk}"]')
        self.assertEqual(matching_song.count(), 1)
        matching_song.click()
        self.assertEqual(picker.locator('[data-picker-label]').inner_text(), 'KJ 152 Ada Kuasa')

    def test_song_picker_filters_songs_by_songbook_name(self):
        page = self._page()
        self._open_modal(page, 'song')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()

        query_results = (
            ('kidung jemaat', self.kj_songs),
            ('kidu', [*self.kj_songs, self.titled_song]),
            ('maat', self.kj_songs),
            ('kidung', [*self.kj_songs, self.titled_song]),
        )
        for query, expected_songs in query_results:
            page.fill('#entry-song-search', query)
            self._wait_for_song_options(page, expected_songs)
            self.assertEqual(
                page.locator(f'#entry-song-options [data-song="{self.hal_song.pk}"]').count(), 0)

    def test_song_picker_reference_number_prefix_includes_sub_number(self):
        page = self._page()
        self._open_modal(page, 'song')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()

        page.fill('#entry-song-search', 'kj 12')
        prefix_matches = [
            *(self.kj_prefix_songs[number] for number in (12, 120, 123, 129)),
            self.kj_subnumber_a,
            self.kj_subnumber_b,
            *self.pkj_prefix_songs.values(),
        ]
        self._wait_for_song_options(page, prefix_matches)

        page.fill('#entry-song-search', 'kj 12a')
        self._wait_for_song_options(page, [self.kj_subnumber_a])

        page.fill('#entry-song-search', 'pkj 12')
        self._wait_for_song_options(page, list(self.pkj_prefix_songs.values()))

    def test_song_picker_searches_by_short_and_full_songbook_reference(self):
        page = self._page()
        self._open_modal(page, 'song')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()

        for query, song in (
                ('kj 123', self.short_reference_song),
                ('kidung jemaat 235', self.full_reference_song)):
            page.fill('#entry-song-search', query)
            page.wait_for_function(
                "document.querySelectorAll('#entry-song-options [data-song]').length === 1")
            page.wait_for_function(
                f"document.querySelector('#entry-song-options [data-song=\\\"{song.pk}\\\"]') !== null")
            self.assertEqual(
                page.locator(f'#entry-song-options [data-song="{song.pk}"]').count(), 1)

    def test_song_picker_reference_can_include_the_title(self):
        page = self._page()
        self._open_modal(page, 'song')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()
        page.fill('#entry-song-search', 'Kidung Jemaat 235 Reference Title Target')
        page.wait_for_function(
            "document.querySelectorAll('#entry-song-options [data-song]').length === 1")
        page.wait_for_function(
            f"document.querySelector('#entry-song-options [data-song=\\\"{self.full_reference_song.pk}\\\"]') !== null")
        self.assertEqual(
            page.locator(f'#entry-song-options [data-song="{self.full_reference_song.pk}"]').count(), 1)
        self.assertEqual(
            page.locator(f'#entry-song-options [data-song="{self.same_title_other_song.pk}"]').count(), 0)

    def test_song_picker_searches_by_reference_when_editing(self):
        page = self._page()
        edit = page.locator(f'[data-entry-edit="{self.reference_entry.pk}"]')
        edit.hover()
        edit.click()
        page.wait_for_selector('dialog[open]')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()
        page.fill('#entry-song-search', 'kidung jemaat 235')
        page.wait_for_function(
            "document.querySelectorAll('#entry-song-options [data-song]').length === 1")
        self.assertEqual(
            page.locator(f'#entry-song-options [data-song="{self.full_reference_song.pk}"]').count(), 1)

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
