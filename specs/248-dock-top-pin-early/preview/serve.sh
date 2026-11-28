#!/usr/bin/env bash
# Spec 248 preview server — the worktree's own code on 8793, real compose DB.
# Credentials inherited from the web container at runtime (never echoed).
set -euo pipefail
WT="$(cd "$(dirname "$0")/../../.." && pwd)"
VENV=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
export DATABASE_URL=$(python3 - <<'EOF'
import subprocess
from urllib.parse import urlsplit, urlunsplit, quote
url = subprocess.run(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'printenv', 'DATABASE_URL'],
    capture_output=True, text=True).stdout.strip()
port = subprocess.run(
    ['docker', 'compose', '-f',
     '/home/rsmbyk/Projects/multimedia-gkps-klender/docker-compose.yml',
     'port', 'db', '5432'], capture_output=True, text=True).stdout.strip().split(':')[-1]
parts = urlsplit(url)
print(urlunsplit((parts.scheme,
                  f'{quote(parts.username, safe="")}:{quote(parts.password, safe="")}'
                  f'@127.0.0.1:{port}', '/multimedia', '', '')))
EOF
)
cd "$WT"
"$VENV" manage.py collectstatic --noinput >/dev/null
exec "$VENV" manage.py runserver 0.0.0.0:8793 --noreload
