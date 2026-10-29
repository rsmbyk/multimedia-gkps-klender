# Quickstart: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and its Chromium builds already
  installed).
- A database no other worktree is using: `DATABASE_URL=postgres://multimedia:***@127.0.0.1:59075/gkps157`.
  Django creates and drops `test_gkps157` for the run, so sibling slices cannot collide with it.
- For the live route only: the compose `media` companion on `127.0.0.1:63174`, and a service in that
  database holding an image entry.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-157
export PY=../multimedia-gkps-klender/.venv/bin/python
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/gkps157"   # real password from docker-compose.yml
```

## Run

```sh
$PY manage.py test tests.e2e.test_image_display.ImageDisplayE2ETests.test_projector_loaded_image_shows_no_placeholder --keepdb --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the new case | the `Run` command above | red before the fix (`Locator expected to be hidden`), green after it |
| the failure state still paints the glyph | `$PY manage.py test tests.e2e.test_image_display.ImageDisplayE2ETests.test_missing_preview_and_projector_icon --keepdb --noinput` | green before and after; its assertion is not rewritten |
| the rest of the module | `$PY manage.py test tests.e2e.test_image_display --keepdb --noinput` | green, apart from the reds `backlog/board.md` already lists as identical on develop |
| the preview's numbers | `$PY specs/157-projector-image-missing-glyph/preview/probe.py` | `loaded`: left `block` / centre `920` / offset `−40px`, right `none` / `960` / `0px` |
| the box itself | open `specs/157-projector-image-missing-glyph/preview/preview.html` | the three buttons set both boards; no glyph on the right board in `Image loaded` |

## Not yet runnable

- The live `/projector?service=<id>` route before the change lands: it needs a service with an image entry
  in the worktree's database and a companion holding those bytes. The command is in
  `preview/README.md` (`runserver 0.0.0.0:8833`), and it is the `manual` row of the plan's traceability
  table, not a gate.
