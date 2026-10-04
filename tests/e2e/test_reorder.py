"""Reordering a Tata Ibadah's entries (spec 006, slice 3).

The order is ARRANGED IN THE SIDEBAR, where it is listed: each entry's row carries the handle
and the arrows, and there is no Reorder button -- the first drag, or the first arrow press, is
what starts rearranging. Save and Discard appear below the sidebar's filter, and the pane on
the right follows. Nothing is written until Save; Discard puts back what was there, and
leaving with an unsaved order asks first, on the shell's own in-page navigation and on a tab
close.
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
        # a break is an entry too, and its row is the thin line rather than a link
        self.break_ = tatib.ServiceEntry.objects.create(
            tatib=self.tatib, kind=tatib.ServiceEntryKind.SECTION_BREAK, title='Doa',
            order_number=4)
        self.texts = [self.first.pk, self.second.pk, self.third.pk]
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
        every = page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#readBody section[data-entry-pk]'))
          .map(function (s) { return Number(s.dataset.entryPk); })""")
        return [pk for pk in every if pk in self.texts]     # the break's section says nothing

    def _row_order(self, page):
        """Every movable row, a break's thin line included, in the sidebar's order."""
        return page.evaluate("""() => [].slice.call(document.querySelectorAll('#chList > li'))
          .filter(function (li) { return !!li.querySelector('[data-move-grip]'); })
          .map(function (li) {
            return Number(li.querySelector('[data-move-grip]').dataset.moveGrip); })""")

    def _sidebar_order(self, page):
        return page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#chList a[data-i]'))
          .filter(function (a) { return a.dataset.i.charAt(0) === 'e'; })
          .map(function (a) { return Number(a.dataset.i.slice(1)); })""")

    def _sidebar_numbers(self, page):
        return page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#chList a[data-i]'))
          .filter(function (a) { return a.dataset.i.charAt(0) === 'e'; })
          .map(function (a) { return a.querySelector('.songrow__c').textContent; })""")

    def _state(self, page):
        """The mode's own attribute: on the document root, above every subtree it drives."""
        return page.get_attribute('html', 'data-reorder')

    def _row(self, page, pk):
        return page.locator('#chList li', has=page.locator('[data-move-grip="%d"]' % pk))

    def _press(self, page, pk, direction):
        """The grip is the only control drawn: focus it and use the arrow keys."""
        grip = page.locator('[data-move-grip="%d"]' % pk)
        grip.focus()
        page.wait_for_timeout(120)
        page.keyboard.press('ArrowUp' if direction == 'up' else 'ArrowDown')
        page.wait_for_timeout(300)

    def _start(self, page):
        """No Reorder button: a move starts the mode. Moving the first row up moves nothing."""
        self._press(page, self.first.pk, 'up')

    # --- where the chrome lives ----------------------------------------------

    def test_the_handles_are_in_the_sidebar_and_the_answers_below_its_filter(self):
        page = self._page(self._service_url())
        # the handles are the sidebar's, one per entry, and the page's pane has none
        self.assertEqual(page.locator('#chList [data-move-grip]').count(), 4)
        self.assertEqual(page.locator('#readBody [data-move-grip]').count(), 0)
        self.assertEqual(page.locator('#readBody [data-move-up]').count(), 0)
        # and there is no Reorder button at all
        self.assertEqual(page.locator('[data-reorder-start]').count(), 0)
        self.assertEqual(self._state(page), None)          # not rearranging yet
        self.assertTrue(page.locator('.ch__reorder').is_hidden())   # nor any answers
        at_rest = self._list_top(page)

        # the strip lives in the sidebar and outside the list that scrolls. Measure it while
        # it is SHOWN: a hidden element's rect is all zeros, which is not a measurement
        self._start(page)
        strip = page.locator('.ch__reorder')
        self.assertEqual(strip.count(), 1)
        self.assertTrue(strip.is_visible())
        self.assertTrue(page.evaluate(
            "() => document.querySelector('.ch__reorder').closest('#chapters') !== null"))
        self.assertTrue(page.evaluate(
            "() => document.querySelector('.ch__reorder').closest('#chBody') === null"))
        self.assertGreaterEqual(
            page.evaluate("""() => {
              const strip = document.querySelector('.ch__reorder').getBoundingClientRect();
              const top = document.querySelector('.ch__top').getBoundingClientRect();
              return Math.round(strip.top - top.bottom);
            }"""), -1)
        # and it holds its place in the column, so starting a drag does not push the list
        # down: hidden with visibility, never display
        self.assertEqual(self._list_top(page), at_rest)

    def _list_top(self, page):
        return page.evaluate("""() => Math.round(
          document.querySelector('#chList').getBoundingClientRect().top)""")

    # --- the mode ------------------------------------------------------------

    def test_dragging_a_handle_starts_the_mode_and_shows_the_answers(self):
        page = self._page(self._service_url())
        self.assertEqual(self._order_in_pane(page), [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._sidebar_order(page), [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._state(page), None)

        # a drag on the handle is what starts it
        row = self._row(page, self.first.pk)
        row.hover()
        page.wait_for_timeout(150)
        grip = page.locator('[data-move-grip="%d"]' % self.first.pk)
        box = grip.bounding_box()
        target = self._row(page, self.third.pk).bounding_box()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        page.mouse.down()
        page.mouse.move(box['x'] + box['width'] / 2, target['y'] + target['height'] - 4, steps=10)
        page.mouse.up()
        page.wait_for_timeout(300)

        self.assertEqual(self._state(page), 'on')
        self.assertTrue(page.locator('[data-reorder-save]').is_visible())
        self.assertTrue(page.locator('[data-reorder-discard]').is_visible())
        # the pane's add controls are gone: there is one thing to do
        self.assertEqual(page.evaluate("""() => [].slice.call(
          document.querySelectorAll('.entry__add')).filter(function (row) {
            return getComputedStyle(row).display !== 'none'; }).length"""), 0)

        # the drag moved it in the sidebar, the pane followed, and the rows renumbered
        self.assertEqual(self._sidebar_order(page)[-1], self.first.pk,
                         self._sidebar_order(page))
        self.assertEqual(self._order_in_pane(page), self._sidebar_order(page))
        self.assertEqual(self._sidebar_numbers(page), ['1', '2', '3'])

    def test_the_morph_starts_at_once_with_no_delay(self):
        """`--ease` is a whole shorthand value (200ms + a curve). Naming a duration beside it
        makes the token's own 200ms a DELAY: the rows sat still, then travelled, and shortening
        the duration could not be felt. The travel must start at once, at rest and while
        dragging."""
        delay = """() => getComputedStyle([].slice.call(document.getElementById('chList').children)
          .filter(li => !!li.querySelector('[data-move-grip]'))[0]).transitionDelay"""
        page = self._page(self._service_url())
        self.assertEqual(page.evaluate(delay), '0s')
        grip = page.locator('[data-move-grip]').first
        grip.hover()
        box = grip.bounding_box()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        page.mouse.down()
        page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2 + 60, steps=6)
        self.assertEqual(page.evaluate(delay), '0s')
        page.mouse.up()

    def test_a_break_can_be_moved_in_the_order(self):
        page = self._page(self._service_url())
        grip = page.locator('[data-move-grip="%d"]' % self.break_.pk)
        self.assertEqual(grip.count(), 1)
        self.assertEqual(self._row_order(page),
                         [self.first.pk, self.second.pk, self.third.pk, self.break_.pk])
        grip.focus()
        page.keyboard.press('ArrowUp')
        page.wait_for_timeout(300)
        self.assertEqual(self._state(page), 'on')
        self.assertEqual(self._row_order(page),
                         [self.first.pk, self.second.pk, self.break_.pk, self.third.pk])

    def test_the_arrows_move_a_row_and_the_pane_follows(self):
        page = self._page(self._service_url())
        self._press(page, self.third.pk, 'up')
        self.assertEqual(self._state(page), 'on')
        self.assertEqual(self._sidebar_order(page), [self.first.pk, self.third.pk, self.second.pk])
        self.assertEqual(self._order_in_pane(page), [self.first.pk, self.third.pk, self.second.pk])
        self.assertEqual(self._sidebar_numbers(page), ['1', '2', '3'])

    def test_discard_puts_the_order_back(self):
        page = self._page(self._service_url())
        self._press(page, self.first.pk, 'down')
        self.assertEqual(self._sidebar_order(page)[0], self.second.pk)

        page.click('[data-reorder-discard]')
        page.wait_for_timeout(250)
        self.assertEqual(self._sidebar_order(page),
                         [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._order_in_pane(page),
                         [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._state(page), 'off')
        # and the pane's add controls are back
        page.locator('section[data-entry-pk="%d"]' % self.first.pk).hover()
        page.wait_for_timeout(300)
        self.assertFalse(page.locator('.entry__add').first.is_hidden())
        # nothing was written -- and the browser goes first: the ORM cannot be touched
        # while Playwright's loop is running
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.first.pk, self.second.pk, self.third.pk, self.break_.pk])

    # --- saving --------------------------------------------------------------

    def test_save_writes_the_new_order_and_leaves_the_mode(self):
        page = self._page(self._service_url())
        self._press(page, self.first.pk, 'down')
        page.click('[data-reorder-save]')
        page.wait_for_function(
            "document.documentElement.dataset.reorder === 'off'",
            timeout=8000)
        self.assertEqual(self._sidebar_order(page),
                         [self.second.pk, self.first.pk, self.third.pk])
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.second.pk, self.first.pk, self.third.pk, self.break_.pk])

    # --- leaving with an unsaved order ---------------------------------------

    def test_leaving_for_another_tata_ibadah_asks_first(self):
        page = self._page(self._service_url())
        self._press(page, self.first.pk, 'down')

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
                         [self.second.pk, self.first.pk, self.third.pk, self.break_.pk])

    def test_the_search_asks_before_it_takes_the_pane_away(self):
        page = self._page(self._service_url())
        self._press(page, self.first.pk, 'down')
        page.click('#railSearch')                     # the shell's own way to the search
        page.wait_for_timeout(400)
        self.assertTrue(page.locator('[data-reorder-confirm]').is_visible())

    def test_closing_the_tab_asks_too(self):
        page = self._page(self._service_url())
        self._press(page, self.first.pk, 'down')
        prevented = page.evaluate("""() => {
          const event = new Event('beforeunload', {cancelable: true});
          window.dispatchEvent(event);
          return event.defaultPrevented;
        }""")
        self.assertTrue(prevented)
        # and it stops asking once the order is the server's
        page.click('[data-reorder-save]')
        page.wait_for_function(
            "document.documentElement.dataset.reorder === 'off'",
            timeout=8000)
        self.assertFalse(page.evaluate("""() => {
          const event = new Event('beforeunload', {cancelable: true});
          window.dispatchEvent(event);
          return event.defaultPrevented;
        }"""))
