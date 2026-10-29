# Quickstart: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`

## Prerequisites

- The Python venv of the **main checkout** — `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv`
  (a worktree has no venv of its own). It has Django 4.0, pytest/Playwright and a Chromium build.
- The compose stack's PostgreSQL, published on `127.0.0.1:59075` (`docker ps` → `…-db-1`). No app
  container is needed: the E2E modules run Django's live server themselves and stub the media companion.
- Nothing else — no `collectstatic`, no companion, no network.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-158
export PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
# a database name of its own: Django makes and drops `test_gkps158`, so another slice's test run
# cannot hold it
export DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/gkps158
```

## Run

```sh
# the two modules this slice touches
$PY manage.py test tests.e2e.test_image_display tests.e2e.test_pdf_display --noinput

# the whole projector module, for regressions around keys, cue and detours
$PY manage.py test tests.e2e.test_projector --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| a small image fills the stage | `$PY manage.py test tests.e2e.test_image_display.ImageDisplayE2ETests.test_projector_enlarges_a_small_image_to_the_stage --noinput` | painted image 1376×688 on a 1440×900 window (was 12×6) |
| a page fills the stage | `$PY manage.py test tests.e2e.test_pdf_display.PDFDisplayE2ETests.test_projector_enlarges_a_pdf_page_to_the_stage --noinput` | painted canvas 603×804 on the same window (was 300×400) |
| `T` switches the axis | `…::test_projector_t_toggles_fit_width_and_height --noinput` | 1608×804 after `T` (cut 116 each side), back to 1376×688 |
| drag and wheel pan, clamped | `…::test_projector_pans_the_overflow_by_drag_and_wheel --noinput` | `translate` follows the pointer and stops at ±116 |
| a press that does not move still navigates | `…::test_projector_press_without_drag_still_steps --noinput` | one screen step, `translate` unchanged |
| the sheet lists `T` and still fits | `…::test_shortcut_sheet_lists_the_fit_key --noinput` | `Image and PDF` group present; sheet 1124×677 at 1200 tall, 992×677 at 1024×768 |
| the design, by eye | `xdg-open specs/158-projector-media-fit/preview/index.html` | the fit, `T` and the pan, with `Today (1:1)` beside them |

## Not yet runnable

- **A live look at this branch's projector against the real library.** The Media Library companion
  (`127.0.0.1:63174`) allows exactly `http://127.0.0.1:63404` and `http://localhost:63404`, and that
  port is the compose `web` container serving `develop`. A worktree server on any other port is refused
  by the companion (`403 Origin is not allowed.`), so the slice's own surface is previewed statically
  and verified through the E2E stubs, which serve the same-origin bytes the page asks for.
- **A unit test of `fitMedia()`** — the repository has no JavaScript test runner (D008); the behaviour is
  pinned by the E2E measurements instead.
- **The six `Verify` rows above, until implementation** — they name cases that land with tasks T003–T018;
  run today, each exits 2 ("no tests ran"). The setup and the two module commands do run.
