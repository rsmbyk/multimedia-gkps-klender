"""The Tata Ibadah type, its slots and the generate flow in a browser (spec 167).

Same runner and the same rule as the other e2e suites: Playwright's loop must not overlap
Django's database access, so every assertion against the database happens after the page
is closed.
"""

import re
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


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TataIbadahTemplateE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 11, 1), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita adalah dalam nama Tuhan.')

        self.template = tatib.TataIbadah.objects.create(name='Skeleton', is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita adalah dalam nama Tuhan.')
        self.fill_in = tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.TEXT, title='Doa Syafaat', order_number=2)
        self.choice = tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.TEXT, title='Doa Pengutusan', order_number=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.TEXT, parent=self.choice,
            order_number=4, title='Doa Damai', text='Tuhan, berilah damai.')
        tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.TEXT, parent=self.choice,
            order_number=5, title='Doa Berkat', text='Tuhan, berkati kami.')
        tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.TEXT, order_number=6,
            title='Pengutusan', text='Pergilah dengan damai.')

        self._stopped = False
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def stop_browser(self):
        """Django's connection is synchronous: it cannot be used while Playwright's loop
        runs, so the loop is stopped before any assertion against the database."""
        if self._stopped:
            return
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        self._stopped = True

    def tearDown(self):
        self.stop_browser()
        super().tearDown()

    def open_template(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service',
                                                      args=[self.template.pk]))

    def test_create_normal_service(self):
        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.page.click('#panelAdd')
        expect(self.page.locator('#editorContent [data-tatib-kinds]')).to_be_visible()
        self.assertEqual(self.page.locator('[data-date-picker-clear]').count(), 0)
        self.page.fill('#editorContent input[name="name"]', 'Ibadah Sore')
        self.page.click('#editorContent .editor__save')
        self.page.wait_for_function(
            "() => document.querySelector('a.book[href*=\"/tatib/\"]') !== null")
        self.stop_browser()
        self.assertTrue(tatib.TataIbadah.objects.filter(name='Ibadah Sore').exists())
        created = tatib.TataIbadah.objects.get(name='Ibadah Sore')
        self.assertEqual(created.kind, tatib.TataIbadahKind.SERVICE)
        self.assertIsNotNone(created.date)

    def test_create_template(self):
        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.page.click('#panelAdd')
        self.page.click('#editorContent [data-tatib-kind="1"]')
        self.assertTrue(self.page.locator('#editorContent .editor__date-field')
                        .is_hidden())
        self.page.fill('#editorContent input[name="name"]', 'Skeleton baru')
        self.page.click('#editorContent .editor__save')
        self.page.wait_for_timeout(600)
        self.stop_browser()
        created = tatib.TataIbadah.objects.get(name='Skeleton baru')
        self.assertEqual(created.kind, tatib.TataIbadahKind.TEMPLATE)
        self.assertIsNone(created.date)

    def test_a_template_page_offers_fill_in_and_choice(self):
        self.open_template()
        buttons = self.page.locator('[data-entry-open]').first.locator('xpath=..').locator(
            '[data-entry-open]')
        labels = [buttons.nth(index).inner_text().strip() for index in range(6)]
        self.assertEqual(labels, ['+ Text', '+ Song', '+ Passage', '+ Media',
                                  '+ Fill-in', '+ Choice'])
        self.assertEqual(self.page.locator('[data-project-window]').count(), 0)
        self.assertEqual(self.page.locator('[data-project-open]').count(), 0)
        expect(self.page.locator('[data-generate-open]')).to_be_visible()

    def test_switching_the_type_keeps_the_date(self):
        """Switching to Template hides the date; switching back must restore it as a date.

        The trigger names the date, not the rule that chose it: writing "Nearest Sunday"
        into it reads as a third kind of value and loses what was picked.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.page.click('#panelAdd')
        expect(self.page.locator('#editorContent [data-tatib-kinds]')).to_be_visible()
        label = self.page.locator('#editorModal [data-date-picker-label]')
        before = label.inner_text().strip()
        self.assertRegex(before, r'\d{4}')
        self.page.fill('#editorModal input[name="name"]', 'Ibadah Uji')

        self.page.click('[data-tatib-kind="1"]')
        self.assertEqual(self.page.locator('#editorModal .editor__date-field').is_hidden(), True)
        state = self.focus_and_values()
        self.assertEqual(state['focus'], 'name', 'the switch should leave the caret in the name')
        self.assertEqual(state['name'], 'Ibadah Uji')

        self.page.click('[data-tatib-kind="0"]')
        expect(self.page.locator('#editorModal .editor__date-field')).to_be_visible()
        state = self.focus_and_values()
        self.assertEqual(state['focus'], 'name')
        self.assertEqual(state['name'], 'Ibadah Uji')
        self.assertEqual(state['caret'], len('Ibadah Uji'))
        after = label.inner_text().strip()
        self.assertEqual(after, before)
        self.assertNotIn('Nearest Sunday', after)

    def focus_and_values(self):
        return self.page.evaluate("""() => {
          const n = document.querySelector('#editorModal input[name="name"]');
          return {focus: document.activeElement === n ? 'name' : (document.activeElement.name || document.activeElement.tagName),
                  name: n.value, caret: n.selectionStart};
        }""")

    def test_a_choice_and_its_options_are_one_block(self):
        """No entry bar in the seam, and the option reads a step below its choice.

        An option belongs to the row above it; a full add bar between them made the pair
        look like two entries that happened to be adjacent.
        """
        self.open_template()
        seam = self.page.evaluate("""() => {
          const choice = document.querySelector('#read .tatib__item--choice');
          const list = choice.querySelector('.choice__options');
          const option = choice.querySelector('.tatib__item--option');
          const title = choice.querySelector('.read__sec');
          return {optionsInside: choice.querySelectorAll('.tatib__item--option').length,
                  addBarInside: choice.querySelectorAll('.entry__add').length,
                  hasList: !!list,
                  optionTitleSize: option ? parseFloat(getComputedStyle(option.querySelector('.read__sec')).fontSize) : null,
                  choiceTitleSize: parseFloat(getComputedStyle(title).fontSize),
                  listRule: list ? getComputedStyle(list).borderLeftWidth : null,
                  optionTitleIcons: option ? option.querySelectorAll('.read__sec svg').length : null};
        }""")
        self.assertTrue(seam['optionsInside'], seam)
        self.assertEqual(seam['addBarInside'], 0, 'an add bar sits inside the choice block')
        self.assertTrue(seam['hasList'], seam)
        self.assertEqual(seam['optionTitleSize'], seam['choiceTitleSize'],
                         'an option and its choice read in the same title style')
        self.assertEqual(seam['listRule'], '1px')
        # the choice already names the kind: an option carries its title, nothing else
        self.assertEqual(seam['optionTitleIcons'], 0, seam)

    def test_the_choices_controls_are_icons_in_a_tight_row(self):
        """Icon-only, revealed per row, and the row no taller than they need.

        The controls belong to the row the pointer is on: hovering an option must not light
        the choice's own controls (":hover" reaches ancestors), and the row's height is the
        buttons plus the same gap they keep from the edge, above and below.
        """
        self.open_template()
        block = self.page.locator('#read .tatib__item--choice').first
        block.hover()
        self.page.wait_for_timeout(200)
        control = self.page.evaluate("""() => {
          const ch = document.querySelector('#read .tatib__item--choice');
          const opt = ch.querySelector('.tatib__item--option');
          const acts = opt.querySelector(':scope > .entry__acts');
          const r = opt.getBoundingClientRect(), a = acts.getBoundingClientRect();
          const label = acts.querySelector('.entry__ctrl-label');
          const dot = getComputedStyle(opt, '::before');
          return {labelPosition: getComputedStyle(label).position,
                  rowH: Math.round(r.height), actsH: Math.round(a.height),
                  top: Math.round(a.y - r.y), bottom: Math.round(r.bottom - a.bottom),
                  right: Math.round(r.right - a.right),
                  dotWidth: dot.width, dotLeft: dot.left};
        }""")
        self.assertEqual(control['labelPosition'], 'absolute', 'the control labels still take room')
        self.assertEqual(control['top'], control['right'])
        self.assertEqual(control['bottom'], control['right'])
        self.assertEqual(control['rowH'], control['actsH'] + 2 * control['right'])
        self.assertEqual(control['dotWidth'], '6px')

        self.page.locator('#read .tatib__item--option').first.hover()
        self.page.wait_for_timeout(200)
        opacities = self.page.evaluate("""() => {
          const ch = document.querySelector('#read .tatib__item--choice');
          return {choice: getComputedStyle(ch.querySelector(':scope > .entry__acts')).opacity,
                  option: getComputedStyle(ch.querySelector('.tatib__item--option > .entry__acts')).opacity};
        }""")
        self.assertEqual(opacities['choice'], '0', 'hovering an option lit the choice controls')
        self.assertEqual(opacities['option'], '1')

    def test_the_generate_modal_shows_the_order(self):
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.assertEqual(self.page.locator('#generateModal .g-row--slot').count(), 2)
        self.assertGreater(self.page.locator('#generateModal .g-fixed').count(), 2)
        opacity = self.page.locator('#generateModal .g-fixed').first.evaluate(
            'el => getComputedStyle(el).opacity')
        self.assertEqual(opacity, '0.52')
        expect(self.page.locator('[data-generate-next]')).to_be_disabled()
        expect(self.page.locator('[data-generate-status]')).to_contain_text('2 left to fill in')

    def test_closing_the_chooser_keeps_the_modal(self):
        self.open_template()
        self.page.click('[data-generate-open]')
        self.page.click('[data-choice-open]')
        expect(self.page.locator('[data-choose] .choose')).to_be_visible()
        self.page.keyboard.press('Escape')
        self.assertFalse(self.page.locator('#generateModal [data-choose]').first.is_visible())
        self.assertTrue(self.page.locator('#generateModal').evaluate('el => el.open'))

    def test_a_fill_in_and_a_choice_settle_then_create(self):
        self.open_template()
        self.page.click('[data-generate-open]')
        # the fill-in: its kind's own modal, validated, never saved
        self.page.click('[data-slot-row="%d"] [data-slot-action]' % self.fill_in.pk)
        expect(self.page.locator('#editorContent form')).to_be_visible()
        self.page.fill('#editorContent input[name="title"]', 'Doa Syafaat')
        self.page.fill('#editorContent textarea[name="text"]', 'Tuhan, dengarkanlah kami.')
        self.page.click('#editorContent .editor__save')
        expect(self.page.locator('[data-slot-row="%d"] .g-value' % self.fill_in.pk)) \
            .to_contain_text('Doa Syafaat')
        # the choice: the chooser lists its options and picking one settles the row
        self.page.click('[data-choice-open]')
        self.page.locator('[data-choose-pick]').first.click()
        expect(self.page.locator('[data-slot-row="%d"] .g-value' % self.choice.pk)) \
            .to_contain_text('Doa Damai')
        expect(self.page.locator('[data-generate-status]')).to_contain_text('All 2 entries settled')
        expect(self.page.locator('[data-generate-next]')).to_be_enabled()
        self.page.click('[data-generate-next]')
        expect(self.page.locator('[data-generate-step="2"]')).to_be_visible()
        self.assertTrue(self.page.input_value('#generateName'))
        self.page.click('[data-generate-create]')
        expect(self.page.locator('[data-generate-confirm]')).to_be_visible()
        before = self.page.url
        self.page.click('[data-generate-accept]')
        self.page.wait_for_url(lambda url: url != before, wait_until='load')
        self.page.wait_for_timeout(300)
        self.stop_browser()
        created = tatib.TataIbadah.objects.exclude(
            pk__in=[self.service.pk, self.template.pk]).get()
        kinds = list(created.service_entries.order_by('order_number')
                     .values_list('kind', flat=True))
        self.assertEqual(kinds, [tatib.ServiceEntryKind.TEXT, tatib.ServiceEntryKind.TEXT,
                                 tatib.ServiceEntryKind.TEXT, tatib.ServiceEntryKind.TEXT])
        self.assertFalse(created.service_entries.filter(
            kind__in=[tatib.ServiceEntryKind.FILL_IN, tatib.ServiceEntryKind.CHOICE]).exists())
        self.assertEqual(self.template.service_entries.count(), 6)

    def test_copy_as_template_asks_and_copies(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service',
                                                      args=[self.service.pk]))
        self.page.eval_on_selector(
            '[data-editor-open="tatib"][data-editor-id="%d"]' % self.service.pk,
            'el => el.click()')
        expect(self.page.locator('#editorContent [data-copy-open]')).to_be_visible()
        self.page.click('#editorContent [data-copy-open]')
        expect(self.page.locator('[data-copy-confirm]')).to_be_visible()
        self.page.click('[data-copy-accept]')
        self.page.wait_for_url(re.compile(r'mode=template'), wait_until='load')
        self.page.wait_for_timeout(300)
        self.stop_browser()
        copy = tatib.TataIbadah.objects.exclude(
            pk__in=[self.service.pk, self.template.pk]).get()
        self.assertEqual(copy.kind, tatib.TataIbadahKind.TEMPLATE)
        self.assertIsNone(copy.date)
        self.assertEqual(copy.service_entries.count(), 1)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class InPageSwapE2ETests(StaticLiveServerTestCase):
    """The sidebar opens a stage without reloading the document (spec 167).

    The generate modal belongs to the stage the shell swaps in, so a script that cached the
    node it was loaded beside keeps a dead reference and the button does nothing until a
    refresh. Everything the modal needs must therefore be read from the document on open.
    """

    def setUp(self):
        self.first = tatib.TataIbadah.objects.create(name='Alpha skeleton', is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.first, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.SONG, title='Nyanyian Pembuka', order_number=1)
        self.second = tatib.TataIbadah.objects.create(name='Beta skeleton', is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.second, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.TEXT, title='Doa Syafaat', order_number=1)
        # an empty template: its six tiles are the only place the second row shows
        self.empty = tatib.TataIbadah.objects.create(name='Empty skeleton', is_active=True)

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def tearDown(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def test_use_template_opens_after_an_in_page_swap(self):
        """The way in: the dated list holds no generate modal, and the sidebar reaches a
        template without reloading the document (spec 167). A script that gave up at load
        because the modal it wanted was missing would never bind the button, so Use template
        would do nothing until a refresh."""
        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.assertEqual(self.page.locator('#generateModal').count(), 0,
                         'the dated list should not carry the generate modal')
        self.page.evaluate('window.__noReload = true')

        self.page.click('#tatibMode')
        href = reverse('web-tatib-service', args=[self.second.pk])
        self.page.click(f'a.book[href="{href}"]')
        self.page.wait_for_url(re.compile(rf'{href}$'), wait_until='load')
        expect(self.page.locator('[data-generate-open]')).to_be_visible()
        self.assertTrue(self.page.evaluate('window.__noReload === true'),
                        'the sidebar reloaded the document')

        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.assertTrue(self.page.evaluate(
            "() => document.getElementById('generateModal').open"))
        expect(self.page.locator('[data-generate-status]')).to_contain_text('left to fill in')

    def test_the_empty_templates_tiles_centre_their_second_row(self):
        """Four kind tiles, then fill-in and choice: the two extras centre under the four.

        A grid puts them in its first two columns, which reads as a ragged left edge.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.empty.pk]))
        self.page.wait_for_timeout(400)
        rows = self.page.evaluate("""() => {
          const tiles = [...document.querySelectorAll('.entry__empty-btn')];
          const byRow = {};
          tiles.forEach(t => {
            const r = t.getBoundingClientRect();
            const key = Math.round(r.y);
            (byRow[key] = byRow[key] || []).push({x: r.x, right: r.right});
          });
          const box = document.querySelector('.entry__empty-actions').getBoundingClientRect();
          return {rows: Object.keys(byRow).sort((a, b) => a - b).map(k => byRow[k]),
                  centre: box.x + box.width / 2};
        }""")
        self.assertEqual([len(row) for row in rows['rows']], [4, 2])
        second = rows['rows'][1]
        middle = (second[0]['x'] + second[-1]['right']) / 2
        self.assertAlmostEqual(middle, rows['centre'], delta=1.5)


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EmptyChoiceE2ETests(StaticLiveServerTestCase):
    """A choice with no options still offers the control that creates the first one."""

    def setUp(self):
        self.template = tatib.TataIbadah.objects.create(name='Empty choice', is_active=True)
        self.choice = tatib.ServiceEntry.objects.create(
            tatib=self.template, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.SCRIPTURE, title='Bacaan', order_number=1)
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def tearDown(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def test_an_empty_choice_offers_add_option(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.template.pk]))
        self.page.wait_for_timeout(400)
        row = self.page.locator('#read .tatib__item--choice').first
        expect(row.locator('.slot__state')).to_have_text('No options yet')
        button = row.locator('[data-add-option]')
        expect(button).to_be_visible()
        # on the list's text column, under the state line, not beside it
        offsets = row.evaluate("""el => {
          const r = el.getBoundingClientRect();
          const b = el.querySelector('[data-add-option]').getBoundingClientRect();
          const state = el.querySelector('.slot__state').getBoundingClientRect();
          return {x: Math.round(b.x - r.x), below: b.y >= state.y + state.height};
        }""")
        self.assertEqual(offsets['x'], 64)
        self.assertTrue(offsets['below'])

        button.click()
        form = self.page.locator('#editorContent form[data-entry-form]')
        expect(form).to_be_visible()
        # the option is created through the same per-kind form, and lands under the choice
        self.assertIn(f'parent={self.choice.pk}', form.get_attribute('action'))
        self.assertIn(f'tatib={self.template.pk}', form.get_attribute('action'))
