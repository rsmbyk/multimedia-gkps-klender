# Tasks: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`
**Plan**: `specs/149-transfer-separator-seam/plan.md`
**Verification split**: 17 test · 5 inspection · 0 manual

`[P]` means order-independent, not concurrent — run in one thread.

## Phase 1 — Setup

- [X] T001 Record the baseline on `develop`: the seam paints two lines 10.5px apart, and the list's box runs 19px past the dialog's inner bottom edge at nine rows and 451px at fifteen (`preview/probe.py`, run against the unmodified stylesheet)

## Phase 2 — Foundational

- [X] T002 Add `media-transfers__list` to `<div id="mediaTransfersList">` in `multimedia/web/templates/reading/base.html:456`, keeping the id for `media-handoff.js:36`

## Phase 3 — US1: the seam is one line (P1) 🎯 MVP

**Goal**: the boundary between this session's transfers and the older ones is drawn once.
**Independent test**: `test_the_session_seam_draws_one_line` alone, on the fake companion's nine jobs.

- [X] T003 [P] [US1] Write `test_the_session_seam_draws_one_line` in `tests/e2e/test_media_library.py` — red: the row above the divider reports `1px`, and two boundaries sit within 20px of the seam; also asserts no divider exists when the dialog is opened from `#mediaTransfersButton`
- [X] T004 [P] [US1] Write `test_the_seam_keeps_equal_space_either_side` in the same module — red: there is no single seam line to measure yet
- [X] T005 [US1] Make T003 pass: add `.media-transfers__row:has(+ .media-transfers__divider) { border-bottom-width: 0; }` beside `.media-transfers__row` in `static/styles/design/components.css`
- [X] T006 [US1] Make T004 pass: confirm the divider's `margin: 9px 0` gives 9px above and 9px below once the 1px border is gone, and move the margin only if the measurement says otherwise
- [X] T007 [US1] Re-run the existing `test_sidebar_transfer_session_shows_active_then_finished` unchanged — a dialog with an active transfer still draws no divider

## Phase 4 — US2: the list scrolls inside the dialog (P2)

**Goal**: nothing paints outside the dialog, and its bottom padding survives the overflow.
**Independent test**: `test_a_long_transfer_list_scrolls_inside_the_dialog` on fifteen completed jobs.

- [X] T008 [P] [US2] Write `test_a_long_transfer_list_scrolls_inside_the_dialog` — red: the list reports `scrollHeight == clientHeight` and its box runs past the dialog's inner bottom edge
- [X] T009 [P] [US2] Write `test_a_short_transfer_list_keeps_its_natural_height` — red only if the new rules change a two-row dialog; it pins that they do not
- [X] T010 [US2] Make T008 pass: add `.media-transfers__dialog { display: flex; flex-direction: column; }` and `.media-transfers__list { min-height: 0; overflow-y: auto; }` in `components.css`, beside the dialog's own rule
- [X] T011 [US2] Make T009 pass: `overflow-y: auto` rather than `scroll`, so a two-row list keeps its natural height and shows no bar
- [X] T012 [US2] Re-measure the preview (`preview/probe.py`) and confirm the two rules reproduce the `## UI/UX` numbers at 1920×1200 in both themes

## Phase 5 — Polish

- [X] T013 Run the targeted suites green: `tests.e2e.test_media_library` (whole module) and the design-token suite
- [X] T014 Card ITEM-159, its board row and the `specs/README.md` index row — re-check `spec:` and `branch:` against the folder that exists
- [X] T015 Bump `VERSION` 1.22.4 → 1.22.5 and write the `CHANGELOG.md` line under `## [Unreleased]`
- [X] T016 Fold `docs/spec/media-library.md` — a new capability with `R1`

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->

## Acceptance

- `tests.e2e.test_media_library` — **30/31** after the rebase onto `develop` @ `954dee75`; the one red
  is ITEM-156, proven identical on `develop` at `05379336` in the main checkout
  (`19.9998779296875 != 12`, same command, database and browser) and already carded there.
- `tests.test_design_tokens` — 6/6.
- Preview probe after the rules landed: seam `2 · 1px + 2px` → `1 · 2px`; the list past the dialog's
  inner bottom edge `19px` → `0px` at nine rows and `451px` → `0px` at fifteen; the lowest visible
  boundary `3.5px` → `76.5px` above the dialog's border.
