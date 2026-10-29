# Quickstart: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`

## Prerequisites

- The main checkout's virtualenv: `~/Projects/multimedia-gkps-klender/.venv/bin/python`
- The compose database: `docker compose port db 5432` (59075 on this machine), `multimedia/multimedia`
- The local media companion on `127.0.0.1:63174` — or a browser route that fakes it

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-145
DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8821 --noreload
```

## Run

```sh
open http://127.0.0.1:8821/tatib/149/
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the label rule | `node -e 'global.window={};require("./static/web/media-size.js");console.log([512,1000,12345,999999,1250000].map(window.gkpsFormatSize).join(" · "))'` | `512 B · 1 KB · 12.3 KB · 1 MB · 1.3 MB` |
| the card and the library | `manage.py test tests.e2e.test_media_library.MediaLibraryE2ETests.test_media_size_reads_in_the_smallest_unit_that_shows_a_number --keepdb` | pass |
| the whole media suite | `manage.py test tests.e2e.test_media_library --keepdb` | pass |
| the dead formatter is gone | `grep -n '\bfmt\b' static/web/media-handoff.js` | no output |

## Not yet runnable

- None.
