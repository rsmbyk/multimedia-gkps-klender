"""The accepted service-order song typography (spec 059)."""
from datetime import date
import os
from pathlib import Path
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SongLabelTypographyE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 12), is_active=True)
        book = songs.Book.objects.create(name='Haleluya', short_name='HAL', is_hymn_book=True)
        other = songs.Book.objects.create(name='Lagu lainnya', is_hymn_book=False)
        self.entries = []
        for order, song in enumerate([
            songs.Song.objects.create(book=book, number=1, title='Jahowa Sihol Pujionku'),
            songs.Song.objects.create(book=other, title='Mars Sekolah GKPS'),
            songs.Song.objects.create(book=book, number=10, title='Paturut Ham Bennami ' * 3),
            songs.Song.objects.create(book=book, number=11, title=''),
        ], 1):
            for number in range(1, 8):
                songs.Verse.objects.create(song=song, number=number, lyric=f'Bait {number}')
            self.entries.append(tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=order, kind=tatib.ServiceEntryKind.SONG,
                song=song, verses=list(range(1, 8)) if order == 1 else [1, 3]))
        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_load_state('networkidle')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def row(self, index):
        return self.page.locator(f'#chList .songrow[data-i="e{self.entries[index].pk}"]')

    def test_typography_wrapping_and_theme_states(self):
        row = self.row(0)
        expect(row.locator('.songrow__reference')).to_have_text('HAL 1')
        expect(row.locator('.songrow__title')).to_have_text('Jahowa Sihol Pujionku')
        expect(row.locator('.songrow__verses')).to_have_text('Bait 1-7')
        expect(row.locator('.songrow__reference')).to_have_css('font-weight', '600')
        expect(row.locator('.songrow__reference')).to_have_css('font-size', '12px')
        expect(row.locator('.songrow__title')).to_have_css('font-size', '14px')
        expect(row.locator('.songrow__verses')).to_have_css('font-size', '12px')
        expect(self.row(1).locator('.songrow__reference')).to_have_count(0)
        expect(self.row(1).locator('.songrow__title')).to_have_text('Mars Sekolah GKPS')
        expect(self.row(3).locator('.songrow__title')).to_have_count(0)
        for theme in ('light', 'dark'):
            self.page.evaluate('(theme) => document.documentElement.dataset.theme = theme', theme)
            for width in (404, 280):
                self.page.evaluate('(width) => document.documentElement.style.setProperty("--songsp-w", width + "px")', width)
                long_row = self.row(2)
                heading = long_row.locator('.songrow__heading').bounding_box()
                verses = long_row.locator('.songrow__verses').bounding_box()
                self.assertGreater(heading['height'], 20)
                self.assertGreaterEqual(verses['y'] + .5, heading['y'] + heading['height'])
                self.assertAlmostEqual(verses['x'], heading['x'], delta=1)
                self.assertTrue(long_row.evaluate('el => el.scrollWidth <= el.clientWidth'))
            # Check the actual composed background, including translucent hover, for AA.
            for selected in (False, True):
                if selected:
                    row.evaluate('el => el.setAttribute("aria-current", "true")')
                else:
                    row.evaluate('el => el.removeAttribute("aria-current")')
                row.hover()
                contrast = row.locator('.songrow__verses').evaluate(r"""el => {
                    const rgb = s => s.match(/[\d.]+/g).map(Number);
                    const fg = rgb(getComputedStyle(el).color);
                    let bg = rgb(getComputedStyle(document.body).backgroundColor);
                    const parents = [];
                    for (let p = el; p; p = p.parentElement) parents.unshift(p);
                    for (const p of parents) {
                        const c = rgb(getComputedStyle(p).backgroundColor), a = c[3] ?? 1;
                        bg = bg.map((v, i) => c[i] * a + v * (1 - a));
                    }
                    const lum = c => c.slice(0, 3).map(v => {
                        v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
                    }).reduce((v, c, i) => v + c * [.2126, .7152, .0722][i], 0);
                    const a = lum(fg), b = lum(bg);
                    return (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
                }""")
                self.assertGreaterEqual(contrast, 4.5, (theme, selected))
        screenshot = os.environ.get('SONG_LABEL_PREVIEW')
        if screenshot:
            self.page.evaluate('document.documentElement.dataset.theme = "light"; document.documentElement.style.setProperty("--songsp-w", "404px")')
            self.page.mouse.move(1400, 850)
            Path(screenshot).parent.mkdir(parents=True, exist_ok=True)
            self.page.locator('.chapters').screenshot(path=screenshot)

    def test_filter_and_selection_use_the_complete_song_label(self):
        self.page.locator('#songFilter').fill('jahowa')
        expect(self.row(0)).to_be_visible()
        expect(self.row(1)).not_to_be_visible()
        self.row(0).click()
        expect(self.page.locator(f'#ti-e{self.entries[0].pk}')).to_be_visible()
        self.page.locator('#songFilter').fill('')
        expect(self.row(1)).to_be_visible()
        self.row(1).click()
        expect(self.page.locator(f'#ti-e{self.entries[1].pk}')).to_be_visible()
