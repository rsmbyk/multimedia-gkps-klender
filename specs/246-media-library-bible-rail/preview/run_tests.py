"""Run a Django lane against a throwaway database from the compose stack.

Reads the web container's DATABASE_URL at runtime; never stores or prints it.
"""
import os
import subprocess
import sys
import urllib.parse

WEB = 'multimedia-gkps-klender-web-1'
DB_NAME = 'gkps246'


def database_url():
    raw = subprocess.check_output(
        ['docker', 'exec', WEB, 'python', '-c',
         'import os; print(os.environ["DATABASE_URL"])'], text=True).strip()
    parts = urllib.parse.urlsplit(raw)
    netloc = parts.netloc
    if '@' in netloc:
        userinfo, host = netloc.rsplit('@', 1)
    else:
        userinfo, host = '', netloc
    published = subprocess.check_output(
        ['docker', 'compose', '-f',
         '/home/rsmbyk/Projects/multimedia-gkps-klender/docker-compose.yml',
         '-p', 'multimedia-gkps-klender', 'port', 'db', '5432'],
        text=True).strip().splitlines()[-1]
    host = '127.0.0.1:' + published.rsplit(':', 1)[-1]
    return urllib.parse.urlunsplit((parts.scheme, userinfo + '@' + host,
                                    '/' + DB_NAME, '', ''))


if __name__ == '__main__':
    os.environ['DATABASE_URL'] = database_url()
    os.execv(sys.executable, [sys.executable, 'manage.py', *sys.argv[1:]])
