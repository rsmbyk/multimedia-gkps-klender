"""The referenced-verse notice sits in the action row (spec 232).

Browser cases read the fetched editor fragment's painted boxes and computed styles on the real
dialog; they do not assert a stylesheet string. HTTP cases check the count, the guard and the
other editors. The two live in different classes because Playwright's sync API makes Django's
async-unsafe guard reject test-client calls from the same test.
"""
import json
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


MEASURE = """() => {
  const row = document.querySelector('#editorContent .editor__actions');
  const note = row && row.querySelector('.editor__refnote');
  const del = document.querySelector('#editorContent [data-verse-delete]');
  const probe = document.createElement('div');
  probe.style.cssText = 'position:absolute;left:-9999px;background:var(--rail-bg);' +
    'border:1px solid var(--divider);color:var(--head-ink)';
  document.body.appendChild(probe);
  const ps = getComputedStyle(probe);
  const tokens = {bg: ps.backgroundColor, border: ps.borderColor, ink: ps.color};
  probe.remove();
  const inkProbe = document.createElement('div');
  inkProbe.style.cssText = 'position:absolute;left:-9999px;color:var(--ink)';
  document.body.appendChild(inkProbe);
  tokens.inkStrong = getComputedStyle(inkProbe).color;
  inkProbe.remove();
  const box = el => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return {x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1),
      h: +r.height.toFixed(1), font: s.fontSize, line: s.lineHeight,
      weight: s.fontWeight, bg: s.backgroundColor, border: s.borderColor,
      ink: s.color, opacity: s.opacity, cursor: s.cursor};
  };
  const glyph = note && note.querySelector('svg');
  const numeral = note && note.querySelector('b');
  return {
    row: row ? box(row) : null,
    order: row ? [...row.children].map(el => el.className.split(' ')[0]) : [],
    note: note ? Object.assign(box(note), {text: note.textContent.replace(/\\s+/g, ' ').trim(), id: note.id}) : null,
    glyph: glyph ? box(glyph) : null,
    numeral: numeral ? {text: numeral.textContent, weight: getComputedStyle(numeral).fontWeight,
      ink: getComputedStyle(numeral).color} : null,
    del: del ? Object.assign(box(del), {disabled: del.disabled, describedBy: del.getAttribute('aria-describedby')}) : null,
    tokens: tokens,
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
  };
}"""


