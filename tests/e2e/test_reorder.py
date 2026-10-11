"""Reordering a Tata Ibadah's entries (spec 006, slice 3; spec 026).

The order is ARRANGED IN THE SIDEBAR, where it is listed: each entry's row carries a grip
and there is no Reorder button -- the first drag, or an arrow press on the focused grip, is
what starts rearranging. A change is WRITTEN AT ONCE (spec 026): there is no Save and no
Discard, nothing unsaved, and the shell never asks before it navigates. The pane on the right
follows the order.
"""
from datetime import date
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
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

    def _row(self, page, pk):
        return page.locator('#chList li', has=page.locator('[data-move-grip="%d"]' % pk))

    def _press(self, page, pk, direction):
        """The grip is the only control drawn: focus it and use the arrow keys."""
        grip = page.locator('[data-move-grip="%d"]' % pk)
        grip.focus()
        page.wait_for_timeout(120)
        page.keyboard.press('ArrowUp' if direction == 'up' else 'ArrowDown')
        page.wait_for_timeout(300)

    def _write_of(self, page):
        """The order's own write (spec 026): a drop or a settled keyboard move posts it."""
        return page.expect_response(lambda response: '/editor/entry/reorder/' in response.url)

    # --- adding at the start (spec 030) --------------------------------------

    def test_the_start_bar_adds_an_entry_at_the_top(self):
        page = self._page(self._service_url())
        bar = page.locator('#readBody .entry__start')
        self.assertEqual(bar.count(), 1)
        # The bar collapses at rest (spec 055): reveal it through the first entry.
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(450)
        bar.locator('[data-entry-open="text"]').click()
        page.wait_for_selector('dialog[open]')
        self.assertEqual(page.input_value('input[name="after"]'), 'start')
        page.fill('textarea[name="text"]', 'Pembuka baru')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')")
        page.wait_for_timeout(500)
        first = page.locator('#readBody section[data-entry-pk]').first
        self.assertIn('Pembuka baru', first.inner_text())

    # --- where the chrome lives ----------------------------------------------

    def test_the_handles_are_in_the_sidebar_and_the_endpoint_below_its_filter(self):
        page = self._page(self._service_url())
        # the handles are the sidebar's, one per entry, and the page's pane has none
        self.assertEqual(page.locator('#chList [data-move-grip]').count(), 4)
        self.assertEqual(page.locator('#readBody [data-move-grip]').count(), 0)
        self.assertEqual(page.locator('#readBody [data-move-up]').count(), 0)
        # and there is no Reorder button at all
        self.assertEqual(page.locator('[data-reorder-start]').count(), 0)
        # the endpoint lives in the sidebar, outside the list that scrolls, and there is
        # no Save, no Discard and no leave-question to find (spec 026)
        self.assertEqual(page.locator('.ch__reorder').count(), 1)
        self.assertTrue(page.evaluate(
            "() => document.querySelector('.ch__reorder').closest('#chapters') !== null"))
        self.assertTrue(page.evaluate(
            "() => document.querySelector('.ch__reorder').closest('#chBody') === null"))
        self.assertEqual(page.locator('[data-reorder-save]').count(), 0)
        self.assertEqual(page.locator('[data-reorder-discard]').count(), 0)
        self.assertEqual(page.locator('[data-reorder-confirm]').count(), 0)

    # --- the drop ------------------------------------------------------------

    def test_dragging_a_handle_reorders_at_once(self):
        page = self._page(self._service_url())
        self.assertEqual(self._order_in_pane(page), [self.first.pk, self.second.pk, self.third.pk])
        self.assertEqual(self._sidebar_order(page), [self.first.pk, self.second.pk, self.third.pk])

        # a drag on the handle is what rearranges -- and its release writes the order
        row = self._row(page, self.first.pk)
        row.hover()
        page.wait_for_timeout(150)
        grip = page.locator('[data-move-grip="%d"]' % self.first.pk)
        box = grip.bounding_box()
        target = self._row(page, self.third.pk).bounding_box()
        with self._write_of(page) as written:
            page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            page.mouse.down()
            page.mouse.move(box['x'] + box['width'] / 2, target['y'] + target['height'] - 4, steps=10)
            page.mouse.up()
        self.assertTrue(written.value.ok)

        # the drag moved it in the sidebar, the pane followed, and the rows renumbered
        self.assertEqual(self._sidebar_order(page)[-1], self.first.pk,
                         self._sidebar_order(page))
        self.assertEqual(self._order_in_pane(page), self._sidebar_order(page))
        self.assertEqual(self._sidebar_numbers(page), ['1', '2', '3'])
        # and the adds never left: there is no mode to take them away -- at rest they
        # collapse (spec 052), so reach one through its item to prove it is still there
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(250)
        self.assertFalse(page.locator('.entry__add').first.is_hidden())
        self.assertEqual(page.locator('[data-reorder-save]').count(), 0)

    def test_a_drop_is_written_at_once(self):
        page = self._page(self._service_url())
        row = self._row(page, self.first.pk)
        row.hover()
        page.wait_for_timeout(150)
        grip = page.locator('[data-move-grip="%d"]' % self.first.pk)
        box = grip.bounding_box()
        target = self._row(page, self.third.pk).bounding_box()
        with self._write_of(page) as written:
            page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            page.mouse.down()
            page.mouse.move(box['x'] + box['width'] / 2, target['y'] + target['height'] - 4, steps=10)
            page.mouse.up()
        self.assertTrue(written.value.ok)
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.second.pk, self.third.pk, self.first.pk, self.break_.pk])

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

    def _drag_start(self, page, pk):
        grip = page.locator('[data-move-grip="%d"]' % pk)
        grip.hover()
        box = grip.bounding_box()
        self.assertIsNotNone(box)
        x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        page.mouse.move(x, y + 10, steps=3)
        return x, y

    def test_drag_preview_follows_pointer_without_a_second_layout_slot(self):
        page = self._page(self._service_url())
        initial = page.evaluate("""() => ({
          height: document.querySelector('#chList').getBoundingClientRect().height,
          children: document.querySelector('#chList').children.length
        })""")
        x, y = self._drag_start(page, self.first.pk)
        ghost = page.locator('[data-reorder-ghost]')
        self.assertEqual(ghost.count(), 1)
        self.assertTrue(page.evaluate("""() => {
          const g = document.querySelector('[data-reorder-ghost]');
          const row = document.querySelector('[data-move-grip="%d"]');
          return g.parentElement === document.body && g.getAttribute('aria-hidden') === 'true'
            && g.inert && !g.querySelector('a, button, [id], [data-move-grip], [tabindex]')
            && getComputedStyle(g).pointerEvents === 'none'
            && getComputedStyle(g).position === 'fixed'
            && getComputedStyle(g).transitionDuration === '0s'
            && getComputedStyle(g.querySelector('.toc__grip')).opacity === '1'
            && getComputedStyle(row.closest('li')).visibility === 'visible'
            && getComputedStyle(row.closest('li').firstElementChild).visibility === 'hidden';
        }""" % self.first.pk))
        first = ghost.bounding_box()
        self.assertIsNotNone(first)
        page.mouse.move(x + 37, y + 32, steps=1)
        second = ghost.bounding_box()
        self.assertIsNotNone(second)
        self.assertAlmostEqual(second['x'] - first['x'], 37, delta=2)
        self.assertAlmostEqual(second['y'] - first['y'], 22, delta=2)
        during = page.evaluate("""() => ({
          height: document.querySelector('#chList').getBoundingClientRect().height,
          children: document.querySelector('#chList').children.length
        })""")
        self.assertEqual(during, initial)
        target = self._row(page, self.third.pk).bounding_box()
        self.assertIsNotNone(target)
        page.mouse.move(x + 37, target['y'] + target['height'] - 4, steps=6)
        self.assertEqual(self._row_order(page),
                         [self.second.pk, self.third.pk, self.first.pk, self.break_.pk])
        page.mouse.up()
        self.assertEqual(ghost.count(), 0)
        self.assertEqual(self._row_order(page),
                         [self.second.pk, self.third.pk, self.first.pk, self.break_.pk])

    def test_grabbed_entry_highlights_its_one_live_destination_slot(self):
        page = self._page(self._service_url())
        list_ = page.locator('#chList')
        initial = list_.evaluate('''el => ({height: el.getBoundingClientRect().height,
          children: el.children.length})''')
        row = self._row(page, self.second.pk)
        original_box = row.bounding_box()
        assert original_box is not None
        original_height = original_box['height']
        grip = row.locator('[data-move-grip]')
        grip.hover()
        box = grip.bounding_box()
        self.assertIsNotNone(box)
        x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
        page.mouse.move(x, y)
        page.mouse.down()
        self.assertFalse(row.evaluate('el => el.classList.contains("is-dragging")'))
        page.mouse.move(x, y + 10, steps=3)
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 1)

        def assert_slot(index):
            self.assertEqual(self._row_order(page).index(self.second.pk), index)
            self.assertEqual(list_.evaluate('''el => ({height: el.getBoundingClientRect().height,
              children: el.children.length})'''), initial)
            slot_box = row.bounding_box()
            assert slot_box is not None
            self.assertAlmostEqual(slot_box['height'], original_height, delta=1)
            self.assertTrue(row.evaluate('''el => {
              const style = getComputedStyle(el);
              const child = getComputedStyle(el.firstElementChild);
              return el.classList.contains('is-dragging')
                && style.visibility === 'visible' && child.visibility === 'hidden'
                && style.backgroundColor !== 'rgba(0, 0, 0, 0)'
                && style.boxShadow === 'none'
                && style.outlineStyle === 'none';
            }'''))

        assert_slot(1)
        first = self._row(page, self.first.pk).bounding_box()
        page.mouse.move(x, first['y'] + 2, steps=4)
        assert_slot(0)
        last = self._row(page, self.break_.pk).bounding_box()
        page.mouse.move(x, last['y'] + last['height'] - 2, steps=5)
        assert_slot(3)
        page.mouse.up()
        self.assertFalse(row.evaluate('el => el.classList.contains("is-dragging")'))
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 0)

    def test_hover_tint_disappears_only_while_grabbing(self):
        page = self._page(self._service_url())
        row = self._row(page, self.second.pk)
        link = row.locator('.songrow')
        page.mouse.move(0, 0)
        page.wait_for_timeout(250)
        resting = link.evaluate('(el) => getComputedStyle(el).backgroundColor')
        row.hover()
        page.wait_for_timeout(250)
        hover = link.evaluate('(el) => getComputedStyle(el).backgroundColor')
        self.assertNotEqual(hover, resting)
        x, y = self._drag_start(page, self.first.pk)
        self.assertTrue(page.locator('#chList').evaluate(
            '(el) => el.classList.contains("is-grabbing")'))
        target = row.bounding_box()
        self.assertIsNotNone(target)
        page.mouse.move(target['x'] + target['width'] / 2,
                        target['y'] + target['height'] / 2, steps=5)
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 1)
        page.wait_for_timeout(250)
        # Pointer capture and the visible destination slot can retain hover on the
        # grabbed row. Force the target's pseudo-state to check the other row too.
        cdp = page.context.new_cdp_session(page)
        cdp.send('DOM.enable')
        cdp.send('CSS.enable')
        document = cdp.send('DOM.getDocument')['root']['nodeId']
        li = cdp.send('DOM.querySelector', {
            'nodeId': document,
            'selector': '#chList li:has([data-move-grip="%d"])' % self.second.pk
        })['nodeId']
        anchor = cdp.send('DOM.querySelector', {
            'nodeId': li, 'selector': '.songrow'
        })['nodeId']
        self.assertTrue(li and anchor)
        cdp.send('CSS.forcePseudoState', {'nodeId': li, 'forcedPseudoClasses': ['hover']})
        cdp.send('CSS.forcePseudoState', {'nodeId': anchor, 'forcedPseudoClasses': ['hover']})
        page.wait_for_timeout(250)
        self.assertEqual(link.evaluate('(el) => getComputedStyle(el).backgroundColor'), resting)
        link.evaluate('(el) => el.setAttribute("aria-current", "true")')
        page.wait_for_timeout(250)
        selected = link.evaluate('(el) => getComputedStyle(el).backgroundColor')
        self.assertEqual(selected, page.evaluate("""() => {
          const swatch = document.createElement('div');
          swatch.style.backgroundColor = 'var(--sidebar-selected-bg)';
          document.body.appendChild(swatch);
          const color = getComputedStyle(swatch).backgroundColor;
          swatch.remove();
          return color;
        }"""))
        link.evaluate('(el) => el.removeAttribute("aria-current")')
        ghost_link = page.locator('[data-reorder-ghost] .songrow')
        self.assertTrue(ghost_link.evaluate(
            '(el) => getComputedStyle(el).backgroundColor.endsWith(", 0)")'))
        cdp.send('CSS.forcePseudoState', {'nodeId': anchor, 'forcedPseudoClasses': []})
        cdp.send('CSS.forcePseudoState', {'nodeId': li, 'forcedPseudoClasses': []})
        page.mouse.up()
        self.assertFalse(page.locator('#chList').evaluate(
            '(el) => el.classList.contains("is-grabbing")'))
        row.hover()
        page.wait_for_timeout(250)
        self.assertEqual(link.evaluate('(el) => getComputedStyle(el).backgroundColor'), hover)

    def test_page_swap_removes_a_drag_preview(self):
        page = self._page(self._service_url())
        self._drag_start(page, self.first.pk)
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 1)
        page.evaluate('() => document.dispatchEvent(new Event("shell:page"))')
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 0)
        self.assertFalse(self._row(page, self.first.pk).evaluate(
            'el => el.classList.contains("is-dragging")'))

    def test_cancel_restores_only_this_gesture_not_earlier_moves(self):
        page = self._page(self._service_url())
        with self._write_of(page):
            self._press(page, self.first.pk, 'down')
        before = self._row_order(page)
        x, y = self._drag_start(page, self.break_.pk)
        page.mouse.move(x, y - 90, steps=8)
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 1)
        page.locator('[data-move-grip="%d"]' % self.break_.pk).dispatch_event(
            'pointercancel', {'pointerId': 1})
        self.assertEqual(page.locator('[data-reorder-ghost]').count(), 0)
        self.assertFalse(self._row(page, self.break_.pk).evaluate(
            'el => el.classList.contains("is-dragging")'))
        self.assertFalse(page.locator('#chList').evaluate(
            '(el) => el.classList.contains("is-grabbing")'))
        self.assertEqual(self._row_order(page), before)

    def test_break_preview_follows_pointer_before_window_blur(self):
        page = self._page(self._service_url())
        before = self._row_order(page)
        x, y = self._drag_start(page, self.break_.pk)
        ghost = page.locator('[data-reorder-ghost]')
        self.assertEqual(ghost.count(), 1)
        first = ghost.bounding_box()
        self.assertIsNotNone(first)
        page.mouse.move(x + 25, y - 18, steps=1)
        slot = self._row(page, self.break_.pk)
        self.assertTrue(slot.evaluate('''el => {
          const style = getComputedStyle(el);
          return el.classList.contains('is-dragging')
            && style.visibility === 'visible'
            && getComputedStyle(el.firstElementChild).visibility === 'hidden'
            && style.backgroundColor !== 'rgba(0, 0, 0, 0)'
            && style.boxShadow === 'none'
            && style.outlineStyle === 'none';
        }'''))
        second = ghost.bounding_box()
        self.assertIsNotNone(second)
        self.assertAlmostEqual(second['x'] - first['x'], 25, delta=2)
        self.assertAlmostEqual(second['y'] - first['y'], -28, delta=2)
        page.evaluate('() => window.dispatchEvent(new Event("blur"))')
        self.assertEqual(ghost.count(), 0)
        self.assertFalse(slot.evaluate('el => el.classList.contains("is-dragging")'))
        self.assertEqual(self._row_order(page), before)

    # --- the keyboard --------------------------------------------------------

    def test_a_break_can_be_moved_in_the_order(self):
        page = self._page(self._service_url())
        grip = page.locator('[data-move-grip="%d"]' % self.break_.pk)
        self.assertEqual(grip.count(), 1)
        self.assertEqual(self._row_order(page),
                         [self.first.pk, self.second.pk, self.third.pk, self.break_.pk])
        grip.focus()
        page.keyboard.press('ArrowUp')
        page.wait_for_timeout(300)
        self.assertEqual(self._row_order(page),
                         [self.first.pk, self.second.pk, self.break_.pk, self.third.pk])

    def test_the_arrows_move_a_row_and_the_pane_follows(self):
        page = self._page(self._service_url())
        self._press(page, self.third.pk, 'up')
        self.assertEqual(self._sidebar_order(page), [self.first.pk, self.third.pk, self.second.pk])
        self.assertEqual(self._order_in_pane(page), [self.first.pk, self.third.pk, self.second.pk])
        self.assertEqual(self._sidebar_numbers(page), ['1', '2', '3'])

    def test_an_arrow_move_is_written_at_once(self):
        page = self._page(self._service_url())
        with self._write_of(page) as written:
            self._press(page, self.first.pk, 'down')
        self.assertTrue(written.value.ok)
        self.assertEqual(self._sidebar_order(page)[0], self.second.pk)
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.second.pk, self.first.pk, self.third.pk, self.break_.pk])

    # --- leaving never asks (spec 026) ---------------------------------------

    def test_leaving_for_another_tata_ibadah_does_not_ask_and_keeps_the_order(self):
        page = self._page(self._service_url())
        with self._write_of(page):
            self._press(page, self.first.pk, 'down')
        page.click('a[href="%s"]' % reverse('web-tatib-service', args=[self.other.pk]))
        page.wait_for_function(
            "document.getElementById('readName').textContent.indexOf('Ibadah Sore') >= 0",
            timeout=8000)
        self.assertEqual(page.locator('[data-reorder-confirm]').count(), 0)
        self.assertIn('Ibadah Sore', page.inner_text('#readName'))
        self._close_browser()
        self.assertEqual(list(self.tatib.service_entries.order_by('order_number')
                              .values_list('pk', flat=True)),
                         [self.second.pk, self.first.pk, self.third.pk, self.break_.pk])

    def test_the_search_takes_the_pane_away_without_asking(self):
        page = self._page(self._service_url())
        with self._write_of(page):
            self._press(page, self.first.pk, 'down')
        page.click('#railSearch')
        page.wait_for_timeout(500)
        self.assertEqual(page.locator('[data-reorder-confirm]').count(), 0)
        self.assertEqual(page.locator('[data-reorder-group]').count(), 0)

    def test_reordering_entries_keeps_legacy_rows_in_their_shared_slots(self):
        self._close_browser()
        legacy = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembacaan', text='KJ 120', order_number=2)
        self.second.order_number = 3
        self.second.save(update_fields=['order_number'])
        self.third.order_number = 5
        self.third.save(update_fields=['order_number'])
        self.setUp_browser()

        page = self._page(self._service_url())
        with self._write_of(page):
            self._press(page, self.first.pk, 'down')
        self.assertEqual(page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#chList > li')).map(li => {
            const grip = li.querySelector('[data-move-grip]');
            if (grip) return 'e' + grip.dataset.moveGrip;
            const link = li.querySelector('a[data-i]');
            return link ? 'l' + link.dataset.i : 'l' + li.dataset.i;
          })"""), [f'e{self.second.pk}', 'l2', f'e{self.first.pk}',
                  f'e{self.break_.pk}', f'e{self.third.pk}'])
        self.assertEqual(page.evaluate("""() => [].slice.call(
          document.querySelectorAll('#readBody > [id^="ti-"]')).map(node => {
            const id = node.id.slice(3);
            return id.charAt(0) === 'e' ? id : 'l' + id;
          })"""), [f'e{self.second.pk}', 'l2', f'e{self.first.pk}',
                  f'e{self.break_.pk}', f'e{self.third.pk}'])
        self.assertEqual(self._sidebar_numbers(page), ['1', '3', '5'])

        self._close_browser()
        actual = sorted(
            [(row.order_number, 'entry', row.pk) for row in self.tatib.service_entries.all()]
            + [(row.order_number, 'legacy', row.pk)
               for row in self.tatib.tataibadahitem_set.all()])
        self.assertEqual(actual, [
            (1, 'entry', self.second.pk), (2, 'legacy', legacy.pk),
            (3, 'entry', self.first.pk), (4, 'entry', self.break_.pk),
            (5, 'entry', self.third.pk),
        ])

    def test_a_section_break_preview_follows_its_sidebar_slot_between_old_rows(self):
        self._close_browser()
        legacy = tatib.TataIbadahItem.objects.create(
            tatib=self.tatib, item_type=tatib.TataIbadahItemType.TEXT,
            title='Pembacaan', text='KJ 120', order_number=2)
        self.second.order_number = 3
        self.second.save(update_fields=['order_number'])
        self.third.order_number = 4
        self.third.save(update_fields=['order_number'])
        self.break_.order_number = 5
        self.break_.save(update_fields=['order_number'])
        self.setUp_browser()

        page = self._page(self._service_url())
        self._press(page, self.break_.pk, 'up')
        pane_anchors = page.locator('#readBody > [data-anchor]').evaluate_all(
            '(nodes) => nodes.map(node => node.dataset.anchor)')
        sidebar_anchors = page.locator('#chList > li').evaluate_all("""(nodes) => nodes.map(li => {
            const link = li.querySelector('[data-i]');
            return link ? link.dataset.i : li.dataset.i;
          })""")
        self.assertEqual(pane_anchors, [
            f'e{self.first.pk}', str(legacy.order_number), f'e{self.second.pk}',
            f'e{self.break_.pk}', f'e{self.third.pk}',
        ])
        self.assertEqual(sidebar_anchors, pane_anchors)
