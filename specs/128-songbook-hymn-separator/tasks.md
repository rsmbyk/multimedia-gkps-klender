# Tasks: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`
**Plan**: `specs/128-songbook-hymn-separator/plan.md`
**Verification split**: 12 test · 2 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Add the panel fixtures to `multimedia/web/tests.py::ReadingViewTests.setUpTestData`: a second hymn book with a larger song count, and ordinary songbooks whose names exercise folding (`buku ende`, `Zebra`), so the assertions below can distinguish group order from accident.

## Phase 2 — Foundational

- [X] T002 [P] Write the failing unit test `test_songbook_panel_puts_hymn_books_before_the_ordinary_ones` in `multimedia/web/tests.py`, reading `response.context['songbook_groups']` (red: the context key does not exist today).
- [X] T003 Implement `_songbook_name_key()` and `_songbook_groups(selected_id=None)` in `multimedia/web/reading/views.py`; pass `songbook_groups` from `BookIndexView`, `BookDetailView` and `SongDetailView` (green T002).

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the panel shows two groups with one separator and no heading.
**Independent test**: `/songs/` renders four hymn rows, one 2px rule, then the ordinary rows, with no `.group__head` in `#panelBody`.

- [X] T004 [P] [US1] Write the failing E2E test `test_the_songbook_panel_draws_one_divider_between_the_groups` in `tests/e2e/test_reading.py::ReadingE2ETests`: two `.group`s, one `border-top: 2px`, `margin-top: 10px`, `padding-top: 10px`, no heading text (red: one group today).
- [X] T005 [P] [US1] Write the failing unit test `test_songbook_panel_has_no_group_heading` asserting the rendered `#panelBody` carries two `section.group` blocks and no `class="group__head"` (red: one block).
- [X] T006 [US1] Convert `multimedia/web/templates/reading/_songbooks_panel.html` to iterate `songbook_groups`, one `section.group` per group, heading-free (green T004, T005).

## Phase 4 — US2 (P1)

**Goal**: ordinary songbooks read A–Z by the folded name; hymn books keep the largest-first order.
**Independent test**: the ordinary group's order equals the folded alphabetical order of the fixture names, and the hymn group stays `NKB`-style count order.

- [X] T007 [P] [US2] Write the failing unit test `test_songbook_panel_orders_ordinary_songbooks_by_folded_name` in `multimedia/web/tests.py` (red: T003 keeps the count order inside each group).
- [X] T008 [P] [US2] Write the unit test `test_songbook_panel_keeps_the_hymn_order_by_song_count`, pinning the unchanged hymn side.
- [X] T009 [US2] Sort both groups in `_songbook_groups()` with `_songbook_name_key()`: hymns by `(-song_total, key)`, ordinary by `key` (green T007, T008).
- [X] T010 [P] [US2] Write the failing E2E test `test_filtering_the_hymn_group_away_takes_the_divider` in `tests/e2e/test_reading.py::ReadingE2ETests`: filter `lagu`, assert the hymn group is `display: none` and the surviving group's `border-top` is `0px` (red: the 2px rule survives).
- [X] T011 [US2] Add `.group.is-hidden + .group { margin-top: 0; padding-top: 0; border-top: 0 }` to `static/styles/design/components.css` below the `.group + .group` rule (green T010).
- [X] T012 [US2] Write the unit test `test_songbook_panel_omits_the_separator_when_only_one_group_has_rows`, with the hymn books absent (pins FR-005's server half).

## Phase 5 — US3 (P2)

**Goal**: the three server routes and the saved renderer draw the same two groups.
**Independent test**: a saved render of `/songs/` carries the same group count and row order as the server page.

- [X] T013 [P] [US3] Write the failing saved-parity test `test_saved_songbook_panel_matches_the_server_grouping` in `tests/e2e/test_saved_render_parity.py::SavedRenderParityTests` (red: the saved renderer emits one flat group).
- [X] T014 [US3] Replace `sortedSongbooks()` in `static/web/offline-render.js` with `songbookGroups()` and `songbooksPanel()`, and route `songPage()` and `listPage()` through them (green T013).
- [X] T015 [P] [US3] Write the unit test `test_songbook_panel_marks_the_current_row_in_either_group`, and `test_song_detail_and_book_detail_panels_use_the_same_groups` (pins FR-006 across the three routes).

## Phase 6 — Polish

- [X] T016 Create `backlog/items/ITEM-131-songbook-hymn-separator.md` from the card template and add its row to `backlog/board.md` (In review with the PR; Done before the merge).
- [X] T017 Bump `VERSION` to `1.20.6` and add the `CHANGELOG.md` line under `## [Unreleased]`.
- [X] T018 Re-run the three targeted modules over the unchanged existing assertions (`inspection` row SC-006).

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
