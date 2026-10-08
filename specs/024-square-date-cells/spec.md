# Spec 024: Make Tata Ibadah calendar date cells square

- **ID:** 024
- **Status:** Accepted
- **Item:** ITEM-026
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Use square date cells in the Tata Ibadah calendar instead of cells wider than they are tall.

## Scope

### In scope

- Equal width and height for day buttons and blank grid slots at desktop and narrow widths.
- Preserve the seven-column weekday alignment and existing rounded corners.
- Preserve Sunday emphasis, today/selected/focus states, and viewport-aware top-layer behavior.

### Out of scope

- Sharp corners or restyling the month navigation buttons.
- Changes to date defaults, selection, keyboard controls, localization, or ISO submission.

## Domain rules

- Every day cell has equal rendered width and height within 1 px subpixel tolerance.
- Blank slots align with the day cells and do not distort the final or first week.
- Square means 1:1 proportions with the current 8 px corner radius retained (confirmed by owner acceptance).
- The calendar remains usable in short/narrow viewports and does not increase modal form height when opened.

## Acceptance scenarios

### Scenario: Square date cells at different widths

- **Given** I start at home, open Tata Ibadah, and open a create/edit calendar
- **When** I view months with four, five, or six weeks at desktop and narrow widths
- **Then** every day button and blank slot has equal width and height within 1 px
- **And** the weekday headings remain aligned above their columns
- **And** rounded corners and Sunday emphasis remain unchanged

### Scenario: Taller calendar remains usable

- **Given** the calendar is open in a short or narrow viewport
- **When** I navigate months or scroll the editor
- **Then** the calendar stays within the viewport and escapes modal clipping
- **And** date selection, keyboard focus, clearing, and ISO submission still work
- **And** the underlying form does not grow when the calendar opens

## Traceability

- Domain/app tests: N/A; no domain behavior changes.
- E2E (passed 2026-10-08): `test_date_picker_cells_are_square_across_widths_and_month_lengths` covers 1440×900, 390×844, 320×500, and 1440×360 with four-, five-, and six-week months. The regression first failed as expected (e.g. 39.42×34 px at 1440×900), then passed after the CSS change. `test_date_picker_emphasizes_sundays_in_light_and_dark_themes` pins Sunday styling; picker selection/keyboard/clear, ISO submission, saved-date loading, validation rerender, and modal-overlap regressions all pass in `tests/e2e/test_editor.py`.
- Implementation: `static/styles/design/components.css`; picker logic and placement code remained unchanged.
