"""Focused local-library tests for spec 103."""

import hashlib
import io
import os
import zipfile
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from multimedia.local_media import (
    LocalLibrary,
    InvalidMedia,
    parse_allowed_origins,
    status_payload,
)


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
