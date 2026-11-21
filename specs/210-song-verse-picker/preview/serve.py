"""Run the slice's dev server against the compose database; no credential is printed."""
import os
import runpy
import subprocess
import sys
from urllib.parse import quote

container = 'multimedia-gkps-klender-db-1'
environment = subprocess.run(
    ['docker', 'exec', container, 'env'], check=True, capture_output=True, text=True
).stdout
password = environment.split('POSTGRES_PASSWORD=', 1)[1].splitlines()[0]
port = subprocess.run(
    ['docker', 'port', container, '5432'], check=True, capture_output=True, text=True
).stdout.strip().splitlines()[-1].rsplit(':', 1)[-1]

sys.path.insert(0, os.getcwd())
os.environ['DATABASE_URL'] = (
    f'postgres://multimedia:{quote(password, safe="")}@127.0.0.1:{port}/multimedia'
)
sys.argv = ['manage.py', 'runserver', '0.0.0.0:8765', '--noreload']
runpy.run_path('manage.py', run_name='__main__')
