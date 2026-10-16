"""Spec 092 browser checks for saved shells and tab-local search state."""

from concurrent.futures import ThreadPoolExecutor

from django.db import connections
from django.test import LiveServerTestCase, override_settings, tag
from playwright.sync_api import Error as PlaywrightError, sync_playwright

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib


def wait_for_offline_ready(page):
    page.evaluate("""(async () => {
      const deadline = Date.now() + 25000;
      while (Date.now() < deadline) {
        const state = await GKPSOffline.status();
        if (state.ready && !state.syncing) return true;
        await new Promise(resolve => setTimeout(resolve, 40));
      }
      throw new Error('Offline library did not become ready');
    })()""")


@override_settings(DEBUG=True)
@tag('e2e')
class OfflineLibraryE2ETests(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        language = bible.Language.objects.create(name='Indonesia')
        version = bible.Version.objects.create(
            lang=language, name='Terjemahan Baru', abbreviation='TB')
        book = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=1)
        translation = bible.BookTranslation.objects.create(
            version=version, book=book, translation='Matius')
        bible.Verse.objects.create(book_translation=translation, chapter=1, verse=1,
                                   text='Kasih Tuhan membuka Injil')
        songbook = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                             is_hymn_book=True)
        song = songs.Song.objects.create(book=songbook, number=12, title='Kasih')
        songs.Verse.objects.create(song=song, number=1, lyric='Kasih Tuhan kekal')
        service = tatib.TataIbadah.objects.create(name='Ibadah Minggu', is_active=True)
        tatib.TataIbadahItem.objects.create(tatib=service, item_type=0, title='Doa',
                                            text='Tuhan dengar kami', order_number=1)
        self.book_id = book.pk
        self.song_id = song.pk
        self.songbook_id = songbook.pk
        self.service_id = service.pk

    def assert_saved_badge_centered_on_stage(self, page):
        page.wait_for_function("""() => {
          const badge = document.querySelector('#offlineSavedSource');
          const stage = document.querySelector('.stage');
          if (!badge || badge.hidden || !stage) return false;
          const badgeRect = badge.getBoundingClientRect();
          const stageRect = stage.getBoundingClientRect();
          return Math.abs((badgeRect.left + badgeRect.width / 2)
            - (stageRect.left + stageRect.width / 2)) < 1;
        }""")
        centers = page.evaluate("""() => {
          const badge = document.querySelector('#offlineSavedSource').getBoundingClientRect();
          const stage = document.querySelector('.stage').getBoundingClientRect();
          return {badge: badge.left + badge.width / 2, stage: stage.left + stage.width / 2};
        }""")
        self.assertAlmostEqual(centers['badge'], centers['stage'], delta=1)

    def test_saved_sidebar_matches_server_order_and_controls(self):
        smaller = songs.Book.objects.create(name='Short Book', short_name='SB')
        songs.Song.objects.create(book=smaller, title='One')
        larger = songs.Book.objects.create(name='Large Book', short_name='LB')
        for number in range(3):
            songs.Song.objects.create(book=larger, title=f'Song {number}')
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/songs/')
            wait_for_offline_ready(page)
            server_order = page.locator('#panelBody .book__n').all_text_contents()
            self.assertLess(server_order.index('Large Book'), server_order.index('Short Book'))
            page.locator('.rail [data-panel="tatib"]').click()
            page.locator('.rail [data-panel="kidung"]').click()
            page.wait_for_function("document.documentElement.dataset.section === 'kidung'")
            self.assertEqual(page.locator('#panelBody .book__n').all_text_contents(), server_order)
            self.assertEqual(page.locator('#panelBody .row-edit').count(), 2)
            self.assertEqual(page.locator('#panelBody .row-edit svg').count(), 2)
            self.assertNotIn('Edit', page.locator('#panelBody .row-edit').first.inner_text())
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator('#panelCollapse').click()
            page.wait_for_function("document.documentElement.dataset.nav === 'mini'")
            self.assertTrue(page.locator('#panelBody .book__a').first.is_visible())
            self.assertEqual(page.locator('#panelBody .book__a').first.inner_text(), 'Mat')
            browser.close()

    def test_saved_content_and_projector_survive_disconnection(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            self.assertGreater(page.locator('#offlineSyncAvailability').count(), 0, page.content()[:1200])
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent.includes('Ready')")
            context.set_offline(True)
            page.locator('.rail__logo').click()
            page.wait_for_function("location.pathname === '/' && document.documentElement.dataset.home === 'landing'")
            page.locator('.rail [data-panel="alkitab"]').click()
            page.wait_for_function("document.documentElement.dataset.nav === 'open'")
            page.get_by_role('link', name='Matius').first.wait_for()
            page.locator('#panelCollapse').click()
            page.wait_for_function("document.documentElement.dataset.nav === 'mini'")
            mini_book = page.get_by_role('link', name='Matius (Mat)').first
            self.assertEqual(mini_book.locator('.book__a').count(), 1,
                             page.locator('#panelBody').evaluate('(el) => el.innerHTML'))
            self.assertTrue(mini_book.locator('.book__a').is_visible())
            self.assertEqual(mini_book.locator('.book__a').inner_text(), 'Mat')
            page.goto(self.live_server_url + f'/bible/{self.book_id}/')
            page.get_by_role('link', name='Matius chapter 1').wait_for()
            page.goto(self.live_server_url + f'/bible/{self.book_id}/1/')
            page.get_by_text('Kasih Tuhan membuka Injil').wait_for()
            self.assertTrue(page.locator('#readEyebrow').evaluate('(el) => el.hidden'))
            page.goto(self.live_server_url + f'/songs/{self.song_id}/')
            page.get_by_text('Kasih Tuhan kekal').wait_for()
            page.goto(self.live_server_url + '/songs/')
            page.get_by_role('link', name='Kidung Jemaat').first.wait_for()
            page.goto(self.live_server_url + f'/songs/book/{self.songbook_id}/')
            page.get_by_role('link', name='Kasih').first.wait_for()
            page.goto(self.live_server_url + f'/tatib/{self.service_id}/')
            page.get_by_text('Tuhan dengar kami').wait_for()
            page.goto(self.live_server_url + f'/obs/service/{self.service_id}/')
            page.locator('#projectorScreens .screen[data-screen]').first.wait_for(state='attached')
            self.assertIn('Tuhan dengar kami', page.locator('#projectorScreens').text_content())
            page.keyboard.press('g')
            page.locator('#projectorFindInput').fill('Mat 1')
            page.get_by_text('Matius 1', exact=True).wait_for()
            page.keyboard.press('Enter')
            page.locator('.projector-detour.is-active').wait_for(state='attached')
            self.assertIn('Kasih Tuhan membuka Injil', page.locator('.projector-detour').text_content())
            page.goto(self.live_server_url + '/search/?q=Kasih')
            page.locator('.result-row').first.wait_for()
            for unsupported_path in (
                '/obs/songs/dock', '/editor/tatib/new/', '/manage/',
                '/future/offline-route/',
            ):
                with self.subTest(path=unsupported_path), self.assertRaises(PlaywrightError):
                    page.goto(self.live_server_url + unsupported_path, timeout=3000)
            browser.close()

    def test_failed_online_content_refresh_keeps_the_saved_reading(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            initial_status = page.evaluate('GKPSOffline.status()')
            saved_render = page.evaluate("GKPSOfflineRender.render('/bible/%d/1/').then(doc => ({found: !!doc, savedHidden: doc && doc.querySelector('#offlineSavedSource').hidden}))" % self.book_id)
            aborted_chunks = []
            def abort_chunk(route):
                aborted_chunks.append(route.request.url)
                route.abort()
            page.route('**/offline/chunk/**', abort_chunk)
            page.locator('.rail [data-panel="alkitab"]').click()
            page.locator('#panelBody .book').filter(has_text='Matius').first.click()
            page.wait_for_function("document.documentElement.dataset.ch === 'open'")
            page.locator('#chList .ch-num').first.click()
            page.get_by_text('Kasih Tuhan membuka Injil').wait_for()
            self.assertEqual(page.url, self.live_server_url + f'/bible/{self.book_id}/1/')
            source = page.locator('#offlineSavedSource')
            self.assertTrue(any('/offline/chunk/bible/' in url for url in aborted_chunks), {
                'aborted': aborted_chunks, 'status': initial_status, 'render': saved_render,
                'source': source.evaluate('el => el.outerHTML'),
            })
            self.assertFalse(source.evaluate('el => el.hidden'), {
                'status': initial_status, 'render': saved_render,
                'source': source.evaluate('el => el.outerHTML'),
            })
            badge = source.evaluate('''el => ({
                position: getComputedStyle(el).position,
                pointerEvents: getComputedStyle(el).pointerEvents,
                top: el.getBoundingClientRect().top,
                parent: el.parentElement.id
            })''')
            self.assertEqual(badge['position'], 'fixed')
            self.assertEqual(badge['pointerEvents'], 'none')
            self.assertEqual(badge['parent'], 'read')
            self.assert_saved_badge_centered_on_stage(page)

            # The badge follows the reading-stage center as its left columns
            # collapse and reopen, without becoming part of document flow.
            rail_bible = page.locator('.rail [data-panel="alkitab"]')
            if page.locator('html').get_attribute('data-nav') == 'open':
                rail_bible.click()
                page.wait_for_function("document.documentElement.dataset.nav === 'closed'")
                self.assert_saved_badge_centered_on_stage(page)
                rail_bible.click()
                page.wait_for_function("document.documentElement.dataset.nav === 'open'")
                self.assert_saved_badge_centered_on_stage(page)

            page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            self.assertAlmostEqual(source.bounding_box()['y'], badge['top'], delta=1)
            page.set_viewport_size({'width': 700, 'height': 600})
            narrow = source.bounding_box()
            self.assertAlmostEqual(narrow['y'], 12, delta=1)
            self.assert_saved_badge_centered_on_stage(page)
            page.emulate_media(media='print')
            self.assertEqual(source.evaluate('el => getComputedStyle(el).display'), 'none')
            page.unroute('**/offline/chunk/**')
            browser.close()

    def test_failed_first_sync_is_atomic_and_missing_content_clears_ready_status(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.route('**/offline/chunk/songs/*/', lambda route: route.abort())
            page.goto(self.live_server_url + '/home/')
            failed = page.evaluate("GKPSOffline.sync().then(() => false, () => true)")
            self.assertTrue(failed)
            state = page.evaluate("GKPSOffline.status()")
            self.assertFalse(state['ready'])
            self.assertIsNone(page.evaluate("GKPSOffline.get('bible', %d)" % self.book_id))
            self.assertIsNone(page.evaluate("GKPSOffline.get('songs', %d)" % self.songbook_id))

            page.unroute('**/offline/chunk/songs/*/')
            page.locator('#offlineSyncButton').click()
            page.locator('#offlineSyncNow').click()
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent === 'Syncing library…'")
            wait_for_offline_ready(page)
            page.wait_for_function("document.querySelector('#offlineLastSynced').textContent !== 'Never'")
            page.wait_for_function("document.querySelector('#offlineLastChecked').textContent !== 'Not checked'")
            self.assertNotEqual(page.locator('#offlineLastSynced').inner_text(), 'Never')
            self.assertNotEqual(page.locator('#offlineLastChecked').inner_text(), 'Not checked')

            def remove_one_saved_chunk(book_id):
                return page.evaluate("""id => new Promise((resolve, reject) => {
                  const request = indexedDB.open('gkps-public-library', 1);
                  request.onerror = () => reject(request.error);
                  request.onsuccess = () => {
                    const db = request.result;
                    const tx = db.transaction('chunks', 'readwrite');
                    tx.objectStore('chunks').delete('songs:' + id);
                    tx.oncomplete = () => { db.close(); resolve(); };
                    tx.onerror = () => { db.close(); reject(tx.error); };
                  };
                })""", book_id)
            remove_one_saved_chunk(self.songbook_id)
            page.locator('#offlineSyncButton').click()  # close
            page.locator('#offlineSyncButton').click()  # recheck storage before displaying Ready
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent === 'Not ready for offline use'")
            self.assertFalse(page.evaluate("GKPSOffline.status().then(state => state.ready)"))
            browser.close()

    def test_status_popover_states_and_narrow_layout(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)

            status_button = page.locator('#offlineSyncButton')
            status_button.focus()
            page.keyboard.press('Tab')
            page.keyboard.press('Shift+Tab')
            self.assertTrue(status_button.evaluate("el => el.matches(':focus-visible')"))
            status_button.click()
            panel = page.locator('#offlineSyncPanel')
            self.assertTrue(panel.is_visible())

            page.wait_for_function("!!navigator.locks && !!navigator.locks.request")
            page.evaluate("""() => {
              navigator.locks.request('gkps-public-library-sync', () => {
              window.__offlineTestLockHeld = true;
              return new Promise(resolve => { window.__offlineTestReleaseLock = resolve; });
              });
              return true;
            }""")
            page.wait_for_function('window.__offlineTestLockHeld === true')
            page.locator('#offlineSyncNow').click()
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent === 'Syncing library…'")
            sync_now = page.locator('#offlineSyncNow')
            self.assertTrue(sync_now.is_disabled())
            self.assertFalse(page.locator('#offlineSyncProgress').is_hidden())
            page.emulate_media(reduced_motion='reduce')
            animation = page.locator('#offlineSyncProgress').evaluate(
                "el => getComputedStyle(el, '::after').animationName")
            self.assertEqual(animation, 'none')
            page.evaluate('window.__offlineTestReleaseLock()')
            wait_for_offline_ready(page)

            page.set_viewport_size({'width': 360, 'height': 640})
            page.wait_for_function("innerWidth === 360 && getComputedStyle(document.documentElement).getPropertyValue('--rail-w').trim() === '64px'")
            bounds = panel.evaluate("el => { const r = el.getBoundingClientRect(); return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,cssWidth:getComputedStyle(el).width,viewport:innerWidth,viewportHeight:innerHeight,rail:getComputedStyle(document.documentElement).getPropertyValue('--rail-w')}; }")
            self.assertGreaterEqual(bounds['left'], 12)
            self.assertLessEqual(bounds['right'], 348, bounds)
            self.assertGreaterEqual(bounds['top'], 0)
            self.assertAlmostEqual(bounds['viewportHeight'] - bounds['bottom'], 12, delta=1, msg=bounds)

            page.locator('#themeBtn').click()
            status_button.click()
            bg = panel.evaluate("el => getComputedStyle(el).backgroundColor")
            token = page.locator('html').evaluate("el => getComputedStyle(el).getPropertyValue('--canvas').trim()")
            self.assertEqual(bg, page.evaluate("value => { const e=document.createElement('div'); e.style.backgroundColor=value; document.body.append(e); const c=getComputedStyle(e).backgroundColor; e.remove(); return c; }", token))

            context.set_offline(True)
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent === 'Ready for offline use'")
            self.assertTrue(page.locator('#offlineSyncNow').is_disabled())
            self.assertEqual(page.locator('#offlineSyncNow').inner_text(), 'Sync when online')
            browser.close()

    def test_search_history_and_new_tab_are_independent(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent.includes('Ready')")
            page.locator('#searchQuery').fill('Kasih')
            page.locator('#globalSearch').evaluate('(form) => form.requestSubmit()')
            page.locator('.result-row').first.wait_for()
            first_url = page.url
            page.locator('#searchQuery').fill('draft text')
            page.locator('.rail__logo').click()
            page.wait_for_function("location.pathname === '/' && document.documentElement.dataset.home === 'landing' && document.querySelector('#searchQuery').value === ''")
            self.assertEqual(page.locator('#searchQuery').input_value(), '')
            page.locator('#railSearch').click()
            page.wait_for_function("document.documentElement.dataset.home === 'results' && document.querySelector('#searchQuery').value === 'draft text'")
            self.assertEqual(page.locator('#searchQuery').input_value(), 'draft text')
            with context.expect_page() as opened:
                page.evaluate("window.open('/home/', '_blank')")
            another = opened.value
            another.wait_for_load_state()
            another.locator('#railSearch').click()
            self.assertEqual(another.locator('#searchQuery').input_value(), '')
            self.assertNotIn('/search', another.url)
            page.locator('#searchQuery').fill('Kasih')
            page.locator('#globalSearch').evaluate('(form) => form.requestSubmit()')
            page.locator('.result-row').first.wait_for()
            self.assertEqual(page.url, first_url)
            self.assertGreater(page.evaluate('history.length'), 2)
            browser.close()

    def test_same_query_history_restores_each_result_generation_and_view_state(self):
        def add_initial_songs():
            try:
                book = songs.Book.objects.get(pk=self.songbook_id)
                for number in range(10):
                    songs.Song.objects.create(book=book, number=100 + number,
                                              title=f'Kasih Nyanyian {number}')
            finally:
                connections.close_all()
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(add_initial_songs).result()

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 720})
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)
            page.locator('#searchQuery').fill('Kasih')
            page.locator('#searchQuery').press('Enter')
            page.locator('.result-group[data-kind="songs"]').wait_for()
            group = page.locator('.result-group[data-kind="songs"]')
            page.wait_for_function("() => { const el = document.querySelector('.result-group[data-kind=\"songs\"] .result-group__count'); return el && el.textContent.includes('11'); }")
            first_id = page.evaluate('history.state.searchId')
            group.locator('.result-more').click()
            page.wait_for_function('''() => {
              const group = document.querySelector('.result-group[data-kind="songs"]');
              return group && group.querySelectorAll('.result-row').length === 11;
            }''')
            self.assertEqual(group.locator('.result-row').count(), 11)
            page.evaluate('window.scrollTo(0, 420)')
            page.wait_for_function('''() => {
              const y = window.scrollY;
              window.__scrollStable = y === window.__previousScroll
                ? (window.__scrollStable || 0) + 1 : 0;
              window.__previousScroll = y;
              return window.__scrollStable >= 5 && y > 100;
            }''')
            first_scroll = page.evaluate('window.scrollY')

            def add_later_song():
                try:
                    songs.Song.objects.create(book_id=self.songbook_id, number=111,
                                              title='Kasih Tambahan')
                finally:
                    connections.close_all()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(add_later_song).result()
            page.evaluate('GKPSOffline.sync()')

            page.locator('#searchQuery').evaluate("""(input) => {
              input.value = 'Kasih';
              input.dispatchEvent(new Event('input', {bubbles: true}));
              input.form.requestSubmit();
            }""")
            page.wait_for_function("() => { const el = document.querySelector('.result-group[data-kind=\"songs\"] .result-group__count'); return el && el.textContent.includes('12'); }")
            second_id = page.evaluate('history.state.searchId')
            self.assertNotEqual(first_id, second_id)
            first_saved_scroll = page.evaluate('''(id) => {
              const snapshot = JSON.parse(sessionStorage.getItem('gkps-search-entry:' + id));
              return snapshot.scroll;
            }''', first_id)
            self.assertLessEqual(abs(first_scroll - first_saved_scroll), 1)
            page.evaluate('window.scrollTo(0, 260)')
            page.locator('#searchQuery').evaluate("""(input) => {
              input.value = 'draft on second result';
              input.dispatchEvent(new Event('input', {bubbles: true}));
            }""")
            second_scroll = page.evaluate('window.scrollY')

            page.go_back()
            page.wait_for_function("() => { const el = document.querySelector('.result-group[data-kind=\"songs\"] .result-group__count'); return el && el.textContent.includes('11'); }")
            self.assertEqual(page.locator('.result-group[data-kind="songs"] .result-row').count(), 11)
            self.assertEqual(page.locator('#searchQuery').input_value(), 'Kasih')
            first_restored_scroll = page.evaluate('window.scrollY')
            self.assertLessEqual(abs(first_restored_scroll - first_saved_scroll), 60,
                                 msg=f'first={first_saved_scroll}, restored={first_restored_scroll}')

            page.go_forward()
            page.wait_for_function("() => { const el = document.querySelector('.result-group[data-kind=\"songs\"] .result-group__count'); return el && el.textContent.includes('12'); }")
            self.assertEqual(page.locator('.result-group[data-kind="songs"] .result-row').count(), 8)
            self.assertEqual(page.locator('#searchQuery').input_value(), 'draft on second result')
            second_restored_scroll = page.evaluate('window.scrollY')
            self.assertLessEqual(abs(second_restored_scroll - second_scroll), 60,
                                 msg=f'second={second_scroll}, restored={second_restored_scroll}')
            browser.close()

    def test_interrupted_update_keeps_previous_generation_until_retry(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            page.wait_for_function("document.querySelector('#offlineSyncAvailability').textContent.includes('Ready')")
            initial = page.evaluate("GKPSOffline.get('songs', %d)" % self.songbook_id)
            self.assertEqual(initial['songs'][0]['verses'][0]['lyric'], 'Kasih Tuhan kekal')
            other_tab = context.new_page()
            other_tab.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(other_tab)
            other_tab.evaluate("""() => {
              window.__offlineEvents = 0;
              window.__offlineCommitEvents = 0;
              GKPSOffline.subscribe(() => window.__offlineEvents++);
              window.__offlineChannel = new BroadcastChannel('gkps-public-library');
              window.__offlineChannel.addEventListener('message', event => {
                if (event.data && event.data.type === 'committed') window.__offlineCommitEvents++;
              });
            }""")

            def update_verse():
                try:
                    verse = songs.Verse.objects.get(song_id=self.song_id, number=1)
                    verse.lyric = 'Kasih Tuhan diperbarui'
                    verse.save()
                finally:
                    connections.close_all()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(update_verse).result()
            page.route('**/offline/chunk/songs/*/', lambda route: route.abort())
            page.locator('#offlineSyncButton').click()
            page.locator('#offlineSyncNow').click()
            page.wait_for_function("document.querySelector('#offlineSyncDetail').textContent.includes('latest update failed')")
            saved = page.evaluate("GKPSOffline.get('songs', %d)" % self.songbook_id)
            self.assertEqual(saved['songs'][0]['verses'][0]['lyric'], 'Kasih Tuhan kekal')

            page.unroute('**/offline/chunk/songs/*/')
            page.locator('#offlineSyncNow').click()
            page.evaluate("""(async id => {
              const deadline = Date.now() + 25000;
              while (Date.now() < deadline) {
                const value = await GKPSOffline.get('songs', id);
                if (value.songs[0].verses[0].lyric === 'Kasih Tuhan diperbarui') return true;
                await new Promise(resolve => setTimeout(resolve, 40));
              }
              throw new Error('Updated song data was not committed');
            })(%d)""" % self.songbook_id)
            other_tab.wait_for_function('window.__offlineCommitEvents > 0 && window.__offlineEvents > 0')
            other_copy = other_tab.evaluate("GKPSOffline.get('songs', %d)" % self.songbook_id)
            self.assertEqual(other_copy['songs'][0]['verses'][0]['lyric'], 'Kasih Tuhan diperbarui')
            browser.close()

    def test_sync_requested_during_an_inflight_generation_rechecks_later_changes(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(self.live_server_url + '/home/')
            wait_for_offline_ready(page)

            # Update the Bible after the sync starts below; update Tata Ibadah only
            # after the old manifest has already been read.
            def change_bible():
                try:
                    verse = bible.Verse.objects.get(book_translation__book_id=self.book_id,
                                                    chapter=1, verse=1)
                    verse.text = 'Bible update starts the blocked sync'
                    verse.save()
                finally:
                    connections.close_all()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(change_bible).result()

            requests = []
            page.on('request', lambda request: requests.append(request.url))
            page.evaluate("""() => {
              const originalFetch = window.fetch.bind(window);
              window.__chunkBlocked = false;
              window.__releaseChunk = null;
              window.fetch = function (input, init) {
                const url = typeof input === 'string' ? input : input.url;
                if (url.includes('/offline/chunk/bible/')) {
                  window.__chunkBlocked = true;
                  return new Promise((resolve, reject) => {
                    window.__releaseChunk = () => originalFetch(input, init).then(resolve, reject);
                  });
                }
                return originalFetch(input, init);
              };
              window.__firstSync = GKPSOffline.sync().catch(() => {});
            }""")
            page.wait_for_function('window.__chunkBlocked === true')

            def change_service():
                try:
                    item = tatib.TataIbadahItem.objects.get(tatib_id=self.service_id,
                                                            order_number=1)
                    item.text = 'Service update during the blocked sync'
                    item.save()
                finally:
                    connections.close_all()
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(change_service).result()
            page.evaluate('window.__queuedSync = GKPSOffline.sync().catch(() => {}); true')
            page.evaluate('window.__releaseChunk()')

            saved_text = page.evaluate("""(async () => {
              await window.__queuedSync;
              const service = await GKPSOffline.get('service', %d);
              return service.rows.find(row => row.order === 1).text;
            })()""" % self.service_id)
            self.assertEqual(saved_text, 'Service update during the blocked sync')
            self.assertTrue(any('/offline/chunk/service/%d/' % self.service_id in url
                                for url in requests), requests)
            browser.close()
