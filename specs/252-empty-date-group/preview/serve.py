"""Serve the real worktree code as the spec-252 live preview.

Reads the Compose database credential at run time; no credential is written to
disk. The dedicated database `gkps252` is seeded with the four states the
preview measures. Run this file with the project venv, in the background.
"""

import os
import subprocess
import sys
from datetime import date
from urllib.parse import urlsplit, urlunsplit

BASE = '/home/rsmbyk/Projects/multimedia-gkps-klender'
WORKTREE = '/home/rsmbyk/Projects/multimedia-gkps-klender-252'
PORT = 8776


def prepare_env():
    raw = subprocess.check_output(
        ['docker', 'compose', 'exec', '-T', 'web', 'printenv', 'DATABASE_URL'],
        cwd=BASE, text=True).strip()
    published = subprocess.check_output(
        ['docker', 'compose', 'port', 'db', '5432'], cwd=BASE,
        text=True).strip().splitlines()[-1].rsplit(':', 1)[-1]
    parts = urlsplit(raw)
    netloc = parts.netloc.replace('db:5432', f'127.0.0.1:{published}')
    os.environ['DATABASE_URL'] = urlunsplit(
        (parts.scheme, netloc, '/gkps252', parts.query, parts.fragment))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'multimedia.settings'
    os.chdir(WORKTREE)
    sys.path.insert(0, WORKTREE)


def ensure_database():
    exists = subprocess.check_output(
        ['docker', 'exec', 'multimedia-gkps-klender-db-1', 'psql', '-U',
         'multimedia', '-d', 'postgres', '-tAc',
         "SELECT 1 FROM pg_database WHERE datname='gkps252'"], text=True)
    if not exists.strip():
        subprocess.check_call(
            ['docker', 'exec', 'multimedia-gkps-klender-db-1', 'createdb',
             '-U', 'multimedia', 'gkps252'])


def seed(collect_static=True):
    import django
    django.setup()
    from django.core.management import call_command
    from multimedia.songs import models as songs
    from multimedia.tatib import models as tatib
    from multimedia.web.reading.date_buckets import present_day

    call_command('migrate', verbosity=0, interactive=False)
    tatib.TataIbadah._base_manager.all().delete()
    songs.Book._base_manager.all().delete()
    today = present_day()
    for offset, name in ((1, 'Alpha'), (2, 'Beta')):
        tatib.TataIbadah.objects.create(
            name=name, date=date.fromordinal(today.toordinal() - offset),
            is_active=True)
    tatib.TataIbadah.objects.create(
        name='Gamma', date=date(today.year, 1, 10), is_active=True)
    for name in ('Polos', 'Polos Dua'):
        tatib.TataIbadah.objects.create(
            name=name, kind=tatib.TataIbadahKind.TEMPLATE, is_active=True)
    songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
    songs.Book.objects.create(name='Lagu Lain', short_name='LL')
    if collect_static:
        call_command('collectstatic', interactive=False, verbosity=0)


if __name__ == '__main__':
    prepare_env()
    ensure_database()
    seed()
    from django.core.management import execute_from_command_line
    execute_from_command_line(
        ['manage.py', 'runserver', f'0.0.0.0:{PORT}', '--noreload'])
