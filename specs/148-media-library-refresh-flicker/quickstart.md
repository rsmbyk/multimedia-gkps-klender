# Quickstart: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Python 3.12, Django 4.0, Playwright 1.47
  with its Chromium builds already installed).
- The compose stack running from the main checkout: `web` on `http://localhost:63404` and `media` on
  `127.0.0.1:63174`. The preview and the frame sampler read the live route; the E2E suite stubs the
  companion itself and needs no service.
- A database URL that no other worktree is using, so a parallel slice's test run cannot collide:
  `DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:<db-port>/gkps148`, with the port from
  `docker compose port db 5432` in the main checkout.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-148
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//; s/"//g; s/ *$//')
DBPORT=$(cd ../multimedia-gkps-klender && docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${DBPORT}/gkps148"
```

## Run

```sh
# the live route the preview names (served by the compose `web` service, nothing to start)
$PY specs/148-media-library-refresh-flicker/preview/frame_sampler.py
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the sampler runs and reports today's defect | `$PY specs/148-media-library-refresh-flicker/preview/frame_sampler.py` | `worst jolt: 56px`, placeholder frames > 0, exit 1 (red until this slice lands) |
| one E2E case runs on this worktree | `$PY manage.py test tests.e2e.test_media_library.MediaLibraryE2ETests.test_connected_library_shows_file_and_status_details --keepdb --noinput` | `OK` — confirmed on the unmodified tree, 3.0s |
| the slice's own cases | `$PY manage.py test tests.e2e.test_media_library --keepdb --noinput` | the five new cases green, and the module's existing cases unchanged |
| the rows still read the same | open `http://localhost:63404/media-library/` and compare a row against its pre-slice text | same names, sizes, service references, cloud states, title |

## Not yet runnable

- Nothing. Every command above runs as written on the worktree; the only expected red is the sampler,
  until the implementation lands.
