# Quickstart: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and its Chromium already
  installed).
- The compose `db` service, and a database URL no other worktree is using:
  `postgresql://multimedia:<db password>@127.0.0.1:<db port>/gkps164`.
- No other `manage.py test` run holding the shared test database (the suite's own `setUp` writes).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-164-dock
export PY=../multimedia-gkps-klender/.venv/bin/python
DBPORT=$(cd ../multimedia-gkps-klender && docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgresql://multimedia:<db password>@127.0.0.1:${DBPORT}/gkps164"
```

## Run

```sh
$PY manage.py test tests.e2e.test_obs_dock multimedia.web.test_obs_dock --keepdb
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the two width behaviours | the `Run` command above | red on 1.23.1's stylesheet (`panel starts at 170 at 900px`, `row is 544 of 1424px`), green after |
| the dock module as a whole | the same | the five existing dock cases still green — 18 tests across the module and the unit file |
| the numbers in `spec.md`'s `## UI/UX` | `$PY specs/164-dock-fluid-width/probe/probe.py http://127.0.0.1:8799` | the table in this slice's spec: panel = viewport at every width, rows = viewport − 16, one column, sticky head, overflow 0 |
| the live page, from this worktree | `DATABASE_URL=… $PY manage.py runserver 0.0.0.0:8799 --noreload`, then `/obs/dock` | resize the window from 320 to 2560: the panel never leaves an empty strip, the picker stays one column, the date follows the row's right edge |
| the shipped page, after the merge | `docker compose exec -T web python manage.py collectstatic --noinput && docker compose restart web`, then `http://localhost:63404/obs/dock` | the same, with Whitenoise serving the new stylesheet |

## Not yet runnable

- The compose page above runs only after the merge, because the compose `web` service serves the
  `develop` checkout; the worktree server covers the same states before it.
