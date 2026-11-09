# Quickstart: song verse editing on the song page

**Spec**: `specs/189-song-verse-editing/spec.md`

## Prerequisites

- Python 3.12, PostgreSQL, Docker compose stack (see repo `docs/` / `docker-compose*`), or existing `~/Projects/multimedia-gkps-klender/.venv` + local dev DB.
- Node not required. Playwright + Chromium for E2E (preinstalled via `.venv`).

## Setup

```sh
python3 specs/189-song-verse-editing/preview/build.py
# writes preview/index.html (static preview — no server)
```

Local stack (run from repo root):

```sh
docker compose up -d --build
python manage.py runserver
```

## Run

- Static preview (no server): open `specs/189-song-verse-editing/preview/index.html` in a browser via `file://`, or `python3 -m http.server 8000` inside that folder if `file://` blocks script execution. Bottom bar switches states; hover a verse to see grip + pencil, `Add verse` opens the editor dialog, drag a grip to reorder.
- Live song page: `http://127.0.0.1:8000/songs/<song_id>/` (e.g. song 1825 used in the preview snapshot); verbs act on the real tables once implemented.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Preview drag trace | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/189-song-verse-editing/preview/probe.py` | `long_drag_trace` 14/14 expected pairs, `grabHeld: true`, `reversals: 0`, `seamsOk: true` |
| Static preview loads | open `preview/index.html` | bars, verses, dialog, states reachable by hand at 1440×900 dark/light and 420×900 |
| Live four verbs | Playwright walk (to be written at Tasks) | add/edit/remove/reorder round-trip on a fixture song without reload |
| Migration fidelity | `python manage.py migrate tatib` on fixture of ten entries | same lyric text before/after (SC-007) |

## Not yet runnable

- Tests of the four verbs against the DB — written at Tasks phase after Gate 2; the dev server currently serves the pre-slice app.
- Release merge — after Implements → Converge → Fold (SDD-19).
