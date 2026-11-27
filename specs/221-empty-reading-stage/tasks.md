# Tasks: an empty reading stage after deleting the open record

**Spec**: `specs/221-empty-reading-stage/spec.md` (Accepted, Gate 1 2026-11-22)
**Plan**: `specs/221-empty-reading-stage/plan.md`
**Branch**: `fix/221-empty-reading-stage`

`[P]` means order-independent, not concurrent: one agent, one thread.

## Phase 1 — Setup

- [X] T001 [P] [US1] Confirm the worktree is on `fix/221-empty-reading-stage` cut from `develop`, `VERSION` reads `1.36.6`, and no `stage=empty` code exists yet — `VERSION`, `static/web/editors.js`
- [X] T002 [P] [US1] Confirm the preview's approved copy and boxes are the contract: "Nothing open." / hint, `.read` 520×153 at (856,40) and 354×126 at (18,76) — `specs/221-empty-reading-stage/preview/README.md`

## Phase 2 — Foundational (the failing tests come first)

- [X] T003 [US1] Write the seven E2E tests in `DeletedStageE2ETests`: song, service, template, songbook, reload/history, off-stage delete and geometry — `tests/e2e/test_deleted_stage.py`
- [X] T004 [US1] Run the module and record the red output: on-stage deletes still land with `data-read="off"` and the search field visible — `tests/e2e/test_deleted_stage.py`

## Phase 3 — US1: deleting the open song keeps a reading view

- [X] T005 [US1] Add `_empty_stage(request)` and set `read_on`, `home_state`, `read_name` and `read_hint` in `BookDetailView` — `multimedia/web/reading/views.py`
- [X] T006 [US1] In `base.html`, suppress the reading header when `read_hint` is set and render the `.entry__empty` block (empty-screen icon, `Nothing open.` title, subtitle) inside `#readBody`
- [X] T006a [US1] Add `.entry__empty-icon` (38px glyph) and the stage-centring rules (stage grid, full-width read, body margins zero) beside the existing `.entry__empty` rules — `static/styles/design/components.css`
- [X] T007 [US1] On an on-stage delete, append `stage=empty` to `parentListUrl(kind)` before `gkpsNavigate(..., {kind:'refresh', replaceUrl:true})`; update the stale `gkpsStage` comment — `static/web/editors.js`
- [X] T008 [US1] Run the song, reload/history and geometry tests and see them green — `tests/e2e/test_deleted_stage.py`

## Phase 4 — US2/US3: the other kinds and the unchanged case

- [X] T009 [US2] Apply the same empty render to `BookIndexView` and `TatibView`, preserving `mode=template` and the list panels — `multimedia/web/reading/views.py`
- [X] T010 [US2] Run the service, template and songbook tests and see them green — `tests/e2e/test_deleted_stage.py`
- [X] T011 [US3] Run the off-stage test and confirm the stage, URL and datasets are unchanged — `tests/e2e/test_deleted_stage.py`

## Phase 5 — Polish and delivery

- [X] T012 Re-assess every traceability row by its declared method; write `converge.md` (pass 1) — `specs/221-empty-reading-stage/converge.md`
- [X] T013 Fold: modify the on-stage landing clause of `R41` with the complete replacement block; write `fold.md` — `docs/spec/reading.md`, `specs/221-empty-reading-stage/fold.md`
- [X] T014 Apply the declared bump: `VERSION` `1.36.6 → 1.36.8` and one `### Fixed` line under `## [Unreleased]` in `CHANGELOG.md`
- [X] T015 Board: card `bump: patch`, and at delivery `status: in-review`, `pr:` and the board row once the PR number exists — `backlog/items/ITEM-236-deleted-record-empty-stage.md`, `backlog/board.md`
- [X] T016 Open the PR (draft, then ready) with the closing report's title and body, and report — nothing pushed until the owner says so
