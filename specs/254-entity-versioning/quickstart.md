# Quickstart: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`

## Prerequisites

- The main checkout's Python 3.12 virtualenv at `~/Projects/multimedia-gkps-klender/.venv`.
- The compose stack running in the main checkout; only `web` bind-mounts that checkout, so tests use the main venv with the worktree's `manage.py`.
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
print(urlunsplit((u.scheme, f'{u.username}:{u.password}@127.0.0.1:{sys.argv[2]}', '/gkps254', u.query, '')))
PY
)
```

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-254
DATABASE_URL="$TEST_URL" ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py check
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Django configuration | `manage.py check` | `System check identified no issues` |
| Version and deletion rules | `DATABASE_URL="$TEST_URL" ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test multimedia.web multimedia.tatib multimedia.web.reading.test_verses --noinput` | all pass; uses test database `test_gkps254` |
| Delete notice in a browser | `tests/e2e/test_verse_reference_notice.py` plus the new song/songbook cases, driven from the worktree's dev server | notice and disabled Delete in all three states |
| Preview numbers | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/254-entity-versioning/preview/probe.py` | `shots/probe.json` agrees with `preview/README.md` |

## Not yet runnable

- The new endpoint and E2E tests named in `tasks.md` do not exist until those tasks land; the commands above are the shape they will use.
- The dev server needs `collectstatic` after any `static/` edit, and a port-conflict check before trusting a local URL.
