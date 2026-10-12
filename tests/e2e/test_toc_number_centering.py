"""Entry numbers sit at the vertical middle of their Tata Ibadah contents rows (spec 063)."""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# For each contents row: the vertical centers of the row and its number, the text's
# offset from the row top, and the number of rendered text lines.
MEASURE_ROWS = """() => [...document.querySelectorAll('#chList a.songrow')].map(row => {
  const box = el => el.getBoundingClientRect();
  const r = box(row), n = box(row.querySelector('.songrow__c'));
  const t = box(row.querySelector('.songrow__t'));
  return {label: row.dataset.txt.slice(0, 30), rowCenter: r.top + r.height / 2,
          numCenter: n.top + n.height / 2, textTop: t.top - r.top, height: r.height};
})"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TocNumberCenteringE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 12), is_active=True)
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, item_type=tatib.TataIbadahItemType.TEXT, order_number=1,
            text='L : Marilah kita bangkit berdiri! Di dalam nama Allah Bapa, '
                 'dan Tuhan Yesus Kristus, serta Roh Kudus')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=2,
            text='Pembacaan Alkitab\nMazmur 23:1-6')
        book = songs.Book.objects.create(name='Haleluya', short_name='HAL', is_hymn_book=True)
        song = songs.Song.objects.create(book=book, number=1, title='Paturut Ham Bennami ' * 3)
        for number in range(1, 4):
            songs.Verse.objects.create(song=song, number=number, lyric=f'Bait {number}')
        self.song_entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, order_number=3,
            song=song, verses=[1, 2, 3])
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=4,
            title='Votum', text='Pertolongan kita')
        self.book = book
        songs.Song.objects.create(book=book, number=2, title='Ale Jesus')
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def open_service(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_load_state('networkidle')

    def measure(self, baseline_number=False):
        """Measure rows; ``baseline_number`` restores the old alignment for comparison."""
        self.page.evaluate("""(on) => document.querySelectorAll('#chList .songrow__c')
          .forEach(n => { n.style.alignSelf = on ? 'baseline' : ''; })""", baseline_number)
        return self.page.evaluate(MEASURE_ROWS)

    def assert_numbers_centered(self, context):
        rows = self.measure()
        self.assertEqual(len(rows), 4, context)
        for row in rows:
            self.assertAlmostEqual(row['numCenter'], row['rowCenter'], delta=1,
                                   msg=(context, row['label']))
        return rows

    def test_numbers_center_on_rows_of_any_line_count(self):
        self.open_service()
        for theme in ('light', 'dark'):
            self.page.evaluate('(t) => document.documentElement.dataset.theme = t', theme)
            for width in (404, 280):
                self.page.evaluate(
                    '(w) => document.documentElement.style.setProperty("--songsp-w", w + "px")', width)
                before = self.measure(baseline_number=True)
                after = self.assert_numbers_centered((theme, width))
                # Only the number moves: text position and row height stay as they were.
                for old, new in zip(before, after):
                    self.assertAlmostEqual(new['textTop'], old['textTop'], delta=.5,
                                           msg=(theme, width, new['label']))
                    self.assertAlmostEqual(new['height'], old['height'], delta=.5,
                                           msg=(theme, width, new['label']))
                single = after[-1]
                self.assertLess(single['height'], 40, 'Votum is a single-line row')
                self.assertGreater(after[0]['height'], 40, 'the legacy text row wraps')
                if width == 280:
                    self.assertGreater(after[2]['height'], 60, 'the song row has three lines')

    def test_numbers_stay_centered_when_hovered_or_selected(self):
        self.open_service()
        row = self.page.locator(f'#chList .songrow[data-i="e{self.song_entry.pk}"]')
        row.hover()
        self.assert_numbers_centered('hover')
        row.evaluate('el => el.setAttribute("aria-current", "true")')
        self.assert_numbers_centered('selected')

    def test_drag_copy_keeps_the_number_centered(self):
        self.open_service()
        grip = self.page.locator(f'[data-move-grip="{self.song_entry.pk}"]')
        grip.hover()
        box = grip.bounding_box()
        x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
        self.page.mouse.move(x, y)
        self.page.mouse.down()
        self.page.mouse.move(x, y + 10, steps=3)
        ghost = self.page.locator('[data-reorder-ghost]')
        self.assertEqual(ghost.count(), 1)
        centers = ghost.evaluate("""g => {
          const r = g.getBoundingClientRect();
          const n = g.querySelector('.songrow__c').getBoundingClientRect();
          return [r.top + r.height / 2, n.top + n.height / 2];
        }""")
        self.page.mouse.up()
        self.assertAlmostEqual(centers[1], centers[0], delta=1)

    def test_songbook_list_keeps_baseline_numbers(self):
        self.page.goto(self.live_server_url + reverse('web-book', args=[self.book.pk]))
        self.page.wait_for_load_state('networkidle')
        numbers = self.page.locator('.songrow__c')
        self.assertGreater(numbers.count(), 0)
        self.assertEqual(numbers.first.evaluate('n => getComputedStyle(n).alignSelf'), 'auto')
