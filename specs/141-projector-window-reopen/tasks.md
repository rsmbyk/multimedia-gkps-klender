# Tasks: reopening the projector window

**Slice**: `specs/141-projector-window-reopen`
**Spec**: `spec.md` (Accepted, gate 1, 2026-10-27)
**Plan**: `plan.md` — bump `patch`

## Phase 1 — Setup

- [X] T001 [P] Run the projector suite on the branch to record a green baseline: `tests/e2e/test_projector.py`

## Phase 2 — Foundational

- [X] T002 Add the reopen button inside `.read__project` in `multimedia/web/templates/reading/tatib.html`: `data-project-window`, `data-projector-url="{% url 'web-projector' %}"`, `data-project-service="{{ service_id }}"`, `aria-label` and `title` "Open projector window", the inline pop-out glyph, placed after Media files and before the Project / Stop toggle
- [X] T003 Add the control's box, its default hide, the `≥721 px` show rule keyed on `[data-displaying="true"]`, and the Tata Ibadah group's `flex-wrap: wrap` + `max-width: 100%` to `static/styles/design/components.css`

## Phase 3 — US1: the window can be reopened without releasing the display

- [X] T004 [P] [US1] Write the failing tests for the control's presence and the reopen act in `tests/e2e/test_projector.py`: `test_the_reopen_control_appears_only_while_the_service_is_on_air` (off air, on air, hidden, released, and a second tab that hears the state), `test_reopening_returns_the_window_to_the_screen_on_air`, `test_reopening_writes_no_display_state` — run them and read the failures
- [X] T005 [US1] Write the failing test for an already-open window: `test_an_open_projector_window_is_focused_not_reloaded`, including a second press while the first is still loading — one window, never two (`tests/e2e/test_projector.py`)
- [X] T006 [US1] Implement the delegated branch and the open/focus helper in `static/web/display.js` until T004–T005 pass: guard on the live service and `on`, open the named window with an empty URL, fill it only when it is blank, focus it
- [X] T007 [P] [US1] Confirm spec 119 still holds with the control present: `test_closing_the_projector_window_leaves_the_display_alone`, `test_project_button_opens_the_display_and_editing_stays_available`, and write `test_stop_projecting_still_releases_with_the_control_present` (`tests/e2e/test_projector.py`)

## Phase 4 — US2: the control fits the pane at every desktop width

- [X] T008 [P] [US2] Write the failing geometry tests: `test_the_project_group_stays_inside_the_pane` (1440 and 1280, with and without Media files) and `test_the_reopen_control_is_not_drawn_on_a_phone` (`tests/e2e/test_projector.py`)
- [X] T009 [US2] Finish the stylesheet rules in `static/styles/design/components.css` until T008 passes: the 34 × 34 box with no padding, the group's wrap inside the pane, the phone gate

## Phase 5 — Polish

- [X] T010 Run the projector and reading E2E suites for regressions: `tests/e2e/test_projector.py`, `tests/e2e/test_reading.py`
- [X] T011 Converge against `plan.md`'s traceability table and write `converge.md`
- [X] T012 Fold the delta into `docs/spec/reading.md` (R14 gains the second control; a new requirement for the reopen act) and write `fold.md`
- [ ] T013 Delivery: `CHANGELOG.md` line and `VERSION` bump `patch`; card ITEM-150 to `Done`; board row; commit at Fold and report — changelog and `VERSION` applied at Fold; the card's `Done` move waits for the PR (nothing pushed yet)
