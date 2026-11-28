#!/usr/bin/env bash
# Spec 248 targeted test runner — reads the compose DB URL at runtime (never echoed),
# uses the throwaway database gkps248 so parallel sessions cannot collide.
# Usage: ./run-tests.sh <test-module> [extra manage.py test args]
set -euo pipefail
WT="$(cd "$(dirname "$0")/../.." && pwd)"
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
                  f'@127.0.0.1:{port}', '/gkps248', '', '')))
EOF
)
cd "$WT"
exec "$VENV" manage.py test "$@" --keepdb
