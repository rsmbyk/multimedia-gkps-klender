# Tasks: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`
**Plan**: `specs/209-open-created-service/plan.md`
**Verification split**: 14 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Verify the worktree is on `feat/209-open-created-service` at base `989347f2`, that
  `specs/209-open-created-service/reproduce.py` runs against `127.0.0.1:63404`, and that no spec/ITEM
  number collides with a sibling branch; no ignore rule is needed (reproduction writes no files).
- [X] T002 Read `multimedia/web/reading/views.py:173-185`, `static/web/editors.js:192-252` and
  `static/web/reading.js:2033-2064` again immediately before editing; record the exact lines in the
  convergence note.

## Phase 2 — Foundational

- [X] T003 Write a failing `tests/e2e/test_editor.py::test_a_created_service_opens_on_the_stage`
  against the base commit: after one sidebar Normal save, read URL, `#readName`, the current row and
  the empty-service actions (FR-001, SC-001).
- [X] T004 Write a failing `test_an_open_from_create_does_not_reload_the_document`: set an in-page
  marker and record `performance.timeOrigin` before the save, then assert both survive and
  `data-nav` is unchanged (FR-002, SC-002).
- [X] T005 Write a failing `test_a_created_service_opens_its_contents_pane`: after the save the
  child pane is open with the new service's entries, matching a row click (FR-002).
- [X] T006 Add `created` and, for `tatib`, `record_kind` to the 200 JSON in
  `multimedia/web/reading/views.py` (`editor_save`); the fields are additive and no other status or
  response shape changes (D001).

## Phase 3 — US1 (P1) 🎯 MVP — the stage follows the create

**Goal**: the operator lands on the service they just made, without a second click or a reload.
**Independent test**: create one Normal service from `/tatib/`; the stage shows its name and empty
actions, the URL is `/tatib/<id>/`, and the page did not reload.

- [X] T007 [US1] In the `editor:saved` listener in `static/web/reading.js`, branch on
  `kind === 'tatib' && detail.created && detail.record_kind === 0` and call
  `navigate('/tatib/' + detail.id + '/', {kind: 'service', forceServer: true})` before the existing
  refresh; restore quiet focus to the new row after navigation resolves (spec 025), and leave the
  refresh branch untouched for every other event (T003–T005, D002).
- [X] T008 [US1] Update `test_add_empty_active_tatib` in `tests/e2e/test_editor.py` to click the
  `.book` row by `[data-name]` after the save instead of `get_by_text`, because the stage heading now
  carries the same name (inspection row US1/AC1).
- [X] T009 [US1] Re-run T003–T005 green and read back the assertions; a pass on an import or timeout
  does not count (TDD-02).

## Phase 4 — US2 (P2) — only a Normal create moves the stage

**Goal**: Template creates, edits and other record saves keep their present behaviour.
**Independent test**: create a Template and edit a service; neither changes the stage or URL.

- [X] T010 [P] [US2] Write a failing `test_an_open_from_create_keeps_the_panel_state`: create a
  Normal service with the first panel collapsed/mini and another record current; `data-nav` and that
  other selection are unchanged (FR-003).
- [X] T011 [P] [US2] Write a failing `test_a_template_create_keeps_the_stage`: a Template create
  leaves stage, URL and `data-ch` as they were (FR-004).
- [X] T012 [P] [US2] Write a failing `test_an_edit_keeps_the_stage`: editing an existing service
  keeps today's list refresh and does not switch the stage (FR-004).
- [X] T013 [US2] Verify the guard in T007 covers all three tests; no second navigation mechanism is
  added, and `static/web/editors.js` is not edited.
- [X] T014 [US2] Inspect `tests/e2e/test_editor.py` song/songbook saves and `static/web/editors.js`
  to confirm other record kinds still dispatch the same event to the refresh branch (inspection row
  FR-004).

## Phase 5 — US3 (P2) — a refused create changes nothing

**Goal**: a failed save never claims a service on the stage.
**Independent test**: submit an invalid form and a refused request; the stage and URL stay put.

- [X] T015 [P] [US3] Write a failing `test_a_refused_create_keeps_the_stage`: validation returns 400,
  the dialog stays open, and URL, heading and marker are unchanged (FR-005, SC-004).
- [X] T016 [P] [US3] Write a failing `test_a_failed_create_keeps_the_stage`: a failed save response
  leaves the stage where it was and shows today's failure message (FR-005).
- [X] T017 [US3] Verify the guard in T007 only runs on a successful 200 response; no extra code is
  needed if T015–T016 pass against the implemented branch.

## Phase 6 — Unchanged flows and verification

- [X] T018 [P] Re-run `test_a_fill_in_and_a_choice_settle_then_create` in
  `tests/e2e/test_tatib_templates.py`: generate still navigates to the created service (FR-006).
- [X] T019 [P] Re-run `test_copy_as_template_asks_and_copies` in `tests/e2e/test_tatib_templates.py`:
  copy-as-template still navigates to its new record (FR-006).
- [X] T020 Run the focused modules `tests.e2e.test_editor` and `tests.e2e.test_tatib_templates`
  with `DJANGO_DEVELOPMENT_MODE=true` after the last edit, and leave the tree alone until the run
  returns; record the counts.
- [X] T021 Converge against the plan's traceability table: type every gap `missing` · `partial` ·
  `contradicts` · `unrequested`, append `converge.md`, at most three passes.
- [X] T022 Fold the typed delta for `reading/R46` into `docs/spec/reading.md`, write `fold.md`, and
  move `last folded` to the fold date with the slice id prepended (SDD-23).

## Phase 7 — Delivery (after Converge)

- [ ] T023 Commit at Fold — spec pack, code, E2E changes, capability delta and board row together,
  only with the focused suites green (GIT-06, C-TDD-GIT).
- [ ] T024 Stamp `VERSION` 1.35.0 → 1.35.1 and add the `## [Unreleased]` `### Fixed` line immediately
  before the merge; create ITEM-222 with `bump: patch` in the same delivery commit (VER-04/07).
- [ ] T025 Set ITEM-222 to `in-review` with the PR number and move its board row, then open the PR
  **as a draft**; do not push, mark ready or close the card without the owner's word (GIT-07).
- [ ] T026 Report what shipped, the verification split, convergence and gaps, the folded capability,
  branch and commit count, version/changelog line, PR title and body, and that nothing is pushed —
  then ask about pushing (SDD-27).

## Phase 8 — Convergence

<!-- written by Converge only; absent until it runs -->
