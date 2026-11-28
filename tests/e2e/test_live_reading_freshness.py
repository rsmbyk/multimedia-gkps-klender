"""Spec 258: stale-page invalidation and sidebar reconciliation in a real browser."""
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover
    HAS_PLAYWRIGHT = False


class Fixtures:
    def make_fixtures(self):
        self.book = songs.Book.objects.create(name='Kidung Harian', short_name='KH')
        self.song = songs.Song.objects.create(book=self.book, number=1, title='Satu')
        self.verse = songs.Verse.objects.create(song=self.song, number=1, lyric='Bait satu')
        self.service = tatib.TataIbadah.objects.create(name='Ibadah', date=date(2026, 11, 1))
        tatib.TataIbadah.objects.filter(pk=self.service.pk).update(version=5)
        self.entry = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LiveReadingFreshnessE2ETests(Fixtures, StaticLiveServerTestCase):
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

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900},
                                     device_scale_factor=1)
        page.add_init_script('window.GKPS_FRESHNESS_INTERVAL = 100;')
        page.add_init_script("window.__animations = []; document.addEventListener('animationstart', e => window.__animations.push(e.animationName), true);")
        page.goto(self.live_server_url + url)
        page.wait_for_selector('#read', state='attached')
        return page

    def _stale_baseline(self, page):
        page.evaluate("""() => {
          const read = document.getElementById('read');
          read.dataset.pageVersion = String(Number(read.dataset.pageVersion) - 1);
        }""")

    def test_stale_service_page_shows_badge_and_disables_controls(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        self._stale_baseline(page)
        page.wait_for_selector('#freshnessBadge:not([hidden])', timeout=5000)
        state = page.evaluate("""() => ({
          text: document.getElementById('freshnessBadge').innerText.replace(/\\s+/g, ' ').trim(),
          disabled: Array.from(document.querySelectorAll('#read button')).every(b => b.disabled),
          invalid: document.documentElement.dataset.pageStale
        })""")
        self.assertIn('This page was edited elsewhere.', state['text'])
        self.assertTrue(state['disabled'])
        self.assertEqual(state['invalid'], 'true')
        page.close()

    def test_invalidation_closes_open_dialog(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        page.eval_on_selector('[data-entry-edit]', 'el => el.click()')
        page.wait_for_selector('#editorModal[open]')
        self._stale_baseline(page)
        page.wait_for_selector('#freshnessBadge:not([hidden])', timeout=5000)
        self.assertFalse(page.evaluate("document.getElementById('editorModal').open"))
        page.close()

    def test_reload_swaps_content_without_browser_navigation(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        self._stale_baseline(page)
        page.wait_for_selector('#freshnessBadge:not([hidden])', timeout=5000)
        page.evaluate("window.__sameDocument = document")
        page.eval_on_selector('#freshnessBadge button', 'el => el.click()')
        page.wait_for_selector('#freshnessBadge[hidden]', state='attached', timeout=5000)
        self.assertTrue(page.evaluate("window.__sameDocument === document"))
        page.close()

    def test_sidebar_inserts_a_new_service_with_animation(self):
        page = self._page(reverse('web-tatib'))
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(tatib.TataIbadah.objects.create,
                        name='Ibadah Baru', date=date(2026, 11, 8)).result()
        page.wait_for_function(
            "() => Array.from(document.querySelectorAll('#panelBody a')).some(a => a.textContent.includes('Ibadah Baru'))",
            timeout=5000)
        page.wait_for_timeout(80)
        running = page.evaluate("window.__animations")
        self.assertIn('freshness-row-in', running)
        page.close()
