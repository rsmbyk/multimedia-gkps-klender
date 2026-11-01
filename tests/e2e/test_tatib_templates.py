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

from multimedia.bible import models as bible
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

        # A choice of every option shape the page has to draw: a passage (a title and no
        # meta), a titled media row (a title and its file), and a text row (words).
        self.rich = tatib.TataIbadah.objects.create(name='Rich skeleton', is_active=True)
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        matius = bible.BookTranslation.objects.create(version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=matius, chapter=5, verse=13,
                                   text='Kamu adalah garam dunia.')
        self.rich_choice = tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.TEXT, title='Bacaan', order_number=1)
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.SCRIPTURE, parent=self.rich_choice,
            order_number=2, book_translation=matius, chapter=5, verse_start=13, verse_end=13)
        banner = tatib.MediaIdentity.objects.create(
            sha256='b' * 64, byte_count=2048, family='image', display_filename='banner.png')
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.MEDIA, parent=self.rich_choice,
            order_number=3, media=banner, media_filename='banner.png', title='Banner')
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.TEXT, parent=self.rich_choice,
            order_number=4, title='Doa Damai', text='Tuhan, berilah damai kepada kami.')
        # Long enough to clamp: an option is a choice, not a paragraph.
        long_file = ('side-view-silhouette-african-elephant-walking-across-green-ground-' * 4)[:246] + '.webp'
        wall = tatib.MediaIdentity.objects.create(
            sha256='c' * 64, byte_count=4096, family='image', display_filename=long_file)
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.MEDIA, parent=self.rich_choice,
            order_number=5, media=wall, media_filename=long_file,
            title='A banner title with enough words in it to wrap past one row')

        # ordinary rows around the choice, so the dialog has fixed rows to draw too
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.SCRIPTURE, order_number=6,
            book_translation=matius, chapter=5, verse_start=13, verse_end=13)
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.MEDIA, order_number=7,
            media=banner, media_filename='banner.png', title='Banner Sore')
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.TEXT, order_number=8,
            title='Doa Penutup', text='Tuhan, sertailah kami.')

        # a choice of media, so the dialog's label for one can be read
        self.media_choice = tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.MEDIA, title='Tayangan', order_number=9)
        random_file = tatib.MediaIdentity.objects.create(
            sha256='d' * 64, byte_count=512, family='image', display_filename='random.jpg')
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.MEDIA, parent=self.media_choice,
            order_number=10, media=banner, media_filename='banner.png', title='Banner Sore')
        tatib.ServiceEntry.objects.create(
            tatib=self.rich, kind=tatib.ServiceEntryKind.MEDIA, parent=self.media_choice,
            order_number=11, media=random_file, media_filename='random.jpg')

        self._stopped = False
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def open_rich(self):
        self.page.set_viewport_size({'width': 1920, 'height': 900})
        self.page.goto(self.live_server_url + reverse('web-tatib-service',
                                                      args=[self.rich.pk]))
        self.page.wait_for_timeout(400)

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
        self.assertLess(seam['optionTitleSize'], seam['choiceTitleSize'],
                        'an option steps down from its choice')
        self.assertEqual(seam['listRule'], '1px')
        # the choice already names the kind: an option carries its title, nothing else
        self.assertEqual(seam['optionTitleIcons'], 0, seam)

    def test_the_options_controls_are_icons_in_a_tight_row(self):
        """The option's controls are icons in a row no taller than they need; the choice's
        keep the page's labels, and hovering an option lights the choice's too -- the option
        is part of its entry.

        The row's height is the buttons plus the same gap they keep from the edge, above
        and below.
        """
        # a pane wide enough for the page's own labels, so the two rows can be told apart
        self.page.set_viewport_size({'width': 1920, 'height': 900})
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
          const choiceLabel = ch.querySelector(':scope > .entry__acts .entry__ctrl-label');
          const dot = getComputedStyle(opt, '::before');
          return {labelPosition: getComputedStyle(label).position,
                  choiceLabelPosition: choiceLabel ? getComputedStyle(choiceLabel).position : null,
                  rowH: Math.round(r.height), actsH: Math.round(a.height),
                  top: Math.round(a.y - r.y), bottom: Math.round(r.bottom - a.bottom),
                  right: Math.round(r.right - a.right),
                  dotWidth: dot.width, dotLeft: dot.left};
        }""")
        self.assertEqual(control['labelPosition'], 'absolute', 'the option labels still take room')
        self.assertEqual(control['choiceLabelPosition'], 'static',
                         'the choice is an entry: its controls keep their labels')
        # equal above and below, and never tighter than the gap they keep from the edge
        self.assertEqual(control['top'], control['bottom'])
        self.assertGreaterEqual(control['top'], control['right'])
        self.assertGreaterEqual(control['rowH'], control['actsH'] + 2 * control['right'])
        self.assertEqual(control['dotWidth'], '6px')

        self.page.locator('#read .tatib__item--option .read__sec').first.hover()
        self.page.wait_for_timeout(200)
        opacities = self.page.evaluate("""() => {
          const ch = document.querySelector('#read .tatib__item--choice');
          const opts = [...ch.querySelectorAll('.tatib__item--option')];
          return {choice: getComputedStyle(ch.querySelector(':scope > .entry__acts')).opacity,
                  hovered: getComputedStyle(opts[0].querySelector(':scope > .entry__acts')).opacity,
                  other: getComputedStyle(opts[1].querySelector(':scope > .entry__acts')).opacity};
        }""")
        # only the row under the pointer opens: not the choice above it, not its sibling
        self.assertEqual(opacities['choice'], '0', 'hovering an option lit the choice controls')
        self.assertEqual(opacities['hovered'], '1')
        self.assertEqual(opacities['other'], '0', 'a sibling option opened too')

        # the choice is an entry: its controls take the same corner every entry's do
        corners = self.page.evaluate("""() => {
          const at = (sel) => { const row = document.querySelector(sel); if (!row) return null;
            const a = row.querySelector(':scope > .entry__acts'); if (!a) return null;
            const r = row.getBoundingClientRect(), b = a.getBoundingClientRect();
            return [Math.round(b.y - r.y), Math.round(r.right - b.right)]; };
          return {entry: at('#read .tatib__item--entry'), choice: at('#read .tatib__item--choice')};
        }""")
        self.assertEqual(corners['choice'], corners['entry'], corners)

        # and the choice's own controls answer to the choice's own header
        self.page.locator('#read .tatib__item--choice .slot__kind').first.hover()
        self.page.wait_for_timeout(200)
        self.assertEqual(
            self.page.evaluate(
                "() => getComputedStyle(document.querySelector('#read .tatib__item--choice > .entry__acts')).opacity"),
            '1')

    def test_an_option_is_drawn_by_its_shape(self):
        """A passage names itself and nothing else, a titled media row names its file, and
        a text row shows its words. An option drawn as a bare title loses all three.
        """
        self.open_rich()
        rows = self.page.evaluate("""() => [...document.querySelectorAll('#read .tatib__item--option')].map(o => {
          const title = o.querySelector('.read__sec');
          const meta = o.querySelector('.read__sub');
          const body = o.querySelector('.choice__opt-text');
          const r = o.getBoundingClientRect(), t = title.getBoundingClientRect();
          return {text: title.textContent.trim(), meta: meta ? meta.textContent.trim() : null,
                  body: body ? body.textContent.trim() : null,
                  top: Math.round(t.y - r.y), bottom: Math.round(r.bottom - t.bottom),
                  rowH: Math.round(r.height)};
        })""")
        passage, media, text = rows[0], rows[1], rows[2]
        self.assertIn('Matius 5:13', passage['text'])
        self.assertIsNone(passage['meta'])
        # a title with no meta sits on its row's centreline, not on its top edge
        self.assertLessEqual(abs(passage['top'] - passage['bottom']), 1, rows)
        self.assertEqual(media['meta'], 'Image · banner.png', rows)
        self.assertIn('berilah damai', text['body'] or '', rows)

    def test_a_long_option_is_capped_at_five_lines(self):
        """Three lines of title and two of meta, so one option can never push the block
        taller than the choice it belongs to.
        """
        self.open_rich()
        capped = self.page.evaluate("""() => {
          const rows = [...document.querySelectorAll('#read .tatib__item--option')];
          const row = rows.find(r => /A banner title/.test(r.textContent)) || rows[rows.length - 1];
          const lines = (el) => el ? Math.round(el.getBoundingClientRect().height /
                                            parseFloat(getComputedStyle(el).lineHeight)) : 0;
          const title = row.querySelector('.read__sec'), meta = row.querySelector('.read__sub');
          return {titleLines: lines(title), metaLines: lines(meta),
                  titleClamp: getComputedStyle(title).webkitLineClamp,
                  metaClamp: meta ? getComputedStyle(meta).webkitLineClamp : null,
                  metaClipped: !!meta && meta.scrollHeight > meta.clientHeight + 1};
        }""")
        self.assertEqual(capped['titleClamp'], '3')
        self.assertEqual(capped['metaClamp'], '2')
        self.assertLessEqual(capped['titleLines'], 3, capped)
        self.assertLessEqual(capped['metaLines'], 2, capped)
        self.assertLessEqual(capped['titleLines'] + capped['metaLines'], 5, capped)
        self.assertTrue(capped['metaClipped'], 'the fixture file name should be long enough to clamp')

    def test_a_slot_added_from_a_row_lands_after_that_row(self):
        """+ Fill-in and + Choice are on every add row; the row they are clicked on is the
        insertion point, so the form has to carry it.
        """
        self.page.set_viewport_size({'width': 1920, 'height': 900})
        self.open_template()
        row = self.page.locator('.entry__add').nth(1)
        marker = row.get_attribute('data-entry-after')
        self.assertTrue(marker, 'the add row names the element it follows')
        for kind, label in (('fill_in', 'Probe fill-in'), ('choice', 'Probe choice')):
            row = self.page.locator('.entry__add').nth(1)
            marker = row.get_attribute('data-entry-after')
            row.locator(f'[data-entry-open="{kind}"]').evaluate('el => el.click()')
            self.page.wait_for_timeout(500)
            self.assertEqual(
                self.page.evaluate(
                    "() => (document.querySelector('.editor__form input[name=after]') || {}).value"),
                marker, f'the {kind} form dropped its insertion point')
            self.page.fill('.editor__form input[name=title]', label)
            self.page.locator('.editor__form [type=submit]').first.evaluate('el => el.click()')
            self.page.wait_for_timeout(900)
        self.stop_browser()
        landed = list(tatib.ServiceEntry.objects.filter(tatib=self.template)
                      .order_by('order_number').values_list('title', flat=True))
        # both landed between the row they were added from and the entry that follows it
        anchor = landed.index('Doa Syafaat')
        self.assertGreater(landed.index('Probe fill-in'), anchor, landed)
        self.assertGreater(landed.index('Probe choice'), anchor, landed)
        self.assertLess(landed.index('Probe fill-in'), landed.index('Doa Pengutusan'), landed)

    def test_one_add_bar_per_seam(self):
        """An option is drawn inside its choice's block, so it must not emit an add bar of
        its own: two of them in the same seam read as a run of separators.
        """
        self.open_template()
        rows = self.page.evaluate("""() => {
          const all = [...document.querySelectorAll('#read .tatib__item, #read .entry__add')]
            .filter(el => !el.parentElement.closest('.tatib__item'))
            .filter(el => el.getBoundingClientRect().height > 0)
            .map(el => el.classList.contains('entry__add') ? 'ADD'
                      : ((el.querySelector('.read__sec') || {}).textContent || 'entry').trim());
          return all;
        }""")
        self.assertNotIn('ADD, ADD', ', '.join(rows))
        self.assertEqual(sum(1 for r in rows if r == 'ADD'), len(rows) - rows.count('ADD'), rows)

    def test_a_long_word_wraps_instead_of_overflowing(self):
        """A file name with no spaces is one long word: it has to break inside the row, in
        the page and in the Use template dialog both, or the dialog grows a horizontal
        scrollbar and the row runs under its own controls.
        """
        self.open_rich()
        page_overflow = self.page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('#read .tatib__item--option .read__sec, #read .tatib__item--option .read__sub')
            .forEach(el => { if (el.scrollWidth > el.clientWidth + 1) out.push(el.textContent.trim().slice(0, 20)); });
          return out;
        }""")
        self.assertEqual(page_overflow, [], 'an option text runs past its own box')

        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.rich.pk]))
        self.page.wait_for_timeout(300)
        self.page.locator('[data-generate-open]').first.evaluate('el => el.click()')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.wait_for_timeout(500)
        modal = self.page.evaluate("""() => {
          const body = document.querySelector('#generateModal .generate__body');
          const rows = [...document.querySelectorAll('#generateModal .g-fixed')];
          return {body: [body.scrollWidth, body.clientWidth],
                  rows: rows.filter(r => r.scrollWidth > r.clientWidth + 1).length};
        }""")
        self.assertEqual(modal['body'][0], modal['body'][1], 'the dialog scrolls sideways')
        self.assertEqual(modal['rows'], 0, 'a muted row runs past the dialog')

    def test_the_generate_modal_shows_the_order(self):
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.assertEqual(self.page.locator('#generateModal .g-row--slot').count(), 2)
        # the two ordinary entries; a choice's options are named by its own row, not listed
        self.assertEqual(self.page.locator('#generateModal .g-fixed').count(), 2)
        fixed_text = self.page.locator('#generateModal').inner_text()
        self.assertNotIn('Doa Damai', fixed_text)
        self.assertNotIn('Doa Berkat', fixed_text)
        # no template syntax on the page: '{# ... #}' is single-line only, and a wrapped
        # one prints its tail as text
        self.assertNotIn('{#', fixed_text)
        self.assertNotIn('#}', fixed_text)
        action = self.page.locator('#generateModal .g-action').first
        self.assertEqual(action.evaluate('el => getComputedStyle(el).backgroundColor'),
                         'rgb(28, 92, 60)', 'Set is not the primary fill')
        opacity = self.page.locator('#generateModal .g-fixed').first.evaluate(
            'el => getComputedStyle(el).opacity')
        self.assertEqual(opacity, '0.52')
        expect(self.page.locator('[data-generate-next]')).to_be_disabled()
        expect(self.page.locator('[data-generate-status]')).to_contain_text('2 left to fill in')

    def test_the_muted_rows_carry_their_kind_mark(self):
        """A fixed row in the dialog states its kind the way the page does: a media chip,
        a song or passage glyph in the gutter, nothing for a text. Without it the list
        reads as a run of same-looking lines.
        """
        self.open_rich()
        self.page.locator('[data-generate-open]').first.evaluate('el => el.click()')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.wait_for_timeout(400)
        marks = self.page.evaluate("""() => [...document.querySelectorAll('#generateModal .g-fixed')].map(r => {
          const icon = r.querySelector('.entry__kind-icon, .entry__media-icon');
          const title = r.querySelector('.read__sec');
          const box = r.getBoundingClientRect();
          return {title: (title ? title.textContent : '').trim(),
                  mark: icon ? (icon.dataset.kindIcon || icon.dataset.mediaIcon) : null,
                  x: icon ? Math.round(icon.getBoundingClientRect().x - box.x) : null,
                  textX: title ? Math.round(title.getBoundingClientRect().x - box.x) : null};
        })""")
        by_title = {m['title'][:12]: m for m in marks}
        # a chip with no glyph is an empty square: the media mark is an svg, not a box
        svgs = self.page.evaluate("""() => [...document.querySelectorAll('#generateModal [data-media-icon]')]
          .map(el => !!el.querySelector('svg'))""")
        self.assertTrue(svgs, 'the dialog draws no media chip at all')
        self.assertTrue(all(svgs), 'a media chip is drawn without its glyph')
        self.assertEqual(by_title['Banner Sore']['mark'], 'image', marks)
        self.assertEqual(by_title['Matius 5:13']['mark'], 'scripture', marks)
        self.assertIsNone(by_title['Doa Penutup']['mark'], marks)
        for row in marks:
            if row['mark']:
                self.assertEqual(row['x'], 0, f"the mark is not in the row's gutter: {row}")

    def test_a_media_pick_reads_type_first_then_its_name(self):
        """A media option names its file type, then the title or file name that tells it
        from its neighbours -- never the title first and never all three at once.
        """
        self.open_rich()
        self.page.locator('[data-generate-open]').first.evaluate('el => el.click()')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.wait_for_timeout(400)
        row = self.page.locator(f'[data-choice-row="{self.media_choice.pk}"]')
        row.locator('[data-choice-open]').evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        labels = self.page.evaluate("""() => [...document.querySelectorAll('#generateModal .choose-layer:not([hidden]) .choose__item')]
          .map(i => i.dataset.pickLabel)""")
        self.assertEqual(labels, ['Image · Banner Sore · banner.png', 'Image · random.jpg'], labels)
        # one family per dialog: the picker's headings wear the meta's face
        families = self.page.evaluate("""() => {
          const layer = document.querySelector('#generateModal .choose-layer:not([hidden])');
          const fam = (sel) => { const el = layer.querySelector(sel); return el ? getComputedStyle(el).fontFamily : null; };
          return {heading: fam('.choose__head h3'), headMeta: fam('.choose__head p'),
                  ref: fam('.choose__ref'), meta: fam('.choose__meta')};
        }""")
        self.assertEqual(families['ref'], families['meta'], families)
        self.assertIn('sans', families['ref'])
        self.assertEqual(families['heading'], families['headMeta'], families)
        self.page.locator('#generateModal .choose-layer:not([hidden]) [data-choose-pick]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(300)
        value = self.page.locator('[data-choice-row][data-set="true"] [data-slot-value]').first
        self.assertEqual(value.inner_text().strip(), 'Image · Banner Sore · banner.png')
        # the file name is the quiet part: the type stays in the row's own ink
        parts = value.evaluate("""el => {
          const main = el.querySelector('.g-value-main'), mute = el.querySelector('.g-value-mute');
          return {main: main && main.textContent, mute: mute && mute.textContent,
                  mainColor: main && getComputedStyle(main).color,
                  muteColor: mute && getComputedStyle(mute).color};
        }""")
        # the type and the title are the entry; only the file's own name steps back
        self.assertEqual(parts['main'], 'Image · Banner Sore')
        self.assertEqual(parts['mute'], 'banner.png')
        self.assertNotEqual(parts['mainColor'], parts['muteColor'], parts)

    def test_a_settled_text_choice_names_its_prayer(self):
        """An untitled text option has no reference, so a settled row used to read blank.
        Its words name it, the same ones the chooser shows.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.locator('[data-choice-open]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        labels = self.page.evaluate("""() => [...document.querySelectorAll('#generateModal .choose-layer:not([hidden]) .choose__item')]
          .map(i => i.dataset.pickLabel)""")
        self.assertTrue(all(label.strip() for label in labels), f'blank pick label: {labels}')
        self.page.locator('#generateModal .choose-layer:not([hidden]) [data-choose-pick]').first.evaluate(
            'el => el.click()')
        self.page.wait_for_timeout(400)
        value = self.page.locator('[data-choice-row][data-set="true"] [data-slot-value]').first
        self.assertTrue(value.inner_text().strip(), 'the settled row names nothing')
        parts = value.evaluate("""el => {
          const title = el.querySelector('.g-value-title'), body = el.querySelector('.g-value-body');
          return {title: title && title.textContent, body: body && body.textContent,
                  titleFont: title && getComputedStyle(title).fontFamily,
                  bodyFont: body && getComputedStyle(body).fontFamily,
                  titleColor: title && getComputedStyle(title).color,
                  bodyColor: body && getComputedStyle(body).color};
        }""")
        # the name and the words are two things: a sans title over a serif body, in two inks
        self.assertEqual(parts['title'], 'Doa Damai', parts)
        self.assertIn('damai', (parts['body'] or '').lower(), parts)
        self.assertIn('sans', parts['titleFont'])
        self.assertIn('serif', parts['bodyFont'])
        self.assertNotEqual(parts['titleColor'], parts['bodyColor'], parts)

    def test_change_is_outlined_once_a_row_is_settled(self):
        """Change revises something already done; Set and Choose are the work still owed.
        Both cannot be the filled accent, or the page stops showing what is left.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        filled = self.page.locator('#generateModal .g-action').first.evaluate(
            'el => getComputedStyle(el).backgroundColor')
        self.assertEqual(filled, 'rgb(28, 92, 60)')

        self.page.locator('[data-choice-open]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        self.page.locator('#generateModal .choose-layer:not([hidden]) [data-choose-pick]').first.evaluate(
            'el => el.click()')
        self.page.wait_for_timeout(400)
        change = self.page.evaluate("""() => {
          const row = document.querySelector('[data-choice-row][data-set="true"]');
          const button = row.querySelector('.g-action');
          const c = getComputedStyle(button);
          return {text: button.textContent.trim(), bg: c.backgroundColor, border: c.borderColor, color: c.color};
        }""")
        self.assertEqual(change['text'], 'Change')
        self.assertEqual(change['bg'], 'rgba(0, 0, 0, 0)', 'Change is still filled')
        self.assertEqual(change['color'], 'rgb(31, 31, 29)')

    def test_the_chooser_shows_a_text_options_words(self):
        """A text option is its words: the picker listed a blank reference and nothing else,
        which made two prayers indistinguishable.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.locator('[data-choice-open]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        rows = self.page.evaluate("""() => [...document.querySelectorAll('#generateModal .choose-layer:not([hidden]) .choose__item')]
          .map(i => ({ref: (i.querySelector('.choose__ref') || {}).textContent || '',
                      body: (i.querySelector('.choose__body') || {}).textContent || ''}))""")
        self.assertTrue(rows, 'no chooser rows')
        for row in rows:
            self.assertTrue(row['body'].strip(), f'option without its words: {row}')
        self.assertIn('damai', ' '.join(r['body'] for r in rows), rows)

    def test_escape_closes_the_preview_not_the_dialog_under_it(self):
        """A preview opened from a chooser row sits above the dialog; Escape belongs to it.
        Swallowing that key to hide the chooser behind it closed the wrong thing.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.locator('[data-choice-open]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        self.page.locator('#generateModal [data-preview-open]').first.click()
        self.page.wait_for_timeout(600)
        self.assertTrue(self.page.evaluate("() => document.getElementById('previewModal').open"))

        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(400)
        state = self.page.evaluate("""() => ({preview: document.getElementById('previewModal').open,
            generate: document.getElementById('generateModal').open})""")
        self.assertFalse(state['preview'], 'Escape left the preview open')
        self.assertTrue(state['generate'], 'Escape closed the dialog the preview came from')

        self.page.keyboard.press('Escape')
        self.page.wait_for_timeout(400)
        self.assertFalse(self.page.locator('#generateModal .choose-layer').is_visible())
        self.assertTrue(self.page.evaluate("() => document.getElementById('generateModal').open"))

    def test_reopening_the_dialog_starts_from_nothing(self):
        """A dialog dismissed and opened again must not carry the last pick: the chooser
        kept its own pressed mark, so the option came back looking chosen.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.locator('[data-choice-open]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        self.page.locator('#generateModal .choose-layer:not([hidden]) [data-choose-pick]').first.evaluate(
            'el => el.click()')
        self.page.wait_for_timeout(400)
        self.page.locator('[data-generate-close]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(400)
        self.page.click('[data-generate-open]')
        self.page.wait_for_timeout(600)
        state = self.page.evaluate("""() => ({
          pressed: document.querySelectorAll('#generateModal [data-choose-pick][aria-pressed="true"]').length,
          set: document.querySelectorAll('#generateModal .g-row--slot[data-set="true"]').length})""")
        self.assertEqual(state, {'pressed': 0, 'set': 0}, state)

    def test_the_backdrop_closes_the_dialog(self):
        """The overlay behind the dialog is a dismissal, like Cancel and Escape; a click
        inside the card is not."""
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        box = self.page.evaluate("""() => { const r = document.getElementById('generateModal').getBoundingClientRect();
          return {left: Math.round(r.left), top: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height)}; }""")
        self.page.mouse.click(max(10, box['left'] - 60), box['top'] + box['h'] // 2)
        self.page.wait_for_timeout(400)
        self.assertFalse(self.page.evaluate("() => document.getElementById('generateModal').open"),
                         'the backdrop left the dialog open')

        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.mouse.click(box['left'] + box['w'] // 2, box['top'] + box['h'] // 2)
        self.page.wait_for_timeout(300)
        self.assertTrue(self.page.evaluate("() => document.getElementById('generateModal').open"),
                        'a click inside the card dismissed it')

    def test_the_count_follows_the_rows_that_are_there(self):
        """The footer counts the rows on the page, not the rows it saw when the dialog
        opened: a page of settled rows still said "1 left to fill in" because a row that
        no longer existed was still being counted.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.wait_for_timeout(300)
        before = self.page.evaluate("() => document.querySelectorAll('#generateModal .g-row--slot').length")
        self.assertIn(f'of {before} settled', self.page.locator('[data-generate-status]').inner_text())

        # a row disappears under the dialog, the way an in-page swap can take one
        self.page.evaluate("""() => {
          const rows = document.querySelectorAll('#generateModal .g-row--slot');
          rows[0].remove();   /* the fill-in; the choice stays, so a pick can follow */
        }""")
        self.page.locator('[data-choice-open]').first.evaluate('el => el.click()')
        self.page.wait_for_timeout(300)
        self.page.locator('#generateModal .choose-layer:not([hidden]) [data-choose-pick]').first.evaluate(
            'el => el.click()')
        self.page.wait_for_timeout(300)
        status = self.page.locator('[data-generate-status]').inner_text().strip()
        # one row is left and it is settled: the footer counts one, not the two it opened on
        self.assertEqual(status, 'All 1 entry settled.', status)

    def test_the_confirmation_is_a_card_over_a_backdrop(self):
        """The confirmation is a surface, not lines laid over the form: its own fill,
        radius and padding above a dimmed layer."""
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.locator('[data-generate-next]').evaluate('el => { el.disabled = false; el.click(); }')
        self.page.wait_for_timeout(300)
        self.page.locator('[data-generate-create]').evaluate('el => el.click()')
        self.page.wait_for_timeout(300)
        card = self.page.evaluate("""() => {
          const layer = document.querySelector('[data-generate-confirm]');
          const box = layer.querySelector('.editor__confirm');
          const l = getComputedStyle(layer), c = getComputedStyle(box);
          return {visible: !layer.hidden, backdrop: l.backgroundColor, position: l.position,
                  fill: c.backgroundColor, radius: c.borderRadius,
                  buttons: [...box.querySelectorAll('button')].map(b => b.textContent.trim())};
        }""")
        self.assertTrue(card['visible'])
        self.assertEqual(card['position'], 'absolute')
        self.assertNotEqual(card['backdrop'], 'rgba(0, 0, 0, 0)', 'no backdrop behind the card')
        self.assertNotIn(card['fill'], ('rgba(0, 0, 0, 0)', 'transparent'), 'the card has no surface')
        self.assertEqual(card['radius'], '12px')
        self.assertEqual(card['buttons'], ['Cancel', 'Create'])

    def test_the_date_label_reads_like_the_new_modal(self):
        """One date, one wording: the dialog's picker prints the full month, as the New
        Tata Ibadah modal's picker does, not a short form only this dialog used.
        """
        self.open_template()
        self.page.click('[data-generate-open]')
        expect(self.page.locator('#generateModal')).to_be_visible()
        self.page.locator('[data-generate-next]').evaluate('el => { el.disabled = false; el.click(); }')
        self.page.wait_for_timeout(300)
        label = self.page.locator('#generateModal [data-date-picker-label]').inner_text().strip()
        self.assertRegex(label, r'^\d{1,2} \w+ \d{4}$', label)
        month = label.split()[1]
        self.assertGreater(len(month), 3, f'short month in a full-date label: {label}')

        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.page.click('#panelAdd')
        expect(self.page.locator('#editorContent [data-date-picker-label]')).to_be_visible()
        theirs = self.page.locator('#editorContent [data-date-picker-label]').inner_text().strip()
        # same wording: both name the month in full
        self.assertEqual(len(theirs.split()[1]), len(month), f'{label} vs {theirs}')

    def test_an_option_is_not_a_row_of_the_sidebar(self):
        """The sidebar arranges the order, and a grip on an option could drag it out of
        the block it belongs to -- the list then numbered two rows under one entry and the
        stage drew the options apart from their choice. The choice's row holds them.
        """
        self.open_template()
        self.page.wait_for_timeout(300)
        rows = self.page.evaluate("""() => [...document.querySelectorAll('[data-move-grip]')].map(g => {
          const li = g.closest('li');
          return {pk: Number(g.dataset.moveGrip), n: li.dataset.num,
                  text: (li.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 24)};
        })""")
        labels = [row['text'] for row in rows]
        self.assertNotIn('Doa Damai', ' '.join(labels), labels)
        self.assertNotIn('Doa Berkat', ' '.join(labels), labels)
        self.assertIn('Doa Pengutusan', ' '.join(labels), labels)
        # one number per row, in sequence
        numbers = [int(row['n']) for row in rows]
        self.assertEqual(numbers, list(range(1, len(rows) + 1)), rows)

        # and a move keeps the choice with its options
        grip = self.page.locator(f'[data-move-grip="{rows[-1]["pk"]}"]')
        grip.focus()
        self.page.keyboard.press('ArrowUp')
        self.page.wait_for_timeout(900)
        self.page.reload()
        self.page.wait_for_timeout(600)
        blocks = self.page.evaluate("""() => [...document.querySelectorAll('#read .tatib__item--choice')]
          .map(c => ({title: (c.querySelector('.read__sec') || {}).textContent,
                      options: [...c.querySelectorAll('.tatib__item--option')].map(o => (o.querySelector('.read__sec') || {}).textContent)}))""")
        self.assertTrue(blocks, 'no choice block on the page')
        for block in blocks:
            self.assertTrue(block['options'], f"choice without its options: {block}")
        self.assertEqual(self.page.evaluate(
            "() => document.querySelectorAll('#read .tatib__item--option').length"), 2)

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
            pk__in=[self.service.pk, self.template.pk, self.rich.pk]).get()
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
            pk__in=[self.service.pk, self.template.pk, self.rich.pk]).get()
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
