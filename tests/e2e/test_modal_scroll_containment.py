"""An open modal keeps the scroll to itself (spec 257).

The report has two shapes: a wheel at the end of a modal's own scrollport, and a wheel over a
modal whose view has no range at all. Both used to chain outward — to the document behind the
top-layer dialog, or from a nested picker to the editor content under it. These tests drive real
wheel input over the project's own dialog classes and read both scroll offsets; they do not assert
the stylesheet text.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


INJECT = """({kind, rows}) => {
  document.getElementById('probeDialog')?.close();
  document.getElementById('probeDialog')?.remove();
  const tall = Array.from({length: rows}, (_, i) =>
    `<p style="margin:0;height:28px">row ${i}</p>`).join('');
  const short = '<p style="margin:0">short</p>';
  let html;
  if (kind === 'preview') {
    html = `<dialog class="preview" id="probeDialog"><div class="preview__body">${tall}</div></dialog>`;
  } else if (kind === 'picker') {
    html = `<dialog class="editor" id="probeDialog"><div class="editor__content">` +
      Array.from({length: 10}, (_, i) => `<p style="margin:0;height:40px">tail ${i}</p>`).join('') +
      `<div class="editor__picker-menu" style="position:static"><div class="editor__picker-options">${tall}</div></div></div></dialog>`;
  } else if (kind === 'header') {
    html = `<dialog class="editor" id="probeDialog">` +
      `<div class="editor__head" style="height:52px">HEADER</div>` +
      `<div class="editor__content">${short}</div></dialog>`;
  } else if (kind === 'short') {
    html = `<dialog class="editor" id="probeDialog"><div class="editor__content">${short}</div></dialog>`;
  } else {
    html = `<dialog class="editor" id="probeDialog"><div class="editor__content">${tall}</div></dialog>`;
  }
  const host = document.createElement('div');
  host.innerHTML = html;
  document.body.appendChild(host.firstElementChild);
  document.getElementById('probeDialog').showModal();
}"""

NAMED = [
    '.editor', '.editor__content', '.editor__date-calendar', '.editor__picker-options',
    '.media-entry__panel--library', '.preview', '.preview__body',
    '.media-transfers__list', '.service-media__list', '.generate__body', '.choose__list',
]


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ModalScrollContainmentE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.contexts = []

    def tearDown(self):
        for context in self.contexts:
            context.close()
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self):
        context = self.browser.new_context(viewport={'width': 1200, 'height': 700})
        self.contexts.append(context)
        page = context.new_page()
        page.goto(self.live_server_url + reverse('web-index'), wait_until='domcontentloaded')
        page.wait_for_timeout(150)
        # The reading shell is one viewport tall; give the document a range so a
        # leaked wheel has somewhere visible to go. The CSS under test is the
        # CSS the server actually serves.
        page.evaluate("""() => {
          document.body.style.minHeight = '4000px';
          window.scrollTo(0, 600);
        }""")
        page.wait_for_timeout(80)
        return page

    def _open(self, page, kind='editor', rows=40):
        page.evaluate(INJECT, {'kind': kind, 'rows': rows})
        page.wait_for_timeout(80)

    def _state(self, page, selector):
        return page.evaluate("""(sel) => {
          const el = document.querySelector('#probeDialog ' + sel);
          return {
            doc: Math.round(window.scrollY),
            scrollTop: el ? el.scrollTop : null,
            range: el ? el.scrollHeight - el.clientHeight : null,
            overscroll: el ? getComputedStyle(el).overscrollBehaviorY : null,
            rootOverflow: getComputedStyle(document.documentElement).overflowY,
            clientWidth: document.documentElement.clientWidth,
          };
        }""", selector)

    def _wheel(self, page, selector, steps=8):
        box = page.eval_on_selector('#probeDialog ' + selector, """el => {
          const b = el.getBoundingClientRect();
          return {x: b.x + b.width / 2, y: b.y + b.height / 2};
        }""")
        page.mouse.move(box['x'], box['y'])
        for _ in range(steps):
            page.mouse.wheel(0, 220)
            page.wait_for_timeout(40)

    # --- US1: the end of a scrollport ----------------------------------------

    def test_wheel_at_the_end_of_editor_content_leaves_the_document_still(self):
        page = self._page()
        self._open(page)
        before = self._state(page, '.editor__content')
        self.assertGreater(before['range'], 0)
        self._wheel(page, '.editor__content')
        after = self._state(page, '.editor__content')
        self.assertEqual(after['scrollTop'], after['range'])
        self.assertEqual(after['doc'], 600)

    def test_wheel_at_the_end_of_preview_body_leaves_the_document_still(self):
        page = self._page()
        self._open(page, kind='preview')
        self._wheel(page, '.preview__body')
        after = self._state(page, '.preview__body')
        self.assertGreater(after['range'], 0)
        self.assertEqual(after['scrollTop'], after['range'])
        self.assertEqual(after['doc'], 600)

    def test_picker_options_at_their_end_do_not_scroll_the_editor(self):
        page = self._page()
        self._open(page, kind='picker')
        self._wheel(page, '.editor__picker-options', steps=10)
        options = self._state(page, '.editor__picker-options')
        editor = self._state(page, '.editor__content')
        self.assertGreater(options['range'], 0)
        self.assertEqual(options['scrollTop'], options['range'])
        self.assertEqual(editor['scrollTop'], 0)
        self.assertEqual(options['doc'], 600)

    # --- US2: no range at all -------------------------------------------------

    def test_short_editor_does_not_scroll_the_document(self):
        page = self._page()
        self._open(page, kind='short')
        self._wheel(page, '.editor__content')
        after = self._state(page, '.editor__content')
        self.assertEqual(after['range'], 0)
        self.assertEqual(after['scrollTop'], 0)
        self.assertEqual(after['doc'], 600)

    def test_wheel_over_the_editor_header_leaves_the_document_still(self):
        page = self._page()
        self._open(page, kind='header')
        self._wheel(page, '.editor__head')
        self.assertEqual(self._state(page, '.editor__content')['doc'], 600)

    def test_closing_the_dialog_restores_document_scrolling_at_the_same_offset(self):
        page = self._page()
        self._open(page, kind='short')
        self._wheel(page, '.editor__content', steps=4)
        before = self._state(page, '.editor__content')
        self.assertEqual(before['doc'], 600)
        page.evaluate("document.getElementById('probeDialog').close()")
        page.mouse.move(600, 350)
        for _ in range(4):
            page.mouse.wheel(0, 220)
            page.wait_for_timeout(40)
        after = self._state(page, 'body')
        self.assertGreater(after['doc'], before['doc'])
        self.assertEqual(after['clientWidth'], before['clientWidth'])

    # --- US3: every modal scrollport -----------------------------------------

    def test_every_named_modal_scrollport_contains_scroll(self):
        page = self._page()
        page.evaluate("""(selectors) => {
          const d = document.createElement('dialog');
          d.id = 'probeDialog'; d.className = 'editor';
          d.innerHTML = selectors.filter(s => s !== '.editor' && s !== '.preview').map(
            s => `<div class="${s.slice(1)}"></div>`).join('');
          document.body.appendChild(d); d.showModal();
        }""", NAMED)
        values = page.evaluate("""(selectors) => ({
          root: getComputedStyle(document.documentElement).overflowY,
          values: selectors.map(s => {
            const el = s === '.editor' || s === '.preview'
              ? document.getElementById('probeDialog') : document.querySelector('#probeDialog ' + s);
            return [s, el ? getComputedStyle(el).overscrollBehaviorY : 'missing'];
          }),
        })""", NAMED)
        self.assertEqual(values['root'], 'hidden')
        for selector, value in values['values']:
            self.assertEqual(value, 'contain', selector)
