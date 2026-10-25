"""The service entry modals in a browser (spec 006, slice 2).

Same runner and skip behaviour as the other e2e suites, including the rule that
matters most here: Playwright's loop must not overlap Django's database access, so a
test closes the browser before it asserts against the database.
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
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EntryModalE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        self.empty = tatib.TataIbadah.objects.create(name='Ibadah Kosong', is_active=True)
        # a service that already holds one item: the ORM must be done with before
        # Playwright's loop starts, or the test body cannot touch the database
        self.full = tatib.TataIbadah.objects.create(
            name='Ibadah Sore', date=date(2026, 8, 30), is_active=True)
        tatib.ServiceEntry.objects.create(tatib=self.full, order_number=1,
                                          kind=tatib.ServiceEntryKind.TEXT,
                                          title='Salam', text='lama')
        self.ordered = tatib.TataIbadah.objects.create(
            name='Ordered service', date=date(2026, 7, 11), is_active=True)
        for order, text in enumerate(('First', 'Last'), 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.ordered, order_number=order,
                kind=tatib.ServiceEntryKind.TEXT, text=text)
        self.legacy = tatib.TataIbadah.objects.create(
            name='Pengakuan Iman', date=date(2026, 7, 12), is_active=True)
        for order, text in enumerate(('Aku percaya kepada Allah.\nYang dikandung dari Roh Kudus.',
                                      'Yang menderita sengsara di bawah Pontius Pilatus.'), 1):
            tatib.TataIbadahItem.objects.create(
                tatib=self.legacy, order_number=order,
                item_type=tatib.TataIbadahItemType.TEXT, text=text)

        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        self.song = songs.Song.objects.create(book=songbook, number=152, title='Ada Kuasa')
        for number in (1, 2, 3):
            songs.Verse.objects.create(song=self.song, number=number, lyric=f'bait {number}')
        # a one-verse song: its checklist has nothing to choose, so it stays shut
        self.solo = songs.Song.objects.create(book=songbook, number=90, title='Bait Tunggal')
        songs.Verse.objects.create(song=self.solo, number=1, lyric='satu')
        if self._testMethodName == 'test_editing_a_hymn_song_shows_its_reference':
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.SONG,
                song=self.song, verses=[1, 2, 3])

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru',
                                               abbreviation='TB')
        mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        self.matius = bible.BookTranslation.objects.create(version=version, book=mat,
                                                           translation='Matius')
        for n in range(1, 6):
            bible.Verse.objects.create(book_translation=self.matius, chapter=5, verse=n,
                                       text=f'ayat {n}')

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

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _reveal(self, page):
        """The controls sit inside their item, so the item is what gets hovered."""
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(250)

    # --- the controls wait for a hover ---------------------------------------

    def test_the_add_controls_wait_for_a_hover(self):
        page = self._page(reverse('web-tatib-service', args=[self.full.pk]))
        controls = page.locator('.entry__add').first
        self.assertEqual(controls.evaluate('el => getComputedStyle(el).opacity'), '0')
        self._reveal(page)
        expect(page.locator('.entry__add').first).to_have_css('opacity', '1')
        self.assertEqual(page.locator('[data-entry-after]').count(), 1)

    def test_legacy_item_controls_stay_revealed_between_item_and_button_row(self):
        page = self._page(reverse('web-home'))
        page.locator('[data-panel="tatib"]').click()
        page.locator(f'.book[href="{reverse("web-tatib-service", args=[self.legacy.pk])}"]').click()
        page.wait_for_function(
            "document.querySelector('#readName') && "
            "document.querySelector('#readName').textContent.trim() === 'Pengakuan Iman'")
        page.wait_for_selector('#readBody > .tatib__item + .entry__add', state='attached')
        item = page.locator('#readBody > .tatib__item').first
        row = page.locator('#readBody > .entry__add').first
        item.hover()
        expect(row).to_have_css('opacity', '1')
        item_box, row_box = item.bounding_box(), row.bounding_box()
        # The add row is not part of the item (spec 036): it starts below the item's box.
        self.assertGreaterEqual(row_box['y'], item_box['y'] + item_box['height'] - 1)
        x = row_box['x'] + row_box['width'] * .8  # the blank right side, not a button
        page.mouse.move(x, item_box['y'] + item_box['height'] - 8)
        expect(row).to_have_css('opacity', '1')
        page.mouse.move(x, row_box['y'] + 8, steps=12)
        page.wait_for_timeout(420)               # beyond the old 220 ms hide delay
        expect(row).to_have_css('opacity', '1')

    def test_save_from_home_keeps_the_tata_ibadah_on_stage(self):
        page = self._page(reverse('web-home'))
        page.locator('[data-panel="tatib"]').click()
        page.locator(f'.book[href="{reverse("web-tatib-service", args=[self.full.pk])}"]').click()
        page.wait_for_function("document.querySelector('#readName').textContent.trim() === 'Ibadah Sore'")
        self.assertTrue(page.url.endswith(reverse('web-tatib-service', args=[self.full.pk])))
        self._reveal(page)
        page.locator('[data-entry-edit]').first.click()
        page.wait_for_selector('dialog[open]')
        page.fill('[name=text]', 'Saved on the service')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(page.locator('#readName')).to_have_text('Ibadah Sore')
        expect(page.locator('.tatib__item--entry .tatib__tx')).to_contain_text('Saved on the service')

    def test_add_after_first_entry_from_home_inserts_before_second(self):
        page = self._page(reverse('web-home'))
        page.locator('[data-panel="tatib"]').click()
        page.locator(f'.book[href="{reverse("web-tatib-service", args=[self.ordered.pk])}"]').click()
        page.wait_for_function("document.querySelector('#readName').textContent.trim() === 'Ordered service'")
        self._reveal(page)
        page.locator('#readBody .entry__add').first.locator('[data-entry-open="text"]').click()
        page.wait_for_selector('dialog[open]')
        page.fill('[name=text]', 'Middle')
        with page.expect_response(lambda response: '/editor/entry/new/save/' in response.url) as saving:
            page.click('.editor__save')
        self.assertEqual(saving.value.status, 200, saving.value.text()[:600])
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(page.locator('#readName')).to_have_text('Ordered service')
        expect(page.locator('#readBody .tatib__item--entry .tatib__tx')).to_have_text(
            ['First', 'Middle', 'Last'])
        self._close_browser()
        self.assertEqual(list(self.ordered.service_entries.order_by('order_number')
                              .values_list('text', flat=True)), ['First', 'Middle', 'Last'])

    # --- a passage ------------------------------------------------------------

    def test_adding_and_editing_a_passage_through_custom_pickers(self):
        page = self._page(reverse('web-home'))
        page.locator('[data-panel="tatib"]').click()
        service_url = reverse('web-tatib-service', args=[self.service.pk])
        page.locator(f'.book[href="{service_url}"]').click()
        page.wait_for_function(
            "document.querySelector('#readName').textContent.trim() === 'Ibadah Minggu III'")
        # nothing in this service yet, so the invitation is the way in
        page.locator('.entry__empty-btn', has_text='Add Passage').first.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New passage')
        book_trigger = page.locator('[data-entry-picker="book"] [data-picker-trigger]')
        book_box = book_trigger.bounding_box()
        assert book_box is not None
        for name in ('chapter', 'verse_start', 'verse_end'):
            picker = page.locator(f'[data-entry-picker="{name}"]')
            trigger = picker.locator('[data-picker-trigger]')
            expect(trigger).to_be_visible()
            box = trigger.bounding_box()
            assert box is not None
            self.assertAlmostEqual(box['height'], book_box['height'], delta=1)

        page.get_by_role('button', name='Book').click()
        page.locator('[data-entry-picker="book"] input[placeholder="Filter books..."]').fill('Matius')
        book_options = page.locator('[data-entry-picker="book"] [data-picker-options]')
        expect(book_options).to_contain_text('Perjanjian Baru')
        page.locator('[data-entry-picker="book"] [data-picker-options] button', has_text='Matius').first.click()
        expect(page.locator('[name=chapter]')).to_have_value('1')
        chapter_picker = page.locator('[data-entry-picker="chapter"]')
        chapter_picker.locator('[data-picker-trigger]').click()
        chapter_picker.locator('[data-picker-option][data-value="5"]').click()
        expect(page.locator('[name=verse_start]')).to_have_value('1')
        # the chapter's last verse leaves nothing to end a range with: the to-verse
        # shuts off and explains itself on hover
        start_picker = page.locator('[data-entry-picker="verse_start"]')
        start_picker.locator('[data-picker-trigger]').click()
        start_picker.locator('[data-picker-option][data-value="5"]').click()
        expect(page.locator('[name=verse_end]')).to_be_disabled()
        expect(page.locator('[data-entry-picker="verse_end"] [data-picker-trigger]')).to_be_disabled()
        expect(page.locator('[data-end-wrap]')).to_have_attribute('data-empty', 'true')
        page.hover('[data-end-wrap]')
        expect(page.locator('.editor__end-tip')).to_have_css('opacity', '1')
        start_picker.locator('[data-picker-trigger]').click()
        start_picker.locator('[data-picker-option][data-value="2"]').click()
        expect(page.locator('[name=verse_end]')).to_be_enabled()
        expect(page.locator('[name=verse_end] option[value="1"]')).to_have_count(0)
        end_picker = page.locator('[data-entry-picker="verse_end"]')
        end_picker.locator('[data-picker-trigger]').click()
        end_picker.locator('[data-picker-option][data-value="4"]').click()
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        page.wait_for_selector('.tatib__item--entry')

        contain = page.locator('.read__sec').first.text_content()
        self.assertIsNotNone(contain)
        self.assertIn('Matius 5:2-4', contain or '')
        row = page.locator('.tatib__item--entry').first
        row.hover()
        row.locator('[data-entry-edit]').click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit passage')
        expect(page.locator('[name=chapter]')).to_have_value('5')
        expect(page.locator('[name=verse_start]')).to_have_value('2')
        expect(page.locator('[name=verse_end]')).to_have_value('4')
        expect(page.locator('[data-entry-picker="chapter"] [data-picker-label]')).to_have_text('5')
        expect(page.locator('[data-entry-picker="verse_start"] [data-picker-label]')).to_have_text('2')
        expect(page.locator('[data-entry-picker="verse_end"] [data-picker-label]')).to_have_text('4')
        start_picker = page.locator('[data-entry-picker="verse_start"]')
        start_picker.locator('[data-picker-trigger]').click()
        start_picker.locator('[data-picker-option][data-value="3"]').click()
        end_picker = page.locator('[data-entry-picker="verse_end"]')
        end_picker.locator('[data-picker-trigger]').click()
        end_picker.locator('[data-picker-option][data-value="5"]').click()
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        self._close_browser()                       # the ORM runs outside Playwright's loop
        saved = tatib.ServiceEntry.objects.get(tatib=self.service)
        self.assertEqual(saved.citation(), 'Matius 5:3-5')

    # --- a song ---------------------------------------------------------------

    def test_the_song_pick_searches_and_the_verses_start_all_checked(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('.entry__empty-btn', has_text='Add Song').first.click()
        page.wait_for_selector('dialog[open]')
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()
        page.fill('#entry-song-search', 'kuasa')
        filtered_songs = page.locator('#entry-song-options [data-song]')
        expect(filtered_songs).to_have_count(1)
        expect(filtered_songs.first).to_have_attribute('data-song-title', self.song.title)
        filtered_songs.first.click()
        expect(page.locator('#entry-verses input[type=checkbox]')).to_have_count(3)
        expect(page.locator('[data-verses-trigger]')).to_have_text('All verses')
        expect(page.locator('[data-verses-trigger]')).to_be_enabled()
        page.locator('[data-verses-trigger]').click()
        expect(page.locator('#entry-verses input[type=checkbox]')).to_have_count(3)
        self.assertEqual(
            page.evaluate("[...document.querySelectorAll('#entry-verses input')].filter(i => i.checked).length"), 3)
        page.locator('#entry-verses input[value="2"]').uncheck()
        expect(page.locator('[data-verses-trigger]')).to_have_text('Verses 1, 3')
        page.keyboard.press('Escape')       # the open menu overlaps the Save button (spec 040)
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")

        self._close_browser()
        saved = tatib.ServiceEntry.objects.get(tatib=self.service, kind=tatib.ServiceEntryKind.SONG)
        self.assertEqual(saved.verses, [1, 3])

    def test_editing_a_hymn_song_shows_its_reference(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        self._reveal(page)
        page.locator('[data-entry-edit]').first.click()
        page.wait_for_selector('dialog[open]')
        label = page.locator('[data-entry-picker="song"] [data-picker-label]')
        self.assertEqual(label.inner_text(), 'KJ 152 Ada Kuasa')

    def test_single_verse_song_keeps_checked_verse_and_disables_picker(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('.entry__empty-btn', has_text='Add Song').click()
        page.locator('[data-entry-picker="song"] [data-picker-trigger]').click()
        page.fill('#entry-song-search', 'tunggal')
        page.wait_for_selector('#entry-song-options [data-song]')
        page.locator('#entry-song-options [data-song]').first.click()
        # one verse is no choice: it stays checked, and the dropdown stays shut
        expect(page.locator('[data-verses-trigger]')).to_be_disabled()
        expect(page.locator('[data-verses-trigger]')).to_have_text('All verses')
        self.assertEqual(
            page.evaluate("[...document.querySelectorAll('#entry-verses input')].filter(i => i.checked).length"), 1)
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")

        self._close_browser()
        saved = tatib.ServiceEntry.objects.get(tatib=self.service, kind=tatib.ServiceEntryKind.SONG)
        self.assertEqual(saved.verses, [1])

    def test_text_save_requires_content_and_does_not_resize(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('.entry__empty-btn', has_text='Add Text').click()
        expect(page.locator('.editor__save')).to_be_disabled()
        expect(page.locator('[name=text]')).to_have_css('resize', 'none')
        page.fill('[name=text]', '   ')
        expect(page.locator('.editor__save')).to_be_disabled()
        page.fill('[name=text]', 'Pembukaan')
        expect(page.locator('.editor__save')).to_be_enabled()

    def test_single_screen_save_follows_the_text_content(self):
        """The Text Save guard works when Single-screen is chosen on Create."""
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.locator('.entry__empty-btn', has_text='Add Text').click()
        page.locator('[data-create-mode="single_screen"]').click()
        expect(page.locator('.editor__save')).to_be_disabled()
        page.fill('[name=text]', 'Doa pembuka')
        expect(page.locator('.editor__save')).to_be_enabled()
        page.fill('[name=text]', '')
        expect(page.locator('.editor__save')).to_be_disabled()

    # --- editing and deleting -------------------------------------------------

    def test_entry_cancel_restores_service_item_without_outline_or_revealed_actions(self):
        page = self._page(reverse('web-tatib-service', args=[self.full.pk]))
        item = page.locator('.tatib__item').first
        item.hover()
        page.locator('[data-entry-edit]').first.click()
        page.wait_for_selector('dialog[open]')
        page.mouse.move(1400, 850)
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(item).to_be_focused()
        self.assertEqual(item.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
        page.wait_for_timeout(300)
        expect(page.locator('.entry__acts').first).to_have_css('opacity', '0')

    def test_editing_an_entry_and_deleting_it_after_a_confirmation(self):
        page = self._page(reverse('web-tatib-service', args=[self.full.pk]))
        entry_id = page.locator('.tatib__item--entry').first.get_attribute('data-entry-pk')
        self._reveal(page)
        page.locator('[data-entry-edit]').first.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit text')
        page.fill('[name=text]', 'baru')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        page.wait_for_selector('.tatib__item--entry')
        expect(page.locator('.tatib__tx').first).to_contain_text('baru')
        saved_item = page.locator(f'.tatib__item--entry[data-entry-pk="{entry_id}"]')
        expect(saved_item).to_be_focused(timeout=5000)
        self.assertEqual(saved_item.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

        # delete asks first; the two answers are one size, the destructive one last
        self._reveal(page)
        page.locator('[data-entry-delete]').first.click()
        page.wait_for_selector('[data-confirm-delete]')

        def box(selector):
            found = page.locator(selector).bounding_box()
            assert found is not None, selector
            return found

        cancel_box, delete_box = box('.editor__cancel'), box('[data-confirm-delete]')
        self.assertEqual(round(cancel_box['height']), round(delete_box['height']))
        self.assertGreaterEqual(delete_box['x'], cancel_box['x'] + cancel_box['width'])
        self.assertEqual(
            page.locator('.editor__cancel').evaluate('el => getComputedStyle(el).font'),
            page.locator('[data-confirm-delete]').evaluate('el => getComputedStyle(el).font'))
        page.click('.editor__cancel')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        page.mouse.move(1400, 850)
        expect(saved_item).to_be_focused()
        self.assertEqual(page.evaluate('getComputedStyle(document.activeElement).outlineStyle'), 'none')
        controls = page.locator('.entry__acts .entry__ctrl')
        self.assertEqual(controls.count(), 3)
        expect(page.locator('.entry__acts [data-preview-open]')).to_have_count(1)
        expect(page.locator('.entry__acts [data-entry-edit]')).to_have_count(1)
        expect(page.locator('.entry__acts [data-entry-delete]')).to_have_count(1)
        expect(page.locator('.entry__acts').first).to_have_css('opacity', '0')
        self.assertEqual(page.locator('.tatib__item--entry').count(), 1)

        self._reveal(page)
        page.locator('[data-entry-delete]').first.click()
        page.wait_for_selector('[data-confirm-delete]')
        page.click('[data-confirm-delete]')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        page.wait_for_timeout(700)
        gone = page.locator('.tatib__item--entry').count()
        self.assertEqual(page.evaluate('document.activeElement.id'), 'read')
        self.assertEqual(page.evaluate('getComputedStyle(document.activeElement).outlineStyle'), 'none')

        # the last entry takes the invitation's place: the rebuilt block is the
        # same centred row of tiles the server would have painted
        empty = page.locator('.entry__empty')
        expect(empty).to_be_visible()
        self.assertEqual(empty.locator('.entry__empty-btn').count(), 5)
        rebuilt = empty.locator('.entry__empty-btn').evaluate_all(
            '(buttons) => buttons.map(button => { const r = button.getBoundingClientRect();'
            ' return [r.x, r.y, r.width, r.height]; })')
        self.assertEqual(len({round(tile[1], 1) for tile in rebuilt}), 1, 'one row after the rebuild')
        for tile in rebuilt:
            self.assertLessEqual(abs(tile[2] - tile[3]), 1, 'square after the rebuild')

        self._close_browser()
        self.assertEqual(gone, 0)
        self.assertEqual(tatib.ServiceEntry.objects.filter(tatib=self.full).count(), 0)

    # --- an empty service -----------------------------------------------------

    def test_an_empty_service_invites_the_first_item(self):
        page = self._page(reverse('web-tatib-service', args=[self.empty.pk]))
        expect(page.locator('.entry__empty-title')).to_contain_text('empty')
        for label in ('Add Passage', 'Add Song', 'Add Text', 'Add Break'):
            expect(page.locator('.entry__empty-btn', has_text=label)).to_have_count(1)
        page.locator('.entry__empty-btn', has_text='Add Text').first.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New text')
        page.fill('[name=text]', 'Pembukaan')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        created = page.locator('.tatib__item--entry').first
        expect(created).to_be_focused(timeout=5000)
        self.assertEqual(created.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

        self._close_browser()
        self.assertEqual(tatib.ServiceEntry.objects.filter(tatib=self.empty).count(), 1)

    def test_an_empty_service_places_its_tiles_a_quarter_of_the_way_down(self):
        page = self._page(reverse('web-tatib-service', args=[self.empty.pk]))

        boxes = page.locator('.entry__empty-btn').evaluate_all(
            '(buttons) => buttons.map(button => { const r = button.getBoundingClientRect();'
            ' return [r.x, r.y, r.width, r.height]; })')
        self.assertEqual(len(boxes), 5)
        self.assertEqual(len({round(box[1], 1) for box in boxes}), 1, 'one row')
        self.assertEqual([round(box[0]) for box in boxes],
                         sorted(round(box[0]) for box in boxes), 'left to right')
        for box in boxes:
            self.assertLessEqual(abs(box[2] - box[3]), 1, 'square')
            self.assertGreaterEqual(min(box[2], box[3]), 44, 'still a hit target')

        # the glyph is the whole face of the button: the label survives as the
        # accessible name and the tooltip, not as visible text
        buttons = page.locator('.entry__empty-btn')
        for index, label in enumerate(('Add Passage', 'Add Song', 'Add Text',
                                       'Add Break', 'Add Media')):
            button = buttons.nth(index)
            self.assertEqual(button.get_attribute('title'), label)
            self.assertEqual(button.locator('svg').count(), 1)
            self.assertEqual(button.locator('.sr').text_content().strip(), label)
            self.assertLessEqual(button.locator('.sr').evaluate(
                'span => span.getBoundingClientRect().width'), 1)

        # the block sits a quarter of the way down the reading area the header
        # left — not the middle, and never back over the header
        geometry = page.evaluate(
            """() => {
              const box = (sel) => document.querySelector(sel).getBoundingClientRect();
              const body = box('#readBody'), empty = box('.entry__empty');
              return {clearOfHeader: empty.top - box('.read__head').bottom,
                      centreIntoBody: (empty.top + empty.bottom) / 2 - body.top,
                      bodyHeight: body.height};
            }""")
        self.assertGreater(geometry['clearOfHeader'], 0, 'the block never overlaps the header')
        self.assertLessEqual(
            abs(geometry['centreIntoBody'] - geometry['bodyHeight'] / 4), 12,
            'the block centres on the quarter mark of the reading area')
        self._close_browser()
