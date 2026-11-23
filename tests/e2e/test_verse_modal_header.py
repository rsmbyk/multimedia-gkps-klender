"""The verse editor header paints one rule, with the other editors' spacing (spec 226).

The large-dialog title rule outranked the header reset, so the title drew its own short rule 37.5px
above the header's divider. These cases read the painted boxes and gaps on the real dialogs; they
do not assert a stylesheet string.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const head = document.querySelector('#editorContent .editor__head');
  if (!head) return null;
  const title = head.querySelector('.editor__title');
  const dialog = document.getElementById('editorModal');
  const label = document.querySelector('#editorContent .editor__field label');
  const box = el => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return {
      x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1),
      h: +r.height.toFixed(1), bottom: +r.bottom.toFixed(1),
      borderBottomWidth: s.borderBottomWidth, padding: s.padding,
      fontSize: s.fontSize, fontWeight: s.fontWeight
    };
  };
  const range = document.createRange(); range.selectNodeContents(title);
  const tr = range.getBoundingClientRect();
  const ruled = [...head.querySelectorAll('*')]
    .filter(el => parseFloat(getComputedStyle(el).borderBottomWidth) > 0);
  return {
    title: box(title), head: box(head), dialog: box(dialog),
    label: label ? box(label) : null,
    titleText: title.textContent.trim(),
    titleTextX: +tr.x.toFixed(1), titleTextBottom: +tr.bottom.toFixed(1),
    gapTop: +(tr.y - dialog.getBoundingClientRect().y).toFixed(1),
    gapBelow: +(head.getBoundingClientRect().bottom - 1 - tr.bottom).toFixed(1),
    gapBorderToLabel: label
      ? +(label.getBoundingClientRect().y - head.getBoundingClientRect().bottom).toFixed(1)
      : null,
    ruledCount: ruled.length,
    ruledClasses: ruled.map(el => el.className),
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class VerseModalHeaderE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        book = songs.Book.objects.create(
            name='Header Rule Book', short_name='HR', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=book, number=1, title='Header rule song')
        for number in (1, 2):
            songs.Verse.objects.create(
                song=self.song, number=number, lyric='line %d' % number)
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def _page(self, color_scheme='light'):
        page = self.browser.new_page(
            viewport={'width': 1366, 'height': 900},
            color_scheme=color_scheme, device_scale_factor=1)
        page.goto(self.live_server_url + reverse('web-song', args=[self.song.pk]))
        page.wait_for_selector('[data-add-verse]')
        return page

    @staticmethod
    def _open(page, selector, large=True):
        # A verse pencil is transparent at rest; a coordinate click can land on the
        # covering row instead. A DOM click takes the page's own handler.
        page.locator(selector).first.evaluate('el => el.click()')
        page.wait_for_selector('#editorModal[open] .editor__head .editor__title')
        if large:
            page.wait_for_function(
                '() => !!document.querySelector(\'#editorContent [data-editor-size="large"]\')')
        page.wait_for_timeout(150)
        return page.evaluate(MEASURE)

    @staticmethod
    def _assert_one_rule(state):
        assert state is not None, 'the editor dialog never rendered'
        assert state['title']['borderBottomWidth'] == '0px', (
            'the title still paints a %s bottom border' % state['title']['borderBottomWidth'])
        assert state['head']['borderBottomWidth'] == '1px', 'the header divider is missing'
        assert state['ruledCount'] == 0, (
            'header descendants still paint a rule: %s' % state['ruledClasses'])

    def test_new_verse_header_has_one_rule(self):
        page = self._page()
        state = self._open(page, '[data-add-verse]')
        self._assert_one_rule(state)
        self.assertEqual(state['titleText'], 'New verse')
        page.close()

    def test_edit_verse_header_has_one_rule(self):
        page = self._page()
        state = self._open(page, '[data-verse-edit]')
        self._assert_one_rule(state)
        self.assertEqual(state['titleText'], 'Edit verse 1')
        page.close()

    def test_header_gap_matches_the_other_editors(self):
        for color_scheme in ('light', 'dark'):
            with self.subTest(color_scheme=color_scheme):
                page = self._page(color_scheme)
                other = self._open(page, '[data-editor-open="song"]', large=False)
                self.assertEqual(other['title']['fontSize'], '18px')
                self.assertEqual(other['title']['padding'], '0px')
                page.keyboard.press('Escape')
                page.wait_for_function('!document.getElementById("editorModal").open')

                verse = self._open(page, '[data-add-verse]')
                self._assert_one_rule(verse)
                self.assertAlmostEqual(verse['gapTop'], 21, delta=1.5)
                self.assertAlmostEqual(verse['gapBelow'], other['gapBelow'], delta=1.5)
                self.assertAlmostEqual(verse['titleTextX'], 289, delta=1)
                self.assertEqual(verse['title']['fontSize'], '21px')
                self.assertEqual(verse['title']['fontWeight'], '640')
                self.assertAlmostEqual(verse['gapBorderToLabel'], 30, delta=1)
                page.close()

    def test_single_rule_follows_a_narrow_dialog(self):
        page = self._page()
        state = self._open(page, '[data-add-verse]')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.wait_for_timeout(150)
        narrow = page.evaluate(MEASURE)
        self._assert_one_rule(narrow)
        self.assertAlmostEqual(narrow['dialog']['w'], narrow['head']['w'], delta=0.1)
        self.assertLessEqual(narrow['dialog']['w'], 358)
        self.assertGreaterEqual(narrow['dialog']['w'], 300)
        page.close()

    def test_non_verse_editor_header_is_unchanged(self):
        page = self._page()
        state = self._open(page, '[data-editor-open="song"]', large=False)
        self._assert_one_rule(state)
        self.assertEqual(state['titleText'], 'New song')
        self.assertEqual(state['title']['fontSize'], '18px')
        self.assertEqual(state['title']['padding'], '0px')
        self.assertAlmostEqual(state['gapBelow'], 16, delta=1.5)
        self.assertAlmostEqual(state['gapBorderToLabel'], 16, delta=1)
        page.close()
