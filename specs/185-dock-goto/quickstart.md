# Quickstart: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`
**Contracts**: `contracts/display-state.md` · **Model**: `data-model.md`

## Prerequisites

- Docker and its compose plugin (the repo's stack).
- Python 3.12 with the repo's virtualenv at the **main checkout**:
  `~/Projects/multimedia-gkps-klender/.venv/bin/python` — worktrees share it.
- Playwright's Chromium in that virtualenv: `playwright install chromium`.
- No new service, no new env var: the slice adds no endpoint and no dependency.

## Setup

The Postgres service runs in the main checkout's compose stack; this worktree's own server reads it
by URL. **Do not start a second stack in the worktree** — its published ports belong to the running
one, and the compose `web` service is bind-mounted to the main checkout, so it never serves this
slice's code.

```sh
cd ~/Projects/multimedia-gkps-klender-185
docker compose -f ../multimedia-gkps-klender/docker-compose.yml up -d db
docker compose -f ../multimedia-gkps-klender/docker-compose.yml port db 5432   # -> 0.0.0.0:59075
export DATABASE_URL=postgresql://multimedia:multimedia@127.0.0.1:59075/multimedia
```

(The password is the compose file's own development value, not a secret.) The venv is the main
checkout's; nothing is installed into the worktree.

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-185
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput   # after any CSS edit
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Then, in the browser (or as OBS browser sources at 400 × 800 for the dock):

```sh
open http://127.0.0.1:8765/obs/dock
open 'http://127.0.0.1:8765/projector?service=<id>'
open 'http://127.0.0.1:8765/obs/source/overlay?service=<id>'
```

The two static previews need no server and no database:

```sh
xdg-open specs/185-dock-goto/preview/index.html
xdg-open specs/185-dock-goto/preview/sync.html
```

`--noreload`: template, CSS and JS edits are picked up per request, Python edits need a restart.
Static files are served from `_static/` through WhiteNoise's manifest, so a CSS change shows only
after `collectstatic` — an un-collected stylesheet reads as "the change did nothing".

The previews are rebuilt from the captured payloads and the product's own stylesheets:

```sh
cd specs/185-dock-goto/preview
~/Projects/multimedia-gkps-klender/.venv/bin/python build.py
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the dock's states, measured | `<venv>/python specs/185-dock-goto/preview/probe.py` | every check `ok`; `## UI/UX`'s numbers printed |
| the three surfaces follow one state | `<venv>/python specs/185-dock-goto/preview/probe_sync.py` | every step `ok`, all nine |
| the preview arrives whole in the chat's frame | `<venv>/python specs/185-dock-goto/preview/probe_frame.py` | every check `ok` (srcdoc, opaque origin) |
| the dock's Go To end to end | `<venv>/python manage.py test tests.e2e.test_dock_goto --noinput` | all pass |
| agreement between surfaces | `<venv>/python manage.py test tests.e2e.test_goto_shared_state --noinput` | all pass |
| nothing else moved | `<venv>/python manage.py test tests.e2e.test_display_session tests.e2e.test_entries --noinput` | unchanged from the base |

Run the E2E modules against a throwaway database so a parallel session's run cannot collide:
`DATABASE_URL=postgresql://multimedia:multimedia@127.0.0.1:59075/gkps185` in front of the command
(the test database is then `test_gkps185`, which no other worktree touches).

## Not yet runnable

- The E2E modules in this table do not exist until Implement's first tasks; the two preview probes
  run today.
- A browser restart is simulated, not performed: the E2E walks clear the session cookie and reload
  (spec 184's own technique), because a Playwright browser cannot restart a user profile mid-run.
