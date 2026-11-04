# Tasks: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md`
**Plan**: `specs/186-display-session-refresh/plan.md`
**Verification split**: 14 test · 3 inspection · 0 manual

## Phase 1 — Setup

- [ ] T001 Confirm the branch is stacked on `feat/185-dock-goto` (`git log --oneline develop..HEAD`
  shows 185's commits beneath this slice's draft) and that `VERSION` still reads `1.26.2` — the bump
  is stamped at delivery, against what actually lands.

## Phase 2 — Foundational

- [ ] T002 [Foundational] Write the failing tests in `tests/e2e/test_display_session_refresh.py`:
  `test_a_focused_dock_stops_painting_a_refused_state` (FR-001, FR-003, SC-001, US1/AC1),
  `test_a_visibility_change_stops_painting_a_refused_state` (US1/AC2),
  `test_the_projector_stops_painting_a_refused_state` (FR-001, SC-002, US1/AC4).
- [ ] T003 [Foundational] Add `reread()` to `static/web/display.js`: read, compare by value, replace
  and `notify()` only on a difference, `syncButton()`, and bind `focus`, `visibilitychange` (when
  visible) and `pageshow` (restored). Export it as `gkpsDisplay.reread`. Makes T002 pass for the dock.
- [ ] T004 [Foundational] Add `rereadSession()` to `static/web/projector.js` and bind the same three
  triggers; it repaints silently (`render(true)`), and paints no detour and no screen when the state
  is refused. Makes T002 pass for the projector.

## Phase 3 — US2 (P1) One read, not a second mechanism

**Goal**: the module notifies only on change, so a focus repaints nothing when nothing changed.
**Independent test**: a `MutationObserver` over the dock's list counts zero mutations across a focus
with the state intact.

- [ ] T005 [P] [US2] Write the failing tests: `test_a_focus_with_the_state_unchanged_repaints_nothing`
  (FR-002, FR-005, SC-003, US2/AC1), `test_a_changed_reread_notifies_a_subscriber_once` (US2/AC2),
  `test_a_refused_state_leaves_every_control_idle` (FR-003).
- [ ] T006 [US2] Make T005 pass: the compare in T003 is what the notify depends on; the dock's
  `sync()` already paints idle from a null state. No second listener.

## Phase 4 — US1 (P1) The other controls follow

- [ ] T007 [P] [US1] Write the failing test `test_the_stored_shape_and_the_messages_are_unchanged`
  (SC-004, FR-004).
- [ ] T008 [US1] Make T007 pass: nothing to change in the module beyond T003 — the test pins the
  stored keys and the message types of spec 185, and fails if the re-read added either.

## Phase 5 — Polish

- [ ] T009 The inspection rows: `git diff --stat` shows `obs-overlay.js` untouched (FR-006), and the
  diff of `display.js` adds no `localStorage.setItem` and no `post(` (FR-004).
- [ ] T010 Run the neighbouring module `tests.e2e.test_display_session` and record any difference
  from the base in `converge.md`.
- [ ] T011 Delivery: `VERSION` 1.26.4, the `## [Unreleased]` line, the board row and `ITEM-190` in the
  same PR as the work — after spec 185 has merged, since this branch is stacked on it.

## Phase N+1 — Convergence

<!-- written by Converge only; absent until it runs -->
