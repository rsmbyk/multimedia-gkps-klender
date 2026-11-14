"""End-to-end tests for the sidebar editors (spec 005).

Same runner and skip behaviour as the reading suite: Django's test runner via
``StaticLiveServerTestCase``, skipped when Playwright or its browser is missing.
"""

import unittest
from datetime import date, datetime, timedelta, timezone

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
class EditorE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.hymn = songs.Book.objects.create(
            name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        self.hymn_song = songs.Song.objects.create(
            book=self.hymn, number=12, title='Di Waktu Pagi', key='c')
        self.book = songs.Book.objects.create(
            name='Kidung Harian', short_name='KH', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=self.book, title='Alpha')
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembukaan', text='KJ 120', order_number=1)
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
        """Playwright's loop must not overlap Django's database access, so any test
        that asserts against the database closes the browser first."""
        if self._playwright is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _fill(self, page, name, value):
        if name == 'date':
            page.locator('[data-date-picker-trigger]').click()
            target = date.fromisoformat(value)
            month_delta = (target.year - date.today().year) * 12 + target.month - date.today().month
            control = '[data-date-picker-next]' if month_delta > 0 else '[data-date-picker-prev]'
            for _ in range(abs(month_delta)):
                page.locator(control).click()
            page.locator(f'[data-date="{value}"]').click()
            return
        widget = page.locator(f'[name="{name}"]')
        if widget.evaluate('el => el.tagName') == 'SELECT':
            page.select_option(f'[name="{name}"]', value)
        else:
            page.fill(f'[name="{name}"]', value)

    def _save(self, page, **fields):
        for name, value in fields.items():
            self._fill(page, name, value)
        page.click('.editor__save')
        # a <dialog> is never detached; it just loses its open attribute
        try:
            page.wait_for_function("!document.querySelector('dialog[open]')", timeout=10000)
        except Exception as error:
            state = page.evaluate('''() => ({
              status: document.getElementById('editorStatus')?.textContent,
              content: document.getElementById('editorContent')?.innerText,
              invalid: [...document.querySelectorAll('#editorContent .is-invalid')]
                .map(el => el.innerText),
              action: document.querySelector('#editorContent form')?.action,
              controls: [...document.querySelectorAll('#editorContent form input')]
                .map(el => ({name: el.name, type: el.type, valueLength: el.value.length}))
            })''')
            raise AssertionError(f'Editor remained open after save: {state}') from error

    # --- the add buttons ---

    def test_add_songbook_through_the_modal(self):
        page = self._page(reverse('web-index'))
        expect(page.locator('dialog[open]')).to_have_count(0)
        page.click('.rail__btn[aria-label="Kidung"]')
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New songbook')
        expect(page.locator('[name="short_name"], [name="is_hymn_book"], [name="lang"]')).to_have_count(0)
        self._save(page, name='Kidung Sekolah')
        expect(page.locator('dialog[open]')).to_have_count(0)
        expect(page.locator('#panelBody .book').filter(has_text='Kidung Sekolah')).to_be_visible()
        self._close_browser()
        book = songs.Book.objects.get(name='Kidung Sekolah')
        self.assertEqual(book.short_name, '')
        self.assertFalse(book.is_hymn_book)

    def test_edit_songbook_modal_omits_fields_and_preserves_their_values(self):
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        row = page.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        row.hover()
        row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit songbook')
        expect(page.locator('[name="short_name"], [name="is_hymn_book"], [name="lang"]')).to_have_count(0)
        self._save(page, name='Kidung Harian Baru')
        expect(page.locator('#panelBody .book').filter(has_text='Kidung Harian Baru')).to_be_visible()
        self._close_browser()
        self.book.refresh_from_db()
        self.assertEqual(self.book.short_name, 'KH')
        self.assertFalse(self.book.is_hymn_book)

    def test_the_editor_dialog_sits_on_the_shared_scrim(self):
        """A modal has to read as a sheet above the page, not a panel in it (spec 086)."""
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        row = page.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        row.hover()
        row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')

        scrim = page.evaluate("""() => getComputedStyle(
          document.querySelector('.editor'), '::backdrop').backgroundColor""")
        dialog = page.evaluate(
            "() => getComputedStyle(document.querySelector('.editor')).backgroundColor")
        self.assertEqual(scrim, 'rgba(20, 20, 18, 0.52)')
        self.assertNotEqual(scrim, dialog)              # the scrim is a paint of its own

        # the lift and the hairline resolve through --shadow-dialog, not the page-level --shadow
        shadow = page.evaluate(
            "() => getComputedStyle(document.querySelector('.editor')).boxShadow")
        self.assertIn('0px 0px 0px 1px', shadow)
        self.assertIn('48px', shadow)

        # and the scrim really paints: a pixel of the page changes under it
        painted = self._corner(page)
        page.add_style_tag(content='.editor::backdrop { background: transparent !important; }')
        self.assertNotEqual(painted, self._corner(page))

    def _corner(self, page):
        """A few pixels of the page, well clear of the centred dialog."""
        return page.screenshot(clip={'x': 6, 'y': 6, 'width': 2, 'height': 2})

    def test_add_song_to_the_open_songbook(self):
        page = self._page(reverse('web-book', args=[self.book.pk]))
        expect(page.locator('#songAdd')).to_be_enabled()
        page.click('#songAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New song')
        self._save(page, title='Lagu Baru')
        expect(page.locator('#chList .songrow').filter(has_text='Lagu Baru')).to_be_visible()
        self._close_browser()
        self.assertTrue(songs.Song.objects.filter(book=self.book, title='Lagu Baru').exists())

    def test_the_add_buttons_exist_on_the_home_to_section_path(self):
        """The path the owner actually uses: land on the home, click through in-page.

        The sidebars are swapped in by reading.js and the add buttons sit outside
        those swapped regions, so a page that never had one has to have it inserted
        -- updating in place left them missing on exactly this path (spec 005).
        """
        page = self._page(reverse('web-index'))
        expect(page.locator('.editor-add')).to_have_count(0)
        page.click('.rail__btn[aria-label="Kidung"]')
        panel_add = page.locator('#panelAdd')
        expect(panel_add).to_be_visible()
        expect(panel_add).to_contain_text('Add songbook')
        panel_add.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New songbook')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        # and it sits inside the sidebar's padding on both sides (review report:
        # a doubled inset pushed it past the edge)
        page.get_by_text(self.book.name, exact=True).first.click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        page.wait_for_timeout(700)                      # let its travel finish
        insets = page.evaluate('''() => {
            const b = document.getElementById('songAdd');
            const s = document.querySelector('.chapters');
            const br = b.getBoundingClientRect(), sr = s.getBoundingClientRect();
            return {left: br.left - sr.left, right: sr.right - br.right}; }''')
        self.assertGreater(insets['left'], 0, 'the add button overflows the left edge')
        self.assertGreater(insets['right'], 0, 'the add button overflows the right edge')
        page.click('.rail__btn[aria-label="Alkitab"]')
        expect(page.locator('#panelAdd')).to_have_count(0)          # and gone again
        self._close_browser()

    def test_escape_inside_the_modal_does_not_also_close_the_sidebar(self):
        """The modal is the innermost layer: Esc must stop there (review report)."""
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        self.assertEqual(page.evaluate("document.documentElement.dataset.nav"), 'open')
        expect(page.locator('#panelAdd')).to_be_visible()
        self._close_browser()

    def test_the_tata_ibadah_mode_toggle_exists_after_clicking_through(self):
        """It is part of the Tata Ibadah toolbar only, and the home path swaps that in."""
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        expect(page.locator('#tatibMode')).to_have_count(0)
        page.click('.rail__btn[aria-label="Tata Ibadah"]')
        mode = page.locator('#tatibMode')
        expect(mode).to_be_visible()
        expect(mode).to_have_attribute('aria-label', 'Show Tata Ibadah templates')
        # and it sits where the mockup puts it: between the field and the collapse
        order = page.evaluate("""() => [...document.querySelectorAll('.panel__filter > *')]
            .map(e => e.id || e.className.split(' ')[0])""")
        self.assertEqual(order[-2:], ['tatibMode', 'panelCollapse'])
        self._close_browser()

    def test_closing_a_sidebar_reveals_no_row_control_and_no_rail_label(self):
        """Closing the song list left the row's control lit and a tile's label hanging."""
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        page.get_by_text(self.book.name, exact=True).first.click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        page.wait_for_timeout(700)
        # close the song list with its own control, then look for anything revealed
        page.click('#chCollapse')
        page.wait_for_function("document.documentElement.dataset.ch === 'closed'")
        page.wait_for_timeout(500)
        lit = page.evaluate("""() => [...document.querySelectorAll('#panelBody .row-edit, #chList .row-edit')]
            .filter(b => getComputedStyle(b).opacity !== '0').length""")
        self.assertEqual(lit, 0, 'a row control was left revealed')
        # The label is painted by ::after, so read that -- an attribute or a missing
        # element proves nothing. First a positive control: hovering must raise it.
        lift = ("Number(getComputedStyle(document.querySelector("
                "'.rail__btn[aria-label=\"Kidung\"]'), '::after').opacity)")
        page.hover('.rail__btn[aria-label="Kidung"]')
        page.wait_for_timeout(900)
        self.assertGreater(page.evaluate(lift), 0.05, 'the label did not appear on hover')
        # closing the panel with its own control puts focus back on the tile, and that
        # must not raise the label again (review report: it did)
        page.click('#panelCollapse')
        page.wait_for_function("document.documentElement.dataset.nav === 'closed'")
        page.wait_for_timeout(700)
        self.assertEqual(page.evaluate(lift), 0, 'the rail label stayed up after closing')
        rails = page.evaluate("""() => [...document.querySelectorAll('.rail__btn[data-tip]')]
            .filter(b => Number(getComputedStyle(b, '::after').opacity) > 0.05).map(b => b.dataset.tip)""")
        self.assertEqual(rails, [], 'a rail label was left up')
        self._close_browser()

    def test_tatib_date_picker_selects_clears_and_supports_keyboard(self):
        page = self._page(reverse('web-tatib'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('input[type="date"]')).to_have_count(0)
        date_value = page.locator('[name="date"]')
        expect(date_value).to_have_attribute('type', 'hidden')

        trigger = page.locator('[data-date-picker-trigger]')
        calendar = page.locator('[data-date-picker-calendar]')
        expect(calendar).to_be_hidden()
        date_picker = page.locator('[data-date-picker]')
        trigger.click()
        expect(calendar).to_be_visible()
        grid = calendar.locator('[data-date-picker-grid]')
        first_week = grid.locator('.editor__date-row').first
        expect(first_week).to_have_css('display', 'grid')
        column_count = first_week.evaluate(
            'el => getComputedStyle(el).gridTemplateColumns.split(" ").length')
        self.assertEqual(column_count, 7)
        today = date.today()
        target = today + timedelta(days=1)
        calendar.locator('[data-date-today]').focus()
        page.keyboard.press('ArrowRight')
        page.keyboard.press('Enter')
        expect(date_value).to_have_value(target.isoformat())
        expected_label = page.evaluate("""value => {
          const [year, month, day] = value.split('-').map(Number);
          return new Intl.DateTimeFormat('id-ID', {
            day: 'numeric', month: 'long', year: 'numeric'
          }).format(new Date(year, month - 1, day));
        }""", target.isoformat())
        expect(trigger).to_have_text(expected_label)

        trigger.click()
        expect(calendar).to_be_visible()
        page.locator('#editorTitle').click()
        expect(calendar).to_be_hidden()

        trigger.click()
        expect(calendar).to_be_visible()
        page.keyboard.press('Escape')
        expect(calendar).to_be_hidden()
        expect(trigger).to_be_focused()
        date_picker.locator('[data-date-picker-clear]').click()
        expect(date_value).to_have_value('')

    def test_new_tatib_date_picker_defaults_to_the_upcoming_sunday_popover(self):
        page = self._page(reverse('web-tatib'))
        page.clock.install(time=datetime(2026, 10, 7, 12, tzinfo=timezone.utc))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')

        date_value = page.locator('[name="date"]')
        trigger = page.locator('[data-date-picker-trigger]')
        calendar = page.locator('[data-date-picker-calendar]')
        date_picker = page.locator('[data-date-picker]')
        expect(date_value).to_have_value('2026-10-11')
        expect(trigger).to_contain_text('11 Oktober 2026')
        picker_height = date_picker.bounding_box()['height']

        trigger.click()
        expect(calendar).to_be_visible()
        expect(calendar).to_have_css('position', 'fixed')
        expect(calendar).to_have_attribute('popover', 'manual')
        expect(calendar).to_have_css('display', 'block')
        trigger_box = trigger.bounding_box()
        picker_after = date_picker.bounding_box()
        calendar_box = calendar.bounding_box()
        self.assertAlmostEqual(picker_after['height'], picker_height)
        self.assertAlmostEqual(
            calendar_box['y'] - (trigger_box['y'] + trigger_box['height']), 8, delta=2)
        expect(calendar.locator('[data-date="2026-10-11"]')).to_have_attribute(
            'aria-selected', 'true')

    def test_date_picker_cells_are_square_across_widths_and_month_lengths(self):
        for width, height in ((1440, 900), (390, 844), (320, 500), (1440, 360)):
            with self.subTest(viewport=(width, height)):
                page = self._page(reverse('web-index'))
                page.set_viewport_size({'width': width, 'height': height})
                page.reload(wait_until='networkidle')
                page.clock.install(time=datetime(2027, 2, 7, 12, tzinfo=timezone.utc))
                page.click('.rail__btn[aria-label="Tata Ibadah"]')
                page.click('#panelAdd')
                page.wait_for_selector('dialog[open]')
                picker = page.locator('[data-date-picker]')
                closed_height = picker.bounding_box()['height']
                page.locator('[data-date-picker-trigger]').click()
                calendar = page.locator('[data-date-picker-calendar]')
                expect(calendar).to_be_visible()

                for previous_months, weeks in ((0, 4), (3, 6), (1, 5)):
                    for _ in range(previous_months):
                        calendar.locator('[data-date-picker-prev]').click()
                    geometry = calendar.evaluate('''el => {
                      const bounds = el.getBoundingClientRect();
                      return {
                        cells: [...el.querySelectorAll('.editor__date-day, .editor__date-empty')]
                          .map(cell => {
                            const box = cell.getBoundingClientRect();
                            return {width: box.width, height: box.height};
                          }),
                        weeks: el.querySelectorAll('.editor__date-row').length,
                        left: bounds.left, top: bounds.top,
                        right: bounds.right, bottom: bounds.bottom,
                        viewportWidth: innerWidth, viewportHeight: innerHeight,
                      };
                    }''')
                    self.assertEqual(geometry['weeks'], weeks, geometry)
                    for cell in geometry['cells']:
                        self.assertGreater(cell['width'], 0)
                        self.assertAlmostEqual(cell['width'], cell['height'], delta=1)
                    self.assertGreaterEqual(geometry['left'], 0, geometry)
                    self.assertGreaterEqual(geometry['top'], 0, geometry)
                    self.assertLessEqual(geometry['right'], geometry['viewportWidth'], geometry)
                    self.assertLessEqual(geometry['bottom'], geometry['viewportHeight'], geometry)
                    expect(calendar.locator('.editor__date-day').first).to_have_css(
                        'border-radius', '8px')
                    self.assertAlmostEqual(picker.bounding_box()['height'], closed_height)
                page.close()

    def test_date_picker_emphasizes_sundays_in_light_and_dark_themes(self):
        page = self._page(reverse('web-index'))
        page.clock.install(time=datetime(2026, 10, 4, 12, tzinfo=timezone.utc))
        page.click('.rail__btn[aria-label="Tata Ibadah"]')
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        page.locator('[data-date-picker-trigger]').click()
        calendar = page.locator('[data-date-picker-calendar]')
        expect(calendar).to_be_visible()

        selected_sunday = calendar.locator('[data-date="2026-10-04"]')
        sunday = calendar.locator('[data-date="2026-10-11"]')
        weekday = calendar.locator('[data-date="2026-10-06"]')
        sunday_heading = calendar.locator('.editor__date-weekdays [data-date-sunday]')
        expect(sunday).to_have_attribute('data-date-sunday', '')
        expect(sunday_heading).to_have_count(1)
        expect(selected_sunday).to_have_attribute('aria-selected', 'true')
        expect(selected_sunday).to_have_attribute('aria-current', 'date')

        for theme in ('light', 'dark'):
            page.evaluate('(theme) => document.documentElement.dataset.theme = theme', theme)
            sunday_style = sunday.evaluate('''el => {
              const style = getComputedStyle(el);
              return {weight: Number(style.fontWeight), color: style.color,
                      background: style.backgroundColor};
            }''')
            weekday_style = weekday.evaluate('''el => {
              const style = getComputedStyle(el);
              return {weight: Number(style.fontWeight), color: style.color,
                      background: style.backgroundColor};
            }''')
            heading_style = sunday_heading.evaluate('''el => {
              const style = getComputedStyle(el);
              return {weight: Number(style.fontWeight), color: style.color};
            }''')
            selected_style = selected_sunday.evaluate('''el => ({
              background: getComputedStyle(el).backgroundColor,
              color: getComputedStyle(el).color
            })''')
            active_colors = page.evaluate('''() => {
              const style = getComputedStyle(document.documentElement);
              return {background: style.getPropertyValue('--active-bg').trim(),
                      color: style.getPropertyValue('--active-ink').trim()};
            }''')
            self.assertGreater(sunday_style['weight'], weekday_style['weight'], theme)
            self.assertNotEqual(sunday_style['color'], weekday_style['color'], theme)
            self.assertNotEqual(sunday_style['background'], weekday_style['background'], theme)
            self.assertGreater(heading_style['weight'], 600, theme)
            self.assertEqual(selected_style['background'], page.evaluate(
                "color => { const probe = document.createElement('div'); "
                "probe.style.backgroundColor = color; document.body.append(probe); "
                "const value = getComputedStyle(probe).backgroundColor; probe.remove(); return value; }",
                active_colors['background']))
            self.assertEqual(selected_style['color'], page.evaluate(
                "color => { const probe = document.createElement('div'); "
                "probe.style.color = color; document.body.append(probe); "
                "const value = getComputedStyle(probe).color; probe.remove(); return value; }",
                active_colors['color']))
            selected_sunday.hover()
            expect(selected_sunday).to_have_css('background-color', selected_style['background'])
            expect(selected_sunday).to_have_css('color', selected_style['color'])
            selected_sunday.focus()
            page.keyboard.press('ArrowDown')
            expect(sunday).to_be_focused()
            expect(sunday).to_have_css('outline-style', 'solid')
            expect(sunday).to_have_css('outline-width', '2px')

        weekday.click()
        expect(page.locator('[name="date"]')).to_have_value('2026-10-06')
        page.locator('[data-date-picker-trigger]').click()
        expect(selected_sunday).to_have_attribute('aria-selected', 'false')
        expect(selected_sunday).to_have_attribute('aria-current', 'date')
        for theme in ('light', 'dark'):
            page.evaluate('(theme) => document.documentElement.dataset.theme = theme', theme)
            expect(selected_sunday).to_have_css('border-top-color', sunday.evaluate(
                'el => getComputedStyle(el).color'))
            expect(selected_sunday).to_have_css('border-top-width', '1px')

    def test_new_tatib_date_picker_defaults_to_today_when_opened_on_sunday(self):
        page = self._page(reverse('web-tatib'))
        page.clock.install(time=datetime(2026, 10, 11, 12, tzinfo=timezone.utc))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')

        expect(page.locator('[name="date"]')).to_have_value('2026-10-11')
        expect(page.locator('[data-date-picker-trigger]')).to_contain_text('11 Oktober 2026')

    def test_date_picker_dropdown_overlaps_the_scrollable_modal_content(self):
        page = self._page(reverse('web-tatib'))
        page.set_viewport_size({'width': 1440, 'height': 500})
        page.clock.install(time=datetime(2026, 10, 7, 12, tzinfo=timezone.utc))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        page.add_style_tag(content='''
            #editorContent { height: 110px !important; max-height: 110px !important;
                              flex: 0 0 110px !important; }
        ''')
        content = page.locator('#editorContent')
        content.evaluate('el => { el.scrollTop = el.scrollHeight; }')
        trigger = page.locator('[data-date-picker-trigger]')
        trigger.click()
        calendar = page.locator('[data-date-picker-calendar]')
        expect(calendar).to_be_visible()

        geometry = page.evaluate('''() => {
          const content = document.getElementById('editorContent');
          const calendar = document.querySelector('[data-date-picker-calendar]');
          const before = content.getBoundingClientRect();
          const bounds = calendar.getBoundingClientRect();
          const clipBottom = before.top + content.clientHeight;
          const overlapY = Math.max(bounds.top + 1, clipBottom + 2);
          const overlapX = Math.max(bounds.left + 1, Math.min(bounds.right - 1,
            window.innerWidth / 2));
          const hit = overlapY < bounds.bottom
            && document.elementFromPoint(overlapX, overlapY)
              ?.closest('[data-date-picker-calendar]') === calendar;
          return {
            top: bounds.top, right: bounds.right, bottom: bounds.bottom,
            clipBottom, overlapY, hit,
            viewportWidth: window.innerWidth, viewportHeight: window.innerHeight,
            contentHeight: content.clientHeight, scrollHeight: content.scrollHeight,
          };
        }''')
        self.assertTrue(geometry['bottom'] > geometry['clipBottom'], geometry)
        self.assertTrue(geometry['hit'], geometry)
        self.assertGreaterEqual(geometry['top'], 0, geometry)
        self.assertGreaterEqual(geometry['right'], 0, geometry)
        self.assertLessEqual(geometry['bottom'], geometry['viewportHeight'], geometry)
        self.assertLessEqual(geometry['right'], geometry['viewportWidth'], geometry)
        self.assertEqual(geometry['contentHeight'], 110, geometry)

        initial_trigger_top = trigger.bounding_box()['y']
        content.evaluate('el => { el.scrollTop = 0; }')
        # The picker repositions on the content's scroll event, which lands after this
        # call: wait for the calendar to re-anchor before reading its geometry.
        page.wait_for_function('''() => {
          const trigger = document.querySelector('[data-date-picker-trigger]').getBoundingClientRect();
          const calendar = document.querySelector('[data-date-picker-calendar]').getBoundingClientRect();
          return Math.abs(calendar.top - trigger.bottom - 8) < 2
              || Math.abs(trigger.top - calendar.bottom - 8) < 2;
        }''', timeout=4000)
        scrolled = page.evaluate('''() => {
          const trigger = document.querySelector('[data-date-picker-trigger]').getBoundingClientRect();
          const calendar = document.querySelector('[data-date-picker-calendar]').getBoundingClientRect();
          return {triggerTop: trigger.top, triggerBottom: trigger.bottom,
                  calendarTop: calendar.top, calendarBottom: calendar.bottom};
        }''')
        self.assertNotAlmostEqual(scrolled['triggerTop'], initial_trigger_top)
        self.assertTrue(
            abs(scrolled['calendarTop'] - scrolled['triggerBottom'] - 8) < 2
            or abs(scrolled['triggerTop'] - scrolled['calendarBottom'] - 8) < 2,
            scrolled)

        page.evaluate('''() => {
          window.__resizeEvents = 0;
          window.addEventListener('resize', () => { window.__resizeEvents += 1; });
        }''')
        page.set_viewport_size({'width': 400, 'height': 360})
        page.wait_for_function('window.__resizeEvents > 0')
        resized = page.evaluate('''() => {
          const calendar = document.querySelector('[data-date-picker-calendar]').getBoundingClientRect();
          return {left: calendar.left, top: calendar.top, right: calendar.right,
                  bottom: calendar.bottom, width: document.documentElement.clientWidth,
                  height: document.documentElement.clientHeight};
        }''')
        self.assertGreaterEqual(resized['left'], 8, resized)
        self.assertGreaterEqual(resized['top'], 8, resized)
        self.assertLessEqual(resized['right'], resized['width'] - 8, resized)
        self.assertLessEqual(resized['bottom'], resized['height'] - 8, resized)

        page.keyboard.press('Escape')
        expect(calendar).to_be_hidden()
        trigger.click()
        expect(calendar).to_be_visible()
        page.locator('#editorModal').evaluate('dialog => dialog.close()')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(page.locator('[data-date-picker-calendar]:popover-open')).to_have_count(0)

    def test_tatib_date_picker_submits_iso_date(self):
        page = self._page(reverse('web-tatib'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        selected = date.today() + timedelta(days=2)
        page.locator('[data-date-picker-trigger]').click()
        page.wait_for_selector('[data-date-picker-calendar]:not([hidden])')
        if selected.month != date.today().month:
            page.locator('[data-date-picker-next]').click()
        iso_date = selected.isoformat()
        page.locator(f'[data-date="{iso_date}"]').click()
        page.fill('[name="name"]', 'Date picker service')
        page.locator('.editor__save').click()
        page.wait_for_function("!document.querySelector('dialog[open]')")
        self._close_browser()
        service = tatib.TataIbadah.objects.get(name='Date picker service')
        self.assertEqual(service.date, selected)

    def test_tatib_date_picker_loads_saved_date_and_clears_on_edit(self):
        page = self._page(reverse('web-tatib'))
        row = page.locator(f'li:has(.book[data-name="{self.service.pk}"])')
        row.hover()
        row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')

        saved_date = self.service.date.isoformat()
        expect(page.locator('[name="date"]')).to_have_value(saved_date)
        page.locator('[data-date-picker-trigger]').click()
        calendar = page.locator('[data-date-picker-calendar]')
        expect(calendar).to_be_visible()
        expect(page.locator(f'[data-date="{saved_date}"]')).to_have_attribute(
            'aria-selected', 'true')
        expect(page.locator('[data-date-picker-month]')).to_contain_text('Agustus 2026')
        page.locator('[data-date-picker-clear]').click()
        expect(page.locator('[name="date"]')).to_have_value('')
        expect(calendar).to_be_hidden()
        page.fill('[name="name"]', 'Recurring service')
        page.locator('.editor__save').click()
        page.wait_for_function("!document.querySelector('dialog[open]')")
        self._close_browser()
        self.service.refresh_from_db()
        self.assertIsNone(self.service.date)

    def test_tatib_date_picker_survives_validation_rerender(self):
        page = self._page(reverse('web-tatib'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        today = date.today()
        date_value = page.locator('[name="date"]')
        calendar = page.locator('[data-date-picker]')
        page.locator('[data-date-picker-trigger]').click()
        calendar.locator('[data-date-today]').click()
        page.locator('[name="name"]').evaluate("el => el.removeAttribute('maxlength')")
        page.locator('[name="name"]').fill('x' * 65)
        page.locator('.editor__save').click()
        expect(page.locator('dialog[open]')).to_be_visible()
        expect(page.locator('.editor__error')).to_be_visible()
        expect(page.locator('[name="name"]')).to_have_value('x' * 65)
        expect(page.locator('input[type="date"]')).to_have_count(0)
        expect(page.locator('[name="date"]')).to_have_value(today.isoformat())
        page.locator('[data-date-picker-trigger]').click()
        expect(page.locator('[data-date-picker-calendar]')).to_be_visible()
        page.keyboard.press('Escape')
        expect(page.locator('[data-date-picker-calendar]')).to_be_hidden()

    def test_add_empty_active_tatib(self):
        page = self._page(reverse('web-tatib'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('New Tata Ibadah')
        expect(page.locator('[name="first_title"], [name="first_text"], [name="is_active"]')).to_have_count(0)
        self._save(page, name='Ibadah Baru', date='2026-11-01')
        expect(page.locator('#panelBody .book').filter(has_text='Ibadah Baru')).to_be_visible()
        page.get_by_text('Ibadah Baru', exact=True).click()
        expect(page.locator('.entry__empty')).to_be_visible()
        expect(page.locator('[data-entry-open="scripture"]')).to_be_visible()
        self._close_browser()
        service = tatib.TataIbadah.objects.get(name='Ibadah Baru')
        self.assertTrue(service.is_active)
        self.assertEqual(service.tataibadahitem_set.count(), 0)

    # --- editing ---

    def test_edit_a_song_row_from_its_hover_control(self):
        page = self._page(reverse('web-book', args=[self.book.pk]))
        row = page.locator(f'li:has(.songrow[data-i="{self.song.pk}"])')
        control = row.locator('.row-edit')
        expect(control).to_have_css('opacity', '0')          # out of the way when idle
        self.assertEqual(control.evaluate('el => getComputedStyle(el).pointerEvents'), 'none')
        row.hover()
        expect(control).to_have_css('opacity', '1')
        control.click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit song')
        expect(page.locator('[name="title"]')).to_have_value('Alpha')
        self._save(page, title='Alpha Baru')
        expect(page.locator('#chList .songrow').filter(has_text='Alpha Baru')).to_be_visible()
        self._close_browser()
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, 'Alpha Baru')

    def test_edit_a_tatib_row(self):
        page = self._page(reverse('web-tatib'))
        row = page.locator(f'li:has(.book[data-name="{self.service.pk}"])')
        row.hover()
        row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        expect(page.locator('#editorTitle')).to_have_text('Edit Tata Ibadah')
        expect(page.locator('[name="name"]')).to_have_value('Ibadah Minggu III')
        self._save(page, name='Ibadah Minggu IV')
        expect(page.locator('#panelBody .book').filter(has_text='Ibadah Minggu IV')).to_be_visible()
        self._close_browser()
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Ibadah Minggu IV')

    def test_pointer_closed_editor_does_not_leave_its_row_control_visible(self):
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        book_row = page.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        book_edit = book_row.locator('.row-edit')
        book_row.hover()
        expect(book_edit).to_have_css('opacity', '1')
        book_edit.click()
        page.wait_for_selector('dialog[open]')
        page.locator('.editor__cancel').click()
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(book_edit).to_have_css('opacity', '0')
        self.assertEqual(book_edit.evaluate('el => getComputedStyle(el).pointerEvents'), 'none')
        book_row.hover()
        expect(book_edit).to_have_css('opacity', '1')

        page.get_by_text(self.book.name, exact=True).first.click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        song_row = page.locator(f'li:has(.songrow[data-i="{self.song.pk}"])')
        song_edit = song_row.locator('.row-edit')
        song_row.hover()
        song_edit.click()
        page.wait_for_selector('dialog[open]')
        page.locator('.editor__cancel').click()
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(song_edit).to_have_css('opacity', '0')

        page.click('.rail__btn[aria-label="Tata Ibadah"]')
        tatib_row = page.locator(f'li:has(.book[data-name="{self.service.pk}"])')
        tatib_edit = tatib_row.locator('.row-edit')
        tatib_row.hover()
        tatib_edit.click()
        page.wait_for_selector('dialog[open]')
        page.locator('.editor__cancel').click()
        page.wait_for_function("!document.querySelector('dialog[open]')")
        expect(tatib_edit).to_have_css('opacity', '0')

    def test_sidebar_save_restores_focus_to_the_matching_kind_row(self):
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        self._save(page, name='Focus Test Songbook')
        book_link = page.locator('#panelBody .book').filter(has_text='Focus Test Songbook')
        expect(book_link).to_be_focused(timeout=5000)
        self.assertEqual(book_link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
        book_id = book_link.get_attribute('data-name')
        book_row = page.locator(f'li:has(.book[data-name="{book_id}"])')
        book_row.hover()
        book_row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        self._save(page, name='Edited Focus Test Songbook')
        book_link = page.locator('#panelBody .book').filter(has_text='Edited Focus Test Songbook')
        expect(book_link).to_be_focused(timeout=5000)
        self.assertEqual(book_link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

        book_link.click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        page.click('#songAdd')
        page.wait_for_selector('dialog[open]')
        self._save(page, title='Focus Test Song')
        song_link = page.locator('#chList .songrow').filter(has_text='Focus Test Song')
        expect(song_link).to_be_focused(timeout=5000)
        self.assertEqual(song_link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
        song_id = song_link.get_attribute('data-i')
        song_row = page.locator(f'li:has(.songrow[data-i="{song_id}"])')
        song_row.hover()
        song_row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        self._save(page, title='Edited Focus Test Song')
        song_link = page.locator('#chList .songrow').filter(has_text='Edited Focus Test Song')
        expect(song_link).to_be_focused(timeout=5000)
        self.assertEqual(song_link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

        page.click('.rail__btn[aria-label="Tata Ibadah"]')
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        self._save(page, name='Focus Test Tata Ibadah', date='2026-11-01')
        tatib_link = page.locator('#panelBody .book').filter(has_text='Focus Test Tata Ibadah')
        expect(tatib_link).to_be_focused(timeout=5000)
        self.assertEqual(tatib_link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
        tatib_id = tatib_link.get_attribute('data-name')
        tatib_row = page.locator(f'li:has(.book[data-name="{tatib_id}"])')
        tatib_row.hover()
        tatib_row.locator('.row-edit').click()
        page.wait_for_selector('dialog[open]')
        self._save(page, name='Edited Focus Test Tata Ibadah')
        tatib_link = page.locator('#panelBody .book').filter(has_text='Edited Focus Test Tata Ibadah')
        expect(tatib_link).to_be_focused(timeout=5000)
        self.assertEqual(tatib_link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
        self._close_browser()

    def test_modal_restoration_quiets_row_outlines_but_keyboard_focus_remains_visible(self):
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')

        def close_editor(row, key):
            link = row.locator('a.book, a.songrow')
            control = row.locator('.row-edit')
            row.hover()
            control.click()
            page.wait_for_selector('dialog[open]')
            page.mouse.move(1400, 850)
            if key == 'Enter':
                page.locator('.editor__cancel').focus()
            page.keyboard.press(key)
            page.wait_for_function("!document.querySelector('dialog[open]')")
            expect(link).to_be_focused()
            self.assertEqual(link.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
            expect(control).to_have_css('opacity', '0')
            page.keyboard.press('Tab')
            expect(control).to_be_focused()
            expect(control).to_have_css('outline-style', 'solid')
            expect(control).to_have_css('outline-width', '2px')
            page.mouse.move(1400, 850)

        book_row = page.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        close_editor(book_row, 'Escape')
        book_row.locator('.book').click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        song_row = page.locator(f'li:has(.songrow[data-i="{self.song.pk}"])')
        close_editor(song_row, 'Enter')
        page.click('.rail__btn[aria-label="Tata Ibadah"]')
        tatib_row = page.locator(f'li:has(.book[data-name="{self.service.pk}"])')
        close_editor(tatib_row, 'Escape')
        self._close_browser()

    def test_keyboard_close_does_not_leave_row_edit_control_visible(self):
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        row = page.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        link = row.locator('.book')
        control = row.locator('.row-edit')

        for close_key in ('Escape', 'Enter'):
            link.focus()
            page.keyboard.press('Tab')
            expect(control).to_be_focused()
            page.keyboard.press('Enter')
            page.wait_for_selector('dialog[open]')
            page.mouse.move(1400, 850)
            if close_key == 'Enter':
                page.locator('.editor__cancel').focus()
            page.keyboard.press(close_key)
            page.wait_for_function("!document.querySelector('dialog[open]')")
            expect(link).to_be_focused()
            expect(control).to_have_css('opacity', '0')
            self.assertEqual(control.evaluate('el => getComputedStyle(el).pointerEvents'), 'none')
            page.keyboard.press('Tab')
            expect(control).to_be_focused()
            expect(control).to_have_css('opacity', '1')
            page.mouse.move(1400, 850)

    def test_keyboard_can_tab_to_a_hidden_row_edit_control(self):
        page = self._page(reverse('web-index'))
        page.click('.rail__btn[aria-label="Kidung"]')
        row = page.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        control = row.locator('.row-edit')
        row.locator('.book').focus()
        page.keyboard.press('Tab')
        expect(control).to_be_focused()
        expect(control).to_have_css('opacity', '1')

    def test_hymn_rows_do_not_offer_edit_controls(self):
        page = self._page(reverse('web-book', args=[self.hymn.pk]))
        self.assertEqual(page.locator('#chList .row-edit').count(), 0)   # its songs
        hymn_panel = self._page(reverse('web-books'))
        hymn_row = hymn_panel.locator(f'li:has(.book[data-name="{self.hymn.pk}"])')
        self.assertEqual(hymn_row.locator('.row-edit').count(), 0)
        free_row = hymn_panel.locator(f'li:has(.book[data-name="{self.book.pk}"])')
        self.assertEqual(free_row.locator('.row-edit').count(), 1)

    def test_validation_error_stays_in_the_modal(self):
        page = self._page(reverse('web-books'))
        page.click('#panelAdd')
        page.wait_for_selector('dialog[open]')
        self._fill(page, 'name', self.book.name)             # already used globally
        expect(page.locator('[name="lang"]')).to_have_count(0)
        page.click('.editor__save')
        expect(page.locator('dialog[open]')).to_have_count(1)  # still open
        expect(page.locator('.editor__error')).to_contain_text(
            'That songbook already exists.')
        expect(page.locator('[name="name"]')).to_have_value(self.book.name)
        self._close_browser()

    def test_the_shell_survives_a_save(self):
        page = self._page(reverse('web-song', args=[self.song.pk]))
        start = page.url
        page.click('#songAdd')
        page.wait_for_selector('dialog[open]')
        self._save(page, title='Lagu Kedua')
        expect(page.locator('dialog[open]')).to_have_count(0)
        self.assertEqual(page.url, start)                      # one page, no reload
        expect(page.locator('.read__title')).to_contain_text('Alpha')   # the stage kept reading
        self._close_browser()
        self.assertTrue(songs.Song.objects.filter(title='Lagu Kedua').exists())
