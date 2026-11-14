# Quickstart — Project button on the song and Bible pages

**Spec**: `specs/193-reading-project-button/spec.md`

## Prerequisites

- The repo's venv (lives in the main checkout: `~/Projects/multimedia-gkps-klender/.venv/bin/python`)
- The compose Postgres: `docker compose port db 5432` for the host port; password from
  `docker-compose.yml`
- Playwright (Python) for the E2E module

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-193
export DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:$(docker compose port db 5432 | cut -d: -f2)/multimedia
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

## Run

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Open a song (`/songs/<id>/`) and a chapter (`/bible/<book>/<chapter>/`) — the Project control sits
in the stage header (song: top row's right end; Bible: title row, right of TB/SIM). Click it with
the projector window closed: `/projector` opens showing the detour. Click again: nothing changes on
the projector. `Back` on the projector returns to whatever was on air.

Note: after editing `static/`, re-run `collectstatic` and restart the server — the page serves
`_static/` through the manifest.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| View/render pins | `manage.py test multimedia.web.tests.ReadingViewTests --keepdb` | green, including the new button pins |
| Browser behaviour | `manage.py test tests.e2e.test_reading_project --keepdb` | green: pointer written, projector paints, window reused, repeat click inert |
| Saved-render parity untouched | `manage.py test tests.e2e.test_saved_render_parity --keepdb` | green (the saved renderer draws no controls) |

## Not yet runnable

- The popup-blocked case has no automation: a browser's popup blocker is not reachable from
  Playwright's context. Verified by inspection (`openProjector` returns on a falsy window handle
  and the Go To write happens before the window act).
