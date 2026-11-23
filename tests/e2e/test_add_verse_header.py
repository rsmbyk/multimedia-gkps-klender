"""Add verse lives in the song header beside Project while verses exist (spec 231).

These cases assert the observable relationship between the two header actions and that the
moved control still opens the editor. A Django response test cannot read painted boxes, so the
geometry case is a Playwright E2E; the render gates are covered by the fast template tests.
"""
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


BOXES = """() => {
  const box = s => {
    const el = document.querySelector(s);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {x: Math.round(r.x), y: Math.round(r.y),
            w: Math.round(r.width), h: Math.round(r.height)};
  };
  return {
    add: box('.verse-add__btn--head'),
    project: box('.read__project-btn'),
    bodyRow: box('.verse-add'),
    addCount: document.querySelectorAll('[data-add-verse]').length
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AddVerseHeaderE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        book = songs.Book.objects.create(name='Lagu Header', short_name='LH', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=book, title='Header verse song')
        for number in (1, 2):
            songs.Verse.objects.create(
                song=self.song, number=number, lyric=f'line {number}')
        self.empty = songs.Song.objects.create(book=book, title='Header empty song')
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def open_song(self, song):
        self.page.goto(self.live_server_url + reverse('web-song', args=[song.pk]),
                       wait_until='networkidle')
        self.page.wait_for_selector('.read__head-top')

    def test_add_verse_sits_left_of_project_in_header(self):
        self.open_song(self.song)
        boxes = self.page.evaluate(BOXES)
        self.assertEqual(boxes['addCount'], 1)
        self.assertIsNotNone(boxes['add'])
        self.assertIsNotNone(boxes['project'])
        self.assertIsNone(boxes['bodyRow'])
        self.assertEqual(boxes['add']['h'], 34)
        self.assertEqual(boxes['project']['h'], 34)
        self.assertLess(boxes['add']['x'], boxes['project']['x'])
        gap = boxes['project']['x'] - (boxes['add']['x'] + boxes['add']['w'])
        self.assertEqual(gap, 8)

    def test_header_add_verse_opens_editor(self):
        self.open_song(self.song)
        self.page.locator('.verse-add__btn--head').click()
        expect(self.page.locator('#editorModal[open]')).to_be_visible()
        title = self.page.locator('#editorContent .editor__title')
        self.assertEqual(title.inner_text(), 'New verse')
        self.assertEqual(self.errors, [])

    def test_empty_song_has_no_header_actions(self):
        self.open_song(self.empty)
        boxes = self.page.evaluate(BOXES)
        self.assertEqual(boxes['addCount'], 1)
        self.assertIsNone(boxes['add'])
        self.assertIsNone(boxes['project'])
        self.assertIsNotNone(self.page.locator('.entry__empty-actions .verse-add__btn'))
