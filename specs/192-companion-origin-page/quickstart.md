# Quickstart: The companion's page manages this computer's origins

**Spec**: `specs/192-companion-origin-page/spec.md`

## Prerequisites

- Docker (the compose stack) for the manual checks; the machine's `.env` no longer needs any
  origin variable.
- The repo venv for the test suites (`~/Projects/multimedia-gkps-klender/.venv/bin/python` from a
  slice worktree, per the machine's standing note), and a throwaway `DATABASE_URL` for suites that
  touch Postgres.
- Playwright (Python) for the page E2E.

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-192
DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:<db-port>/gkps192 \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  multimedia.test_local_media tests.test_docker_compose tests.test_launcher_fonts \
  tests.e2e.test_companion_page --keepdb
```

## Run

```sh
docker compose up -d            # or docker\up.ps1 / ./docker/up.sh
# then open http://127.0.0.1:63174/
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Page reachable with nothing recorded | open `http://127.0.0.1:63174/` | the page renders, empty state shown |
| Refusal names the page | `curl -s -H 'Origin: https://unrecorded.example' http://127.0.0.1:63174/v1/status` | 403 JSON naming the page, no CORS header |
| Local seeds pass | the local web app's Media Library dialog at `http://127.0.0.1:63404` | Connected |
| Recorded origin works | add the production origin on the page, then use the production site's picker | the companion connects |
| Launcher listing | `./docker/up.sh --build` | `gkps: font directories from this computer (n):` + one path per line |

## Not yet runnable

- The Playwright companion test and the launcher harness do not exist until their tasks run
  (T012/T018) — the suites above name them as written.
