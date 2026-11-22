# Tasks: song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`
**Plan**: `specs/223-songrow-focus-ring-clip/plan.md`
**Verification split**: 14 test · 4 inspection · 3 manual

## Phase 1 — Setup

- [X] T001 [P] Create `tests/e2e/test_songrow_focus_ring.py` with the Playwright/
  `StaticLiveServerTestCase` fixture only: a `songs.Book`, several `songs.Song` rows and a helper that
  opens `reverse('web-song', args=[song.pk])` at 900×700 in dark mode. No product file changes.

## Phase 2 — Foundational: the red run before any product code

Written and run **before** `components.css` is touched, so each case fails for its own reason
(TDD-02).

- [X] T002 [P] [US1] Write the failing case for FR-001 / SC-001 / SC-002:
  `test_the_first_rows_ring_fits_inside_the_scrollport` — click the first `#chList` row, press `a`,
  read `scrollTop`, `scrollHeight === clientHeight`, the row/host top gap and the computed outline;
  assert the gap is at least `outlineWidth + outlineOffset`.
- [X] T003 [P] [US1] Write the failing case for US1 AC1 / SC-004:
  `test_a_tabbed_first_row_gets_the_same_complete_ring` — Tab from the page until the first row is
  active and assert the same clearance and outline.
- [X] T004 [P] [US1] Write the failing case for FR-002, FR-003, SC-003 and SC-005:
  `test_focus_does_not_change_the_row_box_or_its_states` — compare heights, 1px pitch, `aria-current`
  and hover colour before/after focus, and assert an unfocused row's `outlineStyle === 'none'`.
- [X] T005 Run the three cases on the unmodified page against `gkps223` and record the red output in
  `analysis.md`; the assertion must name the `0px >= 2px` clearance, not a timeout or import error.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the focused first row's ring has a complete top edge.
**Independent test**: the T002 and T003 cases go green; the T004 invariants stay green.

- [X] T006 [US1] Make FR-001 pass: in `static/styles/design/components.css`, change `.ch__body`'s
  `padding: 0 0 8px` to `padding: 3px 0 8px`. No other declaration, no new selector.
- [X] T007 [US1] Re-run T002–T004: the three cases go green with the same UA outline and unchanged
  row boxes.

## Phase 4 — Polish and regression

- [X] T008 [P] Re-run `tests.e2e.test_reading` (FR-005's evidence); no case in the module changes.
- [X] T009 `inspection` — read the whole diff: one padding declaration, one new test module, no JS,
  no template, no focus rule, no change to the first sidebar or other pages.
- [X] T010 `specs/README.md` — add the index row for 223, `Accepted` (done at gate 1).
- [X] T011 `manual` — click through the preview's unfocused, pointer, Tab, selected, hover,
  scrolled-to-last-row and responsive states in dark and light; record the readings in `converge.md`.
- [X] T012 Fold: append `reading/R52` to `docs/spec/reading.md` and move the header's `last folded`
  and `slices`.
- [X] T013 [Convergence] Compare the present code against every traceability row by its declared
  method; append `## Phase 1: Convergence` to `converge.md` with evidence.

## Phase 5 — Delivery

- [X] T014 `VERSION` 1.36.8 → 1.36.9 and one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`, applied immediately before the merge and re-checked against `origin/develop`.
- [X] T015 Delivery, after the report and on the owner's word: open the PR as a draft against
  `develop`, read `ITEM-238`'s state, set `in-review`, write `pr:`, move the board row, push that
  commit, mark the PR ready. The card is closed in its own later `chore/board-238` branch.

## Closing note

Merged into `develop` on 2026-11-22 as squash `e4d69cd1` via PR #588. The card was closed in its own
`chore/board-238` PR; the anchor issue stays open as the card's pointer.
