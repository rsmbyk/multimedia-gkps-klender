# Quickstart: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and its Chromium builds
  already installed).
- A database of its own, so a concurrent `manage.py test` in another worktree cannot take the same
  `test_*` database: `gkps159`, below.
- For anything on the live page: the compose stack (`web` on `http://localhost:63404`, `media` on
  `127.0.0.1:63174`) serving this branch, which it does only after the merge.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-159
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//; s/"//g; s/ *$//')
DBPORT=$(docker port multimedia-gkps-klender-db-1 5432 | head -1 | sed 's/.*://')
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${DBPORT}/gkps159"
```

## Run

The slice's own cases — five of them, described in `research.md` D004:

```sh
$PY manage.py test tests.e2e.test_preview_body_ring --keepdb --noinput
```

The two modules that must stay green, because they are FR-003's and FR-004's evidence:

```sh
$PY manage.py test tests.e2e.test_entry_preview --keepdb --noinput
$PY manage.py test tests.e2e.test_audio_display --keepdb --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the ring is gone after a space press | `$PY manage.py test tests.e2e.test_preview_body_ring --keepdb --noinput` | green after the fix; red before it — the body's outline reads `2px` where `none` is asserted |
| the ring returns on Tab | the same module | green; the outline reads `2px solid rgb(28, 92, 60)` at offset `-2px` |
| arrow-key scrolling still works | `$PY manage.py test tests.e2e.test_entry_preview --keepdb --noinput` | green — the spec-071 cases unchanged |
| the player still toggles on space | `$PY manage.py test tests.e2e.test_audio_display --keepdb --noinput` | green — `test_preview_plays_seeks_and_closes` unchanged |
| the two panels by hand | open `specs/159-preview-body-ring/preview/preview.html` | panel A: pointer open + space paints nothing; Tab paints the ring |

## Not yet runnable

- **The live page, before the merge.** The compose `web` service serves the `develop` checkout, and a
  worktree server is refused by the companion's origin allow-list (`local_media.py`), so the audio and
  video previews cannot load their media from a slice server. The `manual` row for SC-004 is a
  post-merge step: `collectstatic` inside `web`, restart it, then open an audio preview and press
  space — the dialog's edge stays clean, and one Tab paints the ring.
- **`tests.e2e.test_preview_body_ring` before the fix.** Red by construction; the run is recorded in
  `analysis.md` rather than quoted here as a number today.
