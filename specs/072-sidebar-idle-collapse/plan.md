# Plan 072: Collapse an idle matching sidebar

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-075
- **Bump:** minor

## Why

The first sidebar can remain open over the reading area after the operator stops using it. The accepted interactive preview uses a 60-second idle period and keeps the current reading page visible.

## Scope / edges

**In:** the new reading shell's main icon rail and first sidebar. Auto-collapse applies only when the open sidebar belongs to the section shown on the reading stage. Bible returns to its existing mini state; Kidung and Tata Ibadah use their existing first-sidebar collapse behavior.

**Out:** the search-first home, mismatched sidebar browsing, modal interaction, and the legacy docks and webs.

## Approach

Add one resettable inactivity timer to `static/web/reading.js`. Observe meaningful pointer, keyboard, focus, and scroll interaction on the rail and first panel. Check section, stage, nav, focus, and modal state when the timer expires. Reuse `miniPanel` or the section's manual collapse path; do not invent a new layout. Cancel/restart the timer after in-page navigation and panel state changes.

## TDD

- Domain/app tests: N/A; browser interaction state.
- E2E: targeted fake-clock coverage in `tests/e2e/test_reading.py` for matching/mismatching sections, activity reset, Bible mini state, and keyboard focus.

## Risks

- A stale timer could close a newly opened sidebar after a section switch.
- Auto-collapse must not interrupt an active filter, modal, or reorder gesture.
