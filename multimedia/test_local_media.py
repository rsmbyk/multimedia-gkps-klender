"""Focused local-library tests for spec 103."""

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import zipfile
import tempfile
import threading
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from pypdf import PdfReader

from multimedia.local_media import (
    LocalLibrary,
    MediaHandler,
    InvalidMedia,
    converter_identity,
    families_by_directory,
    font_directories,
    font_inventory,
    parse_allowed_origins,
    status_payload,
)
from multimedia import slide_fonts


class LocalLibraryTests(TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.library = LocalLibrary(Path(self.temp.name))

    def test_configured_volume_root_is_used_and_reused(self):
        root = Path(self.temp.name) / 'docker-volume'
        with patch.dict(os.environ, {'GKPS_MEDIA_LIBRARY_ROOT': str(root)}):
            first = LocalLibrary()
            saved = first.import_bytes('notes.pdf', b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n')
            reopened = LocalLibrary()
            self.assertEqual(reopened.root, root.resolve())
            self.assertEqual(reopened.list_files()[0]['sha256'], saved['sha256'])

    def test_status_payload_does_not_expose_storage_path(self):
        self.library.import_bytes('notes.pdf', b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n')
        payload = status_payload(self.library, 'write-token')
        self.assertNotIn('folder', payload)
        self.assertEqual(payload['file_count'], 1)
        self.assertGreater(payload['total_size'], 0)

    def test_allowed_origins_require_exact_origins_without_paths(self):
        origins = parse_allowed_origins(
            'https://example.org,http://localhost:63404,http://127.0.0.1:63404'
        )
        self.assertEqual(len(origins), 3)
        for invalid in ('', 'https://example.org/app', 'https://example.org/', '*'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                parse_allowed_origins(invalid)

    def test_same_bytes_reuse_the_first_filename_and_upload_date(self):
        payload = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        first = self.library.import_bytes('notes.pdf', payload)
        again = self.library.import_bytes('copy.png', payload)
        self.assertEqual(first['sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(again['name'], 'notes.pdf')
        self.assertEqual(again['uploaded_at'], first['uploaded_at'])
        self.assertEqual(len(self.library.list_files()), 1)
        self.assertEqual(len(list((Path(self.temp.name) / 'files').iterdir())), 1)

    def test_inspection_does_not_copy_bytes_until_import(self):
        payload = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        inspected = self.library.inspect_stream('notes.png', io.BytesIO(payload), len(payload))
        self.assertEqual(inspected['family'], 'pdf')
        self.assertEqual(self.library.list_files(), [])
        self.assertEqual(list(self.library.files_dir.iterdir()), [])
        imported = self.library.import_bytes('notes.png', payload)
        self.assertEqual(imported['sha256'], inspected['sha256'])

    def test_same_filename_with_different_bytes_keeps_both(self):
        first = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        second = b'%PDF-1.7\n2 0 obj\n<<>>\nendobj\n%%EOF\n'
        self.library.import_bytes('notes.pdf', first)
        self.library.import_bytes('notes.pdf', second)
        self.assertEqual(len(self.library.list_files()), 2)

    def test_detected_family_ignores_extension_and_rejects_unsupported(self):
        pdf = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        self.assertEqual(self.library.import_bytes('fake.png', pdf)['family'], 'pdf')
        with self.assertRaises(InvalidMedia):
            self.library.import_bytes('fake.pdf', b'not a pdf')
        avif = b'\x00\x00\x00\x18ftypavif\x00\x00\x00\x00avif'
        self.assertEqual(self.library.import_bytes('photo.mp4', avif)['family'], 'image')

    def test_powerpoint_zip_requires_a_presentation_content_type(self):
        def archive(content_type):
            output = io.BytesIO()
            with zipfile.ZipFile(output, 'w') as container:
                container.writestr('[Content_Types].xml',
                    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                    '<Override PartName="/ppt/presentation.xml" ContentType="' + content_type + '"/></Types>')
                container.writestr('ppt/presentation.xml',
                    '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
            return output.getvalue()
        self.assertEqual(self.library.import_bytes(
            'deck.png', archive('application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'))['family'], 'slides')
        with self.assertRaises(InvalidMedia):
            self.library.import_bytes('fake.pptx', archive('application/xml'))

    def test_slide_display_keeps_original_identity_and_reuses_private_pdf(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as archive:
            archive.writestr('[Content_Types].xml',
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/></Types>')
            archive.writestr('ppt/presentation.xml',
                '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
        source = self.library.import_bytes('misnamed.png', output.getvalue())
        self.assertEqual(source['family'], 'slides')
        conversions = []
        def convert(input_path, output_path):
            conversions.append(input_path.suffix)
            output_path.write_bytes((Path(__file__).resolve().parents[1] / 'tests/fixtures/slides/three-slides.pdf').read_bytes())
        first = self.library.slide_pdf(source['sha256'], convert=convert)
        second = self.library.slide_pdf(source['sha256'], convert=convert)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(conversions, ['.pptx'])
        self.assertEqual(len(self.library.list_files()), 1)
        self.assertEqual(self.library.list_files()[0]['name'], 'misnamed.png')
        self.library.sync_references([], [])
        self.library.remove(source['sha256'])
        self.assertFalse(first.exists())

    def test_slide_conversion_failure_leaves_no_cache_and_can_retry(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as archive:
            archive.writestr('[Content_Types].xml',
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/></Types>')
            archive.writestr('ppt/presentation.xml', '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
        sha = self.library.import_bytes('source.pptx', output.getvalue())['sha256']
        def incomplete(input_path, output_path):
            output_path.write_bytes(b'%PDF-corrupt')
        with self.assertRaises(InvalidMedia):
            self.library.slide_pdf(sha, convert=incomplete)
        self.assertEqual(list(self.library.derived_dir.glob('*.pdf')), [])
        def complete(input_path, output_path):
            output_path.write_bytes((Path(__file__).resolve().parents[1] / 'tests/fixtures/slides/three-slides.pdf').read_bytes())
        self.assertTrue(self.library.slide_pdf(sha, convert=complete).exists())

    def test_concurrent_slide_requests_share_one_conversion(self):
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w') as archive:
            archive.writestr('[Content_Types].xml',
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/></Types>')
            archive.writestr('ppt/presentation.xml', '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>')
        sha = self.library.import_bytes('source.pptx', output.getvalue())['sha256']
        calls = []
        def convert(input_path, output_path):
            calls.append(1)
            output_path.write_bytes((Path(__file__).resolve().parents[1] / 'tests/fixtures/slides/three-slides.pdf').read_bytes())
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            paths = list(executor.map(lambda _: self.library.slide_pdf(sha, convert=convert), range(2)))
        self.assertEqual(paths[0], paths[1])
        self.assertEqual(len(calls), 1)

    def test_real_impress_converts_verified_pptx_when_installed(self):
        if shutil.which('libreoffice') is None:
            self.skipTest('LibreOffice Impress is not installed on this test host')
        sample = Path(__file__).resolve().parents[1] / 'tests/fixtures/slides/three-slides.pptx'
        saved = self.library.import_bytes('misleading.png', sample.read_bytes())
        result = self.library.slide_pdf(saved['sha256'])
        self.assertEqual(result.read_bytes()[:5], b'%PDF-')
        self.assertEqual(len(PdfReader(result).pages), 3)
        # The deck is set in Calibri and Times New Roman; a monospaced face here means the renderer
        # answered a proportional request with one, which re-wraps every slide (spec 166).
        embedded = set(re.findall(rb'/BaseFont\s*/([A-Za-z0-9+\-,._]+)', result.read_bytes()))
        self.assertEqual([name for name in embedded if b'Mono' in name], [])
        self.assertEqual(self.library.list_files()[0]['family'], 'slides')
        self.assertEqual(len(self.library.list_files()), 1)

        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(['libreoffice', '-env:UserInstallation=' + (Path(directory) / 'profile').as_uri(),
                            '--headless', '--convert-to', 'ppt', '--outdir', directory, str(sample)],
                           capture_output=True, timeout=30, check=True)
            legacy = Path(directory) / 'three-slides.ppt'
            saved_legacy = self.library.import_bytes('also-misleading.png', legacy.read_bytes())
            legacy_pdf = self.library.slide_pdf(saved_legacy['sha256'])
            self.assertEqual(legacy_pdf.read_bytes()[:5], b'%PDF-')
            self.assertEqual(len(PdfReader(legacy_pdf).pages), 3)
            self.assertEqual(len(self.library.list_files()), 2)

    def test_converter_identity_changes_when_the_fonts_change(self):
        sample = Path(__file__).resolve().parents[1] / 'tests/fixtures/slides/three-slides.pptx'
        saved = self.library.import_bytes('deck.pptx', sample.read_bytes())
        pdf = sample.with_suffix('.pdf').read_bytes()
        conversions = []

        def convert(input_path, output_path):
            conversions.append(1)
            output_path.write_bytes(pdf)

        with patch('multimedia.local_media.convert_slides', side_effect=convert), \
             patch('multimedia.local_media.subprocess.run') as run, \
             patch('multimedia.local_media.font_inventory', return_value='Carlito\nLiberation Sans'):
            run.return_value.stdout = 'LibreOffice 25.2'
            before = self.library.slide_pdf(saved['sha256'])
        with patch('multimedia.local_media.convert_slides', side_effect=convert), \
             patch('multimedia.local_media.subprocess.run') as run, \
             patch('multimedia.local_media.font_inventory',
                   return_value='Britannic Bold\nCarlito\nLiberation Sans'):
            run.return_value.stdout = 'LibreOffice 25.2'
            after = self.library.slide_pdf(saved['sha256'])
        self.assertNotEqual(before, after)
        self.assertEqual(conversions, [1, 1])

    def test_converter_without_fontconfig_keeps_its_identity(self):
        with patch('multimedia.local_media.subprocess.run', side_effect=OSError('no fc-list')):
            self.assertEqual(font_inventory(), '')
            self.assertEqual(converter_identity('LibreOffice 25.2'),
                             converter_identity('LibreOffice 25.2'))

    def test_a_monospaced_answer_is_a_violation(self):
        resolved = {'Calibri': 'Liberation Mono',
                    'Times New Roman': 'Liberation Serif',
                    'Courier New': 'Liberation Mono'}
        self.assertEqual(slide_fonts.violations(resolved),
                         [('Calibri', 'Liberation Mono')])

    def test_a_metric_compatible_answer_is_not_a_violation(self):
        resolved = {'Calibri': 'Carlito', 'Arial': 'Liberation Sans',
                    'Times New Roman': 'Liberation Serif'}
        self.assertEqual(slide_fonts.violations(resolved), [])

    def test_converter_version_changes_cache_key(self):
        sample = Path(__file__).resolve().parents[1] / 'tests/fixtures/slides/three-slides.pptx'
        saved = self.library.import_bytes('deck.pptx', sample.read_bytes())
        pdf = sample.with_suffix('.pdf').read_bytes()
        conversions = []
        def convert(input_path, output_path):
            conversions.append(1)
            output_path.write_bytes(pdf)
        with patch('multimedia.local_media.convert_slides', side_effect=convert), \
             patch('multimedia.local_media.subprocess.run') as version:
            version.return_value.stdout = 'LibreOffice 1.0'
            first = self.library.slide_pdf(saved['sha256'])
            version.return_value.stdout = 'LibreOffice 2.0'
            second = self.library.slide_pdf(saved['sha256'])
        self.assertNotEqual(first, second)
        self.assertEqual(conversions, [1, 1])
        self.assertEqual(len(self.library.list_files()), 1)

    def test_used_file_is_kept_and_unused_file_gets_deadline(self):
        pdf = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        file = self.library.import_bytes('notes.pdf', pdf)
        self.library.sync_references([file['sha256']])
        self.assertIsNone(self.library.list_files()[0]['delete_at'])
        self.library.sync_references([])
        unused = self.library.list_files()[0]
        self.assertIsNotNone(unused['unused_since'])
        self.assertEqual((datetime.fromisoformat(unused['delete_at']) -
                          datetime.fromisoformat(unused['unused_since'])).days, 30)
        self.library.sync_references([file['sha256']])
        self.assertIsNone(self.library.list_files()[0]['unused_since'])

    def test_today_future_reference_blocks_manual_delete_but_past_reference_does_not(self):
        payload = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        file = self.library.import_bytes('notes.pdf', payload)
        self.library.sync_references([file['sha256']], [file['sha256']])
        with self.assertRaisesRegex(ValueError, 'today or later'):
            self.library.remove(file['sha256'])
        self.library.sync_references([file['sha256']], [])
        self.assertTrue(self.library.remove(file['sha256']))

    def test_shorter_retention_gives_existing_unused_file_until_tomorrow(self):
        pdf = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        self.library.import_bytes('notes.pdf', pdf)
        self.library.sync_references([])
        self.library.set_retention('3')
        deadline = datetime.fromisoformat(self.library.list_files()[0]['delete_at'])
        tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
        self.assertEqual(deadline.date(), tomorrow)
        self.library.set_retention('unlimited')
        self.assertIsNone(self.library.list_files()[0]['delete_at'])
        self.library.set_retention('7')
        self.assertEqual(datetime.fromisoformat(self.library.list_files()[0]['delete_at']).date(), tomorrow)
        self.library.set_retention('90')
        self.assertGreater(datetime.fromisoformat(self.library.list_files()[0]['delete_at']).date(), tomorrow)

    def test_read_rechecks_bytes_and_rejects_unindexed_paths(self):
        pdf = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        file = self.library.import_bytes('notes.pdf', pdf)
        path = self.library.verified_file(file['sha256'])
        self.assertEqual(path.read_bytes(), pdf)
        path.write_bytes(b'X' * len(pdf))
        self.assertIsNone(self.library.verified_file(file['sha256']))
        self.assertEqual(self.library.list_files(), [])
        self.assertIsNone(self.library.verified_file('../index.sqlite3'))


class SlideEndpointTests(TestCase):
    def test_allowed_origin_reads_derived_pdf_and_other_origin_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'slide.pdf'
            output.write_bytes(b'%PDF-1.7\n%%EOF\n')
            class Handler(MediaHandler):
                library = type('Library', (), {
                    'slide_pdf': lambda self, sha: output,
                    'allowed_origins': lambda self: frozenset({'https://example.org'}),
                })()
            server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.addCleanup(server.server_close)
            self.addCleanup(server.shutdown)
            url = f'http://127.0.0.1:{server.server_port}/v1/slides/' + 'a' * 64
            def request(origin):
                return urllib.request.Request(url, headers={
                    'Host': '127.0.0.1:63174', 'Origin': origin})
            with urllib.request.urlopen(request('https://example.org')) as response:
                self.assertEqual(response.headers['Content-Type'], 'application/pdf')
                self.assertEqual(response.read(), output.read_bytes())
            with self.assertRaises(urllib.error.HTTPError) as forbidden:
                urllib.request.urlopen(request('https://wrong.example'))
            self.assertEqual(forbidden.exception.code, 403)

class TransferPlanTests(TestCase):
    def setUp(self):
        import threading
        from multimedia.local_transfers import TransferManager
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.library = LocalLibrary(Path(self.temp.name))
        self.manager = TransferManager.__new__(TransferManager)
        self.manager.library = self.library
        self.manager.lock = threading.RLock()
        self.manager.cancel_events = {}
        self.manager.app_origins = ()

    def test_auto_download_plan_persists_without_browser_and_deduplicates(self):
        from multimedia.local_transfers import now
        sha = 'a' * 64
        args = (sha, 'service.pdf', 'pdf', 42,
                'https://account.r2.cloudflarestorage.com/bucket/file?sig=1',
                (now() + timedelta(days=3)).isoformat())
        self.assertIsNone(self.manager.start_download(*args, automatic=True,
                                                       eligible_until='2026-10-21'))
        self.assertIsNone(self.manager.start_download(*args, automatic=True,
                                                       eligible_until='2026-10-22'))
        reopened = LocalLibrary(Path(self.temp.name))
        with reopened._db() as db:
            plans = list(db.execute('SELECT * FROM auto_downloads'))
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]['eligible_until'], '2026-10-22')

    def test_only_r2_https_urls_are_accepted(self):
        from multimedia.local_transfers import validate_url
        for url in ('http://account.r2.cloudflarestorage.com/file',
                    'https://example.com/file', 'file:///tmp/file'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)

    def test_download_verifies_fingerprint_before_exposing_file(self):
        import threading
        pdf = b'%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF\n'
        sha = hashlib.sha256(pdf).hexdigest()
        url = 'https://account.r2.cloudflarestorage.com/bucket/file?sig=1'
        with patch('multimedia.local_transfers.urllib.request.urlopen', return_value=io.BytesIO(b'X' * len(pdf))):
            with self.assertRaisesRegex(IOError, 'fingerprint'):
                self.manager._download(1, sha, 'service.pdf', len(pdf), url, threading.Event())
        self.assertEqual(self.library.list_files(), [])
        self.assertFalse(list(self.library.root.glob('.download-*')))
        with patch('multimedia.local_transfers.urllib.request.urlopen', return_value=io.BytesIO(pdf)):
            self.manager._download(2, sha, 'service.pdf', len(pdf), url, threading.Event())
        self.assertEqual(self.library.list_files()[0]['sha256'], sha)

    def test_restart_records_failed_job_and_preserves_retry_backoff(self):
        from multimedia.local_transfers import now
        sha = 'a' * 64
        url = 'https://account.r2.cloudflarestorage.com/bucket/file?sig=1'
        self.manager.start_download(sha, 'service.pdf', 'pdf', 42, url,
                                    (now() + timedelta(days=3)).isoformat(),
                                    automatic=True, eligible_until='2026-10-22')
        with self.library._db() as db:
            db.execute('INSERT INTO transfers (direction, sha256, name, size, status, automatic, started_at) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)',
                       ('download', sha, 'service.pdf', 42, 'active', 1, now().isoformat()))
        reopened = LocalLibrary(Path(self.temp.name))
        with reopened._db() as db:
            job = db.execute('SELECT status FROM transfers').fetchone()
            plan = db.execute('SELECT attempts, next_attempt FROM auto_downloads').fetchone()
        self.assertEqual(job['status'], 'failed')
        self.assertEqual(plan['attempts'], 1)
        self.assertGreater(datetime.fromisoformat(plan['next_attempt']), now())


class OriginStoreTests(TestCase):
    """The recorded origin set: add/edit/delete with the exact-origin grammar, persisted (spec 192)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.library = LocalLibrary(Path(self.temp.name))

    def test_add_records_and_persists_across_a_library_rebuild(self):
        self.library.add_origin('https://multimedia.example.org')
        self.library.add_origin('https://staging.multimedia.example.org')
        self.assertEqual(self.library.recorded_origins(),
                         ['https://multimedia.example.org', 'https://staging.multimedia.example.org'])
        reopened = LocalLibrary(Path(self.temp.name))
        self.assertEqual(reopened.recorded_origins(), self.library.recorded_origins())

    def test_add_rejects_each_broken_rule_and_records_nothing(self):
        broken = ('https://multimedia.example.org/', 'multimedia.example.org',
                  'https://ex ample.org', 'https://user@host.example',
                  'https://host.example:99999', 'ftp://host.example',
                  'https://multimedia.example.org/path?query')
        for value in broken:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.library.add_origin(value)
        self.assertEqual(self.library.recorded_origins(), [])

    def test_duplicate_add_is_refused(self):
        self.library.add_origin('https://multimedia.example.org')
        with self.assertRaisesRegex(ValueError, 'already recorded'):
            self.library.add_origin('https://multimedia.example.org')
        self.assertEqual(len(self.library.recorded_origins()), 1)

    def test_edit_rewrites_the_slot_and_delete_renumbers(self):
        self.library.add_origin('https://a.example.org')
        self.library.add_origin('https://b.example.org')
        self.library.update_origin(1, 'https://c.example.org')
        self.assertEqual(self.library.recorded_origins(), ['https://c.example.org', 'https://b.example.org'])
        self.library.remove_origin(1)
        self.assertEqual(self.library.recorded_origins(), ['https://b.example.org'])

    def test_out_of_range_slots_are_named_and_change_nothing(self):
        self.library.add_origin('https://a.example.org')
        with self.assertRaisesRegex(ValueError, 'no origin 3 is recorded'):
            self.library.update_origin(3, 'https://b.example.org')
        with self.assertRaisesRegex(ValueError, 'no origin 3 is recorded'):
            self.library.remove_origin(3)
        with self.assertRaisesRegex(ValueError, 'no origin 0 is recorded'):
            self.library.remove_origin(0)
        self.assertEqual(self.library.recorded_origins(), ['https://a.example.org'])

    def test_allowed_origins_is_the_env_seeds_plus_the_recorded_set(self):
        library = LocalLibrary(Path(self.temp.name), app_origins=('http://localhost:63404',))
        library.add_origin('https://multimedia.example.org')
        self.assertEqual(library.allowed_origins(),
                         frozenset({'http://localhost:63404', 'https://multimedia.example.org'}))
        self.assertEqual(library.recorded_origins(), ['https://multimedia.example.org'])


class ConfigSurfaceTests(TestCase):
    """The companion's own page and config endpoints (spec 192): loopback Host,
    own-or-absent Origin, no media token — reachable with an empty recorded set."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.library = LocalLibrary(Path(self.temp.name), app_origins=('http://localhost:63404',))

        class Handler(MediaHandler):
            library = self.library

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base = f'http://127.0.0.1:{self.server.server_port}'

    def _request(self, path, origin='__absent__', host='127.0.0.1:63174', method='GET', data=None):
        headers = {'Host': host}
        if origin != '__absent__':
            headers['Origin'] = origin
        req = urllib.request.Request(self.base + path, data=data, headers=headers, method=method)
        try:
            return urllib.request.urlopen(req)
        except urllib.error.HTTPError as exc:
            return exc

    def test_page_is_served_with_an_empty_recorded_set(self):
        with self._request('/') as response:
            self.assertEqual(getattr(response, 'code', None), 200)
            self.assertIn('Media companion', response.read().decode())

    def test_page_is_served_on_the_localhost_host_form(self):
        self.assertEqual(getattr(self._request('/', host='localhost:63174'), 'code', None), 200)

    def test_page_is_refused_on_a_foreign_host(self):
        self.assertEqual(getattr(self._request('/', host='evil.example:63174'), 'code', None), 403)

    def test_config_endpoints_need_no_media_token(self):
        with self._request('/v1/origins', origin='http://127.0.0.1:63174') as response:
            self.assertEqual(getattr(response, 'code', None), 200)
            self.assertEqual(json.load(response), {'recorded': [], 'seeds': ['http://localhost:63404']})

    def test_config_endpoints_refuse_a_foreign_origin(self):
        response = self._request('/v1/origins', origin='https://evil.example')
        self.assertEqual(getattr(response, 'code', None), 403)

    def test_refused_request_names_the_page_and_sends_no_cors_header(self):
        response = self._request('/v1/status', origin='https://unrecorded.example')
        self.assertEqual(getattr(response, 'code', None), 403)
        payload = json.loads(response.read())
        self.assertIn('127.0.0.1:63174', payload['error'])
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

    def test_enforcement_sees_a_runtime_recorded_origin_without_a_restart(self):
        refused = self._request('/v1/status', origin='https://multimedia.example.org')
        self.assertEqual(getattr(refused, 'code', None), 403)
        self.library.add_origin('https://multimedia.example.org')
        with self._request('/v1/status', origin='https://multimedia.example.org') as response:
            self.assertEqual(getattr(response, 'code', None), 200)

    def test_local_seeds_pass_with_nothing_recorded(self):
        with self._request('/v1/status', origin='http://localhost:63404') as response:
            self.assertEqual(getattr(response, 'code', None), 200)

    def test_origin_add_edit_delete_through_http(self):
        def add(value):
            return self._request('/v1/origins', origin='http://127.0.0.1:63174', method='POST',
                                 data=json.dumps({'origin': value}).encode())
        with add('https://a.example.org') as response:
            self.assertEqual(getattr(response, 'code', None), 200)
            self.assertEqual(json.load(response)['recorded'], ['https://a.example.org'])
        response = add('https://b.example.org/')
        self.assertEqual(getattr(response, 'code', None), 400)
        self.assertIn('path', json.loads(response.read())['error'])
        self.library.add_origin('https://b.example.org')
        response = add('https://b.example.org')
        self.assertEqual(getattr(response, 'code', None), 409)
        self.assertEqual(json.loads(response.read())['error'], 'that origin is already recorded')

        with self._request('/v1/origins/1', origin='http://127.0.0.1:63174', method='PUT',
                           data=json.dumps({'origin': 'https://c.example.org'}).encode()) as response:
            self.assertEqual(getattr(response, 'code', None), 200)
            self.assertEqual(json.load(response)['recorded'],
                             ['https://c.example.org', 'https://b.example.org'])
        response = self._request('/v1/origins/9', origin='http://127.0.0.1:63174', method='PUT',
                                 data=json.dumps({'origin': 'https://d.example.org'}).encode())
        self.assertEqual(getattr(response, 'code', None), 404)
        self.assertEqual(json.loads(response.read())['error'], 'no origin 9 is recorded')

        with self._request('/v1/origins/2', origin='http://127.0.0.1:63174', method='DELETE') as response:
            self.assertEqual(getattr(response, 'code', None), 200)
            self.assertEqual(json.load(response)['recorded'], ['https://c.example.org'])
        response = self._request('/v1/origins/9', origin='http://127.0.0.1:63174', method='DELETE')
        self.assertEqual(getattr(response, 'code', None), 404)

    def test_font_view_lists_directories_with_family_counts(self):
        fonts_dir = Path(self.temp.name) / 'host-fonts'
        fonts_dir.mkdir()
        (fonts_dir / 'face.ttf').write_bytes(b'not a real font')
        class Handler(MediaHandler):
            library = self.library
            font_view = lambda self: [{'path': str(fonts_dir), 'source': 'C:/Windows/Fonts', 'families': 214}]
        self.server.RequestHandlerClass = Handler  # not used; the subclass below is what runs
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        with urllib.request.urlopen(urllib.request.Request(
                f'http://127.0.0.1:{server.server_port}/v1/fonts', headers={
                    'Host': '127.0.0.1:63174', 'Origin': 'http://127.0.0.1:63174'})) as response:
            payload = json.load(response)
        self.assertEqual(payload, {'directories': [
            {'path': str(fonts_dir), 'source': 'C:/Windows/Fonts', 'families': 214}]})

    def test_fc_list_failure_yields_zero_families_for_every_directory(self):
        fonts_dir = Path(self.temp.name) / 'host-fonts'
        fonts_dir.mkdir()
        with patch('multimedia.local_media.fc_listing', side_effect=OSError('no fontconfig')):
            directories = font_directories(mounts=[(fonts_dir, 'C:/Windows/Fonts')])
        self.assertEqual([entry['families'] for entry in directories], [0])


class FontListingTests(TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.host_dir = Path(self.temp.name) / 'host' / '1'
        self.host_dir.mkdir(parents=True)
        self.operator_dir = Path(self.temp.name) / 'operator'
        self.operator_dir.mkdir()
        self.mounts = [(self.host_dir, 'C:/Windows/Fonts'), (self.operator_dir, '.fonts/')]

    def test_families_group_by_directory_and_deduplicate(self):
        listing = ('/usr/share/fonts/host/1/A.ttf\nArial\n'
                   '/usr/share/fonts/host/1/B.ttf\nArial\n'
                   '/usr/share/fonts/host/1/C.ttf\nCambria\n'
                   '/usr/share/fonts/operator/D.ttf\nBritannic Bold\n')
        counts = families_by_directory(listing)
        self.assertEqual(counts['/usr/share/fonts/host/1'], {'Arial', 'Cambria'})
        self.assertEqual(counts['/usr/share/fonts/operator'], {'Britannic Bold'})

    def test_font_directories_uses_the_injected_listing_and_the_launcher_labels(self):
        listing = (f'{self.host_dir}/A.ttf\nArial\n'
                   f'{self.host_dir}/B.ttf\nArial\n'
                   f'{self.operator_dir}/D.ttf\nBritannic Bold\n')
        with patch.dict(os.environ, {'GKPS_MEDIA_FONT_LABELS': '1=C:/Windows/Fonts'}):
            directories = font_directories(lambda: listing, mounts=self.mounts)
        self.assertEqual(directories, [
            {'path': str(self.host_dir), 'source': 'C:/Windows/Fonts', 'families': 1},
            {'path': str(self.operator_dir), 'source': '.fonts/', 'families': 1},
        ])

    def test_a_failed_fc_list_yields_zero_families_for_every_directory(self):
        with patch('multimedia.local_media.fc_listing', side_effect=OSError('no fontconfig')):
            directories = font_directories(mounts=self.mounts)
        self.assertEqual([entry['families'] for entry in directories], [0, 0])
