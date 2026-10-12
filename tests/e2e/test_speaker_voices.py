"""Liturgy speaker voices in a browser (spec 059).

Same runner and rules as the other e2e suites: fixtures in setUp, the browser closed
before any ORM work. The colours are read from the computed style, so the tokens, the
stylesheets and the classes the views emit are checked together.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False

OFF_WHITE = 'rgb(245, 243, 238)'
INK = 'rgb(31, 31, 29)'
SCREEN_JOIN = 'rgb(142, 194, 204)'
SCREEN_LEADER = 'rgb(156, 132, 99)'
PAGE_JOIN = 'rgb(43, 90, 100)'
PAGE_LEADER = 'rgb(134, 107, 80)'
HEADER_GOLD = 'rgb(255, 209, 102)'


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SpeakerVoicesE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 18), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Votum', text='P: Marilah kita bangkit berdiri\nJ: Amin.\n'
                                'P+J: Marilah kita memuji TUHAN')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        if getattr(self, '_playwright', None) is not None:
            self.browser.close()
            self._playwright.stop()
            self._playwright = None
        super().tearDown()

    def _page(self, url):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900},
                                           color_scheme='light')
        page = context.new_page()
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def test_the_stage_voices_follow_the_theme(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        leader = page.locator('#readBody .tatib__tx.is-leader').first
        assembly = page.locator('#readBody .tatib__tx.is-assembly').first
        join = page.locator('#readBody .tatib__tx.is-join').first
        expect(leader).to_have_css('color', PAGE_LEADER)
        expect(leader.locator('.tatib__sp')).to_have_css('color', PAGE_LEADER)
        expect(assembly).to_have_css('color', INK)
        expect(assembly.locator('.tatib__sp')).to_have_css('color', INK)
        expect(join).to_have_css('color', PAGE_JOIN)

        page.locator('#themeBtn').click()
        expect(page.locator('html')).to_have_attribute('data-theme', 'dark')
        expect(leader).to_have_css('color', SCREEN_LEADER)
        expect(assembly).to_have_css('color', OFF_WHITE)
        expect(join).to_have_css('color', SCREEN_JOIN)

    def test_the_projector_quiets_the_leader_and_marks_the_joined_line(self):
        page = self._page(reverse('web-service-projector', args=[self.service.pk]))
        screens = page.locator('.screen')
        expect(screens.nth(0).locator('.screen__head')).to_have_css('color', HEADER_GOLD)
        expect(screens.nth(0).locator('.screen__line.is-leader')).to_have_css('color',
                                                                              SCREEN_LEADER)
        expect(screens.nth(0).locator('.screen__line.is-assembly')).to_have_css('color',
                                                                                OFF_WHITE)
        expect(screens.nth(1).locator('.screen__line.is-join')).to_have_css('color',
                                                                            SCREEN_JOIN)
