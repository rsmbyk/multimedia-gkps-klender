"""Browser acceptance for the age buckets of the Media Library list and the transfer history (spec 146).

The two lists draw their rows from the loopback companion, so every test routes that origin; the bucket
rule itself is called with a pinned present instant, which is why its edges are asserted rather than
approximated.
"""
import hashlib
import json
import unittest
from datetime import date, datetime, timedelta, timezone

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from multimedia.tatib.models import MediaIdentity, ServiceEntry, ServiceEntryKind, TataIbadah

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def ago(**delta):
    return (datetime.now(timezone.utc) - timedelta(**delta)).isoformat()


def file_row(name, family='image', **delta):
    return {'sha256': hashlib.sha256(name.encode()).hexdigest(), 'name': name, 'family': family,
            'size': 2048, 'uploaded_at': ago(**delta), 'unused_since': None, 'delete_at': None}


def transfer_row(identifier, name, status='completed', **delta):
    started = ago(**delta)
    return {'id': identifier, 'name': name, 'direction': 'upload', 'status': status,
            'size': 2048, 'bytes_done': 2048 if status != 'active' else 1024,
            'started_at': started, 'ended_at': None if status == 'active' else started}


@tag('e2e')
@unittest.skipUnless(HAS_PLAYWRIGHT, 'playwright is not installed')
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class MediaAgeBucketE2ETests(StaticLiveServerTestCase):
    def setUp(self):
        # Fixture rows are written before the sync API starts: its greenlet makes a later ORM call raise
        # SynchronousOnlyOperation, which is why the repo's other browser suites seed in setUp too.
        if self._testMethodName == 'test_the_unused_chip_empties_a_bucket_and_hides_its_heading':
            service = TataIbadah.objects.create(name='Ibadah Minggu', date=date.today() - timedelta(days=2),
                                                is_active=True)
            media = MediaIdentity.objects.create(sha256=hashlib.sha256(b'used.jpg').hexdigest(),
                                                 byte_count=2048, family='image',
                                                 display_filename='used.jpg')
            ServiceEntry.objects.create(tatib=service, order_number=1, kind=ServiceEntryKind.MEDIA,
                                        media=media, media_filename='used.jpg')
        if self._testMethodName == 'test_the_three_shared_labels_read_the_same_on_all_three_lists':
            for name, days in (('Ibadah Minggu', 12), ('Ibadah Sektor', 41), ('Natal I', 330)):
                TataIbadah.objects.create(name=name, date=date.today() - timedelta(days=days), is_active=True)
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch()
        except Exception as error:
            self.playwright.stop()
            raise unittest.SkipTest(f'playwright browser unavailable: {error}')

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    # ---------- helpers ----------

    def library_page(self, files=(), transfers=(), connected=True):
        page = self.browser.new_page(viewport={'width': 1440, 'height': 900})
        if not connected:
            page.route('http://127.0.0.1:63174/**', lambda route: route.abort())
        else:
            def companion(route):
                url = route.request.url
                if url.endswith('/status'):
                    payload = {'connection': 'connected', 'file_count': len(files),
                               'total_size': 2048, 'retention': '30', 'write_token': 'test-token'}
                elif url.endswith('/transfers'):
                    payload = {'transfers': list(transfers), 'retrying': []}
                elif url.endswith('/files') or url.endswith('/references'):
                    payload = {'files': list(files)}
                else:
                    payload = {'files': list(files)}
                route.fulfill(status=200, content_type='application/json', body=json.dumps(payload),
                              headers={'Access-Control-Allow-Origin': self.live_server_url})
            page.route('http://127.0.0.1:63174/**', companion)
        page.goto(self.live_server_url + '/media-library/')
        page.wait_for_selector('#mediaFileList .media-library__file, #mediaEmpty:not([hidden])')
        return page

    def list_headings(self, page):
        return page.eval_on_selector_all(
            '#mediaFileList .media-library__group',
            'nodes => nodes.map(node => [node.textContent, node.dataset.bucket])')

    def transfer_headings(self, page):
        return page.eval_on_selector_all(
            '#mediaTransfersList .media-transfers__group',
            'nodes => nodes.map(node => [node.textContent, node.dataset.bucket])')

    def transfer_names(self, page):
        return page.eval_on_selector_all(
            '#mediaTransfersList .media-transfers__row strong', 'nodes => nodes.map(node => node.textContent)')

    def open_transfers(self, page):
        page.click('#mediaTransfersButton')
        page.wait_for_selector('#mediaTransfersDialog[open]')

    def choose_sort(self, page, key):
        page.click('#mediaSortButton')
        page.click(f'[data-media-sort="{key}"]')
        page.wait_for_timeout(50)

    def file_bucket(self, page, uploaded_at, now):
        return page.evaluate(
            '([iso, now]) => window.gkpsAgeBuckets.fileKey({ uploaded_at: iso }, Date.parse(now))',
            [uploaded_at, now])

    def transfer_bucket(self, page, started_at, now):
        return page.evaluate(
            '([iso, now]) => window.gkpsAgeBuckets.transferKey({ started_at: iso }, Date.parse(now))',
            [started_at, now])

    # ---------- US1 — the Media Library list ----------

    def test_the_list_draws_three_age_buckets(self):
        page = self.library_page(files=[file_row('today.jpg', **{'hours': 2}),
                                        file_row('forty-one.pdf', family='pdf', days=41),
                                        file_row('last-year.jpg', days=330)])
        self.assertEqual(self.list_headings(page),
                         [['Last 30 days', 'last-30-days'],
                          ['Earlier this year', 'earlier-this-year'],
                          ['Older', 'older']])
        self.assertEqual(page.locator('#mediaFileList .media-library__file').count(), 3)

    def test_a_file_buckets_at_its_edges(self):
        page = self.library_page(files=[file_row('today.jpg', **{'hours': 2})])
        now = '2026-10-30T10:00:00+00:00'   # 17:00 WIB
        self.assertEqual(self.file_bucket(page, '2026-10-30T03:00:00+00:00', now), 'last-30-days')
        self.assertEqual(self.file_bucket(page, '2026-09-30T03:00:00+00:00', now), 'last-30-days')
        self.assertEqual(self.file_bucket(page, '2026-09-29T03:00:00+00:00', now), 'earlier-this-year')
        self.assertEqual(self.file_bucket(page, '2025-10-29T03:00:00+00:00', now), 'older')
        # the window beats the year: a file from last December is still inside thirty days
        self.assertEqual(self.file_bucket(page, '2025-12-31T03:00:00+00:00', '2026-01-10T10:00:00+00:00'),
                         'last-30-days')

    def test_the_present_day_is_the_congregations_day(self):
        page = self.library_page(files=[file_row('today.jpg', **{'hours': 2})])
        # 30 Sep 03:00 WIB is thirty days before 30 Oct 17:00 WIB — but thirty-one by the UTC calendar
        self.assertEqual(self.file_bucket(page, '2026-09-29T20:00:00+00:00', '2026-10-30T10:00:00+00:00'),
                         'last-30-days')
        # 1 Jan 2026 03:00 WIB is last year on the UTC calendar, this year on the congregation's
        self.assertEqual(self.file_bucket(page, '2025-12-31T20:00:00+00:00', '2026-03-15T10:00:00+00:00'),
                         'earlier-this-year')
        self.assertEqual(page.evaluate(
            '(now) => window.gkpsAgeBuckets.todayIso(Date.parse(now))', '2026-10-30T16:30:00+00:00'),
            '2026-10-30')  # 23:30 WIB
        self.assertEqual(page.evaluate(
            '(now) => window.gkpsAgeBuckets.todayIso(Date.parse(now))', '2026-10-30T17:30:00+00:00'),
            '2026-10-31')  # 00:30 WIB the next day

    def test_a_bucket_with_no_file_draws_no_heading(self):
        page = self.library_page(files=[file_row('a.jpg', days=1), file_row('b.jpg', days=12)])
        self.assertEqual(self.list_headings(page), [['Last 30 days', 'last-30-days']])

    def test_a_size_sort_draws_no_heading(self):
        page = self.library_page(files=[file_row('a.jpg', days=1), file_row('b.pdf', family='pdf', days=41)])
        self.choose_sort(page, 'size-desc')
        self.assertEqual(self.list_headings(page), [])
        self.assertEqual(page.locator('#mediaFileList .media-library__file').count(), 2)

    def test_an_ascending_sort_reverses_the_buckets(self):
        page = self.library_page(files=[file_row('a.jpg', days=1), file_row('b.pdf', family='pdf', days=41),
                                        file_row('c.jpg', days=330)])
        self.choose_sort(page, 'date-asc')
        self.assertEqual([label for label, _ in self.list_headings(page)],
                         ['Older', 'Earlier this year', 'Last 30 days'])
        self.assertEqual(page.locator('#mediaFileList .media-library__file').first.locator(
            '.media-library__filename').text_content(), 'c.jpg')

    def test_the_heading_keeps_its_class_and_carries_the_bucket_key(self):
        page = self.library_page(files=[file_row('a.jpg', days=2)])
        # One round trip: both surfaces redraw on the companion's two-second poll, so a second read of the
        # same node can find it detached and return empty computed values.
        heading = page.evaluate('''() => {
          const node = document.querySelector('#mediaFileList .media-library__group');
          const style = getComputedStyle(node);
          return { tag: node.tagName, cls: node.className, bucket: node.dataset.bucket,
                   text: node.textContent, transform: style.textTransform, marginTop: style.marginTop };
        }''')
        self.assertEqual(heading['tag'], 'H2')
        self.assertEqual(heading['cls'], 'media-library__group')
        self.assertEqual(heading['bucket'], 'last-30-days')
        self.assertEqual(heading['text'], 'Last 30 days')
        self.assertEqual(heading['transform'], 'uppercase')
        self.assertEqual(heading['marginTop'], '28px')

    def test_a_chip_that_empties_a_bucket_hides_its_heading(self):
        page = self.library_page(files=[file_row('a.jpg', days=2),
                                        file_row('old.pdf', family='pdf', days=41)])
        self.assertEqual(len(self.list_headings(page)), 2)
        page.click('[data-media-type="image"]')
        page.wait_for_timeout(50)
        self.assertEqual(self.list_headings(page), [['Last 30 days', 'last-30-days']])
        page.click('[data-media-type="image"]')
        page.wait_for_timeout(50)
        self.assertEqual(len(self.list_headings(page)), 2)

    def test_the_unused_chip_empties_a_bucket_and_hides_its_heading(self):
        page = self.library_page(files=[file_row('used.jpg', days=2),
                                        file_row('old.pdf', family='pdf', days=41)])
        page.wait_for_timeout(200)  # the references fetch decides which row is unused
        self.assertEqual([label for label, _ in self.list_headings(page)],
                         ['Last 30 days', 'Earlier this year'])
        page.click('#mediaUnusedFilter')
        page.wait_for_timeout(50)
        self.assertEqual(self.list_headings(page), [['Earlier this year', 'earlier-this-year']])
        page.click('#mediaUnusedFilter')
        page.wait_for_timeout(50)
        self.assertEqual(len(self.list_headings(page)), 2)

    # ---------- US2 — the transfer history ----------

    def test_the_dialog_draws_five_age_buckets(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)], transfers=[
            transfer_row(1, 'two-hours.jpg', **{'hours': 2}),
            transfer_row(2, 'three-days.jpg', days=3),
            transfer_row(3, 'twelve-days.jpg', days=12),
            transfer_row(4, 'forty-five-days.jpg', days=45),
            transfer_row(5, 'last-year.jpg', days=330)])
        self.open_transfers(page)
        self.assertEqual(self.transfer_headings(page),
                         [['Last 24 hours', 'last-24-hours'],
                          ['Last 7 days', 'last-7-days'],
                          ['Last 30 days', 'last-30-days'],
                          ['Earlier this year', 'earlier-this-year'],
                          ['Older', 'older']])
        self.assertEqual(len(self.transfer_names(page)), 5)

    def test_a_transfer_buckets_at_its_edges(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)])
        now = '2026-10-30T10:00:00+00:00'
        self.assertEqual(self.transfer_bucket(page, '2026-10-30T09:00:00+00:00', now), 'last-24-hours')
        self.assertEqual(self.transfer_bucket(page, '2026-10-29T10:00:00+00:00', now), 'last-7-days')
        self.assertEqual(self.transfer_bucket(page, '2026-10-24T10:00:00+00:00', now), 'last-7-days')
        self.assertEqual(self.transfer_bucket(page, '2026-10-23T10:00:00+00:00', now), 'last-30-days')
        self.assertEqual(self.transfer_bucket(page, '2026-09-30T10:00:00+00:00', now), 'earlier-this-year')
        self.assertEqual(self.transfer_bucket(page, '2025-10-30T10:00:00+00:00', now), 'older')
        # a row the companion cannot date is still drawn, under the oldest bucket
        self.assertEqual(page.evaluate(
            '(now) => window.gkpsAgeBuckets.transferKey({ started_at: "not a date" }, Date.parse(now))', now),
            'older')

    def test_a_transfer_buckets_by_its_start(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)], transfers=[
            # started forty hours ago, finished an hour ago: the start decided it
            {**transfer_row(1, 'long-one.pdf', **{'hours': 40}),
             'started_at': ago(hours=40), 'ended_at': ago(hours=1)}])
        self.open_transfers(page)
        self.assertEqual(self.transfer_headings(page), [['Last 7 days', 'last-7-days']])

    def test_an_active_transfer_leads_its_own_bucket(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)], transfers=[
            transfer_row(1, 'running-two-days.jpg', status='active', days=2),
            transfer_row(2, 'done-today.jpg', **{'hours': 1}),
            transfer_row(3, 'done-three-days.jpg', days=3)])
        self.open_transfers(page)
        self.assertEqual([label for label, _ in self.transfer_headings(page)],
                         ['Last 24 hours', 'Last 7 days'])
        self.assertEqual(self.transfer_names(page),
                         ['done-today.jpg', 'running-two-days.jpg', 'done-three-days.jpg'])

    def test_rows_inside_a_bucket_keep_their_end_time_order(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)], transfers=[
            {**transfer_row(1, 'five-hours.jpg'), 'started_at': ago(hours=5), 'ended_at': ago(hours=5)},
            {**transfer_row(2, 'one-hour.jpg'), 'started_at': ago(hours=1), 'ended_at': ago(hours=1)}])
        self.open_transfers(page)
        self.assertEqual(self.transfer_names(page), ['one-hour.jpg', 'five-hours.jpg'])

    def test_the_dialog_heading_is_a_third_level_heading(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)],
                                 transfers=[transfer_row(1, 'a.jpg', **{'hours': 2})])
        self.open_transfers(page)
        heading = page.evaluate('''() => {
          const node = document.querySelector('#mediaTransfersList .media-transfers__group');
          const style = getComputedStyle(node);
          return { tag: node.tagName, cls: node.className, bucket: node.dataset.bucket,
                   text: node.textContent, transform: style.textTransform,
                   size: style.fontSize, marginTop: style.marginTop };
        }''')
        self.assertEqual(heading['tag'], 'H3')
        self.assertEqual(heading['cls'], 'media-transfers__group')
        self.assertEqual(heading['bucket'], 'last-24-hours')
        self.assertEqual(heading['text'], 'Last 24 hours')
        self.assertEqual(heading['transform'], 'uppercase')
        self.assertEqual(heading['size'], '12px')
        self.assertEqual(heading['marginTop'], '4px')
        self.assertEqual(page.locator('#mediaTransfersDialog h2').text_content(), 'Transfers')

    def test_the_rail_draws_no_bucket_headings(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)],
                                 transfers=[transfer_row(1, 'running.jpg', status='active', **{'hours': 1})])
        page.wait_for_selector('#mediaTransferRail:not([hidden])')
        page.click('#mediaTransferRail')
        page.wait_for_selector('#mediaTransfersDialog[open]')
        self.assertEqual(self.transfer_headings(page), [])
        self.assertGreater(page.locator('#mediaTransfersList .media-transfers__row').count(), 0)

    # ---------- US3 — the same words on every list ----------

    def test_the_three_shared_labels_read_the_same_on_all_three_lists(self):
        page = self.library_page(files=[file_row('a.jpg', days=2), file_row('b.pdf', family='pdf', days=41),
                                        file_row('c.jpg', days=330)],
                                 transfers=[transfer_row(1, 'a.jpg', **{'hours': 2}),
                                            transfer_row(2, 'b.jpg', days=3),
                                            transfer_row(3, 'c.jpg', days=12),
                                            transfer_row(4, 'd.jpg', days=45),
                                            transfer_row(5, 'e.jpg', days=330)])
        library_labels = [label for label, _ in self.list_headings(page)]
        self.open_transfers(page)
        transfer_labels = [label for label, _ in self.transfer_headings(page)]
        page.goto(self.live_server_url + '/tatib/')
        page.wait_for_selector('.group__head')
        tatib_labels = page.eval_on_selector_all('.group__head', 'nodes => nodes.map(node => node.textContent)')
        self.assertEqual(library_labels, tatib_labels)
        self.assertEqual(transfer_labels[-3:], tatib_labels)
        self.assertEqual(transfer_labels, ['Last 24 hours', 'Last 7 days'] + tatib_labels)

    def test_the_empty_states_are_unchanged(self):
        page = self.library_page(files=[file_row('a.jpg', days=1)], connected=False)
        self.assertEqual(page.locator('#mediaEmpty').text_content(),
                         'Local library unavailable on this computer.')
        self.assertEqual(self.list_headings(page), [])
        page.click('#mediaTransfersButton')
        page.wait_for_selector('#mediaTransfersDialog[open]')
        self.assertEqual(page.locator('#mediaTransfersList .media-transfers__empty').text_content(),
                         'Local library unavailable on this computer.')
        self.assertEqual(self.transfer_headings(page), [])

        empty = self.library_page(files=[])
        self.assertEqual(empty.locator('#mediaEmpty').text_content(), 'No files on this computer yet.')
        self.assertEqual(self.list_headings(empty), [])
        empty.click('#mediaTransfersButton')
        empty.wait_for_selector('#mediaTransfersDialog[open]')
        self.assertEqual(empty.locator('#mediaTransfersList .media-transfers__empty').text_content(),
                         'No transfers yet.')
        self.assertEqual(self.transfer_headings(empty), [])
