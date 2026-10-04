"""Reordering a Tata Ibadah's entries (spec 006, slice 3).

The order is changed in the page -- dragged or arrowed -- and shown at once in the pane and
in the sidebar's contents list, but nothing is saved until Save. Discard puts back what was
there, and leaving with an unsaved order asks first, on the shell's own in-page navigation
and on a tab close.
"""
from datetime import date
import unittest

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
class ReorderE2ETests(StaticLiveServerTestCase):
    """Written before the mode existed; it drives the real page in a real browser."""

    def setUp(self):
        super().setUp()

        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mzm', testament='old', number_of_chapters=150)
        self.translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Mazmur')
        bible.Verse.objects.create(book_translation=self.translation, chapter=23, verse=1,
                                   title='Tuhan, gembalaku', text='TUHAN adalah gembalaku.')

        self.tatib = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu III', date=date(2026, 10, 4), is_active=True)
        self.other = tatib.TataIbadah.objects.create(
            name='Ibadah Sore', date=date(2026, 9, 27), is_active=True)
        self.first = self._entry(1, 'Pembukaan', 'Kasih karunia')
        self.second = self._entry(2, 'Pujian', 'Bersyukurlah')
        self.third = self._entry(3, 'Penutup', 'Amin')
        self.setUp_browser()

    def _entry(self, order, title, text):
        return tatib.ServiceEntry.objects.create(
            tatib=self.tatib, kind=tatib.ServiceEntryKind.TEXT, title=title, text=text,
            order_number=order)

    def setUp_browser(self):
        """Last, after every ORM call: Playwright's loop must not overlap the database."""
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
        page.wait_for_timeout(300)
        return page

    def _service_url(self):
        return reverse('web-tatib-service', args=[self.tatib.pk])

    def _order_in_pane(self, page):
        return page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#readBody section[data-entry-pk]'))
          .map(function (s) { return Number(s.dataset.entryPk); })""")

    def _sidebar_order(self, page):
        return page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#chList a[data-i]'))
          .filter(function (a) { return /^e\\d+$/.test(a.dataset.i); })
          .map(function (a) { return Number(a.dataset.i.slice(1)); })""")

    def _state(self, page):
        """The mode's own attribute: on the pane, which is every entry's parent."""
        return page.get_attribute('#readBody', 'data-reorder')

    def _start(self, page):
        page.click('[data-reorder-start]')
        page.wait_for_timeout(200)

    # --- the mode ------------------------------------------------------------

    def test_the_mode_hides_the_adds_and_previews_the_new_order(self):
        page = self._page(self._service_url())
        self.assertEqual(self._order_in_pane(page), [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._sidebar_order(page), [self.first.pk, self.second.pk, self.third.pk])

        self._start(page)
        self.assertEqual(self._state(page), 'on')
        self.assertFalse(page.locator('[data-reorder-save]').is_hidden())
        self.assertFalse(page.locator('[data-reorder-discard]').is_hidden())
        self.assertTrue(page.locator('[data-reorder-start]').is_hidden())
        # the add controls are gone while there is an order to arrange
        self.assertEqual(page.evaluate("""() => [].slice.call(
          document.querySelectorAll('.entry__add')).filter(function (row) {
            return getComputedStyle(row).display !== 'none'; }).length"""), 0)

        # the arrow moves the last entry up, and the sidebar follows at once
        page.click('[data-move-up="%d"]' % self.third.pk)
        page.wait_for_timeout(200)
        self.assertEqual(self._order_in_pane(page), [self.first.pk, self.third.pk, self.second.pk])
        self.assertEqual(self._sidebar_order(page), [self.first.pk, self.third.pk, self.second.pk])

    def test_a_drag_moves_an_entry_and_the_sidebar_follows(self):
        page = self._page(self._service_url())
        self._start(page)
        box = page.locator('section[data-entry-pk="%d"]' % self.first.pk).bounding_box()
        target = page.locator('section[data-entry-pk="%d"]' % self.third.pk).bounding_box()
        page.mouse.move(box['x'] + 40, box['y'] + 12)
        page.mouse.down()
        page.mouse.move(box['x'] + 40, target['y'] + target['height'] - 8, steps=10)
        page.mouse.up()
        page.wait_for_timeout(250)
        moved = self._order_in_pane(page)
        self.assertEqual(moved[-1], self.first.pk, moved)          # it travelled to the end
        self.assertEqual(self._sidebar_order(page), moved)         # and the sidebar agrees

    def test_discard_puts_the_order_back(self):
        page = self._page(self._service_url())
        self._start(page)
        page.click('[data-move-down="%d"]' % self.first.pk)
        page.wait_for_timeout(200)
        self.assertEqual(self._order_in_pane(page)[0], self.second.pk)

        page.click('[data-reorder-discard]')
        page.wait_for_timeout(200)
        self.assertEqual(self._order_in_pane(page),
                         [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._sidebar_order(page),
                         [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._state(page), 'off')
        # and the add controls are back
        page.locator('section[data-entry-pk="%d"]' % self.first.pk).hover()
        page.wait_for_timeout(300)
        self.assertFalse(page.locator('.entry__add').first.is_hidden())
        # nothing was written -- and the browser goes first: the ORM cannot be touched
        # while Playwright's loop is running
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.first.pk, self.second.pk, self.third.pk])

    # --- saving --------------------------------------------------------------

    def test_save_writes_the_new_order_and_leaves_the_mode(self):
        page = self._page(self._service_url())
        self._start(page)
        page.click('[data-move-down="%d"]' % self.first.pk)
        page.wait_for_timeout(150)
        page.click('[data-reorder-save]')
        page.wait_for_function(
            "document.getElementById('readBody').dataset.reorder === 'off'",
            timeout=8000)
        self.assertEqual(self._order_in_pane(page),
                         [self.second.pk, self.first.pk, self.third.pk])
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.second.pk, self.first.pk, self.third.pk])

    # --- leaving with an unsaved order ---------------------------------------

    def test_leaving_for_another_tata_ibadah_asks_first(self):
        page = self._page(self._service_url())
        self._start(page)
        page.click('[data-move-down="%d"]' % self.first.pk)
        page.wait_for_timeout(200)

        # a sidebar pick: another Tata Ibadah
        page.click('a[href="%s"]' % reverse('web-tatib-service', args=[self.other.pk]))
        page.wait_for_timeout(400)
        self.assertTrue(page.locator('[data-reorder-confirm]').is_visible())
        self.assertIn(self._service_url(), page.url)               # nothing has left yet

        # "Keep editing" leaves everything as it was
        page.click('[data-reorder-stay]')
        page.wait_for_timeout(200)
        self.assertFalse(page.locator('[data-reorder-confirm]').is_visible())
        self.assertIn(self._service_url(), page.url)

        # asking again and saving carries the person on to where they were going
        page.click('a[href="%s"]' % reverse('web-tatib-service', args=[self.other.pk]))
        page.wait_for_timeout(300)
        page.click('[data-reorder-and-save]')
        page.wait_for_function(
            "document.getElementById('readName').textContent.indexOf('Ibadah Sore') >= 0",
            timeout=8000)
        # the shell navigates in place, so the URL never moves: the pane is what shows
        # where the person ended up
        self.assertIn('Ibadah Sore', page.inner_text('#readName'))
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.second.pk, self.first.pk, self.third.pk])

    def test_the_search_asks_before_it_takes_the_pane_away(self):
        page = self._page(self._service_url())
        self._start(page)
        page.click('[data-move-down="%d"]' % self.first.pk)
        page.wait_for_timeout(200)
        page.click('#railSearch')                     # the shell's own way to the search
        page.wait_for_timeout(400)
        self.assertTrue(page.locator('[data-reorder-confirm]').is_visible())

    def test_closing_the_tab_asks_too(self):
        page = self._page(self._service_url())
        self._start(page)
        page.click('[data-move-down="%d"]' % self.first.pk)
        page.wait_for_timeout(200)
        prevented = page.evaluate("""() => {
          const event = new Event('beforeunload', {cancelable: true});
          window.dispatchEvent(event);
          return event.defaultPrevented;
        }""")
        self.assertTrue(prevented)
        # and it stops asking once the order is the server's
        page.click('[data-reorder-save]')
        page.wait_for_function(
            "document.getElementById('readBody').dataset.reorder === 'off'",
            timeout=8000)
        self.assertFalse(page.evaluate("""() => {
          const event = new Event('beforeunload', {cancelable: true});
          window.dispatchEvent(event);
          return event.defaultPrevented;
        }"""))
