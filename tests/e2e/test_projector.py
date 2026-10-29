"""The new service display in a browser (spec 006, slice 4).

Same runner and rules as the other e2e suites: Playwright's loop must not overlap
Django's database access, so the browser is closed before any ORM assertion, and
fixtures are created in setUp rather than in a test body.

Display mode is deliberately a browser state, so the tests work with CONTEXTS: two
pages from one context share it (that is one laptop with two tabs), a second
context is another laptop and must not be affected.
"""

import json
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


def wait_for_goto(page):
    """The Go To index is fetched with the page; wait until the panel can search."""
    page.evaluate("""(async () => {
      const deadline = Date.now() + 25000;
      while (Date.now() < deadline) {
        if (window.GKPSProjectorLibrary && GKPSProjectorLibrary.ready()) return true;
        await new Promise(resolve => setTimeout(resolve, 40));
      }
      throw new Error('Go To index did not load');
    })()""")


try:
    from playwright.sync_api import sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
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
        self.first_legacy_id = tatib.TataIbadahItem.objects.filter(
            tatib=self.service, order_number=1).values_list('pk', flat=True).get()
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
            title='Salam', text='Kasih karunia Tuhan beserta kita semua')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=3, kind=tatib.ServiceEntryKind.SECTION_BREAK,
            title='Persembahan')

        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
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
        # Every chapter runs 1..N, as the real database does: the Go To index carries a
        # count per chapter, so a fixture starting at verse 3 would describe a chapter no
        # Bible has and no search could find.
        for verse in (1, 2, 3):
            bible.Verse.objects.create(book_translation=matius, chapter=5, verse=verse,
                                       text=f'ayat {verse}')
        if self._testMethodName in ('test_a_verse_step_inside_a_chapter_makes_no_request',
                                    'test_a_chapter_crossing_locks_the_cue_and_paints_the_next_chapter'):
            bible.Verse.objects.create(book_translation=matius, chapter=5, verse=4,
                                       text='ayat 4')
            bible.Verse.objects.create(book_translation=matius, chapter=6, verse=1,
                                       text='ayat enam satu')
        if self._testMethodName == 'test_a_previous_chapter_crossing_locks_and_paints':
            bible.Verse.objects.create(book_translation=matius, chapter=4, verse=1,
                                       text='ayat empat satu')
        if self._testMethodName == 'test_goto_passage_translation_flip_brightens_the_label':
            sim_lang = bible.Language.objects.create(name='Simalungun')
            sim_version = bible.Version.objects.create(lang=sim_lang, name='Simalungun',
                                                       abbreviation='SIM')
            mateus = bible.BookTranslation.objects.create(version=sim_version, book=mat,
                                                          translation='Mateus')
            for verse in (1, 2, 3):
                bible.Verse.objects.create(book_translation=mateus, chapter=5, verse=verse,
                                           text=f'ayat {verse} (SIM)')
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=5, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=matius, chapter=5, verse_start=3)

        self.other = tatib.TataIbadah.objects.create(
            name='Ibadah Sore', date=date(2026, 8, 30), is_active=True)

        # a body far too long for one screen, so the fitting has to bring it down
        long_book = bible.Book.objects.create(name='Mzm', testament='old',
                                              number_of_chapters=150)
        long_translation = bible.BookTranslation.objects.create(
            version=version, book=long_book, translation='Mazmur')
        bible.Verse.objects.create(
            book_translation=long_translation, chapter=23, verse=1, title='Tuhan, gembalaku',
            text=' '.join(['Tuhan adalah gembalaku, takkan kekurangan aku.'] * 12))
        self.long_service = tatib.TataIbadah.objects.create(
            name='Ibadah Panjang', date=date(2026, 9, 6), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.long_service, order_number=1, kind=tatib.ServiceEntryKind.SCRIPTURE,
            book_translation=long_translation, chapter=23, verse_start=1)

        if self._testMethodName == 'test_goto_accepts_tb_and_sim_book_abbreviations':
            self.kej = bible.Book.objects.create(
                name='Kej', testament='old', number_of_chapters=50)
            bible.BookTranslation.objects.create(
                version=version, book=self.kej, translation='Kejadian')
            sim_language = bible.Language.objects.create(name='Simalungun')
            sim_version = bible.Version.objects.create(
                lang=sim_language, name='Bibel', abbreviation='SIM')
            bible.BookTranslation.objects.create(
                version=sim_version, book=self.kej, translation='1 Musa', abbreviation='1Mu')
            for translation in bible.BookTranslation.objects.filter(book=self.kej):
                bible.Verse.objects.create(
                    book_translation=translation, chapter=1, verse=1,
                    text=f'{translation.translation} ayat satu.')

            self.panguhum = bible.Book.objects.create(
                name='Hak', testament='old', number_of_chapters=21)
            tb_hakim = bible.BookTranslation.objects.create(
                version=version, book=self.panguhum, translation='Hakim-hakim')
            sim_panguhum = bible.BookTranslation.objects.create(
                version=sim_version, book=self.panguhum, translation='Panguhum',
                abbreviation='Pah')
            for translation, verses in ((tb_hakim, (1, 2)), (sim_panguhum, (1,))):
                for verse in verses:
                    bible.Verse.objects.create(
                        book_translation=translation, chapter=1, verse=verse,
                        text=f'{translation.translation} ayat {verse}.')

            self.first_chronicles = bible.Book.objects.create(
                name='1Ta', testament='old', number_of_chapters=29)
            tawarikh = bible.BookTranslation.objects.create(
                version=version, book=self.first_chronicles, translation='1 Tawarikh')
            bible.Verse.objects.create(
                book_translation=tawarikh, chapter=2, verse=1, text='Tawarikh ayat satu.')

            self.ruth = bible.Book.objects.create(
                name='Rut', testament='old', number_of_chapters=4)
            tb_ruth = bible.BookTranslation.objects.create(
                version=version, book=self.ruth, translation='Rut')
            sim_ruth = bible.BookTranslation.objects.create(
                version=sim_version, book=self.ruth, translation='Rut', abbreviation='Rut')
            for translation in (tb_ruth, sim_ruth):
                bible.Verse.objects.create(
                    book_translation=translation, chapter=1, verse=1,
                    text=f'{translation.version.abbreviation} Ruth ayat satu.')

            for code, name in (('1Sa', '1 Samuel'), ('2Sa', '2 Samuel'),
                               ('Mrk', 'Markus'), ('Luk', 'Lukas')):
                book = bible.Book.objects.create(
                    name=code, testament='old' if code.endswith('Sa') else 'new',
                    number_of_chapters=1)
                for edition in (version, sim_version):
                    translation = bible.BookTranslation.objects.create(
                        version=edition, book=book, translation=name,
                        abbreviation=code if edition == sim_version else '')
                    bible.Verse.objects.create(
                        book_translation=translation, chapter=1, verse=1,
                        text=f'{edition.abbreviation} {name} ayat satu.')

        # a single-screen text: the whole body on one screen, shrunk to fit
        self.single_service = tatib.TataIbadah.objects.create(
            name='Ibadah Satu Layar', date=date(2026, 9, 13), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.single_service, order_number=1,
            kind=tatib.ServiceEntryKind.TEXT, default_screen_mode='single_screen', title='Doa',
            text='\n'.join(f'Baris {n} dari doa yang panjang ini.' for n in range(1, 30)))

        self.untitled_text_line = (
            'L : Marilah kita bangkit berdiri! Di dalam nama Allah Bapa, '
            'dan Tuhan Yesus Kristus, serta Roh Kudus, Pencipta langit dan bumi.')
        self.untitled_service = tatib.TataIbadah.objects.create(
            name='Ibadah Dua Teks', date=date(2026, 9, 20), is_active=True)
        for order in (1, 2):
            tatib.ServiceEntry.objects.create(
                tatib=self.untitled_service, order_number=order,
                kind=tatib.ServiceEntryKind.TEXT, title='', text=self.untitled_text_line)

        if self._testMethodName == 'test_missing_pdf_shows_quiet_icon_then_text_resumes':
            media = tatib.MediaIdentity.objects.create(
                sha256='d' * 64, byte_count=1024, family='pdf', display_filename='notes.pdf')
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=6, kind=tatib.ServiceEntryKind.MEDIA,
                media=media, media_filename='notes.pdf')
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=7, kind=tatib.ServiceEntryKind.TEXT,
                title='Closing', text='Amin')

        if self._testMethodName == 'test_the_project_group_stays_inside_the_pane':
            media = tatib.MediaIdentity.objects.create(
                sha256='e' * 64, byte_count=2048, family='image', display_filename='slide.png')
            tatib.ServiceEntry.objects.create(
                tatib=self.service, order_number=9, kind=tatib.ServiceEntryKind.MEDIA,
                media=media, media_filename='slide.png')

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
        return f'/projector?service={self.service.pk}'

    def _group_geometry(self, page):
        """The reading pane's own edges against the project group's (spec 141)."""
        return page.evaluate("""() => {
          const pane = document.querySelector('.read').getBoundingClientRect();
          const group = document.querySelector('[data-project-group]');
          const box = group.getBoundingClientRect();
          const control = group.querySelector('[data-project-window]');
          const head = document.querySelector('.read__head-top').getBoundingClientRect();
          return {paneLeft: pane.left, paneRight: pane.right, paneWidth: pane.width,
                  groupLeft: box.left, groupRight: box.right, groupWidth: box.width,
                  headHeight: head.height,
                  control: control ? getComputedStyle(control).display : null};
        }""")

    def _slides(self, page):
        return page.eval_on_selector_all(
            '.slide', 'els => els.map(e => ({slide: e.dataset.slide, kind: e.dataset.kind,'
                     ' active: e.classList.contains("is-active"),'
                     ' hidden: e.getAttribute("aria-hidden")}))')

    def test_missing_pdf_shows_quiet_icon_then_text_resumes(self):
        page = self._page(self._projector_url())
        for _ in range(5):
            page.keyboard.press('Control+ArrowRight')
        page.wait_for_function("document.querySelector('.screen.is-active').dataset.entry === '5'")
        media = page.locator('.screen.is-active')
        media.locator('.screen__pdf-missing').wait_for(state='visible')
        self.assertEqual(media.inner_text().strip(), '')
        page.keyboard.press('Control+ArrowRight')
        page.wait_for_function("document.querySelector('.screen.is-active').dataset.entry === '6'")
        self.assertIn('Amin', page.locator('.screen.is-active').inner_text())

    # --- only the words, on the product's dark palette ------------------------

    def test_the_screen_is_only_the_words_on_the_product_palette(self):
        page = self._page(self._projector_url())
        styles = page.evaluate("""() => {
          const body = getComputedStyle(document.body);
          const head = document.querySelector('.screen.is-active .screen__head');
          const line = document.querySelector('.screen.is-active .screen__line');
          return {background: body.backgroundColor, color: body.color,
                  face: body.fontFamily, weight: body.fontWeight,
                  buttons: document.querySelectorAll('button').length,
                  head: head ? getComputedStyle(head).color : null,
                  line: line ? getComputedStyle(line).color : null};
        }""")
        self.assertEqual(styles['background'], 'rgb(20, 19, 15)')   # the dark canvas, not black
        self.assertEqual(styles['color'], 'rgb(245, 243, 238)')     # the warm off-white ink
        self.assertIn('CMG Sans', styles['face'])          # the projector's own bundled face
        self.assertIn('Source Sans 3', styles['face'])     # then the display stack (spec 119)
        self.assertEqual(styles['weight'], '700')
        self.assertGreater(styles['buttons'], 0)            # quiet operator controls
        self.assertEqual(styles['head'], 'rgb(255, 209, 102)')      # the header, brighter still...
        self.assertEqual(styles['line'], styles['color'])           # ...from the words

        fit = page.evaluate("""() => {
          const lines = document.querySelector('.screen.is-active .screen__lines');
          const stage = document.querySelector('#projectorScreens');
          return {size: parseFloat(getComputedStyle(lines).fontSize),
                  fitsWidth: lines.scrollWidth <= stage.clientWidth + 1,
                  fitsHeight: lines.scrollHeight <= stage.clientHeight + 1};
        }""")
        self.assertTrue(fit['fitsWidth'], fit)
        self.assertTrue(fit['fitsHeight'], fit)
        self.assertLessEqual(fit['size'], 200)

        # The fitting must reach the words: the ink stays inside the screen's box.
        ink = page.evaluate("""() => {
          const stage = document.querySelector('#projectorScreens').getBoundingClientRect();
          const lines = document.querySelector('.screen.is-active .screen__lines');
          const range = document.createRange();
          range.selectNodeContents(lines);
          const rect = range.getBoundingClientRect();
          return {insetLeft: rect.left - stage.left, insetRight: stage.right - rect.right,
                  size: parseFloat(getComputedStyle(lines).fontSize)};
        }""")
        self.assertGreaterEqual(ink['insetLeft'], -1, ink)
        self.assertGreaterEqual(ink['insetRight'], -1, ink)

    def test_the_display_box_sits_inside_the_window(self):
        """A box that runs off the screen takes the fitted words with it.

        The projector page is standalone -- it loads tokens.css and projector.css, not the
        product's components.css -- so the design system's border-box reset did not reach
        it and `height: 100%; padding: 64px` resolved as content-box: a 928px box on an
        800px window, whose last 64px hung off the screen. The fitting measures the
        display's own box, so it fitted the words into space that was not there and the
        last line was cut, while every check that compared the ink against that box read
        green -- the box was the thing that was wrong.
        """
        page = self._page(self._projector_url())
        box = page.evaluate("""() => {
          const screen = document.getElementById('projectorScreen');
          const stage = screen.querySelector('.projector__screens').getBoundingClientRect();
          return {boxSizing: getComputedStyle(screen).boxSizing,
                  top: Math.round(stage.top), bottom: Math.round(stage.bottom),
                  viewport: window.innerHeight,
                  scrollHeight: document.documentElement.scrollHeight,
                  left: Math.round(stage.left), right: Math.round(stage.right),
                  width: window.innerWidth};
        }""")
        self.assertEqual(box['boxSizing'], 'border-box', box)
        self.assertGreaterEqual(box['top'], 0, box)
        self.assertLessEqual(box['bottom'], box['viewport'],
                             'the display box runs past the bottom of the window: %s' % box)
        self.assertGreaterEqual(box['left'], 0, box)
        self.assertLessEqual(box['right'], box['width'], box)
        self.assertLessEqual(box['scrollHeight'], box['viewport'],
                             'the display page scrolls: %s' % box)

    def test_the_header_and_the_words_sit_in_the_middle_of_the_screen(self):
        page = self._page(self._projector_url())
        page.keyboard.press('End')                        # the built-in blank after the last entry
        page.keyboard.press('ArrowLeft')                  # the passage, which has a header and a line
        page.wait_for_timeout(300)
        page.wait_for_function(
            "() => !!document.querySelector('.screen.is-active .screen__line')")
        centred = page.evaluate("""() => {
          const stage = document.querySelector('#projectorScreens').getBoundingClientRect();
          const active = document.querySelector('.screen.is-active');
          const head = active.querySelector('.screen__head');
          const lines = active.querySelector('.screen__lines');
          const text = (el) => {                // the TEXT's own box, not the block's
            const range = document.createRange();
            range.selectNodeContents(el);
            return range.getBoundingClientRect();
          };
          const headBox = head ? text(head) : null;
          const lineBox = text(lines);
          const linesBox = lines.getBoundingClientRect();
          const lastLine = Math.max.apply(null, [...lines.querySelectorAll('.screen__line')]
                                                   .map(p => text(p).bottom));
          return {stageCentreX: stage.left + stage.width / 2,
                  stageCentreY: stage.top + stage.height / 2,
                  headCentreX: headBox ? headBox.left + headBox.width / 2 : null,
                  lineCentreX: lineBox.left + lineBox.width / 2,
                  boxCentreY: ((head ? head.getBoundingClientRect().top : linesBox.top)
                               + linesBox.bottom) / 2,
                  inkCentreY: ((headBox ? headBox.top : lineBox.top) + lastLine) / 2};
        }""")
        self.assertAlmostEqual(centred['headCentreX'], centred['stageCentreX'], delta=2)
        self.assertAlmostEqual(centred['lineCentreX'], centred['stageCentreX'], delta=2)
        self.assertAlmostEqual(centred['boxCentreY'], centred['stageCentreY'], delta=1)
        # Spec 091 pins the header to the top while the words use the remaining area.
        self.assertLess(centred['inkCentreY'], centred['stageCentreY'])

    def test_moving_and_toggling_morph_rather_than_jump(self):
        page = self._page(self._projector_url())
        page.keyboard.press('ArrowRight')
        started = page.evaluate("""() => ({
          move: document.querySelector('#projectorScreens').dataset.move || '',
          entering: document.querySelector('.screen.is-active').getAnimations().length,
          leaving: !!document.querySelector('.screen.is-out')})""")
        self.assertEqual(started['move'], 'next')
        self.assertGreater(started['entering'], 0, 'the arriving screen must animate in')
        self.assertTrue(started['leaving'], 'and the one it replaces must animate out')

        page.keyboard.press('ArrowLeft')
        page.wait_for_timeout(60)
        self.assertEqual(page.get_attribute('#projectorScreens', 'data-move'), 'prev')
        back = page.evaluate("""() => document.querySelector('.screen.is-active')
          .getAnimations().map(a => a.animationName)""")
        self.assertIn('screenInBack', back)               # it comes back the way it went

        # turning the display off fades the words rather than blanking them instantly
        page.wait_for_timeout(400)
        self.assertIn('opacity', page.evaluate(
            "() => getComputedStyle(document.querySelector('.screen.is-active')).transitionProperty"))
        page.keyboard.press('Space')
        page.wait_for_timeout(60)
        self.assertLess(float(page.evaluate(
            "() => getComputedStyle(document.querySelector('.screen.is-active')).opacity")), 1.0)
        page.wait_for_timeout(400)
        self.assertEqual(page.evaluate(
            "() => getComputedStyle(document.querySelector('.screen.is-active')).opacity"), '0')

    def test_reduced_motion_makes_every_move_instant(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900},
                                           reduced_motion='reduce')
        page = self._page(self._projector_url(), context)
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(50)
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '1')   # it still moved
        self.assertEqual(page.evaluate(
            "() => [...document.querySelectorAll('.screen')]"
            ".reduce((n, s) => n + s.getAnimations().length, 0)"), 0)

    def test_the_keyboard_moves_and_turns_the_display_on_and_off(self):
        page = self._page(self._projector_url())
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(150)
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '1')
        self.assertIn('Tuhan adalah gembalaku', page.locator('.screen.is-active').inner_text())

        page.keyboard.press('ArrowLeft')
        page.wait_for_timeout(150)
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '0')
        self.assertIn('Mazmur 23', page.locator('.screen.is-active').inner_text())

        page.keyboard.press('Space')
        page.wait_for_timeout(400)                        # the words fade out over ~200ms
        self.assertEqual(page.get_attribute('body', 'data-showing'), 'false')
        self.assertEqual(page.locator('.screen:visible').count(), 0)
        page.keyboard.press('Space')
        page.wait_for_timeout(400)
        self.assertEqual(page.get_attribute('body', 'data-showing'), 'true')
        self.assertEqual(page.locator('.screen:visible').count(), 1)

    def test_quiet_controls_support_keyboard_and_mouse_jumps(self):
        page = self._page(self._projector_url())
        page.keyboard.press('Space')
        page.keyboard.press('Control+ArrowRight')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '3')
        page.keyboard.press('Control+ArrowRight')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '5')
        page.keyboard.press('Control+ArrowRight')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '6')
        page.keyboard.press('Shift+ArrowRight')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '8')
        page.keyboard.press('b')
        self.assertFalse(page.locator('#projectorFind').is_visible())
        page.keyboard.press('j')
        self.assertTrue(page.locator('#entry-list').is_visible())
        page.locator('#entry-list-search').fill('Salam')
        page.keyboard.press('Enter')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '3')
        page.keyboard.press('c')
        self.assertTrue(page.locator('body').evaluate("e => e.classList.contains('corner-hidden')"))
        page.mouse.move(100, 100)
        self.assertTrue(page.locator('body').evaluate("e => e.classList.contains('corner-hidden')"))
        page.keyboard.press('c')
        page.locator('.mouse-zone--next').click(position={'x': 100, 'y': 100})
        page.wait_for_function('document.fullscreenElement !== null')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '3')
        page.locator('.mouse-zone--next').click(position={'x': 100, 'y': 100})
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '4')
        page.locator('#cue-service').click()
        self.assertTrue(page.locator('#entry-list').is_visible())
        page.locator('.entry-list__item[data-entry-index="3"]').click()
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '6')

    def test_first_projection_click_only_enters_fullscreen_in_every_zone(self):
        page = self._page(self._projector_url())
        page.keyboard.press('ArrowRight')
        for zone in ('previous', 'display', 'next'):
            before = page.get_attribute('body', 'data-current-screen')
            showing = page.get_attribute('body', 'data-showing')
            page.locator('.mouse-zone--' + zone).click(position={'x': 40, 'y': 40})
            page.wait_for_function('document.fullscreenElement !== null')
            self.assertEqual(page.get_attribute('body', 'data-current-screen'), before)
            self.assertEqual(page.get_attribute('body', 'data-showing'), showing)
            page.evaluate('document.exitFullscreen()')
            page.wait_for_function('document.fullscreenElement === null')

    def test_overlays_intercept_projector_clicks(self):
        page = self._page(self._projector_url())
        page.locator('.keys').click()
        self.assertTrue(page.locator('body').evaluate("e => e.classList.contains('keys-open')"))
        before = page.get_attribute('body', 'data-current-screen')
        page.mouse.click(16, 200)
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), before)
        self.assertFalse(page.locator('body').evaluate("e => e.classList.contains('keys-open')"))
        page.locator('#cue-service').click()
        page.mouse.click(1200, 200)
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), before)
        self.assertFalse(page.locator('body').evaluate("e => e.classList.contains('entry-list-open')"))

    def test_open_popups_keep_hud_visible_and_goto_has_clear_click_overlay(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.clock.install()
        page.goto(self.live_server_url + self._projector_url())
        page.wait_for_load_state('networkidle')

        for key in ('j', 'g', 'k'):
            page.keyboard.press(key)
            page.clock.fast_forward(31_000)
            self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('controls-idle')"))
            self.assertEqual(page.locator('#corner-cue').evaluate('el => getComputedStyle(el).visibility'), 'visible')
            self.assertEqual(page.locator('.keys').evaluate('el => getComputedStyle(el).visibility'), 'visible')
            if key == 'g':
                dismiss = page.locator('#projectorFindDismiss')
                self.assertTrue(dismiss.is_visible())
                self.assertEqual(dismiss.evaluate('el => getComputedStyle(el).backgroundColor'), 'rgba(0, 0, 0, 0)')
                before = page.get_attribute('body', 'data-current-screen')
                page.mouse.click(1200, 200)
                self.assertTrue(page.locator('body').evaluate("el => el.classList.contains('find-closing')"))
                page.clock.fast_forward(200)
                self.assertFalse(page.locator('#projectorFind').is_visible())
                self.assertEqual(page.get_attribute('body', 'data-current-screen'), before)
            else:
                page.keyboard.press('Escape')
                page.clock.fast_forward(200)

    def test_goto_cycles_one_suggestion_through_all_reference_results(self):
        def add_songs():
            try:
                songbook = songs.Book.objects.get(short_name='KJ')
                for number in range(200, 240):
                    songs.Song.objects.create(book=songbook, number=number, title=f'Kidung {number}')
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(add_songs).result()
        page = self._page(self._projector_url())
        wait_for_goto(page)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('KJ 2')
        page.wait_for_function("document.querySelector('.projector-find__count').textContent === '1 / 40'")
        self.assertEqual(page.locator('.projector-find__row').count(), 1)
        self.assertIn('KJ 200', page.locator('.projector-find__suggestion').inner_text())
        for _ in range(35):
            page.keyboard.press('ArrowDown')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '36 / 40')
        self.assertIn('KJ 235', page.locator('.projector-find__suggestion').inner_text())
        self.assertEqual(page.locator('#projectorFindInput').input_value(), 'KJ 2')
        for _ in range(5):
            page.keyboard.press('ArrowDown')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '1 / 40')
        page.keyboard.press('ArrowUp')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '40 / 40')
        page.locator('#projectorFindInput').fill('unknown')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '0 / 0')

    def test_goto_bare_number_matches_substrings_across_books_in_tiers(self):
        def add_songs():
            try:
                kj = songs.Book.objects.get(short_name='KJ')
                nkb = songs.Book.objects.create(
                    name='Nyanyikanlah Kidung Baru', short_name='NKB', is_hymn_book=True)
                rows = [
                    (kj, 12, 'KJ exact'), (nkb, 12, 'NKB exact'),
                    (nkb, 120, 'Prefix 120'), (nkb, 121, 'Prefix 121'),
                ]
                rows.extend((nkb, number, f'Prefix {number}') for number in range(1200, 1214))
                rows.extend(((nkb, 212, 'Substring 212'), (nkb, 312, 'Substring 312')))
                for book, number, title in rows:
                    songs.Song.objects.create(book=book, number=number, title=title)
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(add_songs).result()

        page = self._page(self._projector_url())
        wait_for_goto(page)
        page.keyboard.press('g')
        field = page.locator('#projectorFindInput')
        field.fill('012')
        expected = ['KJ 12 KJ exact', 'NKB 12 NKB exact',
                    'NKB 120 Prefix 120', 'NKB 121 Prefix 121']
        expected.extend(f'NKB {number} Prefix {number}' for number in range(1200, 1214))
        expected.extend(['NKB 212 Substring 212', 'NKB 312 Substring 312'])
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / %d'" % len(expected))
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text().strip(), expected[0])
        seen = [expected[0]]
        for _ in range(len(expected) - 1):
            page.keyboard.press('ArrowDown')
            seen.append(page.locator('.projector-find__suggestion').inner_text().strip())
        self.assertEqual(seen, expected)
        self.assertEqual(page.locator('.projector-find__count').inner_text(),
                         f'{len(expected)} / {len(expected)}')
        self.assertEqual(field.input_value(), '012')
        page.keyboard.press('ArrowDown')
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text().strip(), expected[0])
        page.keyboard.press('ArrowUp')
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text().strip(), expected[-1])

        field.fill('KJ 12')
        page.wait_for_function("document.querySelector('.projector-find__count').textContent === '1 / 1'")
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text().strip(), 'KJ 12 KJ exact')
        field.fill('Ada Kuasa')
        page.wait_for_function("document.querySelector('.projector-find__count').textContent === '1 / 1'")
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text().strip(), 'KJ 152 Ada Kuasa')

    def test_goto_empty_result_and_overlay_dismissal(self):
        page = self._page(self._projector_url())
        page.route('**/lookup/**', lambda route: route.fulfill(
            status=200, content_type='application/json', body=json.dumps({'results': []})))
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('nothing')
        page.wait_for_function("document.querySelector('.projector-find__suggestion').textContent === 'No matching passage or song'")
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '0 / 0')
        self.assertTrue(page.locator('#projectorFindResults').is_disabled())
        page.keyboard.press('Enter')
        self.assertTrue(page.locator('#projectorFind').is_visible())
        page.locator('#projectorFindInput').fill('')
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text(), 'Start typing to find a match')
        page.locator('#projectorFindDismiss').click(position={'x': 1200, 'y': 200})
        page.locator('#projectorFind').wait_for(state='hidden')

    def test_goto_morph_blocks_clicks_during_close_and_survives_rapid_reopen(self):
        page = self._page(self._projector_url())
        page.clock.install()
        before = page.get_attribute('body', 'data-current-screen')
        page.keyboard.press('g')
        self.assertEqual(page.locator('#projectorFind').evaluate(
            'el => getComputedStyle(el).animationName'), 'projectorListIn')
        page.keyboard.press('Escape')
        self.assertTrue(page.locator('body').evaluate("el => el.classList.contains('find-closing')"))
        self.assertEqual(page.locator('#projectorFind').evaluate(
            'el => getComputedStyle(el).animationName'), 'projectorListOut')
        self.assertTrue(page.locator('#projectorFindDismiss').is_visible())
        page.mouse.click(1200, 200)
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), before)
        page.keyboard.press('g')
        self.assertTrue(page.locator('body').evaluate("el => el.classList.contains('find-open')"))
        self.assertTrue(page.locator('#projectorFindInput').evaluate('el => document.activeElement === el'))
        page.clock.fast_forward(250)
        self.assertTrue(page.locator('#projectorFind').is_visible())
        page.keyboard.press('Escape')
        page.clock.fast_forward(200)
        self.assertFalse(page.locator('#projectorFind').is_visible())
        self.assertFalse(page.locator('#projectorFindDismiss').is_visible())

    def test_goto_morph_is_skipped_for_reduced_motion(self):
        context = self.browser.new_context(reduced_motion='reduce')
        page = self._page(self._projector_url(), context=context)
        page.keyboard.press('g')
        self.assertEqual(page.locator('#projectorFind').evaluate(
            'el => getComputedStyle(el).animationName'), 'none')
        page.keyboard.press('Escape')
        page.locator('#projectorFind').wait_for(state='hidden')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('find-closing')"))


    def test_goto_click_opens_the_selected_suggestion(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('KJ 152')
        page.wait_for_function("document.querySelector('.projector-find__count').textContent === '1 / 1'")
        page.set_viewport_size({'width': 600, 'height': 400})
        self.assertTrue(page.locator('#projectorFind').evaluate("""el => {
          const box = el.getBoundingClientRect();
          return box.left >= 0 && box.right <= innerWidth && box.bottom <= innerHeight;
        }"""))
        page.locator('#projectorFindResults').click()
        page.locator('#projectorFind').wait_for(state='hidden')
        page.wait_for_function("document.querySelector('.projector-detour').classList.contains('is-active')")




    def test_goto_chapter_suggestion_opens_first_available_verse_by_enter_and_click(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        for method in ('Enter', 'click'):
            page.keyboard.press('g')
            page.locator('#projectorFindInput').fill('Mat 5')
            page.wait_for_function("document.querySelector('.projector-find__suggestion').textContent === 'Matius 5'")
            if method == 'Enter':
                page.keyboard.press('Enter')
            else:
                page.locator('#projectorFindResults').click()
            page.wait_for_function("document.querySelector('.projector-detour').classList.contains('is-active')")
            self.assertIn('Matius 5:1', page.locator('.projector-detour').inner_text())
            page.locator('#projectorFind').wait_for(state='hidden')
            page.keyboard.press('Escape')
            page.wait_for_function("!document.querySelector('.projector-detour').classList.contains('is-active')")

    def test_goto_accepts_tb_and_sim_book_abbreviations(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        query = page.locator('#projectorFindInput')
        for abbreviation, expected_name, edition in (
                ('Kej', 'Kejadian', 'TB'), ('1Mu', '1 Musa', 'SIM')):
            page.keyboard.press('g')
            query.fill(abbreviation + ' 1')
            page.wait_for_function(
                "document.querySelector('.projector-find__count').textContent === '1 / 1'")
            self.assertEqual(page.locator('.projector-find__suggestion').inner_text(),
                             expected_name + ' 1')
            page.keyboard.press('Enter')
            page.wait_for_function(
                "document.querySelector('.projector-detour').classList.contains('is-active')")
            self.assertIn(expected_name + ' 1:1', page.locator('.projector-detour').inner_text())
            self.assertEqual(page.locator('.cue-translation').inner_text(), edition)
            page.locator('#projectorFind').wait_for(state='hidden')
            page.keyboard.press('Escape')
            page.wait_for_function(
                "!document.querySelector('.projector-detour').classList.contains('is-active')")

        for abbreviation, expected_name, edition, chapter, reference in (
                ('Pah', 'Panguhum', 'SIM', '1', '1:1'),
                ('1Ta', '1 Tawarikh', 'TB', '2', '2:1')):
            page.keyboard.press('g')
            query.fill(abbreviation + ' ' + chapter)
            page.wait_for_function(
                "document.querySelector('.projector-find__count').textContent === '1 / 1'")
            self.assertEqual(page.locator('.projector-find__suggestion').inner_text(),
                             expected_name + ' ' + reference.split(':')[0])
            page.keyboard.press('Enter')
            page.wait_for_function(
                "document.querySelector('.projector-detour').classList.contains('is-active')")
            self.assertIn(expected_name + ' ' + reference, page.locator('.projector-detour').inner_text())
            self.assertEqual(page.locator('.cue-translation').inner_text(), edition)
            page.locator('#projectorFind').wait_for(state='hidden')
            page.keyboard.press('Escape')
            page.wait_for_function(
                "!document.querySelector('.projector-detour').classList.contains('is-active')")

        page.keyboard.press('g')
        query.fill('Pah 1:1')
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / 1'")
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text(),
                         'Panguhum 1:1')
        page.keyboard.press('Enter')
        page.wait_for_function(
            "document.querySelector('.projector-detour').classList.contains('is-active')")
        self.assertIn('Panguhum 1:1', page.locator('.projector-detour').inner_text())
        self.assertEqual(page.locator('.cue-translation').inner_text(), 'SIM')
        page.locator('#projectorFind').wait_for(state='hidden')

        page.keyboard.press('Escape')
        page.wait_for_function(
            "!document.querySelector('.projector-detour').classList.contains('is-active')")

        page.keyboard.press('g')
        query.fill('Pah 1:2')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '0 / 0')
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text(),
                         'No matching passage or song')
        page.keyboard.press('Escape')
        page.locator('#projectorFind').wait_for(state='hidden')

        page.keyboard.press('g')
        query.fill('Rut 1')
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / 2'")
        suggestion = page.locator('.projector-find__suggestion')
        self.assertEqual(suggestion.inner_text(), 'Rut 1 · TB')
        suffix = suggestion.locator('.projector-find__edition')
        self.assertEqual(suffix.inner_text().strip(), '· TB')
        self.assertEqual(suffix.evaluate('el => getComputedStyle(el).color'),
                         page.locator('.projector-find__count').evaluate(
                             'el => getComputedStyle(el).color'))
        page.keyboard.press('Enter')
        page.wait_for_function(
            "document.querySelector('.projector-detour').classList.contains('is-active')")
        self.assertEqual(page.locator('.cue-translation').inner_text(), 'TB')
        page.locator('.cue-translation').click()
        self.assertEqual(page.locator('.cue-translation').inner_text(), 'SIM')
        page.locator('.cue-translation').click()
        self.assertEqual(page.locator('.cue-translation').inner_text(), 'TB')
        page.locator('#projectorFind').wait_for(state='hidden')
        page.keyboard.press('Escape')
        page.wait_for_function(
            "!document.querySelector('.projector-detour').classList.contains('is-active')")

        page.keyboard.press('g')
        query.fill('Rut 1')
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / 2'")
        page.keyboard.press('ArrowDown')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '2 / 2')
        self.assertEqual(suggestion.inner_text(), 'Rut 1 · SIM')
        suffix = suggestion.locator('.projector-find__edition')
        self.assertEqual(suffix.inner_text().strip(), '· SIM')
        self.assertEqual(suffix.evaluate('el => getComputedStyle(el).color'),
                         page.locator('.projector-find__count').evaluate(
                             'el => getComputedStyle(el).color'))
        page.keyboard.press('Enter')
        page.wait_for_function(
            "document.querySelector('.projector-detour').classList.contains('is-active')")
        self.assertEqual(page.locator('.cue-translation').inner_text(), 'SIM')
        page.locator('#projectorFind').wait_for(state='hidden')

        page.keyboard.press('Escape')
        page.wait_for_function(
            "!document.querySelector('.projector-detour').classList.contains('is-active')")
        for name in ('1 Samuel', '2 Samuel', 'Markus', 'Lukas'):
            for index, edition in ((1, 'TB'), (2, 'SIM')):
                page.keyboard.press('g')
                query.fill(name + ' 1')
                page.wait_for_function(
                    "document.querySelector('.projector-find__count').textContent === '1 / 2'")
                if index == 2:
                    page.keyboard.press('ArrowDown')
                self.assertEqual(page.locator('.projector-find__count').inner_text(),
                                 f'{index} / 2')
                self.assertEqual(suggestion.inner_text(), f'{name} 1 · {edition}')
                page.keyboard.press('Enter')
                page.wait_for_function(
                    "document.querySelector('.projector-detour').classList.contains('is-active')")
                self.assertEqual(page.locator('.cue-translation').inner_text(), edition)
                page.locator('#projectorFind').wait_for(state='hidden')
                page.keyboard.press('Escape')
                page.wait_for_function(
                    "!document.querySelector('.projector-detour').classList.contains('is-active')")

    def test_goto_passage_translation_flip_brightens_the_label(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        highlight = 'rgb(232, 228, 220)'
        detour = page.locator('.projector-detour')
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('Mat 5')
        page.wait_for_function("document.querySelector('.projector-find__suggestion').textContent === 'Matius 5'")
        page.keyboard.press('Enter')
        page.wait_for_function("document.querySelector('.projector-detour').classList.contains('is-active')")
        page.locator('#projectorFind').wait_for(state='hidden')
        label = page.locator('.cue-translation')
        self.assertEqual(label.inner_text(), 'TB')

        page.keyboard.press('t')
        state = label.evaluate("""el => ({text: el.textContent, flash: el.classList.contains('flash'),
          color: getComputedStyle(el).color})""")
        self.assertEqual(state['text'], 'SIM')
        self.assertTrue(state['flash'])
        self.assertEqual(state['color'], highlight)
        self.assertIn('Mateus 5:1', detour.inner_text())
        self.assertIn('ayat 1 (SIM)', detour.inner_text())

        # flipping again during the hold toggles back and stays bright
        page.keyboard.press('t')
        self.assertEqual(label.inner_text(), 'TB')
        self.assertTrue(label.evaluate("el => el.classList.contains('flash')"))
        self.assertEqual(label.evaluate('el => getComputedStyle(el).color'), highlight)
        self.assertIn('Matius 5:1', detour.inner_text())
        page.wait_for_function(
            "!document.querySelector('.cue-translation').classList.contains('flash')", timeout=3000)
        page.wait_for_function(
            "getComputedStyle(document.querySelector('.cue-translation')).color === 'rgb(81, 77, 71)'")

        # the label click flips it too
        label.click()
        self.assertEqual(label.inner_text(), 'SIM')
        self.assertTrue(label.evaluate("el => el.classList.contains('flash')"))
        self.assertEqual(label.evaluate('el => getComputedStyle(el).color'), highlight)
        page.wait_for_function(
            "!document.querySelector('.cue-translation').classList.contains('flash')", timeout=3000)
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('.projector-detour').classList.contains('is-active')")

        # a single-edition verse neither flips nor brightens
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('Mzm 23')
        page.wait_for_function("document.querySelector('.projector-find__suggestion').textContent === 'Mazmur 23'")
        page.keyboard.press('Enter')
        page.wait_for_function("document.querySelector('.projector-detour').classList.contains('is-active')")
        page.locator('#projectorFind').wait_for(state='hidden')
        label = page.locator('.cue-translation')
        self.assertEqual(label.inner_text(), 'TB')
        page.keyboard.press('t')
        self.assertEqual(label.inner_text(), 'TB')
        self.assertFalse(label.evaluate("el => el.classList.contains('flash')"))
        self.assertIn('Mazmur 23:1', detour.inner_text())
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('.projector-detour').classList.contains('is-active')")

        # the service cue keeps its own flip and brighten through the shared helper
        page.mouse.move(0, 0)
        for _ in range(4):
            page.keyboard.press('Control+ArrowRight')
        label = page.locator('.cue-translation')
        self.assertEqual(label.inner_text(), 'TB')
        page.keyboard.press('t')
        self.assertEqual(label.inner_text(), 'SIM')
        page.wait_for_function(
            "getComputedStyle(document.querySelector('.cue-translation')).color === 'rgb(232, 228, 220)'")
        page.wait_for_function(
            "!document.querySelector('.cue-translation').classList.contains('flash')", timeout=3000)
        self.assertEqual(label.inner_text(), 'SIM')

    def test_projector_search_clear_controls_match_both_fields(self):
        page = self._page(self._projector_url())
        page.keyboard.press('j')
        service_search = page.locator('#entry-list-search')
        service_clear = page.locator('#entry-list-clear')
        self.assertFalse(service_clear.is_visible())
        service_search.fill('Salam')
        self.assertTrue(service_clear.is_visible())
        self.assertEqual(page.locator('.entry-list__item').count(), 1)
        service_clear.click()
        self.assertEqual(service_search.input_value(), '')
        self.assertTrue(service_search.evaluate('el => document.activeElement === el'))
        self.assertEqual(page.locator('.entry-list__item').count(), 5)
        self.assertFalse(service_clear.is_visible())
        service_search.fill('Salam')
        service_clear.focus()
        page.keyboard.press('Enter')
        self.assertEqual(service_search.input_value(), '')
        self.assertTrue(page.locator('#entry-list').is_visible())
        page.keyboard.press('Escape')

        page.keyboard.press('g')
        goto_search = page.locator('#projectorFindInput')
        goto_clear = page.locator('#projectorFindClear')
        self.assertFalse(goto_clear.is_visible())
        goto_search.fill('NKB 2')
        self.assertTrue(goto_clear.is_visible())
        goto_clear.click()
        self.assertEqual(goto_search.input_value(), '')
        self.assertTrue(goto_search.evaluate('el => document.activeElement === el'))
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text(), 'Start typing to find a match')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '0 / 0')
        self.assertFalse(goto_clear.is_visible())
        self.assertTrue(page.locator('#projectorFind').is_visible())

    def test_adjacent_untitled_text_cues_share_fit_limit_and_run_only_on_hover(self):
        full = self.untitled_text_line
        page = self._page(f'/projector?service={self.untitled_service.pk}')
        current = page.locator('#cue-prefix .cue-running')
        following = page.locator('#cue-next-name.cue-running')
        self.assertEqual(current.count(), 1)
        self.assertEqual(following.count(), 1)
        self.assertEqual(page.locator('#corner-cue').evaluate(
            'el => getComputedStyle(el).fontWeight'), '550')
        self.assertEqual(current.evaluate('el => getComputedStyle(el).color'), 'rgb(81, 77, 71)')
        self.assertEqual(following.evaluate('el => getComputedStyle(el).color'), 'rgb(81, 77, 71)')
        self.assertEqual(page.locator('#cue-progress').evaluate(
            'el => getComputedStyle(el).color'), 'rgb(232, 228, 220)')
        page.locator('#cue-next').evaluate('el => el.classList.add("on")')
        page.wait_for_function("getComputedStyle(document.querySelector('#cue-next-name')).color === 'rgb(232, 228, 220)'")
        self.assertEqual(following.evaluate('el => getComputedStyle(el).color'), 'rgb(232, 228, 220)')
        page.locator('#cue-next').evaluate('el => el.classList.remove("on")')
        self.assertEqual(page.locator('.entry-list__item').count(), 2)
        self.assertGreater(len(full), 50)
        for width in (1440, 900, 600, 375):
            page.set_viewport_size({'width': width, 'height': 700})
            page.evaluate("window.dispatchEvent(new Event('resize'))")
            limit = int(page.locator('#corner-cue').get_attribute('data-running-limit'))
            self.assertLessEqual(limit, 50)
            self.assertGreaterEqual(limit, 1)
            for node in (current, following):
                self.assertEqual(node.locator('.cue-running__still').inner_text(),
                                 full[:limit] + '…')
                self.assertFalse(node.get_attribute('title'))
            self.assertTrue(page.evaluate("""() => {
              const next = document.querySelector('#cue-next').getBoundingClientRect();
              const keys = document.querySelector('.keys').getBoundingClientRect();
              return keys.left - next.right >= innerWidth * .1 - 1;
            }"""))
        page.set_viewport_size({'width': 1440, 'height': 700})
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        self.assertEqual(page.locator('#corner-cue').get_attribute('data-running-limit'), '50')
        before = page.locator('#cue-progress').bounding_box()['x']
        current.hover()
        page.wait_for_function("getComputedStyle(document.querySelector('#cue-prefix .cue-running')).color === 'rgb(129, 125, 116)'")
        self.assertEqual(current.evaluate('el => getComputedStyle(el).color'), 'rgb(129, 125, 116)')
        self.assertTrue(current.evaluate("el => el.classList.contains('is-running')"))
        self.assertTrue(current.locator('.cue-running__moving').evaluate(
            "el => el.getAnimations()[0].effect.getTiming().iterations === Infinity"))
        self.assertEqual(page.locator('#cue-progress').bounding_box()['x'], before)
        self.assertFalse(following.evaluate("el => el.classList.contains('is-running')"))
        page.mouse.move(700, 300)
        self.assertFalse(current.evaluate("el => el.classList.contains('is-running')"))
        page.keyboard.press('j')
        self.assertIn(full, page.locator('#entry-list-results').inner_text())

    def test_running_cue_respects_reduced_motion(self):
        context = self.browser.new_context(
            viewport={'width': 600, 'height': 700}, reduced_motion='reduce')
        page = self._page(
            f'/projector?service={self.untitled_service.pk}',
            context=context)
        current = page.locator('#cue-prefix .cue-running')
        current.hover()
        self.assertFalse(current.evaluate("el => el.classList.contains('is-running')"))
        self.assertEqual(current.locator('.cue-running__moving').evaluate(
            'el => getComputedStyle(el).display'), 'none')

    def test_corner_controls_share_rest_hover_and_highlight_colors(self):
        page = self._page(self._projector_url())
        color = lambda selector: page.locator(selector).evaluate(
            'el => getComputedStyle(el).color')
        rest, hover, highlight = 'rgb(81, 77, 71)', 'rgb(129, 125, 116)', 'rgb(232, 228, 220)'
        self.assertEqual(color('#corner-cue'), rest)
        self.assertEqual(color('#cue-service'), rest)
        self.assertEqual(color('#cue-next'), rest)
        self.assertEqual(color('.keys'), rest)
        self.assertEqual(color('#cue-progress'), highlight)

        page.locator('#cue-next').hover()
        page.wait_for_function("getComputedStyle(document.querySelector('#cue-next')).color === 'rgb(129, 125, 116)'")
        self.assertEqual(color('#cue-next'), hover)
        page.locator('#cue-service').hover()
        page.wait_for_function("getComputedStyle(document.querySelector('#cue-service')).color === 'rgb(129, 125, 116)'")
        self.assertEqual(color('#cue-service'), hover)
        page.locator('#cue-service').click()
        page.wait_for_function("getComputedStyle(document.querySelector('#cue-service')).color === 'rgb(232, 228, 220)'")
        self.assertEqual(color('#cue-service'), highlight)
        page.keyboard.press('Escape')

        page.locator('.keys').hover()
        page.wait_for_function("getComputedStyle(document.querySelector('.keys')).color === 'rgb(129, 125, 116)'")
        self.assertEqual(color('.keys'), hover)
        self.assertEqual(page.locator('.keys').evaluate(
            'el => getComputedStyle(el).backgroundColor'), 'rgba(0, 0, 0, 0)')
        page.locator('.keys').click()
        page.wait_for_function("getComputedStyle(document.querySelector('.keys')).color === 'rgb(232, 228, 220)'")
        self.assertEqual(color('.keys'), highlight)
        self.assertEqual(page.locator('.keys').evaluate(
            'el => getComputedStyle(el).backgroundColor'), 'rgba(0, 0, 0, 0)')
        page.keyboard.press('Escape')

        for _ in range(3):
            page.keyboard.press('Control+ArrowRight')
        baits = page.locator('.cue-bait')
        self.assertGreater(baits.count(), 1)
        self.assertEqual(color('.cue-bait[aria-pressed="false"]'), rest)
        self.assertEqual(color('.cue-bait[aria-pressed="true"]'), highlight)
        baits.last.hover()
        page.wait_for_function("getComputedStyle(document.querySelector('.cue-bait[aria-pressed=\"false\"]')).color === 'rgb(129, 125, 116)'")
        self.assertEqual(color('.cue-bait[aria-pressed="false"]'), hover)
        page.locator('.cue-bait[aria-pressed="true"]').hover()
        self.assertEqual(color('.cue-bait[aria-pressed="true"]'), highlight)

        page.keyboard.press('Control+ArrowRight')
        translation = page.locator('.cue-translation')
        self.assertEqual(translation.count(), 1)
        self.assertEqual(color('.cue-translation'), rest)
        translation.hover()
        page.wait_for_function("getComputedStyle(document.querySelector('.cue-translation')).color === 'rgb(129, 125, 116)'")
        self.assertEqual(color('.cue-translation'), hover)
        translation.evaluate('el => el.classList.add("flash")')
        page.wait_for_function("getComputedStyle(document.querySelector('.cue-translation')).color === 'rgb(232, 228, 220)'")
        self.assertEqual(color('.cue-translation'), highlight)

    def test_goto_clear_ignores_pending_lookup(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('KJ 152')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '1 / 1')
        page.locator('#projectorFindClear').click()
        self.assertEqual(page.locator('.projector-find__suggestion').inner_text(), 'Start typing to find a match')
        self.assertEqual(page.locator('.projector-find__count').inner_text(), '0 / 0')

    def test_escape_closes_both_hud_layers_without_a_lingering_focus_ring(self):
        page = self._page(self._projector_url())
        for selector, open_class in (('#cue-service', 'entry-list-open'), ('.keys', 'keys-open')):
            button = page.locator(selector)
            button.click()
            page.mouse.move(700, 100)
            page.keyboard.press('Escape')
            self.assertFalse(page.locator('body').evaluate(
                '(body, name) => body.classList.contains(name)', open_class))
            self.assertFalse(button.evaluate("el => el.matches(':focus-visible')"))
            self.assertEqual(button.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')
            page.wait_for_function("!document.body.classList.contains('keys-closing') && !document.body.classList.contains('entry-list-closing')")
            page.locator('#cue-service').focus()
            page.keyboard.press('Tab')
            self.assertTrue(page.evaluate("document.activeElement.matches(':focus-visible')"))

    def test_mouse_closed_hud_layers_do_not_show_focus_ring_on_arrow_navigation(self):
        for selector in ('#cue-service', '.keys'):
            with self.subTest(selector=selector):
                page = self._page(self._projector_url())
                button = page.locator(selector)
                button.click()
                if selector == '#cue-service':
                    page.locator('#entry-list-dismiss').click(position={'x': 1200, 'y': 200})
                else:
                    page.mouse.click(16, 200)
                before = page.get_attribute('body', 'data-current-screen')
                page.keyboard.press('ArrowRight')
                self.assertNotEqual(page.get_attribute('body', 'data-current-screen'), before)
                self.assertFalse(button.evaluate("el => el.matches(':focus-visible')"))
                self.assertEqual(button.evaluate('el => getComputedStyle(el).outlineStyle'), 'none')

    def test_f_and_k_toggle_fullscreen_and_shortcut_sheet(self):
        page = self._page(self._projector_url())
        page.keyboard.press('k')
        self.assertTrue(page.locator('body').evaluate("el => el.classList.contains('keys-open')"))
        page.keyboard.press('k')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('keys-open')"))
        page.keyboard.press('f')
        page.wait_for_function('document.fullscreenElement !== null')
        page.keyboard.press('f')
        page.wait_for_function('document.fullscreenElement === null')
        page.keyboard.press('g')
        page.locator('#projectorFindInput').click()
        page.keyboard.type('kf')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('keys-open')"))
        self.assertIsNone(page.evaluate('document.fullscreenElement'))

    def test_service_list_search_and_arrow_navigation_share_one_picker(self):
        page = self._page(self._projector_url())
        page.keyboard.press('j')
        self.assertTrue(page.locator('#entry-list').is_visible())
        self.assertFalse(page.locator('#projectorFind').is_visible())
        search = page.locator('#entry-list-search')
        self.assertTrue(search.evaluate('el => document.activeElement === el'))
        self.assertEqual(page.locator('.entry-list__item').count(), 5)
        page.keyboard.press('ArrowDown')
        styles = page.locator('#entry-list').evaluate("""list => {
          const current = list.querySelector('[aria-current="true"]');
          const selected = list.querySelector('[data-active="true"]');
          return {current: getComputedStyle(current).backgroundColor,
                  selected: getComputedStyle(selected).backgroundColor,
                  currentMarker: getComputedStyle(current).boxShadow};
        }""")
        self.assertNotEqual(styles['current'], styles['selected'])
        self.assertNotEqual(styles['currentMarker'], 'none')
        search.fill('bait 1')
        self.assertEqual(page.locator('.entry-list__item').count(), 1)
        search.fill('Salam')
        self.assertEqual(page.locator('.entry-list__item').count(), 1)
        self.assertEqual(page.locator('.entry-list__item[data-active="true"]').get_attribute('data-entry-index'), '1')
        page.keyboard.press('Enter')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '3')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('entry-list-open')"))

        page.locator('#cue-service').click()
        search.fill('')
        page.keyboard.press('ArrowDown')
        self.assertEqual(page.locator('.entry-list__item[data-active="true"]').get_attribute('data-entry-index'), '2')
        page.keyboard.press('Enter')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), '5')

        page.keyboard.press('j')
        search.fill('no matching entry')
        self.assertEqual(page.locator('.entry-list__item').count(), 0)
        self.assertTrue(page.locator('.entry-list__empty').is_visible())
        page.keyboard.press('Escape')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('entry-list-open')"))
        page.keyboard.press('j')
        page.keyboard.press('Backspace')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('entry-list-open')"))
        page.keyboard.press('g')
        self.assertTrue(page.locator('#projectorFind').is_visible())

    def test_service_list_arrow_navigation_reaches_both_scroll_ends(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 280})
        page = self._page(self._projector_url(), context)
        page.keyboard.press('j')
        for _ in range(2):
            page.keyboard.press('ArrowDown')
        middle = page.locator('#entry-list').evaluate("""list => {
          const row = list.querySelector('[data-active="true"]').getBoundingClientRect();
          const header = list.querySelector('.entry-list__header').getBoundingClientRect();
          const panel = list.getBoundingClientRect();
          return {rowTop: row.top, rowBottom: row.bottom, headerBottom: header.bottom,
                  panelBottom: panel.bottom, rowCenter: (row.top + row.bottom) / 2,
                  visibleCenter: (header.bottom + panel.bottom) / 2};
        }""")
        self.assertGreaterEqual(middle['rowTop'] + 1, middle['headerBottom'])
        self.assertLessEqual(middle['rowBottom'], middle['panelBottom'] + 1)
        self.assertAlmostEqual(middle['rowCenter'], middle['visibleCenter'], delta=2)
        for _ in range(2):
            page.keyboard.press('ArrowDown')
        end = page.locator('#entry-list').evaluate("""list => {
          const row = list.querySelector('[data-active="true"]').getBoundingClientRect();
          const panel = list.getBoundingClientRect();
          return {rowBottom: row.bottom, panelBottom: panel.bottom,
                  scrollTop: list.scrollTop, maxScroll: list.scrollHeight - list.clientHeight};
        }""")
        self.assertLessEqual(end['rowBottom'], end['panelBottom'])
        self.assertAlmostEqual(end['scrollTop'], end['maxScroll'], delta=1)
        for _ in range(4):
            page.keyboard.press('ArrowUp')
        start = page.locator('#entry-list').evaluate("""list => ({
          rowTop: list.querySelector('[data-active="true"]').getBoundingClientRect().top,
          headerBottom: list.querySelector('.entry-list__header').getBoundingClientRect().bottom,
          scrollTop: list.scrollTop
        })""")
        self.assertGreaterEqual(start['rowTop'] + 1, start['headerBottom'])
        self.assertAlmostEqual(start['scrollTop'], 0, delta=1)

    def test_corner_cue_parts_share_the_bottom_band_vertical_center(self):
        for width, height in ((1366, 768), (1920, 1080)):
            context = self.browser.new_context(viewport={'width': width, 'height': height})
            page = self._page(self._projector_url(), context)
            centers = page.evaluate("""() => {
              const mid = selector => {
                const rect = document.querySelector(selector).getBoundingClientRect();
                return rect.top + rect.height / 2;
              };
              return {
                cue: mid('#corner-cue'), list: mid('#cue-service'),
                dot: mid('.cue-separator'), prefix: mid('#cue-prefix'),
                progress: mid('#cue-progress'), next: mid('#cue-next'), keys: mid('.keys')
              };
            }""")
            expected = height - 32
            for part, center in centers.items():
                self.assertAlmostEqual(center, expected, delta=0.5, msg=(part, centers))
            page.close()
            context.close()

    def test_every_kind_takes_the_shape_it_should_on_screen(self):
        """The running order, screen by screen: content, then a built-in blank after
        each entry and after each song verse. A stored break is still one blank."""
        page = self._page(self._projector_url())
        shape = page.eval_on_selector_all('.screen[data-screen]', """els => els.map(e => ({
          blank: e.classList.contains('is-blank'),
          head: (e.querySelector('.screen__head') || {}).textContent || null,
          lines: [...e.querySelectorAll('.screen__line')].map(p => p.textContent)}))""")
        self.assertEqual([s['blank'] for s in shape],
                         [False, False, True, False, True, True, False, True, False, True, False, True])
        self.assertEqual(shape[0]['head'], 'Nas')        # a legacy row takes the same shape
        self.assertEqual(shape[0]['lines'], ['Mazmur 23'])
        self.assertEqual(shape[1]['lines'], ['Tuhan adalah gembalaku, takkan kekurangan aku.'])
        self.assertEqual(shape[3]['head'], 'Salam')      # a text keeps its own header
        self.assertEqual(shape[3]['lines'], ['Kasih karunia Tuhan beserta kita semua'])
        self.assertIsNone(shape[5]['head'])              # the stored break, after the text's blank
        self.assertEqual(shape[5]['lines'], [])
        self.assertIsNone(shape[6]['head'])              # a song is its lyrics alone
        self.assertEqual(shape[6]['lines'], ['bait 1'])
        self.assertEqual(shape[8]['lines'], ['bait 2'])
        self.assertEqual(shape[10]['head'], 'Matius 5:3')  # a passage names the verse it shows
        self.assertEqual(shape[10]['lines'], ['ayat 3'])

    def test_a_body_too_long_for_the_screen_comes_down_to_fit(self):
        page = self._page(f'/projector?service={self.long_service.pk}')
        fitted = page.evaluate("""() => {
          const stage = document.querySelector('#projectorScreens').getBoundingClientRect();
          const active = document.querySelector('.screen.is-active');
          const lines = active.querySelector('.screen__lines');
          const head = active.querySelector('.screen__head');
          const range = document.createRange();
          range.selectNodeContents(lines);
          const rect = range.getBoundingClientRect();
          return {size: parseFloat(getComputedStyle(lines).fontSize),
                  insideTop: rect.top - stage.top, insideBottom: stage.bottom - rect.bottom,
                  insideLeft: rect.left - stage.left, insideRight: stage.right - rect.right,
                  winBottom: window.innerHeight - rect.bottom,
                  winTop: rect.top, winLeft: rect.left,
                  winRight: window.innerWidth - rect.right,
                  head: head ? head.textContent : ''};
        }""")
        self.assertLess(fitted['size'], 100)              # it came down to fit
        self.assertGreaterEqual(fitted['insideTop'], -1, fitted)
        self.assertGreaterEqual(fitted['insideBottom'], -1, fitted)
        self.assertGreaterEqual(fitted['insideLeft'], -1, fitted)
        self.assertGreaterEqual(fitted['insideRight'], -1, fitted)
        # and inside the WINDOW, not merely inside the box the fitting measured: the box
        # itself sat 64px past the bottom of the screen, and the words went with it
        self.assertGreaterEqual(fitted['winTop'], 0, fitted)
        self.assertGreaterEqual(fitted['winBottom'], 0, fitted)
        self.assertGreaterEqual(fitted['winLeft'], 0, fitted)
        self.assertGreaterEqual(fitted['winRight'], 0, fitted)
        self.assertIn('Mazmur 23:1', fitted['head'])      # the reference still heads it

        # ...and as LARGE as it can be: one pixel more must not fit
        maximal = page.evaluate("""() => {
          const stage = document.querySelector('#projectorScreens');
          const box = stage.getBoundingClientRect();
          const active = document.querySelector('.screen.is-active');
          const lines = active.querySelector('.screen__lines');
          const head = active.querySelector('.screen__head');
          const size = parseFloat(getComputedStyle(lines).fontSize);
          const range = document.createRange();
          const fits = (px) => {                 // the same question the fitting asks
            lines.style.fontSize = px + 'px';
            range.selectNodeContents(lines);
            const ink = range.getBoundingClientRect();
            return (lines.scrollHeight <= stage.clientHeight
                                             - (head ? head.offsetHeight : 0) - 8
                    && ink.top >= box.top + 4 && ink.bottom <= box.bottom - 4
                    && ink.left >= box.left - 1 && ink.right <= box.right + 2);
          };
          const chosen = fits(size);
          const oneLarger = fits(size + 1);
          lines.style.fontSize = size + 'px';    // leave it as it was
          return {size: size, chosen: chosen, oneLarger: oneLarger};
        }""")
        self.assertTrue(maximal['chosen'], maximal)      # the size it chose fits
        self.assertFalse(maximal['oneLarger'], maximal)  # and nothing larger does

        # a body longer than any screen must still come down until it fits, not stop at
        # a floor and run off the bottom
        huge = page.evaluate("""() => {
          const line = document.querySelector('.screen.is-active .screen__line');
          line.textContent = 'Tuhan adalah gembalaku, takkan kekurangan aku. '.repeat(300);
          window.dispatchEvent(new Event('resize'));
          const stage = document.querySelector('#projectorScreens').getBoundingClientRect();
          const lines = document.querySelector('.screen.is-active .screen__lines');
          const range = document.createRange();
          range.selectNodeContents(lines);
          const rect = range.getBoundingClientRect();
          return {size: parseFloat(getComputedStyle(lines).fontSize),
                  above: rect.top - stage.top, below: stage.bottom - rect.bottom,
                  stageHeight: Math.round(stage.height)};
        }""")
        self.assertGreaterEqual(huge['above'], -1, huge)
        self.assertGreaterEqual(huge['below'], -1, huge)

    def test_a_gap_opens_between_the_words_own_lines(self):
        """A screen's own lines get air between them; a wrapped row does not.

        The line-height alone cannot say this: it spaces every row of a wrapped line, so
        two lines of a text entry read as one continuous column.
        """
        page = self._page(self._projector_url())
        measured = page.evaluate("""() => {
          const active = document.querySelector('.screen.is-active');
          const lines = active.querySelector('.screen__lines');
          const range = document.createRange();
          const size = () => parseFloat(getComputedStyle(lines).fontSize);
          const fit = () => window.dispatchEvent(new Event('resize'));

          lines.innerHTML = '<p class="screen__line">'
                          + 'Tuhan adalah gembalaku. '.repeat(6) + '</p>';
          fit();
          const single = (() => {                     // one line, wrapped over its rows
            range.selectNodeContents(lines.querySelector('.screen__line'));
            const ink = range.getBoundingClientRect().height;
            const rows = Math.round(ink / (size() * 1.37));
            return {pitch: ink / rows, size: size(), rows: rows};
          })();

          lines.innerHTML = '<p class="screen__line">Kasih sayang-Mu perlindunganku</p>'
                          + '<p class="screen__line">Di bawah naungan sayap-Mu</p>';
          fit();
          const all = lines.querySelectorAll('.screen__line');
          const first = all[0].getBoundingClientRect();
          const second = all[1].getBoundingClientRect();
          const pair = {gap: second.top - first.bottom, pitch: second.top - first.top,
                        size: size()};

          // the air between the lines is part of what the fitting measures
          const stage = document.getElementById('projectorScreens').getBoundingClientRect();
          range.selectNodeContents(lines);
          const ink = range.getBoundingClientRect();
          return {single: single, pair: pair,
                  insideWindow: ink.top >= stage.top - 1 && ink.bottom <= stage.bottom + 1};
        }""")
        single, pair = measured['single'], measured['pair']
        # a wrapped row is spaced by the line-height and nothing more -- and the ink's own
        # box is the glyphs', a shade shorter than the line box, so it comes in just under
        self.assertLessEqual(single['pitch'], single['size'] * 1.37 + 1, measured)
        self.assertGreater(single['pitch'], single['size'] * 1.25, measured)
        # ... while the words' own lines get extra air between them ...
        self.assertGreater(pair['gap'], pair['size'] * 0.25, measured)
        # ... so a screen of them is roomier than the same rows merely wrapped
        self.assertGreater(pair['pitch'], single['pitch'] + pair['size'] * 0.25, measured)
        self.assertTrue(measured['insideWindow'], measured)

    def test_a_single_screen_text_fits_its_whole_body_on_one_screen(self):
        # Naming the service in the URL is an act of projection (spec 119): the
        # page boots showing screen 1, so nothing has to be switched on.
        page = self._page(f'/projector?service={self.single_service.pk}')
        page.wait_for_selector('.screen.is-active')
        page.wait_for_timeout(200)
        measured = page.evaluate("""() => {
          const screens = document.querySelectorAll('.screen[data-screen]');
          const active = document.querySelector('.screen.is-active');
          const stage = document.getElementById('projectorScreens').getBoundingClientRect();
          const lines = active.querySelector('.screen__lines');
          const range = document.createRange();
          range.selectNodeContents(lines);
          const ink = range.getBoundingClientRect();
          return {count: screens.length,
                  content: [...screens].filter(s => !s.classList.contains('is-blank')).length,
                  fit: active.dataset.fit,
                  fontSize: parseFloat(getComputedStyle(lines).fontSize),
                  inside: ink.top >= stage.top - 1 && ink.bottom <= stage.bottom + 1,
                  text: lines.innerText};
        }""")
        page.close()
        self.assertEqual(measured['content'], 1)               # the whole body, one content screen
        self.assertEqual(measured['count'], 2)                 # then the built-in blank
        self.assertEqual(measured['fit'], 'single')
        self.assertLess(measured['fontSize'], 100)             # the font shrank to fit
        self.assertIn('Baris 1 ', measured['text'])
        self.assertIn('Baris 29 ', measured['text'])           # nothing dropped while it fits
        self.assertTrue(measured['inside'], measured)

    # --- the button, its two states, and the lock across tabs ----------------

    def test_project_action_uses_primary_then_danger_treatment_in_both_themes(self):
        page = self._page(reverse('web-home'))
        page.locator('.rail [data-panel="tatib"]').click()
        page.locator(f'#panelBody .book[data-name="{self.service.pk}"]').click()
        page.wait_for_selector('[data-project-open]')

        def colors():
            return page.evaluate("""() => {
              const group = document.querySelector('[data-project-group]');
              const action = group.querySelector('[data-project-open]');
              const css = getComputedStyle(action);
              const tokenColor = property => {
                const probe = document.createElement('span');
                probe.style.color = `var(${property})`;
                document.body.appendChild(probe);
                const value = getComputedStyle(probe).color;
                probe.remove();
                return value;
              };
              const tokenBackground = property => {
                const probe = document.createElement('span');
                probe.style.backgroundColor = `var(${property})`;
                document.body.appendChild(probe);
                const value = getComputedStyle(probe).backgroundColor;
                probe.remove();
                return value;
              };
              return {displaying: group.dataset.displaying, background: css.backgroundColor,
                color: css.color, border: css.borderTopColor,
                primary: tokenBackground('--active-bg'), primaryInk: tokenColor('--active-ink'),
                danger: tokenColor('--danger')};
            }""")

        def wait_for_state(expected_state):
            page.wait_for_function(
                "expected => document.querySelector('[data-project-group]')"
                ".dataset.displaying === expected",
                arg=expected_state)

        for theme in ('light', 'dark'):
            if theme == 'dark':
                page.locator('#themeBtn').click()
            wait_for_state('false')
            page.mouse.move(1400, 850)
            page.wait_for_timeout(400)
            idle = colors()
            self.assertEqual(idle['displaying'], 'false')
            self.assertEqual(idle['background'], idle['primary'], idle)
            self.assertEqual(idle['color'], idle['primaryInk'], idle)
            with page.expect_popup() as popup_info:
                page.locator('[data-project-open]').click()
            popup = popup_info.value
            page.mouse.move(1400, 850)
            page.wait_for_timeout(400)
            active = colors()
            self.assertEqual(active['displaying'], 'true')
            self.assertEqual(active['color'], active['danger'])
            self.assertEqual(active['border'], active['danger'])
            page.locator('[data-project-open]').click()
            popup.close()

    def test_project_button_opens_the_display_and_editing_stays_available(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())

        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        self.assertIn(self._projector_url(), projector.url)

        # the button now offers the way out
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())

        # a second TAB of the same browser is already in display mode
        tab = self._page(self._service_url(), context)
        self.assertIn('Stop projecting', tab.locator('[data-project-open]').inner_text())
        self.assertEqual(tab.get_attribute('[data-project-group]', 'data-displaying'), 'true')

        # spec 026: an entry write is NOT declined while projecting -- the modal opens in
        # both tabs of the projecting browser
        for other in (page, tab):
            other.locator('.tatib__item').first.hover()
            other.wait_for_timeout(200)
            other.locator('[data-entry-open="text"]').first.click()
            other.wait_for_selector('dialog[open]')
            other.keyboard.press('Escape')
            other.wait_for_function("!document.querySelector('dialog[open]')")

        # the Tata Ibadah's OWN fields stay editable too
        edit = page.locator('.row-edit[data-editor-open="tatib"]').first
        edit.locator('xpath=..').hover()          # the sidebar reveals it on its row
        page.wait_for_timeout(250)
        edit.click()
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('dialog[open]')")

        # a second BROWSER is another laptop: its own state
        alone = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        laptop = self._page(self._service_url(), alone)
        self.assertIn('Project', laptop.locator('[data-project-open]').inner_text())
        self.assertEqual(laptop.get_attribute('[data-project-group]', 'data-displaying'), 'false')
        laptop.locator('.tatib__item').first.hover()
        laptop.wait_for_timeout(200)
        laptop.locator('[data-entry-open="text"]').first.click()
        laptop.wait_for_selector('dialog[open]')          # it may still prepare its service
        laptop.keyboard.press('Escape')

        # stopping from the app ends the display everywhere in this browser
        page.click('[data-project-open]')                 # Stop projecting
        page.wait_for_timeout(300)
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())
        self.assertIn('Project', tab.locator('[data-project-open]').inner_text())

    def test_the_toggle_in_the_projector_stops_it_for_the_whole_browser(self):
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())

        projector.keyboard.press('Space')                 # hide from the display itself
        page.wait_for_timeout(400)
        self.assertEqual(projector.get_attribute('body', 'data-showing'), 'false')
        self.assertEqual(page.get_attribute('[data-project-group]', 'data-displaying'), 'false')
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())

    def test_closing_the_projector_window_leaves_the_display_alone(self):
        """Spec 119: no beat and no reaper — a closed projector ends nothing.

        The display is browser-local state: closing one window, or every window, must
        not touch it. Only the release verb ends a display.
        """
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        tab = self._page(self._service_url(), context)         # another tab, same browser
        for other in (page, tab):
            self.assertEqual(other.get_attribute('[data-project-group]', 'data-displaying'),
                             'true')

        projector.close()
        page.wait_for_timeout(1500)                            # well past any old reaper

        for other in (page, tab):
            self.assertEqual(other.get_attribute('[data-project-group]', 'data-displaying'),
                             'true')
            self.assertIn('Stop projecting', other.locator('[data-project-open]').inner_text())
        state = page.evaluate(
            "() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")
        self.assertIsNotNone(state)
        self.assertTrue(state['on'])

        # editing is available with or without a window (spec 026)
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(200)
        page.locator('[data-entry-open="text"]').first.click()
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')

    # --- reopening the window while the service is on air (spec 141) ---------

    def test_the_reopen_control_appears_only_while_the_service_is_on_air(self):
        """Spec 141: the control is the way back to a closed projector window, so it
        exists exactly when this page's service is the live one and the words are up."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        self.assertFalse(page.locator('[data-project-window]').is_visible(),
                         'the reopen control is drawn while nothing is on air')

        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')

        control = page.locator('[data-project-window]')
        self.assertTrue(control.is_visible(), 'the control is missing while on air')
        self.assertEqual(control.get_attribute('aria-label'), 'Open projector window')
        self.assertEqual(control.get_attribute('title'), 'Open projector window')

        # a second tab hears the state and draws it too
        tab = self._page(self._service_url(), context)
        self.assertTrue(tab.locator('[data-project-window]').is_visible())

        # hidden: the words are off, so the way back is not offered
        projector.keyboard.press('Space')
        page.wait_for_timeout(600)
        self.assertFalse(page.locator('[data-project-window]').is_visible())
        self.assertFalse(tab.locator('[data-project-window]').is_visible())

        # showing again brings it back; releasing takes it away in every tab
        page.click('[data-project-open]')
        page.wait_for_timeout(500)
        self.assertTrue(page.locator('[data-project-window]').is_visible())
        page.click('[data-project-open]')                     # Stop projecting
        page.wait_for_timeout(500)
        self.assertFalse(page.locator('[data-project-window]').is_visible())
        self.assertFalse(tab.locator('[data-project-window]').is_visible())

    def test_reopening_returns_the_window_to_the_screen_on_air(self):
        """Spec 141: the way back lands on the screen that is on air -- not on the
        service's first screen, which is what release-then-Project does."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        page.evaluate("window.gkpsDisplay.screen(4)")
        projector.wait_for_function("document.body.dataset.currentScreen === '4'")
        projector.close()
        page.wait_for_timeout(400)
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())

        with page.expect_popup() as reopened_info:
            page.click('[data-project-window]')
        reopened = reopened_info.value
        reopened.wait_for_url('**/projector')
        reopened.wait_for_load_state('networkidle')
        self.assertNotIn('service=', reopened.url, 'the reopen adopted the service again')
        reopened.wait_for_function("document.body.dataset.currentScreen === '4'")
        self.assertEqual(reopened.get_attribute('body', 'data-showing'), 'true')
        self.assertIn('Stop projecting', page.locator('[data-project-open]').inner_text())

    def test_reopening_writes_no_display_state(self):
        """Spec 141: reopening is a reader's act -- the state, and its timestamp, are
        exactly what they were before the press."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        page.evaluate("window.gkpsDisplay.screen(2)")
        projector.wait_for_function("document.body.dataset.currentScreen === '2'")
        projector.close()
        page.wait_for_timeout(400)
        before = page.evaluate("() => localStorage.getItem('gkps-display')")

        with page.expect_popup() as reopened_info:
            page.click('[data-project-window]')
        reopened = reopened_info.value
        reopened.wait_for_url('**/projector')
        reopened.wait_for_load_state('networkidle')
        reopened.wait_for_function("document.body.dataset.currentScreen === '2'")
        after = page.evaluate("() => localStorage.getItem('gkps-display')")
        self.assertEqual(json.loads(before), json.loads(after))

    def test_an_open_projector_window_is_focused_not_reloaded(self):
        """Spec 141: the window that is already open is brought forward, not loaded
        again -- a reload would restart its media and lose its place."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')
        projector.evaluate("window.__gkpsReopenToken = 'kept'")
        pages_before = len(context.pages)

        page.click('[data-project-window]')
        page.wait_for_timeout(700)
        self.assertEqual(len(context.pages), pages_before, 'a second projector window was opened')
        self.assertEqual(projector.evaluate("window.__gkpsReopenToken"), 'kept',
                         'the projector page was loaded again')

        page.click('[data-project-window]')
        page.wait_for_timeout(500)
        self.assertEqual(len(context.pages), pages_before)

    def test_stop_projecting_still_releases_with_the_control_present(self):
        """Spec 141: the new control is not the stop -- Stop projecting still releases
        the display in every tab (spec 119)."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        popup_info.value.wait_for_load_state('networkidle')
        self.assertTrue(page.locator('[data-project-window]').is_visible())

        page.click('[data-project-open]')                     # Stop projecting
        page.wait_for_timeout(500)
        self.assertIn('Project', page.locator('[data-project-open]').inner_text())
        self.assertFalse(page.locator('[data-project-window]').is_visible())
        state = page.evaluate("() => JSON.parse(localStorage.getItem('gkps-display') || 'null')")
        self.assertIsNone(state['service'])
        self.assertFalse(state['on'])

    def test_the_project_group_stays_inside_the_pane(self):
        """Spec 141: the third control must not spill the group past the reading pane,
        whose narrowest desktop width is 240px (a 1280 window)."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        popup_info.value.close()
        page.wait_for_timeout(400)
        self.assertEqual(page.locator('[data-project-group] button').count(), 3,
                         'the widest group: Media files, the reopen control, Stop projecting')
        for width, height in ((1440, 900), (1280, 800)):
            page.set_viewport_size({'width': width, 'height': height})
            page.wait_for_timeout(400)
            geometry = self._group_geometry(page)
            self.assertNotEqual(geometry['control'], 'none', (width, geometry))
            self.assertLessEqual(geometry['groupRight'], geometry['paneRight'] + 0.5,
                                 f'the group crosses the pane at {width}px: {geometry}')
            self.assertLessEqual(geometry['groupWidth'], geometry['paneWidth'] + 0.5,
                                 f'the group is wider than the pane at {width}px: {geometry}')

        # without Media files the group is narrower, and still inside the pane
        other = self._page(reverse('web-tatib-service', args=[self.untitled_service.pk]), context)
        with other.expect_popup() as other_info:
            other.click('[data-project-open]')
        other_info.value.close()
        other.set_viewport_size({'width': 1280, 'height': 800})
        other.wait_for_timeout(400)
        self.assertEqual(other.locator('[data-project-group] button').count(), 2)
        geometry = self._group_geometry(other)
        self.assertLessEqual(geometry['groupRight'], geometry['paneRight'] + 0.5, geometry)

    def test_the_reopen_control_is_not_drawn_on_a_phone(self):
        """Spec 141 keeps spec 138's phone: the toolbar has no room for the control."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        popup_info.value.close()
        page.wait_for_timeout(300)
        self.assertTrue(page.locator('[data-project-window]').is_visible())

        page.set_viewport_size({'width': 425, 'height': 900})
        page.wait_for_timeout(400)
        self.assertFalse(page.locator('[data-project-window]').is_visible())
        self.assertFalse(page.locator('[data-project-open]').is_visible())

        page.set_viewport_size({'width': 1024, 'height': 900})
        page.wait_for_timeout(400)
        self.assertTrue(page.locator('[data-project-window]').is_visible())
        self.assertTrue(page.locator('[data-project-open]').is_visible())

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

        # editing is available on the swapped pane too (spec 026)
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(250)
        page.locator('[data-entry-open="text"]').first.click()
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')

    # --- the display follows every saved change (spec 026) --------------------

    def test_a_saved_entry_reaches_the_display_without_update(self):
        """A save in the shell is written at once, and the display re-reads by itself:
        nobody presses Update."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')

        asked = []
        projector.on('request', lambda request: asked.append(request.url))
        page.on('request', lambda request: asked.append(request.url))

        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(250)
        page.locator('[data-entry-open="text"]').first.click()
        page.wait_for_selector('dialog[open]')
        page.fill('#id_text', 'Berita baru untuk layar')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')", timeout=8000)
        projector.wait_for_function("document.querySelector('#projectorScreens').textContent.includes('Berita baru untuk layar')",
                                    timeout=8000)
        self.assertTrue([url for url in asked if f'/projector?service={self.service.pk}' in url],
                        f'the display must re-read its service after a save: {asked}')
        self.assertIn('Berita baru untuk layar', projector.locator('#projectorScreens').text_content())

    def test_a_reorder_reaches_the_display_without_update(self):
        """A drop is written at once, and the display re-reads by itself."""
        context = self.browser.new_context(viewport={'width': 1440, 'height': 900})
        page = self._page(self._service_url(), context)
        with page.expect_popup() as popup_info:
            page.click('[data-project-open]')
        projector = popup_info.value
        projector.wait_for_load_state('networkidle')

        asked = []
        projector.on('request', lambda request: asked.append(request.url))

        grip = page.locator('[data-move-grip]').first
        grip.focus()
        page.keyboard.press('ArrowDown')
        page.wait_for_timeout(900)
        self.assertTrue([url for url in asked if f'/projector?service={self.service.pk}' in url],
                        f'the display must re-read its service after a reorder: {asked}')

    def test_goto_lists_without_a_request_per_query(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        requests = []
        page.on('request', lambda request: requests.append(request.url)
                if '/projector/goto/' in request.url else None)
        page.keyboard.press('g')
        field = page.locator('#projectorFindInput')
        for query in ('KJ 15', 'Mat 5', 'KJ 152', 'Ada Kuasa', 'nonsense', ''):
            field.fill(query)
        page.wait_for_timeout(400)
        self.assertEqual(requests, [])

    def test_update_finds_a_song_added_after_the_page_loaded(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        with ThreadPoolExecutor(max_workers=1) as pool:
            def add_song():
                try:
                    book = songs.Book.objects.get(short_name='KJ')
                    song = songs.Song.objects.create(book=book, number=999, title='Fresh title')
                    songs.Verse.objects.create(song=song, number=1, lyric='Fresh lyric')
                finally:
                    connections.close_all()
            pool.submit(add_song).result()
        # A broadcast never reaches the page that sent it: another tab posts the update.
        sender = page.context.new_page()
        sender.goto(self.live_server_url + '/api/')
        sender.evaluate("""() => {
          const channel = new BroadcastChannel('gkps-service-display');
          channel.postMessage({type: 'update'});
          channel.close();
        }""")
        sender.close()
        page.wait_for_timeout(1200)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('KJ 999')
        page.wait_for_function(
            "document.querySelector('.projector-find__suggestion').textContent.includes('KJ 999')")

    def _open_matius_5(self, page):
        wait_for_goto(page)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('Mat 5')
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / 1'")
        statuses = []
        messages = []
        page.on('console', lambda message: messages.append(message.text))
        page.on('pageerror', lambda error: messages.append(str(error)))
        page.on('response', lambda response: statuses.append((response.status, response.url))
                if '/projector/goto/' in response.url else None)
        page.keyboard.press('Enter')
        try:
            page.wait_for_function(
                "document.querySelector('.projector-detour').classList.contains('is-active')",
                timeout=4000)
        except Exception:
            state = page.evaluate("""() => ({
              detour: document.querySelector('.projector-detour').className,
              suggestion: document.querySelector('.projector-find__suggestion').textContent,
              panelHidden: document.querySelector('#projectorFind').hidden,
              disabled: document.querySelector('#projectorFindInput').disabled,
              cue: !!document.querySelector('.cue-loading'),
              body: document.body.dataset.currentScreen,
            })""")
            self.fail(str(state) + ' ' + str(statuses) + ' ' + str(messages))
        page.locator('#projectorFind').wait_for(state='hidden')

    def test_a_verse_step_inside_a_chapter_makes_no_request(self):
        page = self._page(self._projector_url())
        self._open_matius_5(page)
        before = page.locator('.projector-detour').inner_text()
        requests = []
        page.on('request', lambda request: requests.append(request.url)
                if '/projector/goto/' in request.url else None)
        page.keyboard.press('ArrowDown')
        page.wait_for_timeout(250)
        self.assertNotEqual(page.locator('.projector-detour').inner_text(), before)
        self.assertEqual(requests, [])

    def test_a_chapter_crossing_locks_the_cue_and_paints_the_next_chapter(self):
        page = self._page(self._projector_url())
        self._open_matius_5(page)
        page.keyboard.press('End')
        page.wait_for_timeout(200)
        release = []
        page.route('**/projector/goto/chapter/**', lambda route: release.append(route))
        page.keyboard.press('ArrowRight')                  # last verse -> next chapter
        page.wait_for_function("document.querySelector('.cue-loading') !== null")
        spinner = page.locator('.cue-loading').bounding_box()
        keys = page.locator('.keys').bounding_box()
        self.assertLess(spinner['x'] + spinner['width'], keys['x'])
        self.assertAlmostEqual(spinner['y'] + spinner['height'] / 2,
                               keys['y'] + keys['height'] / 2, delta=1.5)
        release.pop().continue_()
        page.wait_for_function(
            "document.querySelector('.projector-detour').textContent.includes('Matius 6')")

    def test_a_previous_chapter_crossing_locks_and_paints(self):
        page = self._page(self._projector_url())
        self._open_matius_5(page)
        page.keyboard.press('Home')
        page.wait_for_timeout(200)
        release = []
        page.route('**/projector/goto/chapter/**', lambda route: release.append(route))
        page.keyboard.press('ArrowLeft')
        page.wait_for_function("document.querySelector('.cue-loading') !== null")
        release.pop().continue_()
        page.wait_for_function(
            "document.querySelector('.projector-detour').textContent.includes('Matius 4:1')")

    def test_a_book_change_locks_and_paints_the_first_chapter(self):
        page = self._page(self._projector_url())
        self._open_matius_5(page)
        release = []
        page.route('**/projector/goto/chapter/**', lambda route: release.append(route))
        page.keyboard.press('Control+ArrowRight')
        page.wait_for_function("document.querySelector('.cue-loading') !== null")
        release.pop().continue_()
        page.wait_for_function(
            "document.querySelector('.projector-detour').textContent.includes('Mazmur 23:1')")

    def test_the_translation_flip_makes_no_request(self):
        page = self._page(self._projector_url())
        self._open_matius_5(page)
        requests = []
        page.on('request', lambda request: requests.append(request.url)
                if '/projector/goto/' in request.url else None)
        page.keyboard.press('t')
        page.wait_for_timeout(250)
        self.assertEqual(page.locator('.cue-translation').inner_text(), 'TB')
        self.assertEqual(requests, [])

    def test_a_selection_locks_the_panel_until_the_content_paints(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('Mat 5')
        page.wait_for_timeout(800)
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / 1'")
        before = page.get_attribute('body', 'data-current-screen')
        release = []
        page.route('**/projector/goto/chapter/**', lambda route: release.append(route))
        page.keyboard.press('Enter')
        page.wait_for_function(
            "document.querySelector('.projector-find__row').classList.contains('is-loading')")
        self.assertTrue(page.locator('#projectorFindInput').is_disabled())
        self.assertEqual(page.locator('.projector-find__spinner').count(), 1)
        self.assertEqual(page.locator('.cue-loading').count(), 1)
        page.keyboard.press('Escape')
        page.wait_for_timeout(150)
        self.assertTrue(page.locator('#projectorFind').is_visible())
        self.assertFalse(page.locator('body').evaluate(
            "el => el.classList.contains('find-closing')"))
        page.keyboard.press('ArrowRight')
        self.assertEqual(page.get_attribute('body', 'data-current-screen'), before)
        release.pop().continue_()
        page.wait_for_function(
            "document.querySelector('.projector-detour').classList.contains('is-active')")
        page.locator('#projectorFind').wait_for(state='hidden')
        self.assertFalse(page.locator('#projectorFind').is_visible())
        self.assertFalse(page.locator('#projectorFindInput').is_disabled())
        self.assertEqual(page.locator('.cue-loading').count(), 0)

    def test_a_failed_selection_restores_the_panel(self):
        page = self._page(self._projector_url())
        wait_for_goto(page)
        page.route('**/projector/goto/chapter/**', lambda route: route.abort())
        page.keyboard.press('g')
        page.locator('#projectorFindInput').fill('Mat 5')
        page.wait_for_function(
            "document.querySelector('.projector-find__count').textContent === '1 / 1'")
        page.keyboard.press('Enter')
        page.wait_for_function(
            "document.querySelector('.projector-find__suggestion').textContent.includes('Could not load')")
        self.assertTrue(page.locator('#projectorFind').is_visible())
        self.assertFalse(page.locator('#projectorFindInput').is_disabled())
        self.assertEqual(page.locator('.cue-loading').count(), 0)

    def test_goto_opened_before_the_index_shows_the_loading_state(self):
        page = self.browser.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        release = []
        page.route('**/projector/goto/index/', lambda route: release.append(route))
        page.goto(self.live_server_url + self._projector_url())
        page.keyboard.press('g')
        page.wait_for_function(
            "document.querySelector('.projector-find__row').classList.contains('is-loading')")
        self.assertTrue(page.locator('#projectorFindInput').is_disabled())
        self.assertEqual(page.locator('.projector-find__spinner').count(), 1)
        self.assertIn('Loading search', page.locator('.projector-find__suggestion').inner_text())
        release.pop().continue_()
        page.wait_for_function(
            "!document.querySelector('.projector-find__row').classList.contains('is-loading')")
        self.assertFalse(page.locator('#projectorFindInput').is_disabled())

    def test_the_page_leaves_no_browser_storage(self):
        page = self.browser.new_context().new_page()
        page.goto(self.live_server_url + '/api/')
        page.evaluate("""() => new Promise((resolve, reject) => {
          const request = indexedDB.open('gkps-public-library', 1);
          request.onupgradeneeded = () => request.result.createObjectStore('chunks');
          request.onsuccess = () => { request.result.close(); resolve(true); };
          request.onerror = () => reject(request.error);
        })""")
        page.evaluate("""() => caches.open('gkps-public-shell-test').then(
          (cache) => cache.put('/home/', new Response('saved shell')))""")
        page.goto(self.live_server_url + '/home/')
        page.wait_for_timeout(400)
        state = page.evaluate("""async () => ({
          databases: (await indexedDB.databases()).map((row) => row.name),
          caches: await caches.keys(),
          workers: (await navigator.serviceWorker.getRegistrations()).length,
        })""")
        self.assertNotIn('gkps-public-library', state['databases'])
        self.assertFalse([name for name in state['caches'] if 'gkps-public-shell' in name])
        self.assertEqual(state['workers'], 0)

    def test_an_empty_service_shows_its_empty_state(self):
        page = self._page(f'/projector?service={self.other.pk}')
        self.assertIn('no items', page.locator('.projector__empty').inner_text())
        self.assertNotIn('offline', page.locator('.projector__empty').inner_text().lower())
        self.assertTrue(page.locator('.projector__empty').is_visible())
        self.assertFalse(page.locator('.projector__empty').evaluate('(el) => el.hidden'))

    def _notice_state(self, page):
        """The empty notice and the stage it shares the screen with."""
        return page.evaluate("""() => {
          const notice = document.querySelector('.projector__empty');
          const stage = document.getElementById('projectorScreens');
          const detour = document.querySelector('.projector-detour');
          return {
            display: getComputedStyle(notice).display,
            hidden: notice.hidden,
            noticeHeight: notice.getBoundingClientRect().height,
            stageHeight: stage.getBoundingClientRect().height,
            detourActive: detour ? detour.classList.contains('is-active') : false,
          };
        }""")

    def _add_first_entry(self):
        with ThreadPoolExecutor(max_workers=1) as pool:
            def add_entry():
                try:
                    tatib.ServiceEntry.objects.create(
                        tatib=self.other, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
                        title='Berita', text='Ayat untuk layar kosong')
                finally:
                    connections.close_all()
            pool.submit(add_entry).result()

    def _broadcast_update(self, page):
        """Another tab posts the update a broadcast never delivers to its sender."""
        sender = page.context.new_page()
        sender.goto(self.live_server_url + '/api/')
        sender.evaluate("""() => {
          const channel = new BroadcastChannel('gkps-service-display');
          channel.postMessage({type: 'update'});
          channel.close();
        }""")
        sender.close()

    def test_the_empty_notice_leaves_the_stage_for_a_goto_passage(self):
        page = self._page(f'/projector?service={self.other.pk}')
        before = self._notice_state(page)
        self.assertEqual(before['display'], 'block')
        self.assertGreater(before['noticeHeight'], 0)
        self.assertFalse(before['detourActive'])

        self._open_matius_5(page)

        after = self._notice_state(page)
        self.assertTrue(after['detourActive'], 'the passage must be on the stage')
        self.assertEqual(after['display'], 'none')
        self.assertTrue(after['hidden'])
        self.assertEqual(page.locator('.projector__empty').bounding_box(), None)
        self.assertAlmostEqual(after['stageHeight'] - before['stageHeight'],
                               before['noticeHeight'], delta=1)
        self.assertIn('ayat 1', page.locator('.projector-detour').inner_text())

    def test_closing_the_detour_brings_the_empty_notice_back(self):
        page = self._page(f'/projector?service={self.other.pk}')
        self._open_matius_5(page)
        self.assertEqual(self._notice_state(page)['display'], 'none')

        page.keyboard.press('Escape')
        page.wait_for_function(
            "!document.querySelector('.projector-detour').classList.contains('is-active')")

        state = self._notice_state(page)
        self.assertEqual(state['display'], 'block')
        self.assertFalse(state['hidden'])
        self.assertTrue(page.locator('.projector__empty').is_visible())

    def test_a_reread_with_screens_hides_the_empty_notice(self):
        page = self._page(f'/projector?service={self.other.pk}')
        self.assertEqual(self._notice_state(page)['display'], 'block')
        self._add_first_entry()

        with page.expect_request(lambda request: f'/projector?service={self.other.pk}' in request.url):
            self._broadcast_update(page)
        page.wait_for_function(
            "document.querySelectorAll('#projectorScreens .screen[data-screen]').length > 0")

        self.assertEqual(self._notice_state(page)['display'], 'none')
        self.assertIn('Ayat untuk layar kosong', page.locator('#projectorScreens').inner_text())

    def test_a_reread_without_screens_keeps_the_empty_notice(self):
        page = self._page(f'/projector?service={self.other.pk}')

        with page.expect_request(lambda request: f'/projector?service={self.other.pk}' in request.url):
            self._broadcast_update(page)
        page.wait_for_timeout(600)

        self.assertEqual(page.locator('#projectorScreens .screen[data-screen]').count(), 0)
        self.assertEqual(self._notice_state(page)['display'], 'block')

    def test_the_reading_shell_carries_no_offline_control(self):
        page = self._page('/home/')
        self.assertEqual(page.locator('#offlineSyncButton').count(), 0)
        self.assertEqual(page.locator('#offlineSyncPanel').count(), 0)
        self.assertEqual(page.locator('#offlineSavedSource').count(), 0)
        sources = page.eval_on_selector_all('script[src]', 'els => els.map(e => e.src)')
        self.assertFalse([src for src in sources if 'offline' in src])
