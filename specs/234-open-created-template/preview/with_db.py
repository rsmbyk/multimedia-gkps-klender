"""Run a management command against the dedicated gkps234 database.

    <VENV>/python preview/with_db.py manage.py test tests.e2e.test_editor --keepdb

The local DATABASE_URL is built from the running compose web container at run time;
no credential is stored here.
"""
import os
import subprocess
import sys
from urllib.parse import quote, urlsplit

WORKTREE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
raw = subprocess.check_output(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'python', '-c',
     "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
user = p.username or 'multimedia'
password = p.password or ''
url = f"{p.scheme}://{user}:{quote(password, safe='')}@127.0.0.1:59075/gkps234"
env = dict(os.environ, DATABASE_URL=url)
cmd = list(sys.argv[1:])
worktree = WORKTREE
if cmd and cmd[0].startswith('--worktree='):
    worktree = cmd.pop(0).split('=', 1)[1]
if cmd and cmd[0].endswith('.py'):
    if not os.path.isabs(cmd[0]):
        cmd[0] = os.path.join(worktree, cmd[0])
    cmd.insert(0, sys.executable)
raise SystemExit(subprocess.call(cmd, cwd=worktree, env=env))
