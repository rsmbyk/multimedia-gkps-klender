#!/usr/bin/env bash
# Targeted song-page template tests for spec 224, isolated from other worktrees' test DBs.
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
print(urllib.parse.urlunsplit((u.scheme, auth + '@127.0.0.1:59075', '/gkps224', '', '')))
PY
)"
cd "$ROOT"
exec "$PY" manage.py test multimedia.web.reading.test_verses multimedia.web.reading.test_verse_add_gate tests.e2e.test_song_empty_placement --keepdb
