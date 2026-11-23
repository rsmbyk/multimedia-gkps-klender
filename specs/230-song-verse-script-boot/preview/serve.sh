#!/usr/bin/env bash
# Live preview for spec 230: serve this worktree on a reserved port against the local compose DB.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
export DATABASE_URL="$("$PY" - <<'PY'
import subprocess, urllib.parse
raw = subprocess.check_output(
    ['docker', 'exec', 'multimedia-gkps-klender-web-1', 'printenv', 'DATABASE_URL'],
    text=True).strip()
u = urllib.parse.urlsplit(raw)
auth = u.username + (':' + urllib.parse.quote(urllib.parse.unquote(u.password), safe='') if u.password else '')
print(urllib.parse.urlunsplit((u.scheme, auth + '@127.0.0.1:59075', u.path, u.query, '')))
PY
)"
exec "$PY" "$ROOT/manage.py" runserver 0.0.0.0:8771 --noreload
