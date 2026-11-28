# Tasks: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`
**Plan**: `specs/258-live-reading-freshness/plan.md`
**Verification split**: 24 test · 0 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Confirm the ignore files and the focused test command in `quickstart.md` run from this worktree with the main checkout's venv.

**Checkpoint: Setup** — focused command runs; no credentials in the tree.

## Phase 2 — Foundational

- [X] T002 [P] [US1] Write the red page-version endpoint test in `multimedia/web/tests.py` (FR-001).
- [X] T003 [US1] Add `/freshness/page/` in `multimedia/web/urls.py` and `views.py`; make T002 green.
- [X] T004 [P] [US4] Write the red fingerprint tests for the three scopes in `multimedia/web/tests.py` (FR-002, FR-011).
- [X] T005 [US4] Add `multimedia/web/reading/freshness.py` and the three list endpoints; make T004 green.
- [X] T006 [US1] Add the page's loaded `data-version` attributes in the service and song templates.

**Checkpoint: Foundational** — four endpoints answer; fingerprints are reproducible from their scopes.

## Phase 3 — US1/US2 (P1) 🎯 MVP

**Goal**: a stale service or song page closes dialogs, disables controls and shows the badge.
**Independent test**: a second-client write makes the page invalid within 10 s.

- [X] T007 [P] [US1] Write the red Playwright test for the 10 s poll and invalidation in `tests/e2e/test_live_reading_freshness.py`.
- [X] T008 [US1] Add the poll loop and stale flag in `static/web/reading.js`; make T007 green.
- [X] T009 [US2] Write the red E2E for dialog closure and disabled controls, then implement in `reading.js` and `components.css`.

## Phase 4 — US3 (P1)

**Goal**: the badge's Reload returns the page to current state in place.
**Independent test**: document identity is unchanged after Reload.

- [X] T010 [P] [US3] Write the red E2E for badge wording, position and Reload.
- [X] T011 [US3] Render the badge from the shell template and wire Reload to the existing `gkpsNavigate` refresh; make T010 green.

## Phase 5 — US4/US5 (P1)

**Goal**: sidebars follow external changes while keeping the operator's view.
**Independent test**: row identity, filter, sort and scroll survive reconciliation.

- [X] T012 [P] [US4] Write the red E2E for fingerprint polling, changed-row update, deletion and insertion.
- [X] T013 [US4] Wire the three list polls and fragment fetch into `reading.js` reuse of `reconcileChildren`; make T012 green.
- [X] T014 [P] [US5] Write the red E2E for filter, sort, scroll and panel state preservation.
- [X] T015 [US5] Preserve those values around reconciliation in `reading.js`; make T014 green.
- [X] T016 [P] [US5] Write the red E2E for template-mode isolation and alphabetical insertion.
- [X] T017 [US5] Anchor the list endpoints in their scopes and apply the existing order functions; make T016 green.

## Phase 6 — Polish

- [X] T018 [US1] Add in-flight and visibility guards to each poll in `reading.js`.
- [X] T019 [US1] Add the failed-poll recovery E2E and make it green.
- [X] T020 Re-run the preview probe and update `preview/README.md` only if measured numbers drift.
- [X] T021 Run the focused endpoint and E2E suites; record the verification split in `converge.md`.

## Phase 7 — Convergence

- [X] T022 [US1–US5] Fix the five Converge gaps: page kind mapping, live baseline, reload reset, animation capture and static manifest.
- [X] T023 [US1–US5] Record the verification evidence and the seven known-red failures in `converge.md`.


## Requirement coverage

- FR-001 → T002, T003 · FR-002 → T004, T005 · FR-003 → T007, T008 · FR-004 → T009 · FR-005 → T010, T011 · FR-006 → T010, T011
- FR-007 → T012, T013 · FR-008 → T012, T013 · FR-009 → T014, T015 · FR-010 → T012, T013 · FR-011 → T004, T005, T017 · FR-012 → T019 · FR-013 → T018
- SC-001 → T007, T008 · SC-002 → T009 · SC-003 → T010, T011 · SC-004 → T012, T013 · SC-005 → T016, T017 · SC-006 → T014, T015