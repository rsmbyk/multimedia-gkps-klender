# Plan 077: Clear sidebar filters when switching main menus

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-080
- **Bump:** patch

## Why

A first- or second-sidebar filter can remain filled after a main-rail section switch. Returning to the earlier menu then shows a stale, unexpectedly narrowed list.

## Scope / edges

**In:** `bookFilter` and `songFilter` when moving among Search, Alkitab, Kidung, and Tata Ibadah through the main icon rail.

**Out:** the global search query, within-section page navigation, same-menu panel open/close, and the dated/template toggle inside Tata Ibadah.

## Approach

Reset both sidebar input values on a successful main-menu change in `static/web/reading.js`, and run their existing input/filter update paths so full lists and clear-button visibility agree. Avoid clearing before a navigation that fails and falls back to a full page load.

## TDD

- Domain/app tests: N/A; client navigation state.
- E2E: targeted `tests/e2e/test_reading.py` paths for Kidung→Tata Ibadah, Tata Ibadah→Alkitab, and return, including clear buttons and full list restoration.

## Risks

- Clearing a sidebar filter must not erase the separate home search query or a filter during a same-section click.
