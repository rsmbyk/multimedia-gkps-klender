#!/usr/bin/env python3
"""Run manage.py in this slice's worktree against the compose Postgres, without printing secrets."""
import os
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
VENV_PY = '/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python'
PORT = subprocess.check_output(
    ['docker', 'port', 'multimedia-gkps-klender-db-1', '5432/tcp'],
    text=True).splitlines()[-1].split(':')[-1].strip()
raw = subprocess.check_output(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'printenv', 'DATABASE_URL'],
    text=True).strip()
parts = urlsplit(raw)
netloc = f'{parts.username}:{parts.password}@127.0.0.1:{PORT}'
env = dict(os.environ, DATABASE_URL=urlunsplit((parts.scheme, netloc, parts.path, '', '')))
os.chdir(REPO)
sys.exit(subprocess.call([VENV_PY, 'manage.py', *sys.argv[1:]], env=env))
