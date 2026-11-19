# Quickstart: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`

## Prerequisites

- Python 3.12 with the repo's venv (`~/Projects/multimedia-gkps-klender/.venv/bin/python` from a worktree).
- The compose database reachable: `docker compose port db 5432` (59075 on this machine).
- Playwright's Chromium installed (`playwright install chromium`).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-203
PW=$(docker exec multimedia-gkps-klender-db-1 printenv POSTGRES_PASSWORD)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/multimedia"
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

`collectstatic` is needed for the page to serve the changed stylesheet locally: the project uses
`CompressedManifestStaticFilesStorage`, so the hashed copy in `_static/` is what `{% static %}` resolves to.
After it, restart the server and hard-reload the tab — the hashed filename changes.

## Run

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload
```

Open `http://127.0.0.1:8767/obs/dock` at 456×1087 (dark) and click the service named `hhhh…`
(25 Oktober 2026, service 149 on the shared local database). The developed page answers the same route on
`:63404` for comparison.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The title wraps inside its column | `preview/probe.py --out shots/live`, read `serviceline` | spill 0, 3 lines (before: 328px, 1 line) |
| The body has no sideways scroll | the same report, `body` | `scrollWidth == clientWidth` (before: 591 vs 456) |
| A run that fits is unchanged | the same report, `random.jpg` / `images (1).jpeg` headers | 19.6px, 1 line, width 79.5 / 103.9 |
| The row's geometry is unchanged | the same report, `numbers` and `chevrons` | 33.6px at left 18; 10px off the row's right, 0px off centre |
| The new suite | `manage.py test tests.e2e.test_dock_text_wrap --keepdb` | 10 tests, all pass |
| The dock's own suites | `manage.py test tests.e2e.test_obs_dock tests.e2e.test_obs_dock_follow tests.e2e.test_dock_bucket_head tests.e2e.test_dock_goto tests.e2e.test_dock_keys --keepdb` | 66 tests, all pass |
| Nothing else moved | `git diff origin/develop -- static/styles/design/obs-dock.css` | three declarations and their comments, all inside the runner's rules |

Run the tests against a throwaway database name so a concurrent session cannot hold the kept test database:

```sh
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/gkps203"
```

## Not yet runnable

- Nothing. Every command above runs against the worktree as it stands.
