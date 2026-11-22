# Quickstart: the song entry's pickers

**Spec**: `specs/210-song-verse-picker/spec.md` · `contracts/none.md` · `data-model.md`

## Prerequisites

- The slice worktree `~/Projects/multimedia-gkps-klender-210` on `feat/210-song-verse-picker`.
- The main checkout's virtualenv at `~/Projects/multimedia-gkps-klender/.venv/bin/python`.
- The compose Postgres service; take the connection URL from the `web` container's own
  environment rather than writing credentials into a file.
- Node (for `node --check`) and a browser for the static preview.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-210
docker compose port db 5432
PW=$(docker exec multimedia-gkps-klender-db-1 printenv POSTGRES_PASSWORD)
# Build DATABASE_URL from that password and the published port at run time.
```

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-210
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Open `specs/210-song-verse-picker/preview/index.html` directly for the approved static
preview, or the portable `song-verse-picker-preview.html` with no sibling files.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Preview script parses | `node --check specs/210-song-verse-picker/preview/preview.js` | no output, exit 0 |
| Portable preview is current | `python3 specs/210-song-verse-picker/preview/build_standalone.py` | file path and byte count |
| Form fragment still renders | `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test multimedia.web.tests multimedia.tatib.tests --keepdb` | green on the slice |
| Picker acceptance | `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_song_entry_pickers --keepdb` | green once the module exists |

## Not yet runnable

- `tests.e2e.test_song_entry_pickers` does not exist until Implement; the command above is the
  declared target, not a current pass.
- The full E2E suite is deferred to the push step; only the module above and the two form
  test modules are in the slice's loop.
- `tests/e2e/test_entry_pickers.py` has a known backdrop race on unmodified `develop`; it is
  not a gate for this slice.
