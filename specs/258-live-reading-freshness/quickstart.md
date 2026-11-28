# Quickstart: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`

## Prerequisites

- The main checkout's Python 3.12 virtualenv at `~/Projects/multimedia-gkps-klender/.venv`.
- The compose stack running in the main checkout; tests use the main venv with this worktree's `manage.py`.
- No credentials are written into this folder; the database URL is read from the running web container.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender
export DB_URL=$(docker compose exec -T web printenv DATABASE_URL)
export PORT=$(docker compose port db 5432 | tail -1 | sed 's/.*://')
export TEST_URL=$(python - "$DB_URL" "$PORT" <<'PY'
import sys
from urllib.parse import urlsplit, urlunsplit
u = urlsplit(sys.argv[1])
print(urlunsplit((u.scheme, f'{u.username}:{u.password}@127.0.0.1:{sys.argv[2]}', '/gkps258', u.query, '')))
PY
)
```

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-258
DATABASE_URL="$TEST_URL" ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py check
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Django configuration | `manage.py check` | `System check identified no issues` |
| Poll endpoints | `manage.py test multimedia.web.tests.FreshnessEndpointTests --noinput` | all pass |
| Badge and sidebar E2E | `manage.py test tests.e2e.test_live_reading_freshness --noinput` | all pass |
| Preview numbers | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/258-live-reading-freshness/preview/probe.py` | `shots/probe.json` agrees with `preview/README.md` |

## Not yet runnable

- The new endpoint and E2E tests named above do not exist until the tasks land; the commands are the shape they will use.
- The dev server needs `collectstatic` after any `static/` edit, and a port-conflict check before trusting a local URL.
