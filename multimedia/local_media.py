"""Per-computer media store and loopback companion for spec 103.

Run with ``python -m multimedia.local_media``. The server never exposes paths
outside its own data root and never puts binary payloads through Vercel.
"""

import hashlib
import io
import json
import os
import secrets
import sqlite3
import sys
import tempfile
import zipfile
from xml.etree import ElementTree
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, urlsplit

MAX_BYTES = 200_000_000
PORT = 63174


class InvalidMedia(ValueError):
    pass


def default_root():
    configured_root = os.environ.get('GKPS_MEDIA_LIBRARY_ROOT')
    if configured_root:
        root = Path(configured_root).expanduser()
        if not root.is_absolute():
            raise ValueError('GKPS_MEDIA_LIBRARY_ROOT must be an absolute path.')
        return root
    if sys.platform == 'win32':
        return Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData' / 'Local') / 'GKPS Klender' / 'Media Library'
    if sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Application Support' / 'GKPS Klender' / 'Media Library'
    data_home = os.environ.get('XDG_DATA_HOME')
    return (Path(data_home) if data_home and Path(data_home).is_absolute()
            else Path.home() / '.local' / 'share') / 'gkps-klender' / 'media-library'


def parse_allowed_origins(value):
    """Parse exact browser origins; paths, wildcards, and malformed URLs fail closed."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Set GKPS_MEDIA_ALLOWED_ORIGINS to exact app origins before starting.')
    origins = value.split(',')
    parsed_origins = set()
    for raw_origin in origins:
        origin = raw_origin.strip()
        if not origin or any(char.isspace() for char in origin):
            raise ValueError('GKPS_MEDIA_ALLOWED_ORIGINS contains an invalid origin.')
        try:
            parsed = urlsplit(origin)
            # Accessing .port also validates malformed or out-of-range ports.
            parsed.port
        except ValueError as exc:
            raise ValueError('GKPS_MEDIA_ALLOWED_ORIGINS contains an invalid origin.') from exc
        if (parsed.scheme not in {'http', 'https'} or not parsed.hostname
                or parsed.username is not None or parsed.password is not None
                or parsed.path or parsed.query or parsed.fragment
                or origin != f'{parsed.scheme}://{parsed.netloc}'):
            raise ValueError('GKPS_MEDIA_ALLOWED_ORIGINS must contain exact origins without paths.')
        parsed_origins.add(origin)
    return frozenset(parsed_origins)


def detect_family(path):
    """Inspect container signatures; filename and browser MIME are untrusted."""
    with path.open('rb') as stream:
        head = stream.read(256)
        stream.seek(max(0, path.stat().st_size - 4096))
        tail = stream.read()
    if head.startswith(b'%PDF-') and b'%%EOF' in tail:
        return 'pdf'
    if head.startswith(b'\x89PNG\r\n\x1a\n') and b'IEND' in tail:
        return 'image'
    if head.startswith(b'\xff\xd8\xff') and tail.rstrip().endswith(b'\xff\xd9'):
        return 'image'
    if head.startswith((b'GIF87a', b'GIF89a')) and tail.rstrip().endswith(b';'):
        return 'image'
    if head.startswith(b'RIFF') and head[8:12] == b'WEBP' and int.from_bytes(head[4:8], 'little') + 8 <= path.stat().st_size:
        return 'image'
    if head.startswith(b'BM') and int.from_bytes(head[2:6], 'little') == path.stat().st_size:
        return 'image'
    if head.startswith((b'II*\x00', b'MM\x00*')):
        return 'image'
    if head.startswith(b'ID3') or (len(head) > 2 and head[0] == 255 and head[1] & 224 == 224):
        return 'audio'
    if head.startswith(b'fLaC'):
        return 'audio'
    if head.startswith(b'OggS'):
        return 'video' if b'theora' in head else 'audio'
    if head.startswith(b'RIFF') and head[8:12] == b'WAVE':
        return 'audio'
    if head.startswith(b'RIFF') and head[8:12] == b'AVI ':
        return 'video'
    if head.startswith(b'\x1a\x45\xdf\xa3'):
        return 'video'
    if head[4:8] == b'ftyp':
        if head[8:12] in (b'avif', b'avis', b'heic', b'heix', b'hevc', b'hevx', b'mif1', b'msf1'):
            return 'image'
        return 'audio' if b'M4A' in head[8:24] else 'video'
    if head.startswith((b'\x00\x00\x01\xba', b'\x00\x00\x01\xb3')):
        return 'video'
    if head.startswith(b'PK\x03\x04'):
        try:
            with zipfile.ZipFile(path) as archive:
                names = ('[Content_Types].xml', 'ppt/presentation.xml')
                if all(name in archive.namelist() and archive.getinfo(name).file_size <= 2_000_000
                       for name in names):
                    content_types = ElementTree.fromstring(archive.read(names[0]))
                    presentation = ElementTree.fromstring(archive.read(names[1]))
                    if (content_types.tag.endswith('}Types')
                            and presentation.tag.endswith('}presentation')
                            and any('presentationml.presentation.main+xml' in element.attrib.get('ContentType', '')
                                    for element in content_types)):
                        return 'slides'
        except (zipfile.BadZipFile, ElementTree.ParseError, RuntimeError):
            pass
    if head.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'):
        marker = 'PowerPoint Document'.encode('utf-16le')
        with path.open('rb') as stream:
            overlap = b''
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                if marker in overlap + block:
                    return 'slides'
                overlap = block[-len(marker):]
    raise InvalidMedia('This file type is not supported or the file is malformed.')


class LocalLibrary:
    def __init__(self, root=None):
        self.root = Path(root or default_root()).expanduser().resolve()
        self.files_dir = self.root / 'files'
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.root / 'index.sqlite3'
        with self._db() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS files (
                sha256 TEXT PRIMARY KEY, name TEXT NOT NULL, family TEXT NOT NULL,
                size INTEGER NOT NULL, uploaded_at TEXT NOT NULL,
                unused_since TEXT, delete_at TEXT)''')
            db.execute('''CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY, value TEXT NOT NULL)''')

    @contextmanager
    def _db(self):
        db = sqlite3.connect(self.db_path)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def list_files(self):
        with self._db() as db:
            rows = [dict(row) for row in db.execute('SELECT * FROM files ORDER BY uploaded_at DESC, sha256')]
        return [row for row in rows if self.verified_file(row['sha256']) is not None]

    def retention(self):
        with self._db() as db:
            row = db.execute("SELECT value FROM settings WHERE key='retention'").fetchone()
        return row['value'] if row else '30'

    def set_retention(self, value):
        if value not in {'3', '7', '30', '90', 'unlimited'}:
            raise ValueError('Choose 3, 7, 30, 90 days, or unlimited.')
        old = self.retention()
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        with self._db() as db:
            db.execute("INSERT OR REPLACE INTO settings VALUES ('retention', ?)", (value,))
            if value != 'unlimited':
                for row in list(db.execute('SELECT sha256, unused_since, delete_at FROM files WHERE unused_since IS NOT NULL')):
                    planned = datetime.fromisoformat(row['unused_since']) + timedelta(days=int(value))
                    previous = datetime.fromisoformat(row['delete_at']) if row['delete_at'] else None
                    if old == 'unlimited':
                        deadline = tomorrow
                    elif int(value) < int(old):
                        deadline = (tomorrow if previous and previous - now > timedelta(days=int(value))
                                    else min(previous, planned) if previous else planned)
                    else:
                        deadline = planned
                    db.execute('UPDATE files SET delete_at=? WHERE sha256=?', (deadline.isoformat(), row['sha256']))
            else:
                db.execute('UPDATE files SET delete_at=NULL WHERE unused_since IS NOT NULL')

    def sync_references(self, used_hashes):
        """Only a fresh complete server inventory authorizes automatic deletion."""
        used = set(used_hashes)
        if any(len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha) for sha in used):
            raise ValueError('Invalid reference inventory.')
        now = datetime.now(timezone.utc)
        retention = self.retention()
        with self._db() as db:
            for row in list(db.execute('SELECT * FROM files')):
                sha = row['sha256']
                if sha in used:
                    db.execute('UPDATE files SET unused_since=NULL, delete_at=NULL WHERE sha256=?', (sha,))
                    continue
                since = datetime.fromisoformat(row['unused_since']) if row['unused_since'] else now
                deadline = (datetime.fromisoformat(row['delete_at']) if row['delete_at']
                            else since + timedelta(days=int(retention)) if retention != 'unlimited' else None)
                if deadline and deadline <= now:
                    (self.files_dir / sha).unlink(missing_ok=True)
                    db.execute('DELETE FROM files WHERE sha256=?', (sha,))
                else:
                    db.execute('UPDATE files SET unused_since=?, delete_at=? WHERE sha256=?',
                               (since.isoformat(), deadline.isoformat() if deadline else None, sha))

    def import_bytes(self, filename, payload):
        return self.import_stream(filename, io.BytesIO(payload), len(payload))

    def _stage_stream(self, filename, source, size):
        if not isinstance(filename, str) or not filename or filename in ('.', '..') or '/' in filename or '\\' in filename:
            raise InvalidMedia('A plain filename is required.')
        if len(filename) > 255:
            raise InvalidMedia('The filename is too long.')
        if not 0 < size <= MAX_BYTES:
            raise InvalidMedia('A file must be between 1 byte and 200 MB.')
        digest = hashlib.sha256()
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=self.root, prefix='.import-', delete=False) as target:
                temp_path = Path(target.name)
                remaining = size
                while remaining:
                    block = source.read(min(1024 * 1024, remaining))
                    if not block:
                        raise InvalidMedia('The file ended before the declared size.')
                    target.write(block)
                    digest.update(block)
                    remaining -= len(block)
                target.flush()
                os.fsync(target.fileno())
            family = detect_family(temp_path)
            sha = digest.hexdigest()
            return temp_path, sha, family
        except Exception:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
            raise

    def inspect_stream(self, filename, source, size):
        temp_path, sha, family = self._stage_stream(filename, source, size)
        try:
            with self._db() as db:
                saved = db.execute('SELECT * FROM files WHERE sha256=?', (sha,)).fetchone()
            if saved and self.verified_file(sha):
                return {**dict(saved), 'reused': True}
            return {'sha256': sha, 'name': filename, 'family': family, 'size': size, 'reused': False}
        finally:
            temp_path.unlink(missing_ok=True)

    def import_stream(self, filename, source, size):
        temp_path, sha, family = self._stage_stream(filename, source, size)
        try:
            with self._db() as db:
                saved = db.execute('SELECT * FROM files WHERE sha256=?', (sha,)).fetchone()
                if saved and self.verified_file(sha):
                    return {**dict(saved), 'reused': True}
                destination = self.files_dir / sha
                os.replace(temp_path, destination)
                temp_path = None
                uploaded = datetime.now(timezone.utc).isoformat()
                db.execute('INSERT OR REPLACE INTO files (sha256, name, family, size, uploaded_at) VALUES (?, ?, ?, ?, ?)',
                           (sha, filename, family, size, uploaded))
                return {**dict(db.execute('SELECT * FROM files WHERE sha256=?', (sha,)).fetchone()),
                        'reused': False}
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def remove(self, sha):
        with self._db() as db:
            row = db.execute('SELECT sha256 FROM files WHERE sha256=?', (sha,)).fetchone()
            if not row:
                return False
            (self.files_dir / sha).unlink(missing_ok=True)
            db.execute('DELETE FROM files WHERE sha256=?', (sha,))
            return True

    def verified_file(self, sha):
        """Return only indexed bytes that still match their saved identity."""
        if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            return None
        with self._db() as db:
            row = db.execute('SELECT size FROM files WHERE sha256=?', (sha,)).fetchone()
        path = self.files_dir / sha
        if not row or not path.is_file() or path.stat().st_size != row['size']:
            return None
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        return path if digest.hexdigest() == sha else None


class MediaHandler(BaseHTTPRequestHandler):
    library = None
    origins = frozenset()
    token = ''

    def _allowed(self):
        origin = self.headers.get('Origin')
        host = self.headers.get('Host', '')
        return host in (f'127.0.0.1:{PORT}', f'localhost:{PORT}') and origin in self.origins

    def _reply(self, status, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        if self._allowed():
            self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
            self.send_header('Vary', 'Origin')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        if not self._allowed():
            return self._reply(403, {'error': 'Origin is not allowed.'})
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-GKPS-Media-Token, X-GKPS-Filename')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Vary', 'Origin')
        self.end_headers()

    def do_GET(self):
        if not self._allowed():
            return self._reply(403, {'error': 'Origin is not allowed.'})
        path = urlparse(self.path).path
        if path == '/v1/status':
            return self._reply(200, status_payload(self.library, self.token))
        if path == '/v1/files':
            return self._reply(200, {'files': self.library.list_files()})
        if path.startswith('/v1/files/'):
            file = self.library.verified_file(path.removeprefix('/v1/files/'))
            if file is None:
                return self._reply(404, {'error': 'File not available.'})
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(file.stat().st_size))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
            self.send_header('Vary', 'Origin')
            self.end_headers()
            with file.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    self.wfile.write(block)
            return
        return self._reply(404, {'error': 'Not found.'})

    def do_POST(self):
        if not self._allowed() or not secrets.compare_digest(
                self.headers.get('X-GKPS-Media-Token', ''), self.token):
            return self._reply(403, {'error': 'Not authorized.'})
        path = urlparse(self.path).path
        if path == '/v1/settings' or path == '/v1/references':
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 1000000:
                    raise ValueError('Invalid request size.')
                payload = json.loads(self.rfile.read(length))
                if path == '/v1/settings':
                    self.library.set_retention(str(payload['retention']))
                    return self._reply(200, {'retention': self.library.retention()})
                self.library.sync_references(payload['hashes'])
                return self._reply(200, {'files': self.library.list_files()})
            except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                return self._reply(400, {'error': str(exc)})
        if path not in ('/v1/import', '/v1/inspect'):
            return self._reply(404, {'error': 'Not found.'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            operation = self.library.inspect_stream if path == '/v1/inspect' else self.library.import_stream
            result = operation(self.headers.get('X-GKPS-Filename', ''), self.rfile, size)
        except (ValueError, InvalidMedia) as exc:
            return self._reply(400, {'error': str(exc)})
        return self._reply(200, result)

    def do_DELETE(self):
        if not self._allowed() or not secrets.compare_digest(
                self.headers.get('X-GKPS-Media-Token', ''), self.token):
            return self._reply(403, {'error': 'Not authorized.'})
        path = urlparse(self.path).path
        if not path.startswith('/v1/files/'):
            return self._reply(404, {'error': 'Not found.'})
        sha = path.removeprefix('/v1/files/')
        if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            return self._reply(400, {'error': 'Invalid fingerprint.'})
        return self._reply(200, {'removed': self.library.remove(sha)})


def status_payload(library, token):
    files = library.list_files()
    return {'connection': 'connected', 'file_count': len(files),
            'total_size': sum(file['size'] for file in files),
            'retention': library.retention(), 'write_token': token}


def main():
    try:
        origins = parse_allowed_origins(os.environ.get('GKPS_MEDIA_ALLOWED_ORIGINS', ''))
        library = LocalLibrary()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    MediaHandler.library = library
    MediaHandler.origins = origins
    MediaHandler.token = secrets.token_urlsafe(32)
    server = ThreadingHTTPServer(('0.0.0.0', PORT), MediaHandler)
    print(f'Media Library companion listening on container port {PORT}', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
