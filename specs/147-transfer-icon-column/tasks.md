# Tasks: a long transfer name ellipsizes instead of moving the row

**Spec**: `specs/147-transfer-icon-column/spec.md`
**Plan**: `specs/147-transfer-icon-column/plan.md`
**Verification split**: 3 test · 5 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Confirm the shipped behaviour before touching anything: open
  `specs/147-transfer-icon-column/preview/preview.html` and read the **Now, 580px** panel — mark widths
  `32 / 21 / 22.75px`, glyph spread `5.5px`, name spread `11.0px`. No setup task exists: no
  dependency, no ignore-file change, no route.

## Phase 2 — Foundational

The three E2E tests are the shared prerequisite of both stories, and TDD-01 forbids writing a test
after the code it covers — so they are written and run red here, before the one declaration that
serves both stories.

- [X] T002 [P] [US1] Write `test_every_transfer_row_shares_one_icon_column` in
  `tests/e2e/test_media_library.py`: nine rows (seven fitting names, two over-long), asserting the set
  of `.media-transfers__mark` widths is exactly `{32.0}` and that the `left` of every `mark svg`,
  every `main strong` and every `main span` has a 0.0px spread.
- [X] T003 [P] [US1] Write `test_a_long_transfer_name_still_ellipsizes_at_the_pinned_column` in the
  same file: the over-long rows' `strong` reports `scrollWidth > clientWidth`, its `clientWidth` is the
  reserved 482px, and the row's height stays 72px.
- [X] T004 [P] [US2] Write `test_the_icon_column_holds_in_a_narrow_dialog` in the same file: at a
  420px viewport the dialog renders 382px (the UA caps the app's 388px `min()`), the text column is
  284px, both spreads are 0.0px, and no row's right edge passes the dialog's right edge.
- [X] T005 [US1] Run the three against the **unmodified** stylesheet and record the red output in
  `analysis.md`'s History: spreads `5.5px` / `11.0px` and `clientWidth` `493` / `491.3` on the two long
  rows — each test failing for its own measurement, not on an import or a selector.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: every row's glyph and every row's text sit on one vertical line, and a long name ellipsizes
inside the column it was always meant to occupy.
**Independent test**: `test_every_transfer_row_shares_one_icon_column` and
`test_a_long_transfer_name_still_ellipsizes_at_the_pinned_column` both green on a nine-row list.

- [X] T006 [US1] Add `flex: none` to `.media-transfers__mark` in
  `static/styles/design/components.css:2753` — one declaration, `width: 32px` kept.
- [X] T007 [US1] Re-run T002 and T003: green. Run
  `tests.e2e.test_media_library` in full — `…::test_sidebar_transfer_session_shows_active_then_finished`
  still passes (the rail's list is the same renderer, FR-005).

## Phase 4 — US2 (P2)

**Goal**: the pinned column survives the dialog narrowing to `min(580px, 100vw - 32px)`.
**Independent test**: `test_the_icon_column_holds_in_a_narrow_dialog` green at a 420px viewport.

- [X] T008 [US2] Re-run T004: green at 420px. Then `inspection` — the two 382px panels of
  `preview/preview.html`: mark column `32px`, both spreads `0.0px`, three names truncating.

## Phase 5 — Polish

- [X] T009 Regenerate the preview with `build_preview.py` and refresh the readout table in
  `preview/README.md` from the new numbers.
- [X] T010 Bump `VERSION` `1.22.4` → `1.22.5` and add one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`, naming the behaviour rather than the file.
- [X] T011 Fold: add R20 to `docs/spec/reading.md` and move the header's `last folded` and `slices`.
- [ ] T012 Delivery, after the report: open the PR as a draft, then move `ITEM-155` from Ready to In
  review with its `pr:` and push that one commit (`C-BOARD-GIT`).

## Phase 6 — Convergence

<!-- written by Converge only; absent until it runs -->
