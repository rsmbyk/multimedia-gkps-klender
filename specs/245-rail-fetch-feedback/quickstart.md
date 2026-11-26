# Quickstart: pending state for Search and Media Library rail tiles

**Spec**: `specs/245-rail-fetch-feedback/spec.md`

## Prerequisites

- Python 3.12 at `~/Projects/multimedia-gkps-klender/.venv/bin/python` (the main checkout's venv;
  the slice worktree has none).
- The local compose stack running: `web` on port 63404, `db` on 59075, `media` on 63174.
- Playwright with Chrome available to that venv for E2E tests and preview probes.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-245
PY=../multimedia-gkps-klender/.venv/bin/python
$PY manage.py collectstatic --noinput
```

`preview/run_local.py` reads `DATABASE_URL` from the compose web container at run time and never
prints the password. It switches the database name to a throwaway one when `GKPS_DB` is set.

## Run

```sh
GKPS_DB=gkps245 python3 preview/run_local.py -- \
  $PY manage.py runserver 0.0.0.0:8787 --noreload
```

Open `http://127.0.0.1:8787/` and click the Search and Media Library rail tiles. Static changes
need `collectstatic` and a server restart; Python edits need a restart as well (`--noreload`).

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Static preview ships no external assets | `python3 ~/.hermes/skills/software-development/obs-browser-surfaces/scripts/verify-chat-preview-frame.py preview/combined.html` | PASS, >0 CSS rules |
| Preview measurements | `~/Projects/multimedia-gkps-klender/.venv/bin/python preview/probe.py` | svg opacity `0.45`, bar 3px at stage y=0, three placeholder shapes, no page errors |
| Targeted E2E (in-between) | `GKPS_DB=gkps245 python3 preview/run_local.py -- $PY manage.py test tests.e2e.test_navigation_pending --keepdb --noinput` | named new cases pass; full suite waits for the push step |
| Full browser suite | same command with `tests` instead of the module | run at the push step, on a throwaway database |

## Not yet runnable

- The full browser suite is deliberately not run in-between; it is executed at the push step.
- The Media Library's companion fetch needs the compose `media` service; without it the library
  page still paints but reports "unavailable on this computer". The pending-state assertions do
  not depend on companion bytes.

## Local companion origins

The companion at `127.0.0.1:63174` only admits the origins in `GKPS_MEDIA_ALLOWED_ORIGINS`. Port 8787 is not in the compose default, so a slice server otherwise reports "Local library unavailable on this computer." Recreate only the companion with the checked-in override:

```sh
cd ~/Projects/multimedia-gkps-klender
docker compose -f docker-compose.yml -f ../multimedia-gkps-klender-245/specs/245-rail-fetch-feedback/preview/media-override.yml \
  up -d --force-recreate --no-deps media
```

This is local container configuration; `docker-compose.yml` and `.env` are untouched.