class Fixtures:
    def make_fixtures(self):
        book = songs.Book.objects.create(
            name='Reference Book', short_name='RB', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=book, number=1, title='Reference song')
        self.referenced = songs.Verse.objects.create(
            song=self.song, number=1, lyric='referenced line')
        self.free = songs.Verse.objects.create(
            song=self.song, number=2, lyric='free line')
        self.service_with_verse('Ibadah Satu')

    def service_with_verse(self, name):
        service = tatib.TataIbadah.objects.create(name=name, is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=service, kind=tatib.ServiceEntryKind.SONG, order_number=1,
            song=self.song, verses=[self.referenced.pk])
        return service


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class VerseReferenceNoticeE2ETests(Fixtures, StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.make_fixtures()
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

    def _page(self, width=1366, height=900, color_scheme='light'):
        page = self.browser.new_page(
            viewport={'width': width, 'height': height},
            color_scheme=color_scheme, device_scale_factor=1)
        page.goto(self.live_server_url + reverse('web-song', args=[self.song.pk]))
        page.wait_for_selector('[data-verse-edit]')
        return page

    @staticmethod
    def _open(page, number=1):
        page.locator('[data-verse-edit]').nth(number - 1).evaluate('el => el.click()')
        page.wait_for_selector('#editorModal[open] .editor__actions')
        page.wait_for_timeout(150)
        return page.evaluate(MEASURE)

    # --- US1: the reason sits beside the disabled action --------------------
    def test_note_leads_the_action_row(self):
        page = self._page()
        state = self._open(page)
        self.assertEqual(state['order'][0], 'editor__refnote', state['order'])
        self.assertEqual(
            state['note']['text'], 'Used in 1 Tata Ibadah — delete unavailable')
        self.assertTrue(state['del']['disabled'])
        page.close()

    def test_note_type_and_glyph_use_existing_tokens(self):
        page = self._page()
        state = self._open(page)
        self.assertEqual(state['glyph']['w'], 15)
        self.assertEqual(state['glyph']['h'], 15)
        self.assertEqual(state['note']['font'], '12px')
        self.assertEqual(state['note']['line'], '18px')
        self.assertEqual(state['note']['ink'], state['tokens']['ink'])
        self.assertEqual(state['numeral']['text'], '1')
        self.assertEqual(state['numeral']['weight'], '700')
        self.assertEqual(state['numeral']['ink'], state['tokens']['inkStrong'])
        page.close()

    def test_desktop_row_keeps_its_height(self):
        page = self._page()
        state = self._open(page)
        self.assertEqual(state['row']['h'], 38, state['row'])
        self.assertEqual(state['note']['h'], 18, state['note'])
        page.close()

    def test_disabled_delete_is_neutral(self):
        page = self._page()
        state = self._open(page)
        self.assertEqual(state['del']['opacity'], '1')
        self.assertEqual(state['del']['cursor'], 'not-allowed')
        self.assertEqual(state['del']['bg'], state['tokens']['bg'])
        self.assertEqual(state['del']['border'], state['tokens']['border'])
        self.assertEqual(state['del']['ink'], state['tokens']['ink'])
        page.close()

    def test_button_is_described_by_the_note(self):
        page = self._page()
        state = self._open(page)
        self.assertTrue(state['note']['id'])
        self.assertEqual(state['del']['describedBy'], state['note']['id'])
        page.close()

    def test_unreferenced_editor_has_no_note(self):
        page = self._page()
        state = self._open(page, number=2)
        self.assertIsNone(state['note'])
        self.assertFalse(state['del']['disabled'])
        page.close()

    # --- US2: the narrow dialog ---------------------------------------------
    def test_narrow_row_wraps_the_note_above_the_buttons(self):
        page = self._page(width=420, height=900)
        state = self._open(page)
        self.assertEqual(state['note']['w'], state['row']['w'], state['note'])
        self.assertEqual(state['note']['h'], 18, state['note'])
        self.assertEqual(state['row']['h'], 66, state['row'])
        self.assertGreater(state['del']['y'], state['note']['y'])
        self.assertFalse(state['overflow'])
        page.close()

    def test_narrow_buttons_keep_their_row(self):
        page = self._page(width=420, height=900)
        state = self._open(page)
        self.assertEqual(state['del']['h'], 38)
        self.assertEqual(state['del']['y'], state['row']['y'] + 28)
        self.assertEqual(state['order'][0], 'editor__refnote')
        page.close()

    def test_both_themes_use_existing_tokens(self):
        for scheme in ('light', 'dark'):
            page = self._page(color_scheme=scheme)
            state = self._open(page)
            self.assertEqual(state['note']['ink'], state['tokens']['ink'], scheme)
            self.assertEqual(state['del']['bg'], state['tokens']['bg'], scheme)
            self.assertEqual(state['del']['opacity'], '1', scheme)
            page.close()


class VerseReferenceNoticeFragmentTests(Fixtures, TestCase):
    """HTTP-side guards; no browser, so Django's async guard stays out of the way."""

    def setUp(self):
        super().setUp()
        self.make_fixtures()

    def test_other_editors_have_no_reference_note(self):
        response = self.client.get(
            reverse('web-editor-edit', args=['song', self.song.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'editor__refnote', response.content)

    def test_delete_is_still_refused(self):
        response = self.client.post(
            reverse('web-verse-delete', args=[self.referenced.pk]),
            HTTP_X_REQUESTED_WITH='fetch')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['count'], 1)

    def test_count_tracks_the_guard(self):
        self.service_with_verse('Ibadah Dua')
        self.service_with_verse('Ibadah Tiga')
        response = self.client.get(
            reverse('web-editor-edit', args=['verse', self.referenced.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Used in <b>3</b> Tata Ibadah', html=False)
        self.assertContains(response, '— delete unavailable', html=False)
