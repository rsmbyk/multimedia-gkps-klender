# Quickstart: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`

## Prerequisites

- The repo's virtualenv, in the main checkout: `~/Projects/multimedia-gkps-klender/.venv`
- Playwright's Chromium for that venv (`~/.cache/ms-playwright/chromium-*`)
- PostgreSQL from the compose stack; its host port comes from `docker compose port db 5432`
- No new dependency, no migration, no `collectstatic` for the preview (it carries copies of the
  stylesheets)

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-149
python3 specs/149-transfer-separator-seam/preview/build_preview.py    # refresh the frozen stylesheets
```

## Run

```sh
# the preview: open the file directly
open specs/149-transfer-separator-seam/preview/preview.html

# the slice running, for the live route
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/gkps149" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8830 --noreload
```

Open `http://127.0.0.1:8830/media-library/`, upload a file, and press the transfers button in the
rail once it finishes.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The seam draws one line | `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_media_library --keepdb` | `test_the_session_seam_draws_one_line` and `test_the_seam_keeps_equal_space_either_side` pass |
| The list scrolls inside the dialog | same command | `test_a_long_transfer_list_scrolls_inside_the_dialog` passes: 0px past the inner bottom edge, 22px at the end of the scroll |
| A short list is unchanged | same command | `test_a_short_transfer_list_keeps_its_natural_height` passes |
| The preview's numbers | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/149-transfer-separator-seam/preview/probe.py` | the table matches `spec.md`'s `## UI/UX`: seam `2 · 1px + 2px` → `1 · 2px`, list past the edge `19px` → `0px` |

The E2E run needs `DATABASE_URL` pointing at a database name no other session is using; the command
above creates and drops `test_gkps149`.

## Not yet runnable

- **The live rail-button path with a real upload.** It needs the local companion and a file to upload;
  the E2E fakes `/v1/transfers`, so the live check is by hand on the dev server above.
