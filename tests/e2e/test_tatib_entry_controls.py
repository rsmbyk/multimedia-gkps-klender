"""The entry controls, floated in their item (spec 033).

Preview, Edit and Delete belong to their item: they sit at its top-right, over the
words, on a brief backing, and appear while the item is hovered or holds keyboard
focus — and always on a device with no hover.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EntryControlsE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.tatib, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia beserta kita')
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

    def _page(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.tatib.pk]))
        page.wait_for_load_state('networkidle')
        return page

    def test_hovering_the_item_reveals_its_controls_over_the_text(self):
        page = self._page()
        acts = page.locator('.tatib__item .entry__acts').first
        item = page.locator('.tatib__item').first
        self.assertEqual(acts.count(), 1)
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        item.hover()
        expect(acts).to_have_css('opacity', '1')
        item_box, acts_box = item.bounding_box(), acts.bounding_box()
        self.assertGreater(acts_box['x'], item_box['x'] + item_box['width'] / 2)
        self.assertLess(acts_box['y'], item_box['y'] + item_box['height'] / 2)

    def test_keyboard_focus_reveals_the_controls(self):
        page = self._page()
        acts = page.locator('.tatib__item .entry__acts').first
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        page.locator('[data-entry-edit]').first.focus()
        expect(acts).to_have_css('opacity', '1')

    def test_the_add_row_is_not_part_of_the_item(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        bar = page.locator('.entry__add').first
        acts = page.locator('.entry__acts').first
        page.mouse.move(1400, 850)
        expect(acts).to_have_css('opacity', '0')
        bar.hover()
        expect(bar).to_have_css('opacity', '1')               # the bar's own buttons show
        expect(acts).to_have_css('opacity', '0')              # the item above is not revealed
        expect(item).to_have_css('background-color', 'rgba(0, 0, 0, 0)')
        item_box, bar_box = item.bounding_box(), bar.bounding_box()
        self.assertLessEqual(item_box['y'] + item_box['height'], bar_box['y'] + 1)   # no overlap

    def test_hovering_the_item_still_reveals_its_add_row(self):
        page = self._page()
        item = page.locator('.tatib__item').first
        bar = page.locator('.entry__add').first
        page.mouse.move(1400, 850)
        expect(bar).to_have_css('opacity', '0')
        item.hover()
        expect(bar).to_have_css('opacity', '1')

    def test_the_no_hover_rule_shows_the_controls(self):
        # Chromium in CI cannot emulate a touch (no-hover, coarse-pointer) device, so
        # assert the rule that serves one exists and would show the controls.
        page = self._page()
        applied = page.evaluate("""() => {
          for (const sheet of document.styleSheets) {
            let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
            for (const rule of rules) {
              if (!rule.media || !rule.media.mediaText.includes('pointer: coarse')) continue;
              for (const inner of rule.cssRules) {
                if (inner.selectorText && inner.selectorText.includes('.entry__acts')
                    && inner.style.opacity === '1') return true;
              }
            }
          }
          return false;
        }""")
        self.assertTrue(applied, 'the no-hover rule is missing')
