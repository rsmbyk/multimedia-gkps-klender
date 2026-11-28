"""Serve the real slice worktree as the spec-256 live preview.

Reads the Compose database credential at run time; no credential is written to
disk. The dedicated database `gkps256` holds the seeded records the probe uses.
Run this file with the project venv, in the background.
"""

import os
import subprocess
import sys
from datetime import date
from urllib.parse import urlsplit, urlunsplit

BASE = '/home/rsmbyk/Projects/multimedia-gkps-klender'
WORKTREE = '/home/rsmbyk/Projects/multimedia-gkps-klender-256'
PORT = 8768


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
        (parts.scheme, netloc, '/gkps256', parts.query, parts.fragment))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'multimedia.settings'
    os.chdir(WORKTREE)
    sys.path.insert(0, WORKTREE)


def ensure_database():
    exists = subprocess.check_output(
        ['docker', 'exec', 'multimedia-gkps-klender-db-1', 'psql', '-U',
         'multimedia', '-d', 'postgres', '-tAc',
         "SELECT 1 FROM pg_database WHERE datname='gkps256'"], text=True)
    if not exists.strip():
        subprocess.check_call(
            ['docker', 'exec', 'multimedia-gkps-klender-db-1', 'createdb',
             '-U', 'multimedia', 'gkps256'])


def seed(collect_static=True):
    import django
    django.setup()
    from django.core.management import call_command
    from multimedia.songs import models as songs
    from multimedia.tatib import models as tatib

    call_command('migrate', verbosity=0, interactive=False)
    tatib.ServiceEntry._base_manager.all().delete()
    tatib.TataIbadahItem._base_manager.all().delete()
    tatib.TataIbadah._base_manager.all().delete()
    songs.Verse._base_manager.all().delete()
    songs.Song._base_manager.all().delete()
    songs.Book._base_manager.all().delete()
    service = tatib.TataIbadah.objects.create(
        name='Preview service', date=date(2026, 12, 6), is_active=True)
    tatib.ServiceEntry.objects.create(
        tatib=service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
        title='Opening', text='Preview text')
    tatib.ServiceEntry.objects.create(
        tatib=service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
        title='Survivor', text='Keep me')
    book = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ',
                                     is_hymn_book=True)
    song = songs.Song.objects.create(book=book, number=12, title='Preview song',
                                     key='c')
    songs.Verse.objects.create(song=song, number=1, lyric='First verse')
    songs.Verse.objects.create(song=song, number=2, lyric='Second verse')
    plain = songs.Book.objects.create(name='Lagu Lain', short_name='LL',
                                      is_hymn_book=False)
    editable_song = songs.Song.objects.create(book=plain, title='Editable song')
    songs.Verse.objects.create(song=editable_song, number=1, lyric='Editable verse')
    songs.Verse.objects.create(song=editable_song, number=2, lyric='Second editable verse')
    if collect_static:
        call_command('collectstatic', interactive=False, verbosity=0)


if __name__ == '__main__':
    prepare_env()
    ensure_database()
    seed()
    from django.core.management import execute_from_command_line
    execute_from_command_line(
        ['manage.py', 'runserver', f'0.0.0.0:{PORT}', '--noreload'])
