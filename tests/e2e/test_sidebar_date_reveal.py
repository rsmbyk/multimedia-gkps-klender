"""Sidebar date and Today-badge reveal states (spec 201).

Headless Chromium on the app's HTTP origin reports ``(hover: hover)`` as false,
so the guarded rule never applies in a LiveServerTestCase browser. These tests
read the shipped selectors out of the same-origin stylesheet and inject them
outside the media guard, then drive real pointer and keyboard states against
the real DOM. A separate assertion keeps the shipped rule honest.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib
from multimedia.web.reading.date_buckets import present_day

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

# Read the display:none rule that hides the row's date / Today badge from the
# app's own stylesheet, including the media guard it currently lives in.
SHIPPED_SELECTORS = """() => {
  const found = [];
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const rule of rules) {
      const inner = rule.cssRules ? [...rule.cssRules] : [rule];
      for (const r of inner) {
        if (r.style && r.style.display === 'none' && r.selectorText &&
            r.selectorText.includes('book__s')) {
          found.push(r.selectorText);
        }
      }
    }
  }
  return found;
}"""

STATE = """(name) => {
  const li = [...document.querySelectorAll('#panelBody li[data-editor-kind]')].find(
    x => x.querySelector('.book__n')?.textContent.trim() === name);
  if (!li) return null;
  const s = li.querySelector('.book__s');
  const t = li.querySelector('.book__today');
  const b = li.querySelector('.book');
  return {
    date: getComputedStyle(s).display,
    badge: t ? getComputedStyle(t).display : null,
    focusWithin: li.matches(':focus-within'),
    hover: li.matches(':hover'),
    active: document.activeElement ? (document.activeElement.className || document.activeElement.tagName) : '',
    activeFocusVisible: document.activeElement ? document.activeElement.matches(':focus-visible') : false,
    height: li.getBoundingClientRect().height,
    label: b ? b.getAttribute('aria-label') : null,
    editOpacity: getComputedStyle(li.querySelector('.row-edit')).opacity,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SidebarDateRevealE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Uji', date=present_day() - __import__('datetime').timedelta(days=3),
            is_active=True)
        self.today = tatib.TataIbadah.objects.create(
            name='Ibadah Hari Ini', date=present_day(), is_active=True)
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open_sidebar(self, page=None):
        page = page or self.page
        page.goto(self.live_server_url + reverse('web-index'))
        page.wait_for_load_state('networkidle')
        if ((page.viewport_size or {}).get('width', 1440) <= 720
                and page.locator('html').get_attribute('data-rail') != 'open'):
            page.locator('#drawerControl').click()
            page.wait_for_timeout(250)
        page.locator('.rail [data-panel="tatib"]').click()
        page.locator('#panelBody li[data-editor-kind]').first.wait_for()
        return page

    def inject_shipped_rule(self, page=None):
        page = page or self.page
        selectors = page.evaluate(SHIPPED_SELECTORS)
        self.assertTrue(selectors, 'the date-hide rule was not found in the stylesheet')
        page.add_style_tag(content=',\n'.join(selectors) + ' { display: none !important; }')
        return selectors

    def probe(self, name, page=None):
        return (page or self.page).evaluate(STATE, name)

    def row(self, name, page=None):
        return (page or self.page).locator('#panelBody li[data-editor-kind]').filter(
            has=(page or self.page).locator('.book__n', has_text=name)).first

    def test_the_shipped_rule_uses_the_action_reveal_not_focus_within(self):
        self.open_sidebar()
        selectors = '\n'.join(self.inject_shipped_rule())
        self.assertNotIn('focus-within', selectors)
        self.assertIn('focus-visible', selectors)
        self.assertIn(':has(', selectors)

    def test_a_clicked_row_paints_its_date_again(self):
        self.open_sidebar()
        self.inject_shipped_rule()
        name = self.service.name
        self.assertEqual(self.probe(name)['date'], 'block')
        self.row(name).locator('.book').hover()
        self.assertEqual(self.probe(name)['date'], 'none')

        self.row(name).locator('.book').click()
        self.page.wait_for_timeout(500)
        self.page.mouse.move(1350, 850)
        self.page.wait_for_timeout(250)
        clicked = self.probe(name)
        self.assertTrue(clicked['focusWithin'], clicked)
        self.assertEqual(clicked['date'], 'block', clicked)

        self.page.mouse.click(1350, 850)
        self.page.wait_for_timeout(150)
        self.assertEqual(self.probe(name)['date'], 'block')

    def test_keyboard_focus_on_an_action_hides_the_date_until_it_leaves(self):
        self.open_sidebar()
        self.inject_shipped_rule()
        name = self.service.name
        self.row(name).locator('.book').focus()
        focused_link = self.probe(name)
        self.assertTrue(focused_link['focusWithin'])
        self.assertEqual(focused_link['date'], 'block', focused_link)

        self.page.keyboard.press('Tab')
        on_pencil = self.probe(name)
        self.assertEqual(on_pencil['active'], 'row-edit', on_pencil)
        self.assertTrue(on_pencil['activeFocusVisible'])
        self.assertEqual(on_pencil['date'], 'none', on_pencil)

        self.page.keyboard.press('Tab')
        on_trash = self.probe(name)
        self.assertEqual(on_trash['active'], 'row-delete', on_trash)
        self.assertEqual(on_trash['date'], 'none', on_trash)

        self.page.keyboard.press('Tab')
        self.assertEqual(self.probe(name)['date'], 'block')

    def test_the_today_badge_follows_the_date_reveal(self):
        self.open_sidebar()
        self.inject_shipped_rule()
        name = self.today.name
        rest = self.probe(name)
        self.assertIsNotNone(rest['badge'])
        self.assertNotEqual(rest['badge'], 'none', rest)

        self.row(name).locator('.book').hover()
        self.assertEqual(self.probe(name)['badge'], 'none')

        self.row(name).locator('.book').click()
        self.page.wait_for_timeout(500)
        self.page.mouse.move(1350, 850)
        self.page.wait_for_timeout(250)
        clicked = self.probe(name)
        self.assertTrue(clicked['focusWithin'])
        self.assertNotEqual(clicked['badge'], 'none', clicked)

    def test_the_row_box_and_label_do_not_change_across_the_states(self):
        self.open_sidebar()
        self.inject_shipped_rule()
        name = self.service.name
        rest = self.probe(name)
        self.row(name).locator('.book').click()
        self.page.wait_for_timeout(500)
        self.page.mouse.move(1350, 850)
        self.page.wait_for_timeout(250)
        clicked = self.probe(name)
        self.assertEqual(clicked['height'], rest['height'])
        self.assertEqual(clicked['label'], rest['label'])
        self.row(name).locator('.book').hover()
        self.assertEqual(self.probe(name)['height'], rest['height'])

    def test_touch_keeps_the_controls_and_date_visible(self):
        context = self.browser.new_context(
            viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        try:
            page = self.open_sidebar(context.new_page())
            self.inject_shipped_rule(page)
            state = self.probe(self.service.name, page)
            self.assertNotEqual(state['date'], 'none', state)
            self.assertEqual(state['editOpacity'], '1', state)
        finally:
            context.close()
