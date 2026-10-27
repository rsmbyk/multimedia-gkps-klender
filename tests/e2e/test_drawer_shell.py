"""The drawer shell on small screens (spec 138).

Every assertion is a rectangle, a computed style or one of the shell's own state
attributes — the three things the spec's success criteria name. Run under
Django's runner through ``StaticLiveServerTestCase``; skips cleanly without
Playwright.
"""
from datetime import date
import re
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

OVERLAY_MAX = 1272
PHONE_MAX = 720

STATE = """() => {
  const d = document.documentElement.dataset;
  return {
    nav: d.nav, ch: d.ch, rail: d.rail || 'closed',
    drawerOpen: d.drawerOpen || null, section: d.section, mode: d.mode || null,
  };
}"""

BOX = """(selector) => {
  const el = document.querySelector(selector);
  if (!el) return null;
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  return {
    left: Math.round(r.left), right: Math.round(r.right),
    top: Math.round(r.top), bottom: Math.round(r.bottom),
    width: Math.round(r.width), height: Math.round(r.height),
    visible: !!el.getClientRects().length && cs.visibility !== 'hidden',
    z: Number(cs.zIndex) || 0,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DrawerShellE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 25), is_active=True)
        for order, text in enumerate(
                ['Nyanyian pembuka.', 'Doa pembuka.'] + [f'Bagian {n}.' for n in range(3, 13)], 1):
            tatib.ServiceEntry.objects.create(
                tatib=self.service, kind=tatib.ServiceEntryKind.TEXT,
                order_number=order, text=text)
        self.other_service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu Pelajar', date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.other_service, kind=tatib.ServiceEntryKind.TEXT,
            order_number=1, text='Nyanyian pembuka.')

        self.songbook = songs.Book.objects.create(name='Buku Ende', short_name='BE',
                                                  is_hymn_book=True)
        self.song = songs.Song.objects.create(book=self.songbook, number=1, title='Sihol Pujionku')
        songs.Verse.objects.create(song=self.song, number=1, lyric='Bait satu')
        self.song2 = songs.Song.objects.create(book=self.songbook, number=2, title='Haholongan')
        songs.Verse.objects.create(song=self.song2, number=1, lyric='Bait satu')

        indonesian = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=indonesian, name='Terjemahan Baru',
                                               abbreviation='TB')
        self.book = book = bible.Book.objects.create(name='Kej', testament='old', number_of_chapters=50)
        self.translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Kejadian')
        bible.Verse.objects.create(book_translation=self.translation, chapter=1, verse=1,
                                   text='Pada mulanya Allah menciptakan langit dan bumi.')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)     # a missing element is a red test, not a hang

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    # -- helpers ---------------------------------------------------------

    def open(self, view, *args):
        self.page.goto(self.live_server_url + reverse(view, args=args))
        self.page.wait_for_load_state('networkidle')
        expect(self.page.locator('.rail')).to_be_attached()

    def at(self, width, height=900):
        self.page.set_viewport_size({'width': width, 'height': height})
        self.page.wait_for_timeout(200)

    def state(self):
        return self.page.evaluate(STATE)

    def box(self, selector):
        return self.page.evaluate(BOX, selector)

    def stage_width(self):
        return self.box('.stage')['width']

    def visible(self, selector):
        result = self.box(selector)
        return bool(result and result['visible'] and result['width'] > 0)

    def open_rail_section(self, section='tatib'):
        self.page.click(f'.rail__menu .rail__btn[data-panel="{section}"]')
        self.page.wait_for_timeout(260)

    def open_menu(self):
        self.page.click('#drawerControl')
        self.page.wait_for_timeout(260)

    def close_stack(self):
        """Put the shell back to the page: the server boots the desktop's open panel."""
        state = self.state()
        for _ in range(4):
            state = self.state()
            if state['rail'] == 'closed' and state['nav'] == 'closed' and state['ch'] == 'closed':
                break
            self.page.keyboard.press('Escape')
            self.page.wait_for_timeout(400)
        state = self.state()
        self.assertEqual((state['rail'], state['nav'], state['ch']),
                         ('closed', 'closed', 'closed'))

    def wait_for_url(self, fragment):
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))

    # -- US1: a drawer over the page ------------------------------------

    def test_the_stage_keeps_its_width_when_a_drawer_opens(self):
        self.open('web-tatib-service', self.service.pk)
        for width in (1024, 768):
            self.at(width)
            self.close_stack()
            closed = self.stage_width()
            self.open_rail_section()
            one = self.stage_width()
            self.assertEqual(closed, one, (width, 'level 1 moved the stage'))
            self.assertEqual(self.state()['drawerOpen'], 'true', width)
            self.assertFalse(self.visible('.drawer-backdrop') is False, (width, 'no backdrop'))

    def test_the_columns_layout_is_unchanged_above_the_breakpoint(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1440)
        self.close_stack()
        closed = self.stage_width()
        self.open_rail_section()
        one = self.stage_width()
        self.assertLess(one, closed, 'the desktop no longer pushes')
        self.assertIsNone(self.state()['mode'], 'the overlay must not apply above the breakpoint')

    # -- US2: one stack --------------------------------------------------

    def test_the_second_level_covers_its_parent(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        self.page.wait_for_timeout(300)
        state = self.state()
        self.assertEqual((state['nav'], state['ch']), ('open', 'open'), 'the stack did not open')
        panel = self.box('#panel')
        chapters = self.box('#chapters')
        self.assertEqual(panel['left'], chapters['left'])
        self.assertEqual(panel['width'], chapters['width'])
        self.assertGreaterEqual(chapters['z'], panel['z'])

    def test_a_drawer_rests_behind_the_rail(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        rail = self.box('.rail')
        panel = self.box('#panel')
        self.assertGreater(rail['z'], panel['z'], 'the rail is not painted above the drawer')
        closed = self.box('#panel')
        self.assertLessEqual(closed['right'], rail['right'] + 1,
                             'a closed drawer is not behind the rail')

    def test_only_one_sections_stack_is_open(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        self.assertTrue(self.visible('#panel'))
        # switching section is a navigation; the new page must not inherit the stack
        self.page.click('.rail__menu .rail__btn[data-panel="kidung"]')
        expect(self.page.locator('html')).to_have_attribute('data-section', 'kidung')
        self.page.wait_for_timeout(400)
        state = self.state()
        # a section switch keeps the stage and the URL; only the lists move
        self.assertEqual(state['section'], 'kidung')
        self.assertEqual((state['nav'], state['ch']), ('open', 'closed'))

    # -- US3: the backdrop closes, the rail restores ---------------------

    def test_the_backdrop_closes_the_stack(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        self.assertTrue(self.visible('.drawer-backdrop'))
        self.page.mouse.click(1000, 450)           # the dimmed page, past the drawers
        self.page.wait_for_timeout(300)
        state = self.state()
        self.assertEqual((state['nav'], state['ch']), ('closed', 'closed'))
        self.assertIsNone(state['drawerOpen'])

    def test_the_rail_reopens_the_last_level(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        self.page.mouse.click(1000, 450)
        self.page.wait_for_timeout(300)
        self.open_rail_section()
        self.page.wait_for_timeout(300)
        state = self.state()
        self.assertEqual((state['nav'], state['ch']), ('open', 'open'))

    def test_escape_closes_the_stack(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(700)      # the wipe runs: 200ms + its timer
        state = self.state()
        self.assertEqual((state['rail'], state['nav'], state['ch']), ('closed', 'closed', 'closed'))

    # -- US4: the phone --------------------------------------------------

    def test_the_phone_shows_the_toolbar_and_no_strip(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.assertTrue(self.visible('.topbar'), 'no toolbar at the phone width')
        self.assertLessEqual(self.box('.rail')['right'], 1, 'the rail strip is still on screen')
        self.assertEqual(self.stage_width(), 425)
        self.assertTrue(self.visible('#themeBtn') or self.visible('.topbar #themeBtn'),
                        'the theme control is not in the toolbar')
        self.assertLessEqual(self.box('#themeBtn')['right'], 425)

    def test_the_phone_drawers_span_the_window(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        self.page.wait_for_timeout(300)
        panel = self.box('#panel')
        self.assertEqual((panel['left'], panel['width']), (0, 425))

    def test_the_control_opens_and_closes_the_stack(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.assertEqual(self.page.evaluate(
            "() => document.querySelector('#drawerControl').dataset.glyph"), 'menu')
        self.open_menu()
        self.assertEqual(self.state()['rail'], 'open')
        self.assertEqual(self.page.evaluate(
            "() => document.querySelector('#drawerControl').dataset.glyph"), 'close')
        self.page.click('#drawerControl')
        self.page.wait_for_timeout(250)
        state = self.state()
        self.assertEqual((state['rail'], state['nav'], state['ch']), ('closed', 'closed', 'closed'))

    def test_the_menu_lists_the_sections_with_their_names(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        names = self.page.evaluate(
            "() => [...document.querySelectorAll('.rail__menu .rail__btn .rail__name')]"
            ".filter((n) => n.getClientRects().length).map((n) => n.textContent.trim())")
        self.assertEqual(names, ['Search', 'Alkitab', 'Kidung', 'Tata Ibadah', 'Media Library'])
        self.assertFalse(self.visible('.rail__logo'), 'the logo is inside the menu drawer')

    def test_the_project_control_is_hidden_on_a_phone(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.assertFalse(self.visible('[data-project-open]'), 'the Project control is still drawn')
        self.at(1024)
        self.assertTrue(self.visible('[data-project-open]'))

    def test_a_service_offers_no_contents_drawer_on_a_phone(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        self.page.wait_for_timeout(300)
        state = self.state()
        self.assertEqual(state['nav'], 'open')
        self.assertEqual(state['ch'], 'closed', 'a service opened a contents drawer on a phone')

    def test_a_sections_list_opens_over_the_menu(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        self.page.wait_for_timeout(300)
        state = self.state()
        self.assertEqual((state['rail'], state['nav']), ('open', 'open'),
                         'the menu closed instead of staying underneath')
        self.assertGreater(self.box('#panel')['z'], self.box('.rail')['z'])

    def test_a_service_row_on_a_phone_opens_the_page(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        self.page.wait_for_timeout(300)
        self.page.click(f'#panelBody a[href="{reverse("web-tatib-service", args=[self.other_service.pk])}"]')
        self.wait_for_url(f'/tatib/{self.other_service.pk}/')
        self.page.wait_for_timeout(400)
        self.assertIn(f'/tatib/{self.other_service.pk}/', self.page.url)
        state = self.state()
        self.assertEqual((state['rail'], state['nav'], state['ch']), ('closed', 'closed', 'closed'))

    def test_a_selected_menu_row_paints_its_name_in_the_icon_ink(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        self.page.wait_for_timeout(400)
        colours = self.page.evaluate("""() => {
          const row = document.querySelector('.rail__menu .rail__btn[aria-current], '
            + '.rail__menu .rail__btn[aria-expanded="true"]');
          if (!row) return null;
          const name = row.querySelector('.rail__name');
          return {name: getComputedStyle(name).color, row: getComputedStyle(row).color};
        }""")
        self.assertIsNotNone(colours, 'no selected row in the menu')
        self.assertEqual(colours['name'], colours['row'])

    # -- US5: nothing behind moves --------------------------------------

    def test_the_page_behind_a_drawer_does_not_scroll(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024, 400)
        self.close_stack()
        self.page.evaluate("() => window.scrollTo(0, 120)")
        self.page.wait_for_timeout(120)
        before = self.page.evaluate("() => Math.round(window.scrollY)")
        self.assertGreater(before, 0, 'the fixture page is too short to scroll')
        self.open_rail_section()
        self.page.mouse.wheel(0, 400)
        self.page.wait_for_timeout(250)
        after = self.page.evaluate("() => Math.round(window.scrollY)")
        self.assertEqual(before, after, 'the page scrolled behind the drawer')

    def test_each_drawers_own_back_control_steps_one_level(self):
        self.open('web-bible-chapter', self.book.pk, 1)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="alkitab"]')
        self.page.wait_for_timeout(400)
        self.assertEqual(self.state()['nav'], 'open')
        # a book row opens the chapter list; that drawer closes with its own control
        self.page.locator('#panelBody a.book').first.click()
        self.page.wait_for_timeout(900)
        state = self.state()
        self.assertEqual((state['nav'], state['ch']), ('open', 'open'))
        self.page.click('#chCollapse')
        self.page.wait_for_timeout(500)
        state = self.state()
        self.assertEqual(state['ch'], 'closed')
        self.assertEqual(state['nav'], 'open')

    def test_a_rows_edit_control_shows_without_hover(self):
        self.context.close()
        self.context = self.browser.new_context(viewport={'width': 1024, 'height': 900},
                                                has_touch=True, is_mobile=False)
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        opacity = self.page.evaluate(
            "() => getComputedStyle(document.querySelector('#panelBody .row-edit')).opacity")
        self.assertEqual(opacity, '1', 'the edit control is still hover-only under a touch pointer')

    def test_a_phone_row_is_two_lines(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        self.open_menu()
        self.page.click('.rail__menu .rail__btn[data-panel="tatib"]')
        self.page.wait_for_timeout(300)
        metrics = self.page.evaluate("""() => {
          const row = document.querySelector('#panelBody .book');
          const name = row.querySelector('.book__n').getBoundingClientRect();
          const date = row.querySelector('.book__s').getBoundingClientRect();
          const edit = row.parentElement.querySelector('.row-edit').getBoundingClientRect();
          return {nameBottom: Math.round(name.bottom), dateTop: Math.round(date.top),
                  nameRight: Math.round(name.right), editLeft: Math.round(edit.left),
                  editOpacity: getComputedStyle(row.parentElement.querySelector('.row-edit')).opacity};
        }""")
        self.assertGreaterEqual(metrics['dateTop'], metrics['nameBottom'] - 1,
                                'the date is not under the name')
        self.assertLess(metrics['nameRight'], metrics['editLeft'], 'the name runs under the pencil')
        self.assertEqual(metrics['editOpacity'], '1')

    def test_the_toolbar_icons_share_one_size(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(425)
        widths = self.page.evaluate("""() => {
          /* the drawn glyph, not a sibling waiting its turn: the theme button
             holds three, two of them scaled and transparent at any moment */
          const drawn = (sel) => {
            const el = [...document.querySelectorAll(sel)].find((n) => {
              const cs = getComputedStyle(n);
              return cs.opacity > .5 && n.getClientRects().length;
            });
            return el ? Math.round(el.getBoundingClientRect().width) : null;
          };
          return {control: drawn('#drawerControl svg'), theme: drawn('#themeBtn svg')};
        }""")
        self.assertIsNotNone(widths['control'])
        self.assertIsNotNone(widths['theme'])
        self.assertEqual(widths['control'], widths['theme'])

    def test_resizing_across_the_breakpoint_leaves_a_fitting_state(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        self.at(1440)
        state = self.state()
        self.assertEqual(state['rail'], 'closed')
        self.at(425)
        self.assertTrue(self.visible('.topbar'))
        self.at(1440)
        self.assertFalse(self.visible('.topbar'))

    def test_a_navigation_keeps_the_open_stack(self):
        self.open('web-tatib-service', self.service.pk)
        self.at(1024)
        self.close_stack()
        self.open_rail_section()
        # the contents cover their parent: step back to the list, then choose
        self.page.click('#chCollapse')
        self.page.wait_for_timeout(500)
        before = self.state()
        self.page.click(f'#panelBody a[href="{reverse("web-tatib-service", args=[self.other_service.pk])}"]')
        self.wait_for_url(f'/tatib/{self.other_service.pk}/')
        self.page.wait_for_timeout(500)
        after = self.state()
        self.assertIn(f'/tatib/{self.other_service.pk}/', self.page.url)
        self.assertEqual(after['nav'], before['nav'], 'the stack closed under the operator')
        # the arriving service brings its own contents, exactly as today
        self.assertEqual(after['ch'], 'open')
