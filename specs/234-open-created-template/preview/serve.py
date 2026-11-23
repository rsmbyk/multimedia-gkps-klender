"""Serve a worktree against the dedicated preview database (spec 234).

Usage:
    python serve.py --port 8774 --worktree /path/to/after
Credentials are read from the compose web container at run time.
"""
import argparse
import os
import subprocess
from urllib.parse import quote, urlsplit

VENV_PYTHON = '/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python'
HERE = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--port', default='8774')
parser.add_argument('--db', default='gkps234')
parser.add_argument('--worktree', default=os.path.abspath(os.path.join(HERE, '..', '..', '..')))
args = parser.parse_args()

raw = subprocess.check_output(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'python', '-c',
     "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
user = p.username or 'multimedia'
password = p.password or ''
url = f"{p.scheme}://{user}:{quote(password, safe='')}@127.0.0.1:59075/{args.db}"
env = dict(os.environ, DATABASE_URL=url)
subprocess.check_call([VENV_PYTHON, 'manage.py', 'collectstatic', '--noinput'],
                      cwd=args.worktree, env=env)
print(f'serving {args.worktree} on {args.port}, database {args.db}', flush=True)
os.chdir(args.worktree)
os.execve(VENV_PYTHON,
          [VENV_PYTHON, 'manage.py', 'runserver', f'0.0.0.0:{args.port}', '--noreload'], env)
