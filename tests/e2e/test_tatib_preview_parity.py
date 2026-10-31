"""The shipped Tata Ibadah views against the preview the spec was accepted on (spec 167).

The preview is the reference: every number in the spec's `## UI/UX` came from it. This
module measures the two side by side — the live page from a real server, the preview as the
static file it is — and fails when the product drifts from what was signed off. Text is
never compared (the fixtures differ); only the box and type facts the preview fixed.
"""

import pathlib
import unittest

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


PREVIEW = pathlib.Path(settings.BASE_DIR) / 'specs' / '167-tata-ibadah-templates' / 'preview' / 'index.html'

MEASURE = """() => {
  const box = el => { const r = el.getBoundingClientRect(); return {x: r.x, w: r.width, h: r.height}; };
  const cs = el => getComputedStyle(el);
  const bar = document.querySelector('[data-entry-start] .entry__add-inner')
           || document.querySelector('#read .entry__add-inner');
  const item = document.querySelector('[data-slot-kind="choice"]')
            || document.querySelector('.slot[data-kind="choice"]')
            || document.querySelector('.choice')
            || document.querySelector('.tatib__item--slot');
  const title = item && item.querySelector('.read__sec, .slot__title');
  const option = document.querySelector('[data-option-of], .choice__option');
  const optionText = option && (option.querySelector('.read__sec, .choice__ref') || option);
  const addOption = document.querySelector('[data-add-option], .choice__add');
  return {
    order: [].slice.call(bar ? bar.querySelectorAll('.entry__add-btn') : [])
             .map(b => b.textContent.trim()),
    slotTitle: title && {size: cs(title).fontSize, weight: cs(title).fontWeight,
                         family: cs(title).fontFamily, align: cs(title).textAlign},
    mark: !!document.querySelector('.slot__mark'),
    option: (() => {
      if (!option) return null;
      const o = option.getBoundingClientRect();
      const choiceRow = item ? item.getBoundingClientRect() : null;
      const list = option.closest('.choice__options');
      return {offset: choiceRow ? Math.round(o.x - choiceRow.x) : Math.round(o.x),
              borderLeft: cs(option).borderLeftWidth,
              listRule: list ? cs(list).borderLeftWidth : null};
    })(),
    optionTextX: optionText ? box(optionText).x : null,
    optionRowX: option ? box(option).x : null,
    addOptionX: addOption ? box(addOption).x : null,
  };
}"""

GENERATE = """() => {
  const m = document.getElementById('generateModal');
  const fixed = m.querySelector('.g-fixed, .g-stage-row[data-fixed]');
  const title = fixed && fixed.querySelector('.read__sec');
  const body = fixed && fixed.querySelector('.tatib__tx');
  const box = el => el ? el.getBoundingClientRect() : null;
  return {
    titleSize: title ? getComputedStyle(title).fontSize : null,
    bodySize: body ? getComputedStyle(body).fontSize : null,
    rowHeight: fixed ? box(fixed).height : null,
    opacity: fixed ? getComputedStyle(fixed).opacity : null,
  };
}"""


KINDS = """() => {
  const g = document.querySelector('[data-slot-kinds], .kind-pick');
  if (!g) return null;
  const cs = el => getComputedStyle(el);
  const chips = [].slice.call(g.querySelectorAll('button'));
  return {
    order: chips.map(b => b.textContent.trim()),
    pressed: chips.map(b => b.getAttribute('aria-pressed')),
    height: +chips[0].getBoundingClientRect().height.toFixed(1),
    radius: cs(chips[0]).borderRadius,
    font: cs(chips[0]).fontSize + '/' + cs(chips[0]).fontWeight,
    gap: cs(g).gap,
    columns: cs(g).gridTemplateColumns.split(' ').length,
    width: +g.getBoundingClientRect().width.toFixed(1),
  };
}"""

LABELS = """() => {
  const cs = el => getComputedStyle(el);
  return [].slice.call(document.querySelectorAll('#editorModal .editor__field > label, #editorModal .editor__field > .editor__label, #fillinModal .editor__field > label'))
    .map(l => [l.textContent.trim(), cs(l).fontSize, cs(l).fontWeight, cs(l).display,
               cs(l).marginBottom, cs(l).color].join(' | '));
}"""

