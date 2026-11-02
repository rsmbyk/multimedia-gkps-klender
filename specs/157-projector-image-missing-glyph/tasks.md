# Tasks: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`
**Plan**: `specs/157-projector-image-missing-glyph/plan.md`
**Verification split**: 12 test · 9 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Confirm the failure before touching anything: open
  `specs/157-projector-image-missing-glyph/preview/preview.html` and press `Image loaded` — the left board
  draws the glyph at x 1720–1800 with `display: block` and the picture at centre 920, the right board
  `none` at 960 — then run `preview/probe.py` for the same numbers, and read `static/web/projector.js:220`
  (`missing.hidden = true`) against `projector.html:46` (no `hidden`). No setup task exists: no dependency,
  no ignore file, no route.

## Phase 2 — Foundational

None. The two cases and the three code lines share no prerequisite: `_page`'s route stub, the service
fixture and the reach to the image screen already exist in `tests/e2e/test_image_display.py:34-71`.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: an image screen shows the picture alone, and the glyph only when the bytes failed.
**Independent test**: `test_projector_loaded_image_shows_no_placeholder` green while the 404 case stays
green; red before the code change.

- [X] T002 [P] [US1] Write `test_projector_loaded_image_shows_no_placeholder` in
  `tests/e2e/test_image_display.py`: drive to the image screen with `_page`'s 200 route, then assert
  `.screen.is-active .screen__image` is visible and `.screen.is-active .screen__image-missing` is hidden.
  Covers FR-001, FR-005, US1/AC1, US2/AC1.
- [X] T003 [P] [US1] Write `test_a_pending_image_screen_paints_nothing` in the same file: give `_page` a
  `pending=True` keyword whose file route returns without fulfilling, drive to the image screen, and
  assert neither `.screen__image` nor `.screen__image-missing` is visible. Covers FR-004, SC-003, US1/AC3.
- [X] T004 Run T002 and T003 against the **unmodified** template and script and record the red output in
  `analysis.md`'s History: both fail on `Locator expected to be hidden` for
  `.screen.is-active .screen__image-missing`, which computes `display: block`.
- [X] T005 [P] [US1] `multimedia/web/templates/reading/projector.html:46` — add `hidden` to the image
  box's `<svg class="screen__image-missing" …>`, as the audio, video, PDF and slides placeholders below it
  already carry.
- [X] T006 [P] [US1] `static/web/projector.js:220` — `missing.setAttribute('hidden', '')` in place of
  `missing.hidden = true`; `:232` — `missing.removeAttribute('hidden')` in place of `missing.hidden = false`.
- [X] T007 [US1] `static/web/projector.js:198-209` (`clearImageScreen`) — reset the host's placeholder when
  the screen is left, mirroring `clearVideoScreen` (`:137-143`).
- [X] T008 [US1] Re-run T002 and T003: green.

## Phase 4 — US2 (P2)

**Goal**: the suite cannot pass this again by accident.
**Independent test**: the 404 case still asserts the glyph is visible, with its assertion untouched, and
the loaded case now covers the other half.

- [X] T009 [US2] Run `…::test_missing_preview_and_projector_icon` unchanged — covers FR-002, US1/AC2,
  US2/AC2 — and read the case to confirm no assertion was rewritten to suit the fix.
- [X] T010 [US2] Run `manage.py test tests.e2e.test_image_display --keepdb --noinput` in full: green apart
  from the reds `backlog/board.md` already lists as identical on develop. Covers SC-004.

## Phase 5 — Polish

- [X] T011 `inspection` — read the diff: one template attribute, three lines in `projector.js`, two cases
  and one keyword in the test module; `static/styles/design/projector.css`, `media-image.js`, the
  audio/video/PDF/slides paths and the preview modal are untouched (FR-006). Covers FR-003's reset by
  inspection, US1/AC4, and the two edges that share the existing catch — the revoked object URL
  (`projector.js:202-207`), the abort's token guard (`:221-227`) and `static/web/media-image.js:22`'s MIME throw.
- [X] T012 `inspection` — `preview/probe.py`: `loaded` (right `none` / `960 ÷ 960`, left `block` /
  `920 ÷ 960` / `−40px`), `failed` (`80×80 at x 920–1000`), `pending` (left paints the glyph, right
  nothing), and the oversize edge re-measured at a 1280×720 stage. Covers SC-001, SC-002.
- [X] T013 Run `tests.e2e.test_audio_display`, `tests.e2e.test_video_display`,
  `tests.e2e.test_pdf_display`: unchanged. Covers SC-005.
- [X] T014 Add the spec's index row to `specs/README.md`, naming 157 and `Accepted`.
- [X] T015 Move `ITEM-164` to `Ready` on `backlog/board.md` (gate 1 accepted) and record the anchor issue
  in its `issue:` field (BRD-10).
- [X] T016 Bump `VERSION` `1.22.10` → the next patch as read at delivery, and add one `### Fixed` line
  under `## [Unreleased]` in `CHANGELOG.md`.
- [X] T017 Fold: add R3 to `docs/spec/projector.md` and move the header's `last folded` and `slices`
  (SDD-23, `fold.md`).
- [X] T018 Delivery, after the report: open the PR as a draft, then read `ITEM-164`'s state and set
  `in-review`, write `pr:` and move the board row, and push that one commit (`C-BOARD-GIT`) — on the
  owner's word only (GIT-07).

## Phase 6 — Convergence

- [X] T019 [Convergence, post-merge] `manual` — after the merge, from `preview/README.md`'s Live check:
  open `/projector?service=<id>` on the compose `web` container, press Space and step to the image screen
  (the picture alone), then stop the `media` container and step back (the glyph, no picture).
  Checked 2026-11-02 on `/projector?service=144` at 1.26.0: screen 4 showed the picture alone with the
  companion up (natural width 182px, glyph hidden); after `docker stop media` and a step away and back,
  the picture was hidden and the glyph shown; the companion was restarted afterwards.

<!-- written by Converge only beyond this point; absent until it runs -->
