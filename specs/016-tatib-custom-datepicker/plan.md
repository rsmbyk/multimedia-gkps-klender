# Plan 016: Use a custom date picker for Tata Ibadah forms

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-018
- **Bump:** patch

## Why

The Tata Ibadah editor needs a consistent date control that does not invoke browser-specific native date-picker UI.

## Scope / edges

**In:** A dependency-free custom calendar in the Tata Ibadah create/edit forms, optional-date clearing, keyboard and accessible operation, ISO form submission.

**Out:** Date formatting in the service page header, other app date controls, changes to date validation or recurring-template semantics.

## Approach

Render a custom calendar trigger and popup alongside a hidden ISO date value consumed by the existing Django date field. Provide month navigation, day selection, selected/today semantics, keyboard movement, Escape/outside close, and a clear-date action. Initialize from an existing date when editing and from a sensible current month when creating. Rebind the calendar after server-rendered form errors/modal refreshes.

## TDD

- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`) for create/edit selection, keyboard interaction, clearing, ISO submission, and validation re-render.
- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`) for ISO date parsing and optional dates.

## Risks

- Modal refresh replaces form DOM; event handling must work after a 400 validation response.
- Avoid locale-dependent date strings in POSTs and ensure the popup stays within the dialog on narrow viewports.
