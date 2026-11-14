# Plan 020: Use a date popover with a Sunday default

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-022
- **Bump:** patch

## Why

The Tata Ibadah create form should open with the next service date ready, while keeping the date control compact and usable in its modal.

## Scope / edges

**In:** Positioning the existing accessible calendar as a dropdown/popover beneath its field; selecting the nearest Sunday by default on create.

**Out:** Changing saved edit dates, optional dates for recurring templates, date validation, or other date controls.

## Approach

Anchor the existing calendar to the date trigger and overlay it below the field. Initialize only new forms to the nearest Sunday using the application-local date; if today is Sunday, select today. Keep editing forms' stored date (including blank) unchanged. Retain keyboard operation, clearing, and ISO submission.

## TDD

- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`) for Sunday, non-Sunday, and edit-form initialization.
- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`) for dropdown placement, Sunday selection, clear, and form submission.

## Risks

- An absolute popover can be clipped by the modal's scroll container; verify it remains visible and operable at the date field.
- A date default must not turn an undated edit into a dated service.
