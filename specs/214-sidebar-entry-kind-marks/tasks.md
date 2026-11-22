# Tasks: a contents row marks its entry's kind

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md` · **Plan**: `plan.md`
**Branch**: `feat/214-sidebar-entry-kind-marks` · **Bump**: `patch`

Order: Setup → Foundational → one phase per story (red then green for each `test` row) → Polish.
`[P]` means order-independent, not concurrent: one agent, one thread, in the order printed here.

## Setup

- [X] T001 [P] verify the slice worktree is on feat/214-sidebar-entry-kind-marks based on origin/develop
- [X] T002 [P] confirm the preview probe runs and reproduce the spec’s 24px / 42px / 66px figures

## Foundational

- [X] T003 [P] add `mark` and `mark_kind` keys to every toc row in multimedia/web/reading/views.py
- [X] T004 [P] create multimedia/web/templates/reading/_toc_mark.html with one glyph per kind and the slot kind modifier
- [X] T005 [P] include the partial after `.songrow__c` in multimedia/web/templates/reading/_toc.html
- [X] T006 [P] add scoped `.songrow__mark`, 24px number box and 8px gap rules in static/styles/design/components.css
- [X] T007 [P] append the requirements checklist item for the slot modifier (already at CHK016)

## TDD-US1

- [X] T008 [P] [US1] write a failing test for US1/AC1 — passage and song rows carry distinct marks in tests/e2e/test_sidebar_kind_marks.py::test_passage_and_song_rows_carry_their_marks
- [X] T009 [US1] make US1/AC1 — passage and song rows carry distinct marks pass in tests/e2e/test_sidebar_kind_marks.py::test_passage_and_song_rows_carry_their_marks
- [X] T010 [P] [US1] write a failing test for US1/AC2 — text and media rows carry their marks in tests/e2e/test_sidebar_kind_marks.py::test_text_and_media_rows_carry_their_marks
- [X] T011 [US1] make US1/AC2 — text and media rows carry their marks pass in tests/e2e/test_sidebar_kind_marks.py::test_text_and_media_rows_carry_their_marks
- [X] T012 [P] [US1] write a failing test for US1/AC3 — slot rows keep the dashed frame and corner kind modifier in tests/e2e/test_sidebar_kind_marks.py::test_slot_rows_keep_the_kind_modifier
- [X] T013 [US1] make US1/AC3 — slot rows keep the dashed frame and corner kind modifier pass in tests/e2e/test_sidebar_kind_marks.py::test_slot_rows_keep_the_kind_modifier
- [X] T014 [P] [US1] write a failing test for US1/AC4 — the mark set is pairwise distinct in multimedia/web/tests.py::ServiceEntryViewTests::test_mark_set_is_pairwise_distinct
- [X] T015 [US1] make US1/AC4 — the mark set is pairwise distinct pass in multimedia/web/tests.py::ServiceEntryViewTests::test_mark_set_is_pairwise_distinct

## TDD-US2

- [X] T016 [P] [US2] write a failing test for US2/AC1 — a row’s accessible name is unchanged in tests/e2e/test_sidebar_kind_marks.py::test_row_accessible_name_is_unchanged
- [X] T017 [US2] make US2/AC1 — a row’s accessible name is unchanged pass in tests/e2e/test_sidebar_kind_marks.py::test_row_accessible_name_is_unchanged
- [X] T018 [P] [US2] write a failing test for US2/AC2 — the mark takes no pointer in tests/e2e/test_sidebar_kind_marks.py::test_mark_takes_no_pointer
- [X] T019 [US2] make US2/AC2 — the mark takes no pointer pass in tests/e2e/test_sidebar_kind_marks.py::test_mark_takes_no_pointer
- [X] T020 [P] [US2] write a failing test for US2/AC3 — focus never lands on the mark in tests/e2e/test_sidebar_kind_marks.py::test_focus_never_lands_on_the_mark
- [X] T021 [US2] make US2/AC3 — focus never lands on the mark pass in tests/e2e/test_sidebar_kind_marks.py::test_focus_never_lands_on_the_mark

## TDD-US3

- [X] T022 [P] [US3] write a failing test for US3/AC1 + FR-005 + SC-003 — number centre, 24px box and row heights hold in tests/e2e/test_sidebar_kind_marks.py::test_number_centre_and_row_heights_hold
- [X] T023 [US3] make US3/AC1 + FR-005 + SC-003 — number centre, 24px box and row heights hold pass in tests/e2e/test_sidebar_kind_marks.py::test_number_centre_and_row_heights_hold
- [X] T024 [P] [US3] write a failing test for US3/AC2 + SC-004 — three-line clamp and pane wrap hold at 404px and 280px in tests/e2e/test_sidebar_kind_marks.py::test_three_line_clamp_and_pane_wrap_hold
- [X] T025 [US3] make US3/AC2 + SC-004 — three-line clamp and pane wrap hold at 404px and 280px pass in tests/e2e/test_sidebar_kind_marks.py::test_three_line_clamp_and_pane_wrap_hold
- [X] T026 [P] [US3] write a failing test for US3/AC3 + FR-006 — a deleted target keeps its mark in multimedia/web/tests.py::ServiceEntryViewTests::test_deleted_target_keeps_its_mark
- [X] T027 [US3] make US3/AC3 + FR-006 — a deleted target keeps its mark pass in multimedia/web/tests.py::ServiceEntryViewTests::test_deleted_target_keeps_its_mark

## TDD-FR

- [X] T028 [P] [FR] write a failing test for FR-001 + SC-001 — every numbered row has exactly one mark in the second child seat in multimedia/web/tests.py::ServiceEntryViewTests::test_every_numbered_row_has_one_mark
- [X] T029 [FR] make FR-001 + SC-001 — every numbered row has exactly one mark in the second child seat pass in multimedia/web/tests.py::ServiceEntryViewTests::test_every_numbered_row_has_one_mark
- [X] T030 [P] [FR] write a failing test for FR-002 — the mark set covers every kind, slots badged in multimedia/web/tests.py::ServiceEntryViewTests::test_mark_set_covers_every_kind
- [X] T031 [FR] make FR-002 — the mark set covers every kind, slots badged pass in multimedia/web/tests.py::ServiceEntryViewTests::test_mark_set_covers_every_kind
- [X] T032 [P] [FR] write a failing test for FR-003 — marks are present in the first response and after the in-place rebuild in multimedia/web/tests.py::ServiceEntryViewTests::test_marks_survive_in_place_rebuild
- [X] T033 [FR] make FR-003 — marks are present in the first response and after the in-place rebuild pass in multimedia/web/tests.py::ServiceEntryViewTests::test_marks_survive_in_place_rebuild
- [X] T034 [P] [FR] write a failing test for FR-007 + SC-006 — contrast holds in both themes in tests/e2e/test_sidebar_kind_marks.py::test_contrast_in_both_themes
- [X] T035 [FR] make FR-007 + SC-006 — contrast holds in both themes pass in tests/e2e/test_sidebar_kind_marks.py::test_contrast_in_both_themes
- [X] T036 [P] [FR] write a failing test for FR-008 — the dock and projector keep their own rows in tests/e2e/test_sidebar_kind_marks.py::test_dock_and_projector_keep_their_own_rows
- [X] T037 [FR] make FR-008 — the dock and projector keep their own rows pass in tests/e2e/test_sidebar_kind_marks.py::test_dock_and_projector_keep_their_own_rows

## TDD-SC

- [X] T038 [P] [SC] write a failing test for SC-002 — the column sits between the number and the label in tests/e2e/test_sidebar_kind_marks.py::test_column_sits_between_number_and_label
- [X] T039 [SC] make SC-002 — the column sits between the number and the label pass in tests/e2e/test_sidebar_kind_marks.py::test_column_sits_between_number_and_label
- [X] T040 [P] [SC] write a failing test for edge — a section-break entry and a legacy EOS row carry no mark in multimedia/web/tests.py::ServiceEntryViewTests::test_divider_row_has_no_mark
- [X] T041 [SC] make edge — a section-break entry and a legacy EOS row carry no mark pass in multimedia/web/tests.py::ServiceEntryViewTests::test_divider_row_has_no_mark
- [X] T042 [P] [SC] write a failing test for edge — a slot with no readable kind draws its frame without a badge in multimedia/web/tests.py::ServiceEntryViewTests::test_slot_with_no_kind_draws_no_badge
- [X] T043 [SC] make edge — a slot with no readable kind draws its frame without a badge pass in multimedia/web/tests.py::ServiceEntryViewTests::test_slot_with_no_kind_draws_no_badge
- [X] T044 [P] [SC] write a failing test for edge — the column holds at drawer and phone widths in tests/e2e/test_sidebar_kind_marks.py::test_mark_column_at_drawer_and_phone_widths
- [X] T045 [SC] make edge — the column holds at drawer and phone widths pass in tests/e2e/test_sidebar_kind_marks.py::test_mark_column_at_drawer_and_phone_widths

## Polish

- [X] T046 [P] inspection: no animation, keyframes or transition on `.songrow__mark` or `.slot__badge` in static/styles/design/components.css
- [X] T047 [P] re-run the frozen suites: number centring, text wrap, stage kind marks, slot badge
- [X] T048 [P] run the preview probe on the live slice and record the measured figures in Converge
- [X] T049 [P] prepare the board card, changelog line and fold notes (no commit before Fold)
