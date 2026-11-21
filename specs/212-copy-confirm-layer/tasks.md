# Tasks: the Copy as template confirmation is a layer of the edit modal

**Spec**: `specs/212-copy-confirm-layer/spec.md`
**Plan**: `specs/212-copy-confirm-layer/plan.md`
**Verification split**: 13 test · 2 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Verify the worktree is on `fix/212-copy-confirm-layer` at base `245399fe` (VERSION 1.35.2),
  that spec 212 / ITEM-226 / `reading` R47 are still free on `origin/develop` and on every sibling
  branch, and that `specs/*/preview/shots/` is already ignored (it is, `.gitignore:223–225`).
- [X] T002 Read `static/styles/design/components.css:510–535` and `:2640–2655`,
  `static/styles/design/generate.css:158–176` and `multimedia/web/templates/reading/_copy_confirm.html`
  again immediately before editing; record the exact line numbers in `converge.md`.

## Phase 2 — Foundational

- [X] T003 Write a failing `tests/e2e/test_tatib_templates.py::TataIbadahTemplateE2ETests::test_the_copy_confirmation_covers_the_form`:
  open a template's Edit modal from the sidebar's row button, record the dialog's height, press
  `[data-copy-open]`, then assert the layer's rect equals the dialog's, the dialog's height is
  unchanged to a tenth of a pixel, `elementFromPoint` at the form Save's centre resolves inside the
  layer, the layer's `border-top-left-radius` is 14px, and after `[data-copy-cancel]` the layer is
  `display: none` with `hidden` set (FR-001, FR-002, FR-005, SC-001, SC-002).
- [X] T004 Write a failing `test_the_copy_confirmation_card_matches_the_preview`: with the confirmation
  open, assert the card is 448 × 176.3 (± 1), padding 22px, radius 12px, a `--canvas` fill and a
  non-`none` shadow; the heading is 18px / weight 650; the body is 13.5px; the actions row is `flex`
  with `flex-end` and an 8px gap; the accept button's right edge is 22px inside the card's and the two
  answers are 38px tall (FR-003, FR-004, SC-003, SC-004).
- [X] T005 Run both against the unmodified stylesheet and confirm they fail for the right reason — the
  layer is `static`/`block` and the card has no padding, not an import or selector error (TDD-02).

## Phase 3 — US1 (P1) 🎯 MVP — the confirmation covers the form

**Goal**: pressing Copy as template puts one card over the form instead of stacking a second one under it.
**Independent test**: open a template's Edit modal, press Copy as template; the dialog keeps its height,
the card is centred over a dimmed form, and the form's Save is no longer clickable.

- [X] T006 [US1] Add the layer, the `[hidden]` restatement and the card's box rules to
  `components.css` after `.editor__confirm`, scoped to `.editor__confirm-layer` (D001, D002, D003, D006).
- [X] T007 [US1] Add the card's type and the right-aligned actions row to the same block (FR-004).
- [X] T008 [US1] Re-run T003 green and read the assertions back; a pass on a timeout does not count (TDD-02).

## Phase 4 — US2 (P2) — the card reads as the preview that was accepted

**Goal**: the confirmation carries the fill, radius, shadow and type scale spec 167's preview drew.
**Independent test**: the card's numbers in the shipped page equal the preview's, and the dark theme
needs no rule of its own.

- [X] T009 [US2] Re-run T004 green (FR-003, FR-004, SC-003, SC-004).
- [X] T010 [US2] Re-run `test_copy_as_template_asks_and_copies` unchanged: the copy still navigates to
  the new template (FR-006).
- [X] T011 [US2] Re-run `test_a_fill_in_and_a_choice_settle_then_create`: the generate page's own
  confirmation is unchanged by the scoping (D001).
- [X] T012 [US2] `inspection` — open `preview/index.html`, press **Dark**, and read the card and scrim:
  they take the dark `--canvas` and `--backdrop`, because the rules name no colour.

## Phase 5 — Polish

- [X] T013 `inspection` — in `preview/index.html` at a 380px viewport, the card is capped by
  `min(468px, 100%)` inside the layer's 16px padding and never overflows the dialog.
- [X] T014 Fold: append `R47` to `docs/spec/reading.md` with its scenarios, move `last folded` and the
  slice list; write `fold.md`.
- [X] T015 Delivery: `VERSION` 1.35.2 → 1.35.3, one `## [Unreleased]` line in `CHANGELOG.md`, the card
  at `in review` with `branch` and `pr`, the board row moved.
