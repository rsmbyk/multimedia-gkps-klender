#!/usr/bin/env python3
"""Run a command with the local compose database URL, without printing credentials.

The URL is read from the web container at run time; the password is never written to a
file or shown in output. For tests the database name is switched to a throwaway one so
parallel agent sessions cannot lock the same test database.

    python3 preview/run_local.py -- <command> ...
    GKPS_DB=gkps245 python3 preview/run_local.py -- ../multimedia-gkps-klender/.venv/bin/python manage.py test ...
"""
import os
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit, urlunsplit

CONTAINER = 'multimedia-gkps-klender-web-1'
DB_CONTAINER = 'multimedia-gkps-klender-db-1'


def mapped_db_port():
    out = subprocess.check_output(['docker', 'port', DB_CONTAINER, '5432/tcp'], text=True)
    match = re.search(r'(?:127\.0\.0\.1|0\.0\.0\.0):(\d+)', out)
    if not match:
        raise RuntimeError('no host port published for the compose db service')
    return match.group(1)


def database_url():
    raw = subprocess.check_output(
        ['docker', 'exec', CONTAINER, 'python', '-c',
         'import os; print(os.environ["DATABASE_URL"])'], text=True).strip()
    parsed = urlsplit(raw)
    user = unquote(parsed.username or '')
    password = unquote(parsed.password or '')
    host = '127.0.0.1'
    port = mapped_db_port()
    name = os.environ.get('GKPS_DB') or (parsed.path.lstrip('/') or 'multimedia')
    return urlunsplit((parsed.scheme, f'{user}:{password}@{host}:{port}',
                       '/' + name, parsed.query, parsed.fragment))


def main():
    if len(sys.argv) < 2 or sys.argv[1] != '--':
        raise SystemExit('usage: run_local.py -- <command> ...')
    env = os.environ.copy()
    env['DATABASE_URL'] = database_url()
    raise SystemExit(subprocess.call(sys.argv[2:], env=env))


if __name__ == '__main__':
    main()
