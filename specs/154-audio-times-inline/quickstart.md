# Quickstart: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Plan**: `plan.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and its Chromium build already
  installed).
- The compose `db` on `127.0.0.1:59075` (`docker compose port db 5432` from the main checkout), and a
  database URL no other worktree is using.
- For the browser preview only: the compose `media` companion on `127.0.0.1:63174` serving the audio file
  behind entry `e1`, with `http://localhost:8814` in `GKPS_MEDIA_ALLOWED_ORIGINS` (see `research.md` D005).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-154
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*: *//')
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/gkps154"
export DJANGO_SECRET_KEY=dev-insecure-local-only-change-me
```

## Run the case

```sh
$PY manage.py test tests.e2e.test_audio_display.AudioDisplayE2ETests.test_preview_times_read_current_over_total_beside_the_bar --noinput
```

## Run the module (the line touches the player the other five cases drive)

```sh
$PY manage.py test tests.e2e.test_audio_display --noinput
```

`test_untitled_preview_and_projector_idle_display_off` fails on unmodified `develop` too (`data-showing`
stays `true` — ITEM-140), so a single red there is not this slice.

## Open the preview

```sh
$PY manage.py collectstatic --noinput        # Whitenoise serves `_static/`, not `static/`
$PY manage.py runserver 0.0.0.0:8814 --noreload
```

Then `http://localhost:8814/tatib/144/` → entry `e1`'s Preview. The player appears only when the companion
answers that origin (D005); otherwise the dialog shows `Audio unavailable on this computer`.
