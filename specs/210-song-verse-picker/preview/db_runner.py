"""Run targeted tests against a throwaway database; never print the password."""
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
name = 'gkps210'
check = subprocess.run(
    ['docker', 'exec', container, 'psql', '-U', 'multimedia', '-d', 'postgres', '-tAc',
     f"SELECT 1 FROM pg_database WHERE datname='{name}'"],
    check=True, capture_output=True, text=True,
)
if not check.stdout.strip():
    subprocess.run(['docker', 'exec', container, 'createdb', '-U', 'multimedia', name],
                   check=True)
sys.path.insert(0, os.getcwd())
os.environ['DATABASE_URL'] = (
    f'postgres://multimedia:{quote(password, safe="")}@127.0.0.1:{port}/{name}'
)
sys.argv = ['manage.py', 'test', *sys.argv[1:], '--keepdb']
runpy.run_path('manage.py', run_name='__main__')
