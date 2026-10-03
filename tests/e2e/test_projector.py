"""The new service display in a browser (spec 006, slice 4).

Same runner and rules as the other e2e suites: Playwright's loop must not overlap
Django's database access, so the browser is closed before any ORM assertion, and
fixtures are created in setUp rather than in a test body.

Display mode is deliberately a browser state, so the tests work with CONTEXTS: two
pages from one context share it (that is one laptop with two tabs), a second
context is another laptop and must not be affected.
"""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProjectorE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 8, 23), is_active=True)
        # a running order with every kind in it, and a long body to fit on a screen
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, order_number=1, item_type=tatib.TataIbadahItemType.TEXT,
            title='Nas', text='Mazmur 23\n\nTuhan adalah gembalaku, takkan kekurangan aku.')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.SECTION_BREAK,
            title='Persembahan')

        s_lang = songs.Language.objects.create(name='Indonesian')
        songbook = songs.Book.objects.create(lang=s_lang, name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=152, title='Ada Kuasa')
        for number in (1, 2):
            songs.Verse.objects.create(song=song, number=number, lyric=f'bait {number}')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=4, kind=tatib.ServiceEntryKind.SONG,
            song=song, verses=[1, 2])

        b_lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=b_lang, name='Terjemahan Baru',
                                               abbreviation='TB')
        mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        matius = bible.BookTranslation.objects.create(version=version, book=mat,
                                                      translation='Matius')
        bible.Verse.objects.create(book_translation=matius, chapter=5, verse=3, text='ayat 3')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=5, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=matius, chapter=5, verse_start=3)

        self.other = tatib.TataIbadah.objects.create(
            name='Ibadah Sore', date=date(2026, 8, 30), is_active=True)

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

    def _page(self, url, context=None):
        context = context or self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    def _service_url(self):
        return reverse('web-tatib-service', args=[self.service.pk])

    def _projector_url(self):
        return reverse('web-service-projector', args=[self.service.pk])

    def _slides(self, page):
        return page.eval_on_selector_all(
            '.slide', 'els => els.map(e => ({slide: e.dataset.slide, kind: e.dataset.kind,'
                     ' active: e.classList.contains("is-active"),'
                     ' hidden: e.getAttribute("aria-hidden")}))')

    # --- one slide at a time, fitted to the screen ---------------------------

    def test_one_slide_at_a_time_and_the_font_fits_the_screen(self):
        page = self._page(self._projector_url())
        shown = [s for s in self._slides(page) if s['active']]
        self.assertEqual(len(shown), 1)
        self.assertEqual(shown[0]['slide'], '1')          # the legacy row opens the display
        self.assertIn('Mazmur 23', page.locator('.slide.is-active').inner_text())

        fit = page.evaluate("""() => {
          const body = document.querySelector('.slide.is-active .slide__body');
          const stage = document.querySelector('#projectorSlides');
          const size = parseFloat(getComputedStyle(body).fontSize);
          return {size, fitsWidth: body.scrollWidth <= stage.clientWidth + 1,
                  fitsHeight: body.scrollHeight <= stage.clientHeight + 1,
                  stageWidth: stage.clientWidth};
        }""")
        self.assertTrue(fit['fitsWidth'], fit)
        self.assertTrue(fit['fitsHeight'], fit)
        self.assertLessEqual(fit['size'], 100)

        # next moves on, prev comes back
        page.click('[data-projector="next"]')
        page.wait_for_timeout(150)
        self.assertIn('Salam', page.locator('.slide.is-active').inner_text())
        page.click('[data-projector="next"]')
        page.wait_for_timeout(150)
        self.assertIn('Persembahan', page.locator('.slide.is-active').inner_text())
        self.assertEqual(page.locator('.slide.is-active .slide__body').count(), 0)  # label alone
        page.click('[data-projector="prev"]')
        page.wait_for_timeout(150)
        self.assertIn('Salam', page.locator('.slide.is-active').inner_text())

        # the last slide's next is off, and the first slide's prev is off
        page.click('[data-projector="next"]')
        page.click('[data-projector="next"]')
        page.click('[data-projector="next"]')
        page.wait_for_timeout(200)
        self.assertIn('ayat 3', page.locator('.slide.is-active').inner_text())
        self.assertTrue(page.locator('[data-projector="next"]').is_disabled())

        # the toggle takes the words off the screen and brings them back
        page.click('[data-projector="toggle"]')
        page.wait_for_timeout(150)
        self.assertEqual(page.get_attribute('body', 'data-showing'), 'false')
        self.assertEqual(page.locator('.slide:visible').count(), 0)
        self.assertEqual(page.get_attribute('[data-projector="toggle"]', 'aria-pressed'), 'false')
        self.assertEqual(page.get_attribute('[data-projector="toggle"]', 'aria-label'),
                         'Show the display')
        page.click('[data-projector="toggle"]')
        page.wait_for_timeout(150)
        self.assertEqual(page.get_attribute('body', 'data-showing'), 'true')
        self.assertEqual(page.locator('.slide:visible').count(), 1)

    # --- the button, its two states, and the lock across tabs ----------------

    def test_project_button_opens_the_display_and_locks_the_browser(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())
        self.assertTrue(page.locator('[data-project-update]').is_hidden())

        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        self.assertIn(self._projector_url(), projector.url)

        # the button now offers the way out and the way to refresh
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())
        self.assertFalse(page.locator('[data-project-update]').is_hidden())

        # a second TAB of the same browser is already in display mode
        tab = self._page(self._service_url(), context)
        self.assertIn('Stop projecting', tab.locator('[data-project-open]').inner_text())
        self.assertFalse(tab.locator('[data-project-update]').is_hidden())
        self.assertEqual(tab.get_attribute('[data-project-group]', 'data-displaying'), 'true')

        # and an entry write is declined there, with the reason, in both tabs
        for other in (page, tab):
            other.locator('.tatib__item').first.hover()
            other.wait_for_timeout(200)
            other.locator('[data-entry-open="text"]').first.click()
            other.wait_for_timeout(300)
            self.assertEqual(other.locator('dialog[open]').count(), 0)
            self.assertFalse(other.locator('[data-project-note]').is_hidden())
            self.assertIn('Stop projecting', other.locator('[data-project-note]').inner_text())

        # the Tata Ibadah's OWN fields stay editable: only entries are locked
        edit = page.locator('.row-edit[data-editor-open="tatib"]').first
        edit.locator('xpath=..').hover()          # the sidebar reveals it on its row
        page.wait_for_timeout(250)
        edit.click()
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")

        # a second BROWSER is another laptop: its own state, and not locked
        alone = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        laptop = self._page(self._service_url(), alone)
        self.assertIn('Project', laptop.locator('[data-project-open]').inner_text())
        self.assertEqual(laptop.get_attribute('[data-project-group]', 'data-displaying'), 'false')
        laptop.locator('.tatib__item').first.hover()
        laptop.wait_for_timeout(200)
        laptop.locator('[data-entry-open="text"]').first.click()
        laptop.wait_for_selector('dialog[open]')          # it may still prepare its service
        laptop.keyboard.press('Escape')

        # stopping from the app releases the lock everywhere in this browser
        page.click('[data-project-open]')                 # Stop projecting
        page.wait_for_timeout(300)
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())
        self.assertIn('Project', tab.locator('[data-project-open]').inner_text())
        tab.locator('.tatib__item').first.hover()
        tab.wait_for_timeout(200)
        tab.locator('[data-entry-open="text"]').first.click()
        tab.wait_for_selector('dialog[open]')
        tab.keyboard.press('Escape')

    def test_the_toggle_in_the_projector_stops_it_for_the_whole_browser(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())

        projector.click('[data-projector="toggle"]')      # hide from the display itself
        page.wait_for_timeout(400)
        self.assertEqual(projector.get_attribute('body', 'data-showing'), 'false')
        self.assertEqual(page.get_attribute('[data-project-group]', 'data-displaying'), 'false')
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())

    # --- the path a person actually clicks through ---------------------------

    def test_the_display_works_on_the_path_a_person_clicks_through(self):
        """From the home page, the way the operator gets there. The shell swaps the
        reading pane IN PLACE, so a project button bound to the node it sat on at
        load is present and dead on exactly this path -- and works on a deep link."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(reverse('web-home'), context)
        page.locator('[data-panel="tatib"]').click()
        page.wait_for_timeout(700)
        page.locator(f'.book[href="{self._service_url()}"]').click()   # the service row
        page.wait_for_timeout(1000)
        self.assertEqual(page.locator('[data-project-open]').count(), 1)
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())

        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        self.assertIn(self._projector_url(), projector.url)
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())

        # the lock reaches the swapped pane too
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(250)
        page.locator('[data-entry-open="text"]').first.click()
        page.wait_for_timeout(300)
        self.assertEqual(page.locator('dialog[open]').count(), 0)
        self.assertIn('Stop projecting', page.locator('[data-project-note]').inner_text())

    # --- Update re-reads what is on screen -----------------------------------

    def test_update_re_reads_the_page_and_keeps_the_place(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        projector.click('[data-projector="next"]')        # the text entry
        projector.wait_for_timeout(200)
        projector.click('[data-projector="next"]')        # the section break
        projector.wait_for_timeout(200)
        self.assertIn('Persembahan', projector.locator('.slide.is-active').inner_text())

        asked = []
        projector.on('request', lambda request: asked.append(request.url))
        page.click('[data-project-update]')
        page.wait_for_timeout(700)
        self.assertTrue([url for url in asked if self._projector_url() in url],
                        f'Update must re-read the page: {asked}')     # fresh lyrics reach it
        self.assertIn('Persembahan', projector.locator('.slide.is-active').inner_text())
