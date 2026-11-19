# Tasks: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`
**Plan**: `specs/201-sidebar-date-focus/plan.md`
**Verification split**: 9 test · 2 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Confirm the worktree is `fix/201-sidebar-date-focus` on base `92edc752`, the spec number/card ID are free, and the preview probe passes.

## Phase 2 — Foundational

- [X] T002 Add `tests/e2e/test_sidebar_date_reveal.py` with the dated + Today fixtures and the stylesheet/rule assertion helper that survives headless hover media (D003).

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the date paints again after a click once the pointer leaves.
**Independent test**: click a dated service row, move the pointer away, read the date's computed `display`.

- [X] T003 [P] [US1] Write the failing E2E `test_a_clicked_row_paints_its_date_again` for FR-001/SC-001 in `tests/e2e/test_sidebar_date_reveal.py`; run it red.
- [X] T004 [P] [US1] Write the failing E2E `test_keyboard_focus_on_an_action_hides_the_date_until_it_leaves` for FR-001/SC-002; run it red.
- [X] T005 [US1] Replace the `li:focus-within` date selector with the hover/action-focus selectors in `static/styles/design/components.css`; keep the `@media (hover: hover)` guard.
- [X] T006 [US1] Add `test_the_row_box_and_label_do_not_change_across_the_states` for SC-003 and make it green.

## Phase 4 — US2 (P2)

**Goal**: the Today badge follows the date's reveal in every state.
**Independent test**: click a Today row and move the pointer away; the badge paints again, and still steps aside on hover/action focus.

- [X] T007 [US2] Write the failing E2E `test_the_today_badge_follows_the_date_reveal` for FR-002; run it red against the base rule after T005's date-only change, then make it green with the badge selector.
- [X] T008 [US2] Add the touch case `test_touch_keeps_the_controls_and_date_visible` to the same module; verify the `@media (hover: none)` rules are untouched.

## Phase N — Polish

- [X] T009 Run the focused module plus `tests.e2e.test_reading` and `tests.e2e.test_drawer_shell`; re-run the preview probe after the CSS change (the frozen base sheet must keep the TODAY column unchanged).
- [X] T010 Fold the clarified wording into `docs/spec/reading.md` `R41` and `R9`; write `fold.md` with the typed deltas and counts.
- [ ] T011 Delivery commit: `VERSION` 1.34.0 → 1.34.1, one `## Fixed` changelog line, card `ITEM-211` moved with its bump — only after the closing report.

## Phase N+1 — Convergence

<!-- written by Converge only; absent until it runs -->
