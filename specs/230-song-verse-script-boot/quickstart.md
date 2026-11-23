# Quickstart: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`

## Prerequisites

- Python 3.12 venv at `~/Projects/multimedia-gkps-klender/.venv` (this worktree has none of its own).
- `DATABASE_URL` exported for the local compose PostgreSQL service, as for every GKPS dev run.
- Playwright Chromium installed for the Django E2E runner.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-230
# export DATABASE_URL from the compose web container's own environment
```

## Run

```sh
# live preview on the slice's own code
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8771 --noreload
# open http://127.0.0.1:8771/ and click Songs -> Lagu -> Anggo Marhorja Tonduy In
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| before/after behaviour and boxes | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/230-song-verse-script-boot/preview/probe.py` | `add_dialog_open=True`, `edit_dialog_open=True`, button box unchanged on port 8771; both `False` on 63404 |
| acceptance module | `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_song_verse_script_boot --keepdb` | all cases green |
| neighbouring module | `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test multimedia.web.reading.test_verse_add_gate --keepdb` | all cases green |

## Not yet runnable

- The acceptance module command above becomes runnable when T002/T003 create
  `tests/e2e/test_song_verse_script_boot.py` during Implement.
- The compare server on port 63404 is the main checkout's compose web service; if it is stopped,
  start it with `docker compose up -d web` from the main checkout before running the probe.
