# Tasks: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`
**Plan**: `specs/131-retire-break-entry/plan.md`
**Verification split**: 16 test · 0 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 `specs/131-retire-break-entry/preview/probe_break_controls.py` — the headless probe that photographs
  the add row and the empty tile row, prints their geometry, and saves both frames before and after removing
  the Break control

## Phase 2 — Foundational (red first, both files)

- [X] T002 [P] `multimedia/web/tests.py` — `ServiceEntryKindRetirementTests::test_no_page_offers_a_break`
  (three add surfaces, no `data-entry-open="section_break"`),
  `…::test_an_empty_service_offers_four_tiles` (four buttons, four labels, `Add Break` absent),
  `…::test_the_kind_and_its_rows_survive` (value `3`, display name, an existing row still renders)
- [X] T003 [P] `multimedia/web/tests.py` — `ServiceEntryKindRetirementTests::test_the_break_kind_cannot_be_created`
  (three POST shapes, `404`, no row) and `…::test_an_existing_break_cannot_be_edited` (form `404`, save `404`,
  row unchanged)
- [X] T004 `tests/e2e/test_entries.py` — the tile counts `5 → 4`, the label tuple without `Add Break`, and an
  assertion that no `Add Break` tile exists, in the rebuild and in the empty service
- [X] T005 `tests/e2e/test_tatib_section_break.py` — `test_plus_break_adds_the_break_at_once_without_a_dialog`
  becomes `test_the_add_row_offers_no_break`; add `test_a_break_deletes_from_its_divider` (hover → Delete →
  confirm → row gone, order compacted)
- [X] T006 `tests/e2e/test_edit_request_feedback.py` — remove `test_non_modal_break_write_disables_only_its_initiating_button`:
  the behaviour it guards (a break's direct write) no longer exists, per TDD-07

## Phase 3 — US1 (P1) 🎯 MVP: no surface offers a new Break

**Goal**: the three creation surfaces and the writing endpoints refuse the kind.
**Independent test**: an add row, the start bar and an empty service offer four kinds; a direct POST creates nothing.

- [X] T007 [US1] `multimedia/web/reading/entries.py` — remove `SectionBreakEntryForm` and the `section_break`
  entries in `KINDS`, `FORMS` and `TITLES`; `build_entry_form` now answers `None`, which the views already turn
  into `Http404('Unknown kind.')`
- [X] T008 [US1] `multimedia/web/templates/reading/tatib.html` — the Break button leaves the start bar, the
  per-item add row and the empty tile row
- [X] T009 [US1] `static/styles/design/components.css` — `.entry__empty-actions` `repeat(5, …)` →
  `repeat(4, …)`; comment updated; the narrow-container rule stays three columns
- [X] T010 [US1] `static/web/entries.js` — `EMPTY_ADD_ICONS` and `EMPTY_ADD_LABELS` lose `section_break`, the
  rebuild's kind list loses it, `addBreak()` and its special case in the click handler are removed
- [X] T011 [US1] `static/web/offline-render.js` — `addButtons` and `emptyAddButtons` lose `section_break`
  (names and glyph maps too)
- [X] T012 [US1] Sweep the creation surfaces: `grep -rn 'section_break' multimedia/web/templates static/web`
  returns only the rendering paths (`views.py`, `_toc.html`), never an add control

## Phase 4 — US2 (P1): the breaks already written still read as dividers

**Goal**: no rendering change; the existing assertions are the proof.
**Independent test**: open a service holding a Break: one divider on stage and in the sidebar, one projector screen.

- [X] T013 [US2] Run `tests.e2e.test_tatib_section_break`'s divider tests, `tests.e2e.test_projector`'s break
  screen test and `multimedia/web/tests.py`'s divider tests against the changed branch — all green, no edits

## Phase 5 — US3 (P1): delete and reorder keep working, edit is refused

**Goal**: the retired kind stays deletable and movable, and cannot be edited or recreated.
**Independent test**: delete a break from the divider; drag it; ask the edit form for it.

- [X] T014 [US3] `tests/e2e/test_tatib_section_break.py::…::test_a_break_deletes_from_its_divider` green
  (from T005); `tests/e2e/test_reorder.py::…::test_dragging_a_section_break_from_its_divider_reorders_the_row` green
- [X] T015 [US3] `tests.e2e.test_edit_request_feedback` green after T006 (the remaining feedback paths)

## Phase 6 — Polish

- [X] T016 [P] Re-run `preview/probe_break_controls.py` on the finished branch and compare with the spec's
  numbers; retake the frames if the tree moved
- [X] T017 Docs at Fold: `CHANGELOG.md`, `VERSION`, `specs/README.md`, `backlog/board.md`,
  `docs/spec/reading.md` (the capability requirement), and the `five tiles` comment in
  `tests/e2e/test_saved_render_parity.py`

## Phase 7 — Convergence

**Converged on pass 2** — see `converge.md`. No requirement gap; three removals recorded (a test whose behaviour is gone, two tests repointed at Text, the empty row's fifth track). Two failures on other suites reproduced on `develop` and are not this slice's. The fold is `docs/spec/reading.md` `R6` (modified) + `R8` (added), recorded in `fold.md`.

- [X] T018 `converge.md` — every requirement re-read against the shipped diff; no code assumed complete because
  a box is ticked (SDD-22)