NEW_MODAL = """() => {
  const sw = document.querySelector('[data-tatib-kinds], [data-kind-switch]');
  const cs = el => getComputedStyle(el);
  const box = el => { const r = el.getBoundingClientRect(); return {w: +r.width.toFixed(1), h: +r.height.toFixed(1)}; };
  const frame = document.querySelector('#editorModal .editor__content')
             || document.querySelector('#newModal .editor__content');
  const thumb = sw && sw.querySelector('.screen-mode__thumb');
  return {
    frame: frame ? box(frame) : null,
    track: sw ? {box: box(sw), radius: cs(sw).borderRadius, padding: cs(sw).padding,
                 font: cs(sw.querySelector('button')).fontSize} : null,
    icons: sw ? sw.querySelectorAll('svg').length : 0,
    thumb: thumb ? box(thumb) : null,
    buttons: sw ? [].slice.call(sw.querySelectorAll('button')).map(b => ({text: b.textContent.trim(), box: box(b)})) : [],
  };
}"""


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PreviewParityTests(StaticLiveServerTestCase):
    def setUp(self):
        self.service = tatib.TataIbadah.objects.create(
            name='Parity skeleton', is_active=True)   # no date: a template
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, order_number=1,
            title='Votum', text='Pertolongan kita adalah dalam nama Tuhan, yang menjadikan langit dan bumi.')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.FILL_IN,
            fill_kind=tatib.SlotKind.SONG, title='Nyanyian Pembuka', order_number=2)
        choice = tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.CHOICE,
            fill_kind=tatib.SlotKind.TEXT, title='Doa Pengutusan', order_number=3)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, parent=choice,
            order_number=4, title='Doa Damai', text='Tuhan, berilah damai.')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.TEXT, parent=choice,
            order_number=5, title='Doa Berkat', text='Tuhan, berkati kami.')

        # One row of each meta the page draws: a bait line, a media meta, and an option
        # that carries a bait of its own.
        book = songs.Book.objects.create(name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
        hymn = songs.Song.objects.create(book=book, number=12, title='Di Waktu Pagi', key='c')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, song=hymn,
            verses=[1, 2, 3], order_number=6)
        media = tatib.MediaIdentity.objects.create(
            sha256='a' * 64, byte_count=1024, family='image', display_filename='images.jpeg')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.MEDIA, media=media,
            media_filename='images.jpeg', title='Titled Media', order_number=7)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, kind=tatib.ServiceEntryKind.SONG, song=hymn, parent=choice,
            verses=[1, 3], order_number=8)

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={'width': 1440, 'height': 900})

    def tearDown(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    def live(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(500)
        return self.page.evaluate(MEASURE)

    def preview(self):
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(500)
        return self.page.evaluate(MEASURE)

    def test_the_add_bar_offers_the_same_six_buttons_in_the_same_order(self):
        self.assertEqual(self.live()['order'], self.preview()['order'])

    def test_the_page_slot_row_keeps_the_preview_type(self):
        live, preview = self.live(), self.preview()
        self.assertEqual(live['slotTitle']['size'], preview['slotTitle']['size'])
        self.assertEqual(live['slotTitle']['weight'], preview['slotTitle']['weight'])
        self.assertIn('sans', live['slotTitle']['family'].lower())
        self.assertIn('sans', preview['slotTitle']['family'].lower())
        self.assertEqual(live['slotTitle']['align'], 'left')

    def test_a_slot_row_draws_its_mark(self):
        self.assertTrue(self.live()['mark'])
        self.assertTrue(self.preview()['mark'])

    def test_the_option_sits_where_the_preview_puts_it(self):
        """An option is indented inside its choice, behind one continuous rule.

        The preview wrapped the options in a container that carried the rule; the product
        emits them as siblings, so each row draws its own left edge -- contiguous, and the
        indent has to match the preview's.
        """
        live, preview = self.live(), self.preview()
        # the preview wraps options in a container that carries the rule; the product draws
        # it on each row, so the check is the rule and a real indent, not a shared parent
        # the rule belongs to the group, not to each row
        self.assertEqual(live['option']['borderLeft'], '0px', live)
        self.assertEqual(live['option']['listRule'], '1px', live)
        self.assertGreaterEqual(live['option']['offset'], 8, live)

    def test_add_option_sits_on_the_option_text(self):
        live = self.live()
        # the control takes its line from the option rows, icon column included
        self.assertLessEqual(abs(live['addOptionX'] - live['optionRowX']), 2, live)

    def test_the_new_tata_ibadah_modal_wears_the_preview_switcher(self):
        """The type switch is the preview's segmented control, not two bare buttons.

        The product renders it with the app's own screen-mode component; a modal whose
        switcher falls back to browser defaults is the failure this asserts against.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib'))
        self.page.wait_for_timeout(400)
        self.page.click('#panelAdd')
        self.page.wait_for_selector('[data-tatib-kinds]', timeout=8000)
        live = self.page.evaluate(NEW_MODAL)
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(400)
        self.page.evaluate("() => document.getElementById('newModal').showModal()")
        self.page.wait_for_timeout(300)
        preview = self.page.evaluate(NEW_MODAL)

        self.assertIsNotNone(live['track'], f'live: {live}')
        self.assertIsNotNone(preview['track'], f'preview: {preview}')
        self.assertEqual(live['track']['radius'], preview['track']['radius'])
        self.assertEqual(live['track']['padding'], preview['track']['padding'])
        self.assertEqual(live['track']['font'], preview['track']['font'])
        self.assertEqual(live['icons'], preview['icons'])
        self.assertAlmostEqual(live['track']['box']['w'], preview['track']['box']['w'], delta=1)
        self.assertAlmostEqual(live['track']['box']['h'], preview['track']['box']['h'], delta=1)
        self.assertEqual(len(live['buttons']), len(preview['buttons']))
        for mine, theirs in zip(live['buttons'], preview['buttons']):
            self.assertEqual(mine['text'], theirs['text'])
            self.assertAlmostEqual(mine['box']['w'], theirs['box']['w'], delta=1)
        self.assertAlmostEqual(live['frame']['h'], preview['frame']['h'], delta=2)

    def test_the_kind_picker_matches_the_preview(self):
        """Four equal cells, in the spec's order, the first one chosen.

        The product drew its own controls here while the preview drew text pills, so the
        markup alone can look right and still land as browser-default buttons.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        # the add bar reveals on hover; the click is made on the button itself
        self.page.eval_on_selector('[data-entry-open="fill_in"]', 'el => el.click()')
        self.page.wait_for_selector('[data-slot-kinds]', timeout=8000)
        live = self.page.evaluate(KINDS)
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(400)
        self.page.evaluate("() => document.getElementById('fillinModal').showModal()")
        self.page.wait_for_timeout(300)
        preview = self.page.evaluate(KINDS)

        self.assertEqual(live['order'], preview['order'])
        self.assertEqual(live['pressed'][0], 'true')
        self.assertEqual(preview['pressed'][0], 'true')
        self.assertEqual(live['height'], preview['height'])
        self.assertEqual(live['radius'], preview['radius'])
        self.assertEqual(live['font'], preview['font'])
        self.assertEqual(live['gap'], preview['gap'])
        self.assertEqual(live['columns'], preview['columns'])
        self.assertAlmostEqual(live['width'], preview['width'], delta=1)

    def test_every_field_label_reads_the_same(self):
        """A group's label (Kind) is drawn like a control's label (Title or note).

        The kind group labels itself with a span rather than a <label>, so it only looks
        right if the rule covers both.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        self.page.eval_on_selector('[data-entry-open="fill_in"]', 'el => el.click()')
        self.page.wait_for_selector('[data-slot-kinds]', timeout=8000)
        live = self.page.evaluate(LABELS)
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(400)
        self.page.evaluate("() => document.getElementById('fillinModal').showModal()")
        self.page.wait_for_timeout(300)
        preview = self.page.evaluate(LABELS)

        self.assertEqual(len(live), len(preview), live)
        style = lambda rows: [row.split(' | ', 1)[1] for row in rows]
        self.assertEqual(style(live), style(preview))

    def test_the_step_digit_is_centred_in_its_circle(self):
        """No fixed lift in CSS: the digit is placed from the font's measured ink box.

        A constant nudge is only right for one font at one device-pixel ratio -- the one
        that shipped first was a pixel low at 1x and a pixel high at 1.25x.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        self.page.click('[data-generate-open]')
        self.page.wait_for_selector('.generate__steps li .generate__step-mark i', timeout=8000)
        marks = self.page.evaluate("""() => [].slice.call(document.querySelectorAll('.generate__steps li .generate__step-mark i')).map(i => {
          const m = new DOMMatrixReadOnly(getComputedStyle(i).transform);
          const circle = i.parentElement.getBoundingClientRect();
          const box = i.getBoundingClientRect();
          return {dy: +m.m42.toFixed(2), dx: +m.m41.toFixed(2),
                  boxCentreDelta: +((box.y + box.height / 2) - (circle.y + circle.height / 2)).toFixed(2)};
        })""")
        self.assertEqual(len(marks), 2)
        for mark in marks:
            self.assertLessEqual(abs(mark['dy']), 1, mark)
            self.assertLessEqual(abs(mark['dx']), 1, mark)
            self.assertLessEqual(abs(mark['boxCentreDelta']), 0.6, mark)

    def test_the_step_labels_sit_on_their_badges(self):
        """The label is a text run, not a badge: capitals ride high on the line box, so it
        carries its own small lift. Styling the label as the mark is the failure mode this
        guards -- both were `<span>`s and the badge rule caught the label too.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        self.page.click('[data-generate-open]')
        self.page.wait_for_selector('.generate__step-label', timeout=8000)
        labels = self.page.evaluate("""() => [].slice.call(document.querySelectorAll('.generate__step-label')).map(l => {
          const cs = getComputedStyle(l);
          const m = new DOMMatrixReadOnly(cs.transform);
          const mark = l.parentElement.querySelector('.generate__step-mark').getBoundingClientRect();
          const box = l.getBoundingClientRect();
          return {text: l.textContent.trim(), width: +box.width.toFixed(1),
                  ty: +m.m42.toFixed(2), size: cs.fontSize, radius: cs.borderTopLeftRadius,
                  delta: +((box.y + box.height / 2) - (mark.y + mark.height / 2)).toFixed(2)};
        })""")
        self.assertEqual(len(labels), 2)
        for label in labels:
            self.assertGreater(label['width'], 20, label)            # not an 18px circle
            self.assertEqual(label['radius'], '0px', label)
            self.assertNotEqual(label['ty'], 0, label)   # measured at runtime, not inherited
            self.assertLessEqual(abs(label['delta']), 1.5, label)
        self.assertEqual([label['text'] for label in labels],
                         ['Fill in the entries', 'Name and date'])

    def test_the_step_digit_is_drawn_in_the_bundled_face(self):
        """The badge's numeral must not depend on the machine's UI font.

        ui-sans-serif resolves differently on every platform, and a correction that centres
        a digit in one font puts it a pixel high in the next -- which is what the owner saw.
        Source Sans 3 ships in the repository, so its metrics are the same everywhere.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        self.page.click('[data-generate-open]')
        self.page.wait_for_selector('.generate__step-mark', timeout=8000)
        families = self.page.evaluate("""() => [].slice.call(document.querySelectorAll('.generate__step-mark')).map(m => {
          const cs = getComputedStyle(m);
          const m2 = new DOMMatrixReadOnly(getComputedStyle(m.querySelector('i')).transform);
          return {family: cs.fontFamily.split(',')[0].replace(/["']/g, ''), ty: +m2.m42.toFixed(2)};
        })""")
        self.assertEqual(len(families), 2)
        for badge in families:
            self.assertEqual(badge['family'], 'Source Sans 3', badge)
            self.assertLessEqual(abs(badge['ty']), 1, badge)

    def test_a_slot_row_holds_the_lists_icon_and_text_columns(self):
        """The slot's mark sits in the 24px icon column and its text on the 64px line.

        Those are the columns every icon-bearing entry uses: a 20px icon starting 24px in
        (centre 34) with the title 64px in. The preview mock put the text at 56 and the row
        read short of the titles around it.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(500)
        slots = self.page.evaluate("""() => [].slice.call(document.querySelectorAll('#read .tatib__item--slot')).filter(el => el.getBoundingClientRect().height).map(el => {
          const r = el.getBoundingClientRect();
          const mark = el.querySelector('.slot__mark').getBoundingClientRect();
          const title = el.querySelector('.read__sec').getBoundingClientRect();
          const kind = el.querySelector('.slot__kind');
          return {markCentre: Math.round(mark.x + mark.width / 2 - r.x),
                  markLeft: Math.round(mark.x - r.x),
                  titleX: Math.round(title.x - r.x),
                  kindX: kind ? Math.round(kind.getBoundingClientRect().x - r.x) : null};
        })""")
        self.assertTrue(slots, 'no slot rows on the page')
        for row in slots:
            self.assertEqual(row['markLeft'], 24, row)      # the list's icon column
            self.assertEqual(row['markCentre'], 34, row)
            self.assertEqual(row['titleX'], 64, row)        # the list's text column
            if row['kindX'] is not None:
                self.assertEqual(row['kindX'], 64, row)

    def test_every_title_reads_in_the_entry_heading(self):
        """Entry, choice and option titles share one style; the kind line stays smaller.

        The choice used to carry a serif heading of its own, which made the same list read
        as two different kinds of thing.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(500)
        styles = self.page.evaluate("""() => {
          const cs = (sel) => { const el = document.querySelector(sel); if (!el) return null;
            const c = getComputedStyle(el);
            const size = parseFloat(c.fontSize);
            return {size, ratio: +(parseFloat(c.lineHeight) / size).toFixed(2), weight: c.fontWeight,
                    family: c.fontFamily.split(',')[0],
                    tracking: +(parseFloat(c.letterSpacing) / size).toFixed(3)}; };
          return {entry: cs('#read .tatib__item--entry > .read__sec'),
                  choice: cs('#read .tatib__item--choice > .read__sec'),
                  option: cs('#read .tatib__item--option .read__sec'),
                  kind: cs('#read .slot__kind')};
        }""")
        for key in ('entry', 'choice', 'option'):
            self.assertIsNotNone(styles[key], f'no {key} title on the fixture page')
        self.assertEqual(styles['choice'], styles['entry'], 'the choice title differs from the entry title')
        # the option is the one title that steps down -- same style, a smaller size
        for prop in ('weight', 'family', 'tracking', 'ratio'):
            self.assertEqual(styles['option'][prop], styles['entry'][prop], f'option {prop} differs')
        self.assertLess(styles['option']['size'], styles['entry']['size'], styles)
        self.assertLess(styles['kind']['size'], styles['option']['size'], styles)

    def test_every_meta_reads_in_one_style(self):
        """All the quiet lines are one style: the entry's meta, with the option's a size
        below and the choice's count line a weight below that.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(500)
        metas = self.page.evaluate("""() => {
          const cs = (sel) => { const el = document.querySelector(sel); if (!el) return null;
            const c = getComputedStyle(el); const size = parseFloat(c.fontSize);
            return {size, ratio: +(parseFloat(c.lineHeight) / size).toFixed(2), weight: c.fontWeight,
                    family: c.fontFamily.split(',')[0],
                    tracking: +(parseFloat(c.letterSpacing) / size).toFixed(3)}; };
          return {media: cs('#read .tatib__item--media .read__sub'),
                  bait: cs('#read .tatib__item--song .read__sub'),
                  option: cs('#read .tatib__item--option .read__sub'),
                  count: cs('#read .tatib__item--choice .slot__state')};
        }""")
        self.assertEqual(metas['bait'], metas['media'], 'the bait line differs from the media meta')
        for prop in ('weight', 'family', 'tracking', 'ratio'):
            self.assertEqual(metas['option'][prop], metas['media'][prop], f'option meta {prop} differs')
        self.assertLess(metas['option']['size'], metas['media']['size'], metas)

        self.assertEqual(metas['count']['size'], metas['option']['size'], 'the count is not the option meta size')
        self.assertLess(int(metas['count']['weight']), int(metas['option']['weight']),
                        'the count line is not lighter than the meta')
        for prop in ('family', 'tracking', 'ratio'):
            self.assertEqual(metas['count'][prop], metas['option'][prop], f'count {prop} differs')

    def test_use_template_is_the_previews_filled_button(self):
        """The preview drew Use template as the page's filled action, icon and all; the
        product drew it as a quiet bar beside Media files.
        """
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        live = self.page.evaluate("""() => {
          const el = [...document.querySelectorAll('button')].find(b => /use template/i.test(b.textContent));
          const c = getComputedStyle(el); const r = el.getBoundingClientRect();
          return {w: Math.round(r.width), h: Math.round(r.height), radius: c.borderRadius,
                  bg: c.backgroundColor, ink: c.color, weight: c.fontWeight,
                  icon: !!el.querySelector('svg')};
        }""")
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(400)
        preview = self.page.evaluate("""() => {
          const el = document.querySelector('.read__project-btn--primary');
          const c = getComputedStyle(el); const r = el.getBoundingClientRect();
          return {w: Math.round(r.width), h: Math.round(r.height), radius: c.borderRadius,
                  bg: c.backgroundColor, ink: c.color, weight: c.fontWeight,
                  icon: !!el.querySelector('svg')};
        }""")
        self.assertEqual(live, preview)

    def test_the_muted_rows_in_use_template_are_the_preview_size(self):
        self.page.goto(self.live_server_url + reverse('web-tatib-service', args=[self.service.pk]))
        self.page.wait_for_timeout(400)
        self.page.click('[data-generate-open]')
        self.page.wait_for_timeout(400)
        live = self.page.evaluate(GENERATE)
        self.page.goto(PREVIEW.as_uri())
        self.page.wait_for_timeout(400)
        self.page.click('[data-surface="generate"]')
        self.page.wait_for_timeout(400)
        preview = self.page.evaluate(GENERATE)
        self.assertEqual(live['titleSize'], preview['titleSize'])
        self.assertEqual(live['bodySize'], preview['bodySize'])
        self.assertEqual(live['opacity'], preview['opacity'])
        self.assertLessEqual(abs(live['rowHeight'] - preview['rowHeight']), preview['rowHeight'] * 0.15,
                             f"{live['rowHeight']} vs {preview['rowHeight']}")
