# Quickstart: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)

## Prerequisites

- The repo's virtualenv, in the main checkout: `~/Projects/multimedia-gkps-klender/.venv`
- Playwright's Chromium for that venv (`~/.cache/ms-playwright/chromium-*`)
- PostgreSQL from the compose stack; its host port comes from `docker compose port db 5432`
- No new dependency, no migration, no `collectstatic` for the preview (it carries copies of the
  stylesheets); the live route needs `collectstatic` only if `DEBUG` is off

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-152
python3 specs/152-transfer-scrollbar-edge/preview/build_preview.py    # refresh the frozen stylesheets
```

## Run

```sh
# the preview: open the file directly (Chromium/Chrome — Firefox draws its own bar)
open specs/152-transfer-scrollbar-edge/preview/preview.html

# the slice running, for the live route
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/gkps152" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8832 --noreload
```

Open `http://127.0.0.1:8832/media-library/` and press the Transfers button in the page's toolbar.
Nine completed transfers are enough for the list to scroll at a 760px-tall window.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The list reaches the dialog's edges | `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_media_library --keepdb` | `test_the_transfer_list_reaches_the_dialog_edges` passes: 1px inside the border box on the right and the bottom, and the dialog reports `overflow: clip` |
| The content does not move | same command | `test_the_transfer_content_keeps_its_insets`, `test_a_short_transfer_list_has_no_reserved_gutter` pass |
| The frame and the scroll's end do not move | same command | `test_the_dialog_frame_and_scroll_end_do_not_move` passes: title 23, heading 23, title→list 14, last row 22px above the border at the end |
| The painted result | `~/Projects/multimedia-gkps-klender/.venv/bin/python specs/152-transfer-scrollbar-edge/preview/probe.py` | `canvas bar → right border (px)` 22 → 0; `list bottom inside dialog border box` 23 → 1; `thumb bottom → dialog bottom edge` 24.4 → ~2.4; every other distance equal between the columns |
| Dark, narrow, short | `probe.py --theme dark`, `probe.py --width 420 --height 820`, `probe.py --rows 2` | the same 22 → 0 and 23 → 1, and the content insets unchanged |

The E2E run needs `DATABASE_URL` pointing at a database name no other session is using; the command
above creates and drops `test_gkps152`. The suite runs headless, which paints overlay scrollbars here,
so it measures the list's box and the lane's arithmetic — not the painted bar (D007).

## Not yet runnable

- **The painted bar inside the E2E suite.** It needs a headed browser, which the suite does not
  launch; the probe covers it and `converge.md` quotes its columns.
- **A real upload through the companion.** The preview and the E2E both fake `/v1/transfers`; the
  live check is by hand on the dev server above.
