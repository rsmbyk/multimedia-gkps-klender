"""The entry dialog's frame in a browser (spec 133).

The frame is only real in a laid-out page, so the numbers the spec pins — the 840×760 box, the 72.5px
title band, the 788px field gutter, the Text box that fills the leftover height, the 18px gutters at a
narrow window, and a dialog that ignores the page's scroll — are asserted here, on the project's own
route, in Chromium.

Same runner and skip behaviour as the other e2e suites: Django's `LiveServerTestCase`, Playwright's
Python binding, and no database access while the browser is open.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const dialog = document.querySelector('#editorModal');
  const box = (el) => { const r = el.getBoundingClientRect();
    return {x: r.x, y: r.y, w: r.width, h: r.height, bottom: r.bottom}; };
  const style = (el, prop) => getComputedStyle(el).getPropertyValue(prop);
  const grow = dialog.querySelector('[data-editor-grow]');
  return {
    box: box(dialog),
    titleBox: box(dialog.querySelector('.editor__title')),
    titlePadding: style(dialog.querySelector('.editor__title'), 'padding'),
    titleSize: style(dialog.querySelector('.editor__title'), 'font-size'),
    titleDivided: style(dialog.querySelector('.editor__title'), 'border-bottom-width'),
    contentPadding: style(dialog.querySelector('#editorContent'), 'padding'),
    firstField: box(dialog.querySelector('.editor__form > .editor__field')),
    firstFieldMargin: style(dialog.querySelector('.editor__form > .editor__field'), 'margin'),
    textarea: grow ? box(grow.querySelector('textarea')) : null,
    actions: box(dialog.querySelector('.editor__actions')),
    actionsMargin: style(dialog.querySelector('.editor__actions'), 'margin'),
    save: box(dialog.querySelector('.editor__save')),
    viewport: {w: window.innerWidth, h: window.innerHeight},
    scrollY: window.scrollY,
    documentScrolls: document.documentElement.scrollHeight > window.innerHeight,
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EntryDialogFrameE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.empty = tatib.TataIbadah.objects.create(
            name='Ibadah Kosong', date=date(2026, 10, 25), is_active=True)
        # a stage long enough that its later entries sit below the fold of a 900px window
        self.full = tatib.TataIbadah.objects.create(
            name='Ibadah Panjang', date=date(2026, 10, 18), is_active=True)
        for order in range(1, 13):
            tatib.ServiceEntry.objects.create(
                tatib=self.full, order_number=order, kind=tatib.ServiceEntryKind.TEXT,
                text=f'Bagian {order}. ' + 'Salam sejahtera bagi kita semua. ' * 12)
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

    def _page(self, url, width=1440, height=900):
        page = self.browser.new_page(viewport={'width': width, 'height': height})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _open_new(self, page, kind):
        page.wait_for_timeout(400)          # the stage's entrance animation settles
        page.locator(f'[data-entry-open="{kind}"]').first.click(force=True)
        page.wait_for_selector('#editorModal[open]')
        page.wait_for_function(
            "() => { const t = document.querySelector('#editorTitle');"
            " return t && t.textContent.trim().toLowerCase().startsWith('new '); }")
        page.wait_for_timeout(350)          # the dialog's own entrance settles
        return page.evaluate(MEASURE)

    def _open_edit(self, page, index=0):
        """The Edit control sits behind a hover on its row; a DOM click skips the overlap."""
        control = page.locator('[data-entry-edit]').nth(index)
        control.scroll_into_view_if_needed()
        control.hover()
        page.wait_for_timeout(150)
        control.evaluate('el => el.click()')
        page.wait_for_selector('#editorModal[open]')
        page.wait_for_timeout(350)
        return page.evaluate(MEASURE)

    def _close(self, page):
        page.keyboard.press('Escape')
        page.wait_for_selector('#editorModal[open]', state='detached')

    # --- the frame is the media modal's own -----------------------------------

    def test_new_text_dialog_matches_new_media(self):
        page = self._page(reverse('web-tatib-service', args=[self.empty.pk]))
        text = self._open_new(page, 'text')
        self._close(page)
        media = self._open_new(page, 'media')

        self.assertEqual(text['box']['w'], 840)
        self.assertEqual(text['box']['h'], 760)
        self.assertEqual(text['box']['x'], media['box']['x'])
        self.assertEqual(text['box']['y'], media['box']['y'])
        self.assertEqual(text['titleBox']['h'], media['titleBox']['h'])
        self.assertEqual(text['titlePadding'], media['titlePadding'])
        self.assertEqual(text['titlePadding'], '20px 26px')
        self.assertEqual(text['titleSize'], '21px')
        self.assertEqual(text['titleDivided'], '1px')
        self.assertEqual(text['contentPadding'], '0px')
        self.assertEqual(text['firstField']['x'], media['firstField']['x'])
        self.assertEqual(text['firstField']['w'], media['firstField']['w'])
        self.assertEqual(text['firstField']['w'], 788)
        self.assertEqual(text['firstFieldMargin'], media['firstFieldMargin'])
        self.assertEqual(text['actions']['y'], media['actions']['y'])
        self.assertEqual(text['actionsMargin'], media['actionsMargin'])
        self.assertEqual(text['save']['x'], media['save']['x'])
        self.assertFalse(text['documentScrolls'])
        self._close_browser()

    def test_text_box_fills_the_frame(self):
        page = self._page(reverse('web-tatib-service', args=[self.empty.pk]))
        create = self._open_new(page, 'text')
        # the box ends where the action row's own 14px margin begins
        self.assertAlmostEqual(create['textarea']['bottom'] + 14, create['actions']['y'], delta=1)
        self.assertGreater(create['textarea']['h'], 400)      # the six-row box was 131.3

        self._close(page)
        page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.full.pk]))
        page.wait_for_load_state('networkidle')
        edit = self._open_edit(page, index=0)
        self.assertAlmostEqual(edit['textarea']['bottom'] + 14, edit['actions']['y'], delta=1)
        self.assertGreater(edit['textarea']['h'], 450)
        self.assertEqual(edit['box']['h'], 760)
        self._close_browser()

    # --- it holds at a narrow window and at any scroll position ---------------

    def test_narrow_window_uses_the_small_gutters(self):
        page = self._page(reverse('web-tatib-service', args=[self.empty.pk]))
        self._open_new(page, 'text')
        page.set_viewport_size({'width': 390, 'height': 844})   # the frame is under test, not the click
        page.wait_for_timeout(350)
        narrow = page.evaluate(MEASURE)
        # 100vw − 32px is 358, clamped by the UA's own `max-width: calc(100% − 6px − 2em)` for a modal
        self.assertEqual(narrow['box']['w'], 352)
        self.assertEqual(narrow['box']['h'], 760)
        self.assertEqual(narrow['titlePadding'], '16px 18px')
        self.assertAlmostEqual(narrow['firstField']['x'] - narrow['box']['x'], 18, delta=1)
        self.assertAlmostEqual(narrow['textarea']['bottom'] + 14, narrow['actions']['y'], delta=1)
        self.assertFalse(narrow['documentScrolls'])
        self._close_browser()

    def test_dialog_is_centred_on_a_scrolled_page(self):
        page = self._page(reverse('web-tatib-service', args=[self.full.pk]))
        page.evaluate('() => window.scrollTo(0, document.documentElement.scrollHeight)')
        page.wait_for_timeout(250)
        measured = self._open_edit(page, index=11)   # the last of the twelve entries
        self.assertGreater(measured['scrollY'], 0)            # the page really is scrolled
        expected = (measured['viewport']['h'] - measured['box']['h']) / 2
        self.assertAlmostEqual(measured['box']['y'], expected, delta=1)
        self.assertGreaterEqual(measured['box']['y'], 0)
        self.assertLessEqual(measured['box']['bottom'], measured['viewport']['h'])
        self._close_browser()
