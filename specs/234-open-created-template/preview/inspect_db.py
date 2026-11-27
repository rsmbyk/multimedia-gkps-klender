"""Print the preview database's Tata Ibadah records (spec 234 probe helper)."""
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
os.environ['DATABASE_URL'] = (f"{p.scheme}://{user}:{quote(password, safe='')}"
                              f'@127.0.0.1:59075/gkps234')
os.environ['DJANGO_SETTINGS_MODULE'] = 'multimedia.settings'
import sys
sys.path.insert(0, WORKTREE)
import django
django.setup()
from multimedia.tatib.models import TataIbadah
for row in TataIbadah.objects.order_by('pk').values('pk', 'name', 'kind', 'date'):
    print(row)
