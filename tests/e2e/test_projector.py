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
        bible.Verse.objects.create(book_translation=matius, chapter=5, verse=3, text='ayat 3')
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

        # a single-screen text: the whole body on one screen, shrunk to fit
        self.single_service = tatib.TataIbadah.objects.create(
            name='Ibadah Satu Layar', date=date(2026, 9, 13), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.single_service, order_number=1,
            kind=tatib.ServiceEntryKind.TEXT, default_screen_mode='single_screen', title='Doa',
            text='\n'.join(f'Baris {n} dari doa yang panjang ini.' for n in range(1, 30)))

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
        self.assertIn('CMG Sans', styles['face'])          # the current projector's own face
        self.assertIn('Source Sans Pro', styles['face'])   # and the rest of the OBS surfaces'
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
        page.keyboard.press('j')
        self.assertTrue(page.locator('#projectorFind').is_visible())
        page.locator('#projectorFindInput').fill('Salam')
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
        page.keyboard.press('j')
        page.locator('#projectorFindInput').click()
        page.keyboard.type('kf')
        self.assertFalse(page.locator('body').evaluate("el => el.classList.contains('keys-open')"))
        self.assertIsNone(page.evaluate('document.fullscreenElement'))

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
        page = self._page(reverse('web-service-projector', args=[self.long_service.pk]))
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
        page = self._page(reverse('web-service-projector', args=[self.single_service.pk]))
        page.keyboard.press('Space')                          # turn the display on
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

    def test_closing_the_projector_window_stops_the_display(self):
        """Closing the window ends the display by itself, in every tab of the browser.

        A tab that did not open the window cannot watch the handle close, so the projector
        also leaves a beat behind (web/projector.js); the opener knows at once, and the
        other tab hears the stop it posts. Nobody presses Stop.
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

        for other in (page, tab):
            other.wait_for_function(
                "document.querySelector('[data-project-group]').dataset.displaying === 'false'",
                timeout=10000)
            self.assertIn('Project', other.locator('[data-project-open]').inner_text())

        # editing is available with or without a window (spec 026)
        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(200)
        page.locator('[data-entry-open="text"]').first.click()
        page.wait_for_selector('dialog[open]')
        page.keyboard.press('Escape')

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

        page.locator('.tatib__item').first.hover()
        page.wait_for_timeout(250)
        page.locator('[data-entry-open="text"]').first.click()
        page.wait_for_selector('dialog[open]')
        page.fill('#id_text', 'Berita baru untuk layar')
        page.click('.editor__save')
        page.wait_for_function("!document.querySelector('dialog[open]')", timeout=8000)
        page.wait_for_timeout(800)
        self.assertTrue([url for url in asked if self._projector_url() in url],
                        f'the display must re-read after a save: {asked}')

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
        self.assertTrue([url for url in asked if self._projector_url() in url],
                        f'the display must re-read after a reorder: {asked}')
