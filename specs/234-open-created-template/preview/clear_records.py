"""Delete all preview Tata Ibadah rows before a fresh probe run (spec 234)."""
import os
import subprocess
from urllib.parse import quote, urlsplit

VENV_PYTHON = '/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python'
WORKTREE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
raw = subprocess.check_output(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'python', '-c',
     "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
user = p.username or 'multimedia'
password = p.password or ''
env = dict(os.environ,
           DATABASE_URL=(f"{p.scheme}://{user}:{quote(password, safe='')}"
                         f'@127.0.0.1:59075/gkps234'),
           DJANGO_SETTINGS_MODULE='multimedia.settings')
code = ('import django; django.setup(); '
        'from multimedia.tatib.models import TataIbadah; '
        'print("deleted", TataIbadah.objects.all().delete()[0])')
subprocess.check_call([VENV_PYTHON, '-c', code], cwd=WORKTREE, env=env)
