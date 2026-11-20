# Quickstart: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md`

## Prerequisites

- Python 3.12 venv at `../multimedia-gkps-klender/.venv/bin/python` (Django 4.0.1, Playwright).
- Chromium from `playwright install chromium`.
- A reachable Postgres. The main compose stack's DB is on port 59075.

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-202
export DATABASE_URL='postgres://multimedia:multimedia@127.0.0.1:59075/multimedia'
../multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_obs_caption_height --tag=e2e -v 2
```

Open `/obs/source/overlay` at 1920×1080 with a song on air to see the rest size; a long lyric shows
the fit and the floor.
