# Quickstart: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md`

## Prerequisites

- The Python venv of the **main checkout** — `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv`
  (a worktree has no venv of its own). Django 4.0, Playwright and a Chromium build are in it.
- The compose stack's PostgreSQL, published on `127.0.0.1:59075` (`docker compose ps` → `…-db-1`). No app
  container is needed: the E2E modules run Django's live server themselves and stub the media companion.
- Nothing else — no `collectstatic`, no companion, no network.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-164-rest
export PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
# a database name of its own: Django makes and drops `test_gkps164`, so another slice's test run
# cannot hold it
export DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:59075/gkps164
```

## Run

```sh
# the unit module this slice changes
$PY manage.py test multimedia.web.test_media --noinput

# the dock's browser module and the projector's, for the stepping and row rules
$PY manage.py test tests.e2e.test_obs_dock tests.e2e.test_projector --noinput

# the media display modules, whose services all hold media entries
$PY manage.py test tests.e2e.test_image_display tests.e2e.test_video_display \
    tests.e2e.test_pdf_display tests.e2e.test_powerpoint_display tests.e2e.test_audio_display --noinput
```

## See it by hand

```sh
# the slice's own server; templates and JS refresh per request
$PY manage.py runserver 0.0.0.0:8864 --noreload
```

- `http://127.0.0.1:8864/projector?service=149` — step with `→`: line, rest, image, rest, image, rest,
  image, rest, image, rest.
- `http://127.0.0.1:8864/obs/dock` — open service 149, point at entry 2: its inner list reads `IMAGE`
  then `Rest`; `→` from screen 2 lands on the rest.
- The static comparison: `specs/165-media-entry-rest/preview/preview.html` (regenerate with
  `python3 specs/165-media-entry-rest/preview/build_preview.py`).
