"""Durable, companion-owned single-request R2 transfers."""

import hashlib
import http.client
import os
import tempfile
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit


def now():
    return datetime.now(timezone.utc)


def validate_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password
            or not parsed.hostname.endswith('.r2.cloudflarestorage.com')):
        raise ValueError('Only an HTTPS R2 transfer URL is accepted.')
    return parsed


class Cancelled(Exception):
    pass


class TransferManager:
    def __init__(self, library):
        self.library = library
        self.cancel_events = {}
        self.lock = threading.RLock()
        self.thread = threading.Thread(target=self._schedule, daemon=True)
        self.thread.start()

    def list(self):
        with self.library._db() as db:
            rows = [dict(row) for row in db.execute(
                "SELECT * FROM transfers ORDER BY CASE WHEN status='active' THEN 0 ELSE 1 END, "
                "CASE WHEN status='active' THEN started_at ELSE ended_at END DESC, id DESC")]
            retrying = [dict(row) for row in db.execute('SELECT sha256, next_attempt FROM auto_downloads')]
        return {'transfers': rows, 'retrying': retrying}

    def _insert(self, direction, sha, name, size, automatic=False):
        with self.library._db() as db:
            active = db.execute("SELECT id FROM transfers WHERE sha256=? AND direction=? AND status='active'",
                                (sha, direction)).fetchone()
            if active:
                return active['id'], False
            cursor = db.execute(
                'INSERT INTO transfers (direction, sha256, name, size, status, automatic, started_at) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (direction, sha, name, size, 'active', int(automatic), now().isoformat()))
            return cursor.lastrowid, True

    def _run(self, job_id, direction, sha, name, size, url, automatic,
             complete_url=None, completion_token=None):
        event = threading.Event()
        with self.lock:
            self.cancel_events[job_id] = event
        def worker():
            error, status, permanent = None, 'completed', False
            try:
                if direction == 'upload':
                    self._upload(job_id, sha, size, url, event)
                    self._complete_upload(sha, complete_url, completion_token)
                else:
                    self._download(job_id, sha, name, size, url, event)
            except Cancelled:
                status = 'cancelled'
            except Exception as exc:
                status, error = 'failed', str(exc)[:500]
                permanent = isinstance(exc, urllib.error.HTTPError) and exc.code == 404
            finally:
                with self.library._db() as db:
                    db.execute('UPDATE transfers SET status=?, ended_at=?, error=? WHERE id=?',
                               (status, now().isoformat(), error, job_id))
                    if direction == 'download' and automatic:
                        if status == 'completed' or permanent:
                            db.execute('DELETE FROM auto_downloads WHERE sha256=?', (sha,))
                        else:
                            row = db.execute('SELECT attempts, expires_at FROM auto_downloads WHERE sha256=?',
                                             (sha,)).fetchone()
                            if row:
                                attempts = row['attempts'] + 1
                                delay = min(300, 5 * (2 ** min(attempts - 1, 6)))
                                # Deterministic per-identity jitter prevents synchronized retries.
                                delay += int(sha[:2], 16) % 5
                                db.execute('UPDATE auto_downloads SET attempts=?, next_attempt=? WHERE sha256=?',
                                           (attempts, (now() + timedelta(seconds=delay)).isoformat(), sha))
                with self.lock:
                    self.cancel_events.pop(job_id, None)
        threading.Thread(target=worker, daemon=True).start()

    def _progress(self, job_id, count):
        with self.library._db() as db:
            db.execute('UPDATE transfers SET bytes_done=? WHERE id=?', (count, job_id))

    def start_upload(self, sha, url, complete_url, completion_token):
        validate_url(url)
        parsed = urlsplit(complete_url)
        origin = parsed.scheme + '://' + parsed.netloc
        if origin not in self.library.allowed_origins() or parsed.path != f'/media-library/cloud/{sha}/complete/':
            raise ValueError('Upload completion endpoint is not allowed.')
        if not completion_token or len(completion_token) > 256:
            raise ValueError('Upload completion token is missing.')
        file = self.library.verified_file(sha)
        if file is None:
            raise ValueError('This file is not available on this computer.')
        with self.library._db() as db:
            row = db.execute('SELECT name, size FROM files WHERE sha256=?', (sha,)).fetchone()
        with self.lock:
            job_id, created = self._insert('upload', sha, row['name'], row['size'])
            if created:
                self._run(job_id, 'upload', sha, row['name'], row['size'], url, False,
                          complete_url, completion_token)
        return job_id

    def _complete_upload(self, sha, url, token):
        parsed = urlsplit(url)
        if parsed.hostname in ('localhost', '127.0.0.1'):
            origin = os.environ.get('GKPS_MEDIA_SERVER_ORIGIN', 'http://web:8000').rstrip('/')
            url = origin + parsed.path
        request = urllib.request.Request(url, data=b'', method='POST',
                                         headers={'Authorization': 'Bearer ' + token})
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise IOError('Upload verification failed.')

    def start_download(self, sha, name, family, size, url, expires_at, automatic=False,
                       eligible_until=None):
        validate_url(url)
        if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            raise ValueError('Invalid fingerprint.')
        if not 0 < size <= 200_000_000:
            raise ValueError('Invalid file size.')
        expiry = datetime.fromisoformat(expires_at)
        if expiry <= now():
            raise ValueError('Online availability has expired.')
        if self.library.verified_file(sha):
            return None
        if automatic:
            if not eligible_until:
                raise ValueError('Automatic download needs its service eligibility date.')
            from datetime import date
            date.fromisoformat(eligible_until)
            with self.library._db() as db:
                db.execute('INSERT OR IGNORE INTO auto_downloads '
                           '(sha256, name, family, size, url, expires_at, next_attempt, eligible_until) '
                           'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           (sha, name, family, size, url, expires_at, now().isoformat(), eligible_until))
                db.execute('UPDATE auto_downloads SET url=?, expires_at=?, eligible_until=? WHERE sha256=?',
                           (url, expires_at, eligible_until, sha))
            return None  # The scheduler honors the persisted backoff, including after reload.
        with self.lock:
            job_id, created = self._insert('download', sha, name, size, automatic)
            if created:
                self._run(job_id, 'download', sha, name, size, url, automatic)
        return job_id

    def cancel(self, job_id):
        with self.lock:
            event = self.cancel_events.get(job_id)
            if not event:
                return False
            with self.library._db() as db:
                row = db.execute('SELECT automatic, direction FROM transfers WHERE id=?', (job_id,)).fetchone()
            if row and row['direction'] == 'download' and row['automatic']:
                raise ValueError('Automatic downloads cannot be cancelled.')
            event.set()
            return True

    def _upload(self, job_id, sha, size, url, event):
        parsed = validate_url(url)
        connection = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=60)
        path = parsed.path + ('?' + parsed.query if parsed.query else '')
        try:
            connection.putrequest('PUT', path)
            connection.putheader('Content-Length', str(size))
            connection.putheader('Content-Type', 'application/octet-stream')
            connection.endheaders()
            sent = 0
            with (self.library.files_dir / sha).open('rb') as stream:
                while True:
                    if event.is_set():
                        raise Cancelled()
                    block = stream.read(1024 * 1024)
                    if not block:
                        break
                    connection.send(block)
                    sent += len(block)
                    self._progress(job_id, sent)
            response = connection.getresponse()
            if response.status not in (200, 201, 204):
                raise IOError(f'R2 upload returned HTTP {response.status}.')
            if event.is_set():
                raise Cancelled()
        finally:
            connection.close()

    def _download(self, job_id, sha, name, size, url, event):
        validate_url(url)
        temp_path = None
        try:
            digest = hashlib.sha256()
            with tempfile.NamedTemporaryFile(dir=self.library.root, prefix='.download-', delete=False) as target:
                temp_path = Path(target.name)
                with urllib.request.urlopen(url, timeout=60) as source:
                    received = 0
                    while True:
                        if event.is_set():
                            raise Cancelled()
                        block = source.read(1024 * 1024)
                        if not block:
                            break
                        received += len(block)
                        if received > size:
                            raise IOError('Downloaded file exceeds the expected size.')
                        target.write(block)
                        digest.update(block)
                        self._progress(job_id, received)
                target.flush()
                os.fsync(target.fileno())
            if received != size or digest.hexdigest() != sha:
                raise IOError('Downloaded bytes do not match the file fingerprint.')
            if event.is_set():
                raise Cancelled()
            with temp_path.open('rb') as source:
                imported = self.library.import_stream(name, source, size)
            if imported['sha256'] != sha:
                raise IOError('Local import did not preserve the fingerprint.')
        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)

    def _schedule(self):
        while True:
            try:
                with self.library._db() as db:
                    due = [dict(row) for row in db.execute(
                        'SELECT * FROM auto_downloads WHERE next_attempt<=?', (now().isoformat(),))]
                for task in due:
                    from zoneinfo import ZoneInfo
                    if (datetime.fromisoformat(task['expires_at']) <= now() or
                            task['eligible_until'] and task['eligible_until'] < now().astimezone(ZoneInfo('Asia/Jakarta')).date().isoformat() or
                            self.library.verified_file(task['sha256'])):
                        with self.library._db() as db:
                            db.execute('DELETE FROM auto_downloads WHERE sha256=?', (task['sha256'],))
                        continue
                    with self.lock:
                        job_id, created = self._insert('download', task['sha256'], task['name'], task['size'], True)
                        if created:
                            self._run(job_id, 'download', task['sha256'], task['name'], task['size'], task['url'], True)
            except Exception:
                pass
            time.sleep(1)
