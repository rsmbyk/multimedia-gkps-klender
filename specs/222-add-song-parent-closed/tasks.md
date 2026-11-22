# Tasks: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`
**Plan**: `specs/222-add-song-parent-closed/plan.md`
**Verification split**: 14 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Confirm the slice worktree is on `fix/222-add-song-parent-closed` from `develop`, and that the accepted spec, preview and research are present.

## Phase 2 — Foundational

- [X] T002 Write a failing E2E test in `tests/e2e/test_editor.py` for FR-001/FR-002/SC-001–SC-003/US1 AC1–AC3: from the home page click through Kidung, open a non-hymn songbook, collapse only the first sidebar, assert `#songAdd` is `flex` and 38px while `#panelAdd` is `none`, and exercise the mini state directly.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the second-level `Add song` control stays usable when the first sidebar is mini or closed.
**Independent test**: the E2E path above, plus clicking `Add song` in that state and reaching the "New song" dialog.

- [X] T003 [P] [US1] Add the failing assertions for SC-002 (dialog opens) and SC-004/US1 AC4 (closing the songs list leaves no visible add control) to the same E2E test.
- [X] T004 [US1] Scope the hide rule in `static/styles/design/components.css` to `.panel .editor-add`, leaving `.ch__add .editor-add` governed by its own sidebar.
- [X] T005 [US1] Run the E2E test to green, checking the failure was the `display: none` assertion before the fix.

## Phase 4 — Polish

- [X] T006 [P] Verify the static preview and the product CSS agree on the 38px box and hidden `#panelAdd`, at 1440×900, 1000×800 and 390×844.
- [X] T007 Inspect that no editor, template, hymn-book or JS path was changed (FR-005, US1 AC6).

## Phase 5 — Delivery

- [X] T008 Fold `reading/R51` into `docs/spec/reading.md`, stamp the patch bump and changelog line in the delivery commit, and leave the card for its separate close PR.

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->
