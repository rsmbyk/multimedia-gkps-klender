# Tasks: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`
**Plan**: `specs/231-add-verse-in-header/plan.md`
**Verification split**: 14 test · 6 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Confirm `ITEM-246` exists, carries `spec: 231-add-verse-in-header` and `branch: fix/231-add-verse-top`, and its anchor issue is recorded.

## Phase 2 — Foundational

- [X] T002 Confirm `songs_verse.js` reads one `[data-add-verse]` node and that the header node would satisfy the reorder write (`backlog` none; code read only).

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a song with verses offers Add verse in the header, immediately left of Project.
**Independent test**: at 1440×900 `/songs/1880/` shows the two buttons in one row and no dashed row below the lyrics.

- [X] T003 [P] [US1] [US1/AC1, SC-001] Write `tests/e2e/test_add_verse_header.py::test_add_verse_sits_left_of_project_in_header` (red on develop).
- [X] T004 [P] [US1] [US1/AC2, FR-004, SC-005] Write `tests/e2e/test_add_verse_header.py::test_header_add_verse_opens_editor` (red on develop).
- [X] T005 [US1] [US1/AC3, FR-002] Update `multimedia/web/reading/test_verse_add_gate.py::test_song_with_verses_keeps_single_header_add_control` to assert the header node and no `.verse-add` row (red first).
- [X] T006 [US1] [FR-001] Move the Add verse button into `read_actions` before Project in `multimedia/web/templates/reading/song.html`, gated on `can_edit_verses and verse_rows`.
- [X] T007 [US1] [FR-005] Add the scoped `.read__project .verse-add__btn--head` height/padding rule in `static/styles/design/components.css`.
- [X] T008 [US1] [US1/AC5, SC-006] Add `test_hymn_song_draws_no_add_verse_but_keeps_project` and confirm the read-only gate still holds.

## Phase 4 — US2 (P2)

**Goal**: an empty song keeps exactly one centre Add verse and no header action.
**Independent test**: `/songs/1909/` has an empty header row and one 112×38 invitation button.

- [X] T009 [P] [US2] [US2/AC1, FR-003] Add `test_empty_song_has_no_header_actions` (red on a build that renders header actions unconditionally).
- [X] T010 [US2] [US2/AC2, US2/AC3, SC-003, SC-004] Re-run the spec-224 pins `test_empty_song_has_one_add_verse_button` and `test_empty_song_has_no_after_verse_row` unchanged.

## Phase 5 — Polish

- [X] T011 [P] [FR-007] Add the `R56` block to `docs/spec/reading.md` at Fold and update the `slices`/`last folded` header.
- [X] T012 [US1/AC4, SC-001, SC-002] Verify the live preview boxes at 1440×900 and the 560px manual state; record them in `converge.md`.
- [X] T013 Add the changelog line and declare the patch level in the delivery commit; leave `VERSION` untouched until then.

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->
