"""Create and migrate the dedicated preview database for spec 234.

Credentials are read from the running compose web container at run time; none are
stored in this file. Usage:

    ../.venv/bin/python specs/234-open-created-template/preview/setup_db.py gkps234
"""
import os
import subprocess
import sys
from urllib.parse import quote, urlsplit

VENV_PYTHON = '/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python'
WORKTREE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

raw = subprocess.check_output(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'python', '-c',
     "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
db_name = sys.argv[1] if len(sys.argv) > 1 else 'gkps234'
user = p.username or 'multimedia'
password = p.password or ''
local_url = f"{p.scheme}://{user}:{quote(password, safe='')}@127.0.0.1:59075/{db_name}"
created = subprocess.run(
    ['docker', 'exec', '-e', f'PGPASSWORD={password}',
     'multimedia-gkps-klender-db-1', 'psql', '-U', user, '-d', 'postgres',
     '-c', f'CREATE DATABASE {db_name}'], capture_output=True, text=True)
print('create:', (created.stdout + created.stderr).strip() or 'ok')
env = dict(os.environ, DATABASE_URL=local_url)
subprocess.check_call([VENV_PYTHON, 'manage.py', 'migrate', '--noinput'],
                      cwd=WORKTREE, env=env)
print(f'migrated {db_name}')
