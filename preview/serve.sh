#!/usr/bin/env bash
# Serve this worktree on a local port using the compose Postgres.
# Builds DATABASE_URL at runtime so no credential is stored in a file.
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${1:-8772}"
VENV=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
DB_URL="$("$VENV" - <<'PY'
import subprocess
from urllib.parse import quote, urlsplit
raw = subprocess.check_output(
    ["docker", "exec", "multimedia-gkps-klender-web-1", "python",
     "-c", "import os;print(os.environ['DATABASE_URL'])"], text=True).strip()
p = urlsplit(raw)
print(f"{p.scheme}://{p.username}:{quote(p.password or '', safe='')}@127.0.0.1:59075{p.path}")
PY
)"
export DATABASE_URL="$DB_URL"
exec "$VENV" manage.py runserver "0.0.0.0:$PORT" --noreload
