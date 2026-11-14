"""Immediate, cancellable editor loading for sidebar and service-entry forms."""

import unittest
from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse

from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

try:
    from playwright.sync_api import expect, sync_playwright

    HAS_PLAYWRIGHT = True
except ImportError:  # pragma: no cover - depends on the environment
    HAS_PLAYWRIGHT = False


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ImmediateEditorOpenE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.book = songs.Book.objects.create(
            name='Kidung Harian', short_name='KH', is_hymn_book=False)
        self.song = songs.Song.objects.create(book=self.book, title='Alpha')
        self.service = tatib.TataIbadah.objects.create(
            name='Ibadah Minggu', date=date(2026, 10, 4), is_active=True)
        tatib.ServiceEntry.objects.create(
            tatib=self.service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
            title='Welcome', text='Marilah kita bangkit berdiri!')
        tatib.TataIbadahItem.objects.create(
            tatib=self.service, order_number=2, item_type=tatib.TataIbadahItemType.TEXT,
            title='Legacy row', text='Amin.')

        self._playwright = sync_playwright().start()
        try:
            self.browser = self._playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on environment
            self._playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self._playwright.stop()
        super().tearDown()

    def _page(self, url):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(self.live_server_url + url)
        page.wait_for_load_state('networkidle')
        return page

    @staticmethod
    def _form(title='Loaded form'):
        return (
            '<div class="editor__body">'
            f'<h2 class="editor__title" id="editorTitle">{title}</h2>'
            '<form class="editor__form" action="/editor/mock/save/">'
            '<div class="editor__field"><label>Title<input type="text" name="title"></label></div>'
            '<div class="editor__actions">'
            '<button class="editor__save" type="submit">Save</button>'
            '<button class="editor__cancel" type="button" data-editor-close>Cancel</button>'
            '</div></form></div>'
        )

    @staticmethod
    def _hold_editor_requests(page):
        routes = []
        page.route('**/editor/**', lambda route: routes.append(route))
        return routes

    def _activate_and_finish(self, page, selector, expected_loading_title, routes):
        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator(selector).first.evaluate('(element) => element.click()')

        expect(page.locator('#editorModal[open]')).to_be_visible()
        expect(page.locator('.editor__loading')).to_be_visible()
        expect(page.locator('#editorTitle')).to_have_text(expected_loading_title)
        self.assertTrue(routes, 'the form request should be pending behind the loading state')

        route = routes[-1]
        route.fulfill(status=200, content_type='text/html', body=self._form())
        expect(page.locator('#editorTitle')).to_have_text('Loaded form')
        expect(page.locator('#editorContent input[name="title"]')).to_be_focused()
        page.locator('.editor__cancel').click()
        page.wait_for_function("!document.querySelector('#editorModal').open")

    def test_sidebar_editor_forms_open_immediately_and_ignore_repeat_activation(self):
        page = self._page(reverse('web-index'))
        routes = self._hold_editor_requests(page)
        page.locator('.rail__btn[aria-label="Kidung"]').click()

        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('#panelAdd').click()
        expect(page.locator('#editorModal[open]')).to_be_visible()
        expect(page.locator('#editorTitle')).to_have_text('New songbook')
        expect(page.locator('.editor__loading')).to_be_visible()

        # A second activation from behind the open modal must not start another fetch.
        page.locator('#panelAdd').evaluate('(element) => element.click()')
        expect(page.locator('.editor__loading')).to_be_visible()
        self.assertEqual(len(routes), 1)

        spinner = page.locator('.editor__loading-spinner').bounding_box()
        label = page.locator('.editor__loading-label').bounding_box()
        self.assertAlmostEqual(spinner['x'] + spinner['width'] / 2,
                               label['x'] + label['width'] / 2, delta=1)
        self.assertGreater(label['y'], spinner['y'] + spinner['height'])
        self.assertEqual(page.locator('.editor__loading').evaluate(
            'element => getComputedStyle(element).gap'), '10px')
        self.assertEqual(page.locator('.editor__loading').evaluate(
            'element => getComputedStyle(element).flexDirection'), 'column')

        routes[0].fulfill(status=200, content_type='text/html', body=self._form())
        expect(page.locator('#editorTitle')).to_have_text('Loaded form')
        expect(page.locator('#editorContent input[name="title"]')).to_be_focused()
        page.locator('.editor__cancel').click()
        page.wait_for_function("!document.querySelector('#editorModal').open")

        # All sidebar Add/Edit controls use the same loading path.
        self._activate_and_finish(page, '.row-edit[data-editor-open="songbook"]',
                                  'Edit songbook', routes)
        page.locator(f'.book[data-name="{self.book.pk}"]').click()
        page.wait_for_function("document.documentElement.dataset.ch === 'open'")
        self._activate_and_finish(page, '#songAdd', 'New song', routes)
        self._activate_and_finish(page, '.row-edit[data-editor-open="song"]',
                                  'Edit song', routes)
        page.locator('.rail__btn[aria-label="Tata Ibadah"]').click()
        self._activate_and_finish(page, '#panelAdd', 'New Tata Ibadah', routes)
        self._activate_and_finish(page, '.row-edit[data-editor-open="tatib"]',
                                  'Edit Tata Ibadah', routes)

    def test_service_entry_and_legacy_forms_share_immediate_loading(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        routes = self._hold_editor_requests(page)

        self._activate_and_finish(page, '[data-entry-open="text"]', 'Add Text', routes)
        self._activate_and_finish(page, '[data-entry-edit]', 'Edit entry', routes)
        self._activate_and_finish(page, '[data-old-item-edit]', 'Edit row', routes)

    def test_cancel_invalidates_old_response_across_editor_paths(self):
        page = self._page(reverse('web-tatib-service', args=[self.service.pk]))
        routes = self._hold_editor_requests(page)
        page.evaluate('window.AbortController = undefined')

        page.locator('.rail__btn[aria-label="Kidung"]').click()
        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('#panelAdd').click()
        expect(page.locator('#editorTitle')).to_have_text('New songbook')
        page.keyboard.press('Escape')
        page.wait_for_function("!document.querySelector('#editorModal').open")

        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('[data-entry-open="text"]').first.evaluate(
                '(element) => element.click()')
        expect(page.locator('#editorTitle')).to_have_text('Add Text')
        self.assertEqual(len(routes), 2)

        routes[0].fulfill(status=200, content_type='text/html',
                          body=self._form('Stale sidebar form'))
        expect(page.locator('#editorTitle')).to_have_text('Add Text')
        expect(page.locator('.editor__loading')).to_be_visible()

        routes[1].fulfill(status=200, content_type='text/html', body=self._form())
        expect(page.locator('#editorTitle')).to_have_text('Loaded form')
        expect(page.locator('#editorContent')).not_to_contain_text('Stale sidebar form')

    def test_failed_load_closes_the_modal_and_a_later_click_can_retry(self):
        page = self._page(reverse('web-index'))
        routes = []

        def hold_for_failure(route):
            routes.append(route)

        page.route('**/editor/**', hold_for_failure)
        page.locator('.rail__btn[aria-label="Kidung"]').click()
        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('#panelAdd').click()
        expect(page.locator('#editorModal[open]')).to_be_visible()
        expect(page.locator('.editor__loading')).to_be_visible()
        routes[0].abort('internetdisconnected')
        expect(page.locator('#editorModal[open]')).to_have_count(0, timeout=5000)
        expect(page.locator('.edit-toast__title')).to_contain_text('Could not load editor')

        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('#panelAdd').click()
        expect(page.locator('.editor__loading')).to_be_visible()
        routes[1].fulfill(status=200, content_type='text/html', body=self._form())
        expect(page.locator('#editorTitle')).to_have_text('Loaded form')

    def test_loading_layout_is_responsive_and_cancel_or_backdrop_invalidates_response(self):
        page = self._page(reverse('web-index'))
        page.set_viewport_size({'width': 320, 'height': 480})
        page.emulate_media(reduced_motion='reduce')
        page.emulate_media(color_scheme='light')
        page.wait_for_function("document.documentElement.dataset.theme === 'light'")
        light_arc = page.evaluate("""() => {
          const probe = document.createElement('span');
          probe.style.borderTopColor = 'var(--active-bg)';
          document.body.appendChild(probe);
          const color = getComputedStyle(probe).borderTopColor;
          probe.remove();
          return color;
        }""")
        page.locator('#themeBtn').click()
        page.wait_for_function("document.documentElement.dataset.theme === 'dark'")
        dark_arc = page.evaluate("""() => {
          const probe = document.createElement('span');
          probe.style.borderTopColor = 'var(--active-bg)';
          document.body.appendChild(probe);
          const color = getComputedStyle(probe).borderTopColor;
          probe.remove();
          return color;
        }""")
        self.assertNotEqual(light_arc, dark_arc)
        routes = self._hold_editor_requests(page)
        page.evaluate('window.AbortController = undefined')
        page.locator('.rail__btn[aria-label="Kidung"]').click()

        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('#panelAdd').click()
        dialog = page.locator('#editorModal[open]')
        expect(dialog).to_be_visible()
        self.assertEqual(page.locator('.editor__loading-title').evaluate(
            'element => getComputedStyle(element).fontSize'), '20px')
        expect(page.locator('.editor__loading-label')).to_have_text('Loading editor…')
        expect(page.locator('.editor__cancel')).to_be_focused()
        bounds = dialog.bounding_box()
        self.assertLessEqual(bounds['width'], 288)
        self.assertLessEqual(bounds['height'], 440)
        self.assertEqual(page.locator('#editorContent').evaluate(
            'element => getComputedStyle(element).padding'), '24px')
        self.assertEqual(page.locator('.editor__loading-spinner').evaluate(
            'element => [element.getBoundingClientRect().width, element.getBoundingClientRect().height]'),
            [18, 18])
        self.assertEqual(page.locator('.editor__loading-label').evaluate(
            'element => getComputedStyle(element).fontSize'), '14px')
        self.assertEqual(page.locator('.editor__loading-spinner').evaluate(
            'element => getComputedStyle(element).borderTopColor'), dark_arc)
        self.assertEqual(page.locator('.editor__loading-spinner').evaluate(
            'element => getComputedStyle(element).animationName'), 'none')

        page.locator('.editor__cancel').click()
        page.wait_for_function("!document.querySelector('#editorModal').open")
        routes[0].fulfill(status=200, content_type='text/html', body=self._form('Canceled form'))
        expect(page.locator('#editorModal[open]')).to_have_count(0)

        page.locator('#themeBtn').click()
        page.wait_for_function("document.documentElement.dataset.theme === 'light'")
        with page.expect_request(lambda request: '/editor/' in request.url):
            page.locator('#panelAdd').click()
        expect(page.locator('.editor__loading')).to_be_visible()
        self.assertEqual(page.locator('.editor__loading-spinner').evaluate(
            'element => getComputedStyle(element).borderTopColor'), light_arc)
        page.locator('#editorModal').evaluate(
            "dialog => dialog.dispatchEvent(new MouseEvent('click', {bubbles: true}))")
        page.wait_for_function("!document.querySelector('#editorModal').open")
        routes[1].fulfill(status=200, content_type='text/html', body=self._form('Backdrop form'))
        expect(page.locator('#editorModal[open]')).to_have_count(0)
