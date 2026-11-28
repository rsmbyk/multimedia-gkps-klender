"""Run GKPS tests against the isolated compose Postgres used by spec 256.

Usage: python run-tests.py <test-label> [more labels...]
The credential is read from the running compose web container at call time and
never written to disk or printed.
"""

import os
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

BASE = '/home/rsmbyk/Projects/multimedia-gkps-klender'
WORKTREE = '/home/rsmbyk/Projects/multimedia-gkps-klender-256'
DB_NAME = 'gkps256'
VENV_PYTHON = os.path.join(BASE, '.venv/bin/python')

if os.path.realpath(sys.executable) != os.path.realpath(VENV_PYTHON):
    os.execv(VENV_PYTHON, [VENV_PYTHON, __file__, *sys.argv[1:]])

raw = subprocess.check_output(
    ['docker', 'compose', 'exec', '-T', 'web', 'printenv', 'DATABASE_URL'],
    cwd=BASE, text=True).strip()
port = subprocess.check_output(
    ['docker', 'compose', 'port', 'db', '5432'], cwd=BASE,
    text=True).strip().splitlines()[-1].rsplit(':', 1)[-1]
parts = urlsplit(raw)
netloc = parts.netloc.replace('db:5432', f'127.0.0.1:{port}')
os.environ['DATABASE_URL'] = urlunsplit(
    (parts.scheme, netloc, '/' + DB_NAME, parts.query, parts.fragment))
os.environ['DJANGO_SETTINGS_MODULE'] = 'multimedia.settings'
os.chdir(WORKTREE)
sys.path.insert(0, WORKTREE)

from django.core.management import execute_from_command_line

execute_from_command_line(
    ['manage.py', 'test', *sys.argv[1:], '--noinput', '--keepdb', '--verbosity=2'])
