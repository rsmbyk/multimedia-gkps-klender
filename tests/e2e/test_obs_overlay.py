"""The OBS caption overlay — what it paints, per entry kind (specs 119 and 180).

The overlay is a browser source for OBS: it renders the browser-local display
state and carries no controls at all. Songs keep the bare subtitle caption, a
lyric block legible over the video with no plate. A passage and a liturgy text
wear a plate instead, so the screen's heading — the Bible reference and the
verse's own title, or the entry's title — can sit above the words.
"""

import re
import unittest
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

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
class ObsOverlayE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 18), is_active=True)
        # 1 — a liturgy text: a leader's line and the congregation's answer.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam',
            text=('L. Di dalam nama Allah Bapa, dan Tuhan Yesus Kristus, serta Roh Kudus, '
                  'Pencipta langit dan bumi, yang telah memanggil kita ke dalam persekutuan '
                  'dengan Anak-Nya.\nJ. Amin.'))
        # 2 — a hymn, the surface the caption was designed for.
        songbook = songs.Book.objects.create(
            name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=152, title='Ada Kuasa')
        song_verse = songs.Verse.objects.create(
            song=song, number=1,
            lyric='Bait satu baris yang pertama\nBait satu baris yang kedua')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.SONG,
            song=song, verses=[song_verse.pk])
        # 3 — a passage in its own edition, with a second edition to flip to.
        lang = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=lang, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
        matius = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(
            book_translation=matius, chapter=5, verse=3,
            title='Kesembuhan pada hari Sabat',
            text='ayat 3, orang lumpuh disembuhkan pada hari Sabat')
        sim_lang = bible.Language.objects.create(name='Simalungun')
        sim_version = bible.Version.objects.create(
            lang=sim_lang, name='Simalungun', abbreviation='SIM')
        mateus = bible.BookTranslation.objects.create(
            version=sim_version, book=book, translation='Mateus')
        bible.Verse.objects.create(
            book_translation=mateus, chapter=5, verse=3,
            text='ayat 3 (SIM), na malum do halak na sarion i')
        # A second verse, so the same panel serves two screens of very different size.
        bible.Verse.objects.create(
            book_translation=matius, chapter=5, verse=4,
            text=('ayat 4, sebuah ayat yang jauh lebih panjang daripada ayat sebelumnya, '
                  'supaya panelnya harus melebar sampai ukuran penuh sebelum ia berhenti '
                  'dan kata-katanya selesai dibungkus ke baris-barisnya sendiri'))
        bible.Verse.objects.create(
            book_translation=mateus, chapter=5, verse=4,
            text='ayat 4 (SIM), na ganjang do ayat on, asa bolak hian panepina i')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=matius, chapter=5, verse_start=3, verse_end=4)
        # 4 — a leader's turn continuing on an unmarked line (spec 211).
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=4, kind=tatib.ServiceEntryKind.TEXT,
            title='Pengakuan Iman',
            text=('L. Aku percaya kepada Allah\n'
                  'Bapa yang mahakuasa, Khalik langit dan bumi.'))
        # 5 — the same turn with a new voice after it, held on one screen.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=5, kind=tatib.ServiceEntryKind.TEXT,
            title='Pengakuan Iman', default_screen_mode=tatib.TextScreenMode.SINGLE_SCREEN,
            text=('L. Aku percaya kepada Allah\n'
                  'Bapa yang mahakuasa, Khalik langit dan bumi.\n'
                  'J. Amin.'))
        # 6 — a continuation long enough to wrap inside the plate.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=6, kind=tatib.ServiceEntryKind.TEXT,
            title='Pengakuan Iman',
            text=('L. Aku percaya kepada Allah\n'
                  'Bapa yang mahakuasa, Khalik langit dan bumi, dan kepada Yesus Kristus, '
                  'Anak-Nya yang tunggal, Tuhan kita, yang dikandung daripada Roh Kudus, '
                  'lahir dari anak dara Maria, yang menderita di bawah pemerintahan '
                  'Pontius Pilatus, disalibkan, mati dan dikuburkan.'))
        # 7 — two screens: the second begins mid-turn and paints no mark.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=7, kind=tatib.ServiceEntryKind.TEXT,
            title='Pengakuan Iman',
            text=('L. Di dalam nama Allah Bapa\n'
                  'dan Tuhan Yesus Kristus\n'
                  'dan Roh Kudus, Pencipta langit dan bumi\n'
                  'yang telah memanggil kita ke dalam persekutuan.'))
        # 8 — a cue resets the voice; a later body has no speaker at all.
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=8, kind=tatib.ServiceEntryKind.TEXT,
            title='Nyanyian',
            text=('Nyanyian: Kidung Jemaat 152\n'
                  'Tuhan, kasihanilah kami\n'
                  '\n'
                  'Hari ini kita berdoa bersama\n'
                  'Tuhan, dengarkanlah kami.'))

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

    # ---------- helpers -------------------------------------------------------

    def _dock(self, context):
        """The dock with this service open, before anything is projected."""
        dock = context.new_page()
        dock.goto(self.live_server_url + '/obs/dock')
        dock.locator(f'.servicerow[data-service="{self.service.pk}"]').click()
        dock.wait_for_selector('.entryrow')
        return dock

    def _overlay_blank(self, context):
        """The overlay before anything is on air — the page, painting nothing."""
        page = context.new_page()
        page.goto(self.live_server_url + '/obs/source/overlay')
        return page

    def _project(self, context, entry_index):
        """Open the dock, project the entry at that index, and hand the dock back."""
        dock = self._dock(context)
        dock.locator('.entryrow').nth(entry_index).click()
        dock.locator(f'.entryli[data-index="{entry_index}"] .screenerow').first.click()
        dock.wait_for_function(
            "service => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s && s.service === service && s.on === true; }", arg=self.service.pk)
        return dock

    def _project_screen(self, context, entry_index, screen_index):
        """Project a chosen screen of an entry, for bodies whose turn spans screens."""
        dock = self._dock(context)
        dock.locator('.entryrow').nth(entry_index).click()
        dock.locator(f'.entryli[data-index="{entry_index}"] .screenerow').nth(screen_index).click()
        dock.wait_for_function(
            "service => { const s = JSON.parse(localStorage.getItem('gkps-display') || 'null');"
            " return s && s.service === service && s.on === true; }", arg=self.service.pk)
        return dock

    def _overlay(self, context, selector):
        overlay = context.new_page()
        overlay.goto(self.live_server_url + '/obs/source/overlay')
        overlay.wait_for_selector(selector)
        # Pixel measurements (lefts, wrap rows) read positions and glyph runs:
        # the enter motion scales the plate (a mid-flight read shifts the words'
        # x by a couple of pixels) and a mid-swap read measures the fallback
        # font's metrics. Both waits are cheap once the page is settled.
        overlay.wait_for_function(
            """sel => { const el = document.querySelector(sel);
                 if (!el) return false;
                 const t = getComputedStyle(el).transform;
                 return t === 'none' || t === 'matrix(1, 0, 0, 1, 0, 0)'; }""",
            arg=selector)
        overlay.evaluate("() => document.fonts.ready")
        return overlay

    def _flush_geometry(self, overlay):
        """The lines' glyph x against the plate's content edge (spec 211's no-indent case)."""
        return overlay.evaluate("""() => {
            const plate = document.querySelector('.obs-overlay__plate');
            const sheet = getComputedStyle(plate);
            const contentLeft = plate.getBoundingClientRect().left
                + parseFloat(sheet.paddingLeft) + parseFloat(sheet.borderLeftWidth);
            const lines = [...document.querySelectorAll('.obs-overlay__line')];
            const firstX = node => {
              const range = document.createRange();
              range.selectNodeContents(node);
              return [...range.getClientRects()].filter(r => r.width > 0)[0].left;
            };
            return {
              text: lines.map(line => line.textContent),
              lefts: lines.map(firstX),
              contentLeft: contentLeft,
              marks: document.querySelectorAll('.obs-overlay__speaker').length,
              continued: document.querySelectorAll('.obs-overlay__line.is-continuation').length
            };
        }""")

    def _computed(self, page, selector, *properties):
        return page.evaluate("""([selector, properties]) => {
            const element = document.querySelector(selector);
            if (!element) return null;
            const style = getComputedStyle(element);
            return Object.fromEntries(properties.map(p => [p, style[p]]));
        }""", [selector, list(properties)])

    # ---------- songs ---------------------------------------------------------

    def test_a_song_screen_keeps_the_bare_caption_style(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 1)
        overlay = self._overlay(context, '.obs-overlay__caption')
        self.assertIn('Bait satu baris', overlay.locator('.obs-overlay__caption').inner_text())
        # No plate and no heading: a lyric is read as a subtitle, straight over the video.
        self.assertEqual(overlay.locator('.obs-overlay__plate').count(), 0)
        self.assertEqual(overlay.locator('.obs-overlay__kicker').count(), 0)
        self.assertEqual(overlay.evaluate("document.getElementById('overlayStage').dataset.kind"),
                         'song')
        self.assertEqual(overlay.evaluate(
            "() => document.querySelectorAll('.obs-overlay__caption span').length"), 2)

        style = self._computed(overlay, '.obs-overlay__caption', 'fontWeight', 'color',
                               'backgroundColor', 'textShadow')
        self.assertEqual(style['fontWeight'], '800')
        self.assertEqual(style['backgroundColor'], 'rgba(0, 0, 0, 0)')
        self.assertIn('rgb(0, 0, 0)', style['textShadow'])
        # The caption's rest is 5 % of the stage height (spec 202).
        css = (Path(settings.BASE_DIR) / 'static' / 'styles' / 'design'
               / 'obs-overlay.css').read_text(encoding='utf-8')
        scale = re.search(r'\.obs-overlay__caption\s*\{[^}]*font-size: ([\d.]+)cqh', css)
        expected = float(scale.group(1)) * 720 / 100
        size = float(self._computed(overlay, '.obs-overlay__caption', 'fontSize')['fontSize'][:-2])
        self.assertAlmostEqual(size, expected, places=1)
        context.close()

    def test_a_song_screen_does_not_repeat_the_entry_title(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 1)
        overlay = self._overlay(context, '.obs-overlay__caption')
        self.assertNotIn('Ada Kuasa', overlay.locator('.obs-overlay__stage').inner_text())
        context.close()

    # ---------- passages and liturgy texts ------------------------------------

    def test_a_passage_wears_a_plate_naming_its_reference_and_title(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 2)
        overlay = self._overlay(context, '.obs-overlay__plate')
        self.assertEqual(overlay.locator('.obs-overlay__caption').count(), 0)
        self.assertEqual(overlay.locator('.obs-overlay__kicker').text_content(), 'Matius 5:3')
        self.assertEqual(overlay.locator('.obs-overlay__title').text_content(),
                         'Kesembuhan pada hari Sabat')
        # The reference is set in small caps by the stylesheet, not rewritten in the DOM.
        self.assertEqual(self._computed(overlay, '.obs-overlay__kicker',
                                        'textTransform')['textTransform'], 'uppercase')
        self.assertIn('ayat 3', overlay.locator('.obs-overlay__body').inner_text())

        # The plate is the background the words sit on: a near-opaque dark fill,
        # so white body text reads over a bright frame without the fat outline.
        style = self._computed(overlay, '.obs-overlay__plate', 'backgroundColor',
                               'position', 'bottom', 'textAlign', 'borderTopLeftRadius',
                               'fontSize')
        self.assertNotEqual(style['backgroundColor'], 'rgba(0, 0, 0, 0)')
        self.assertEqual(style['position'], 'absolute')
        # A scripture is a quotation: a centred card whose corner is rounded in
        # proportion to its own type, not the liturgy's near-square panel.
        self.assertEqual(style['textAlign'], 'center')
        self.assertGreaterEqual(float(style['borderTopLeftRadius'][:-2])
                                / float(style['fontSize'][:-2]), 0.25)
        body = self._computed(overlay, '.obs-overlay__line', 'textShadow')
        self.assertEqual(body['textShadow'], 'none')
        context.close()

    def test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 0)
        overlay = self._overlay(context, '.obs-overlay__plate')
        self.assertEqual(overlay.locator('.obs-overlay__kicker').text_content(), 'Salam')
        self.assertEqual(overlay.locator('.obs-overlay__line').count(), 2)
        self.assertEqual(overlay.locator('.obs-overlay__line.is-leader').count(), 1)
        self.assertIn('Di dalam nama', overlay.locator('.obs-overlay__line.is-leader').inner_text())
        self.assertEqual(overlay.evaluate("document.getElementById('overlayStage').dataset.kind"),
                         'liturgy')

        # A liturgy is spoken, not quoted: a flat, left-aligned panel whose bar marks
        # the leading edge — not the passage's rounded, centred card.
        plate = self._computed(overlay, '.obs-overlay__plate', 'textAlign',
                               'borderLeftWidth', 'borderTopLeftRadius', 'fontSize')
        self.assertEqual(plate['textAlign'], 'left')
        self.assertGreaterEqual(float(plate['borderLeftWidth'][:-2]), 1.5)
        self.assertLessEqual(float(plate['borderTopLeftRadius'][:-2])
                             / float(plate['fontSize'][:-2]), 0.1)

        # The leader's line is a cue, so it sits quieter than the congregation's.
        def ink(selector):
            colour = self._computed(overlay, selector, 'color')['color']
            channels = [float(value) for value in re.findall(r'[\d.]+', colour)]
            if len(channels) == 3:
                channels.append(1.0)
            red, green, blue, alpha = channels
            plate = [float(value) for value in
                     re.findall(r'[\d.]+', plate_style['backgroundColor'])]
            # Both lines share the plate, so the plate flattened over black is their
            # common backdrop; what differs is the ink's own alpha.
            return [alpha * channel + (1 - alpha) * plate_channel * plate[3]
                    for channel, plate_channel in zip((red, green, blue), plate)]

        plate_style = self._computed(overlay, '.obs-overlay__plate', 'backgroundColor')
        self.assertLess(sum(ink('.obs-overlay__line.is-leader')),
                        sum(ink('.obs-overlay__line:not(.is-leader)')))
        context.close()

    def test_a_panel_enters_and_leaves_with_a_short_motion(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        overlay = self._overlay_blank(context)
        overlay.evaluate("""() => {
            window.__overlayMotion = [];
            document.addEventListener('animationstart', (event) => {
                const running = event.target.getAnimations();
                window.__overlayMotion.push({
                    name: event.animationName,
                    duration: running.length ? running[0].effect.getTiming().duration : null
                });
            }, true);
        }""")

        # A panel appears: it fades and rises into its place.
        dock = self._dock(context)
        dock.locator('.entryrow').nth(2).click()          # the passage
        dock.locator('.entryli[data-index="2"] .screenerow').first.click()
        overlay.wait_for_selector('.obs-overlay__plate')
        overlay.wait_for_timeout(400)

        # The display blanks: the panel fades away instead of vanishing.
        dock.evaluate('window.gkpsDisplay.hide()')
        overlay.wait_for_function(
            "() => document.getElementById('overlayStage').children.length === 0")

        motion = overlay.evaluate('() => window.__overlayMotion')
        self.assertEqual([entry['name'] for entry in motion],
                         ['overlay-plate-in', 'overlay-plate-out'], motion)
        self.assertEqual([entry['duration'] for entry in motion], [180, 120], motion)
        context.close()

    def test_a_second_screen_morphs_the_panel_box(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        dock = self._dock(context)
        dock.locator('.entryrow').nth(2).click()          # the passage: verse 3 first
        dock.locator('.entryli[data-index="2"] .screenerow').first.click()
        overlay = self._overlay(context, '.obs-overlay__plate')
        before = overlay.evaluate(
            "() => document.querySelector('.obs-overlay__plate').offsetWidth")

        dock.keyboard.press('ArrowDown')                  # the entry's second verse
        overlay.wait_for_function(
            "() => { const plate = document.querySelector('.obs-overlay__plate');"
            " return !!(plate && plate.classList.contains('is-resizing')); }")
        overlay.wait_for_timeout(500)
        after = overlay.evaluate(
            "() => document.querySelector('.obs-overlay__plate').offsetWidth")
        inline = overlay.evaluate("""() => {
          const plate = document.querySelector('.obs-overlay__plate');
          return [plate.style.width, plate.style.height, plate.className];
        }""")

        self.assertNotEqual(after, before)                # it took the second verse's measure
        self.assertEqual(inline, ['', '', 'obs-overlay__plate'])
        context.close()

    def test_a_caption_enters_and_leaves_with_the_same_clock(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        overlay = self._overlay_blank(context)
        overlay.evaluate("""() => {
            window.__overlayMotion = [];
            document.addEventListener('animationstart', (event) => {
                const running = event.target.getAnimations();
                window.__overlayMotion.push({
                    name: event.animationName,
                    duration: running.length ? running[0].effect.getTiming().duration : null
                });
            }, true);
        }""")

        dock = self._dock(context)
        dock.locator('.entryrow').nth(1).click()        # the song
        dock.locator('.entryli[data-index="1"] .screenerow').first.click()
        overlay.wait_for_selector('.obs-overlay__caption')
        overlay.wait_for_timeout(400)

        dock.evaluate('window.gkpsDisplay.hide()')
        overlay.wait_for_function(
            "() => document.getElementById('overlayStage').children.length === 0")

        motion = overlay.evaluate('() => window.__overlayMotion')
        self.assertEqual([entry['name'] for entry in motion],
                         ['overlay-caption-in', 'overlay-caption-out'], motion)
        self.assertEqual([entry['duration'] for entry in motion], [180, 120], motion)
        context.close()

    def test_a_wrapped_speaker_line_hangs_under_its_words(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 0)
        overlay = self._overlay(context, '.obs-overlay__plate')
        measured = overlay.evaluate("""() => {
            const line = document.querySelector('.obs-overlay__line.is-leader');
            const speaker = line.querySelector('.obs-overlay__speaker');
            const words = line.querySelector('.obs-overlay__words');
            const range = document.createRange();
            range.selectNodeContents(words);
            const rects = [...range.getClientRects()].filter(rect => rect.width > 0);
            return {
                speaker: speaker ? speaker.textContent : null,
                words: words ? words.textContent.slice(0, 24) : null,
                rows: rects.length,
                lefts: rects.map(rect => Math.round(rect.left)),
                lineLeft: Math.round(line.getBoundingClientRect().left)
            };
        }""")
        self.assertEqual(measured['speaker'], 'L.')
        self.assertTrue(measured['words'].startswith('Di dalam nama'), measured['words'])
        self.assertGreaterEqual(measured['rows'], 2, measured)
        # Every visual row of the words begins on the same x — the wrap hangs under the
        # words, not under the speaker mark or the panel's edge.
        self.assertLessEqual(max(measured['lefts']) - min(measured['lefts']), 1, measured)
        self.assertGreater(measured['lefts'][0], measured['lineLeft'], measured)

        # The marks on a screen share one column, sized by the widest: the answer's words
        # begin on the leader's x, not after its own narrow "J.".
        answer_left = overlay.evaluate("() => { const answer = "
                                       "document.querySelector('.obs-overlay__line.is-assembly "
                                       ".obs-overlay__words');"
                                       " return answer ? Math.round(answer.getBoundingClientRect().left) : null; }")
        self.assertIsNotNone(answer_left, 'the answer line has no words span')
        self.assertLessEqual(abs(answer_left - measured['lefts'][0]), 1,
                             f'answer words at {answer_left}, leader at {measured["lefts"][0]}')
        context.close()

    # ---------- a speaker's turn (spec 211) ------------------------------------

    def test_a_continuation_hangs_at_the_marked_words(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 3)
        overlay = self._overlay(context, '.obs-overlay__plate')
        measured = overlay.evaluate("""() => {
            const lines = [...document.querySelectorAll('.obs-overlay__line')];
            const marked = document.querySelector('.obs-overlay__line.has-mark');
            const words = marked.querySelector('.obs-overlay__words');
            const cont = lines.find(line => line !== marked);
            const firstX = node => {
              const range = document.createRange();
              range.selectNodeContents(node);
              return [...range.getClientRects()].filter(r => r.width > 0)[0].left;
            };
            return {
              lines: lines.length,
              mark: marked.querySelector('.obs-overlay__speaker').textContent,
              wordsX: firstX(words),
              contX: firstX(cont),
              contText: cont.textContent,
              contClass: cont.className,
              hasSpeakerSpan: !!cont.querySelector('.obs-overlay__speaker'),
              wordsColor: getComputedStyle(words).color,
              contColor: getComputedStyle(cont).color
            };
        }""")
        self.assertEqual(measured['lines'], 2, measured)
        self.assertEqual(measured['mark'], 'L.', measured)
        self.assertTrue(measured['contText'].startswith('Bapa'), measured)
        self.assertLessEqual(abs(measured['contX'] - measured['wordsX']), 1, measured)
        self.assertIn('is-continuation', measured['contClass'], measured)
        self.assertIn('is-leader', measured['contClass'], measured)
        self.assertFalse(measured['hasSpeakerSpan'], measured)
        self.assertEqual(measured['contColor'], measured['wordsColor'], measured)
        context.close()

    def test_the_widest_mark_sets_the_continuation_column(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 4)
        overlay = self._overlay(context, '.obs-overlay__plate')
        measured = overlay.evaluate("""() => {
            const firstX = node => {
              const range = document.createRange();
              range.selectNodeContents(node);
              return [...range.getClientRects()].filter(r => r.width > 0)[0].left;
            };
            const cont = document.querySelector('.obs-overlay__line.is-continuation');
            return {
              lines: document.querySelectorAll('.obs-overlay__line').length,
              marks: [...document.querySelectorAll('.obs-overlay__speaker')].map(m => m.textContent),
              words: [...document.querySelectorAll('.obs-overlay__words')].map(firstX),
              contX: cont ? firstX(cont) : null
            };
        }""")
        self.assertEqual(measured['lines'], 3, measured)
        self.assertEqual(measured['marks'], ['L.', 'J.'], measured)
        self.assertLessEqual(max(measured['words']) - min(measured['words']), 1, measured)
        self.assertIsNotNone(measured['contX'], measured)
        self.assertLessEqual(abs(measured['contX'] - measured['words'][0]), 1, measured)
        context.close()

    def test_a_wrapped_continuation_keeps_every_row_at_the_words_column(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project(context, 5)
        overlay = self._overlay(context, '.obs-overlay__plate')
        measured = overlay.evaluate("""() => {
            const cont = document.querySelector('.obs-overlay__line.is-continuation');
            if (!cont) return {cont: false};
            const firstX = node => {
              const range = document.createRange();
              range.selectNodeContents(node);
              return [...range.getClientRects()].filter(r => r.width > 0)[0].left;
            };
            const range = document.createRange();
            range.selectNodeContents(cont);
            const rects = [...range.getClientRects()].filter(r => r.width > 0);
            const plate = document.querySelector('.obs-overlay__plate');
            const sheet = getComputedStyle(plate);
            return {
              cont: true,
              words: firstX(document.querySelector('.obs-overlay__words')),
              lefts: rects.map(rect => rect.left),
              inkRight: Math.max(...rects.map(rect => rect.right)),
              contentRight: plate.getBoundingClientRect().right
                  - parseFloat(sheet.paddingRight) - parseFloat(sheet.borderRightWidth)
            };
        }""")
        self.assertTrue(measured['cont'], measured)
        self.assertGreaterEqual(len(measured['lefts']), 2, measured)
        self.assertLessEqual(max(measured['lefts']) - min(measured['lefts']), 1, measured)
        self.assertLessEqual(abs(measured['lefts'][0] - measured['words']), 1, measured)
        self.assertLessEqual(measured['inkRight'], measured['contentRight'] + 1, measured)
        context.close()

    def test_a_no_mark_screen_keeps_its_continuations_flush(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self._project_screen(context, 6, 1)
        overlay = self._overlay(context, '.obs-overlay__plate')
        measured = self._flush_geometry(overlay)
        self.assertEqual(len(measured['text']), 2, measured)
        self.assertTrue(measured['text'][0].startswith('dan Roh'), measured)
        self.assertEqual(measured['marks'], 0, measured)
        self.assertEqual(measured['continued'], 0, measured)
        for left in measured['lefts']:
            self.assertLessEqual(abs(left - measured['contentLeft']), 1, measured)
        context.close()

    def test_a_cue_and_an_ordinary_body_stay_flush(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        dock = self._project_screen(context, 7, 0)
        overlay = self._overlay(context, '.obs-overlay__plate')
        cue = self._flush_geometry(overlay)
        self.assertEqual(len(cue['text']), 2, cue)
        self.assertTrue(cue['text'][0].startswith('Nyanyian:'), cue)
        self.assertEqual(cue['continued'], 0, cue)
        for left in cue['lefts']:
            self.assertLessEqual(abs(left - cue['contentLeft']), 1, cue)

        dock.locator('.entryli[data-index="7"] .screenerow').nth(1).click()
        overlay.wait_for_function(
            "() => document.querySelector('.obs-overlay__body').textContent.includes('Hari ini')")
        body = self._flush_geometry(overlay)
        self.assertEqual(len(body['text']), 2, body)
        self.assertEqual(body['marks'], 0, body)
        self.assertEqual(body['continued'], 0, body)
        for left in body['lefts']:
            self.assertLessEqual(abs(left - body['contentLeft']), 1, body)
        context.close()

    def test_the_translation_flip_repaints_the_plate_heading(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        dock = self._project(context, 2)
        overlay = self._overlay(context, '.obs-overlay__plate')
        self.assertEqual(overlay.locator('.obs-overlay__kicker').text_content(), 'Matius 5:3')

        dock.keyboard.press('t')
        overlay.wait_for_function(
            "() => (document.querySelector('.obs-overlay__kicker') || {}).textContent"
            " === 'Mateus 5:3'")
        self.assertIn('na malum', overlay.locator('.obs-overlay__body').inner_text())
        context.close()

    # ---------- the shell -----------------------------------------------------

    def test_hide_empties_the_overlay_and_nothing_is_focusable(self):
        context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        dock = self._project(context, 0)
        overlay = self._overlay(context, '.obs-overlay__plate')

        # Listen-only: no button, link, input, or tab stop exists on the page.
        self.assertEqual(overlay.evaluate("""() => document.querySelectorAll(
            'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])').length"""), 0)

        dock.evaluate("window.gkpsDisplay.hide()")
        overlay.wait_for_function(
            "() => document.getElementById('overlayStage').children.length === 0")
        self.assertEqual(overlay.evaluate("document.getElementById('overlayStage').dataset.kind"),
                         '')
        context.close()
