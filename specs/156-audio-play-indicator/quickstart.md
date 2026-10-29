# Quickstart: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`

## Prerequisites

- The repo's virtualenv, in the main checkout: `~/Projects/multimedia-gkps-klender/.venv`
- Playwright's Chromium for that venv
- PostgreSQL from the compose stack (host port 59075) and its media companion on `127.0.0.1:63174`
- The slice's worktree: `~/Projects/multimedia-gkps-klender-156`
- No new dependency, no migration, no `collectstatic` — the dev server serves `static/` straight from disk

## Run — the live preview

```sh
cd ~/Projects/multimedia-gkps-klender-156
DATABASE_URL="postgresql://multimedia:<password>@127.0.0.1:59075/multimedia" \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8815 --noreload
```

Open <http://127.0.0.1:8815/projector?service=144>, press `Space`, click the list icon in the bottom-left
corner, type `Sujud`, and pick entry 7 — the audio screen, with its control above the seek bar.

The companion only answers origins it lists (`GKPS_MEDIA_ALLOWED_ORIGINS`); 8815 was added to the running
container for this preview, and `http://localhost:8814` (another slice's server) is still there.

## Measure

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/156-audio-play-indicator/preview/measure.py http://127.0.0.1:8815 144
```

Prints the control, the bar, the times and the player box in the paused, playing, idle and returned
states at 1920×1200, 1280×800 and 640×480. Every number in the spec's `## UI/UX` comes from this run.

## Test

```sh
cd ~/Projects/multimedia-gkps-klender-156
DATABASE_URL="postgresql://multimedia:<password>@127.0.0.1:59075/gkps156" \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_audio_display
```

A throwaway database name (`gkps156`) keeps the run clear of other slices' test databases on the shared
Postgres. `test_untitled_preview_and_projector_idle_display_off` is red on `develop` too — board card
ITEM-140, not this slice.

## Read the diff

```sh
git -C ~/Projects/multimedia-gkps-klender-156 diff -- static/styles/design/projector.css static/web/projector.js
```
