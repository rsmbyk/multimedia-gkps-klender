# Spec 023: Make Sundays more prominent in the Tata Ibadah date picker

- **ID:** 023
- **Status:** Accepted
- **Item:** ITEM-025
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make Sundays easy to identify in the Tata Ibadah date picker, which is commonly used to schedule weekly services.

## Scope

### In scope

- Visually emphasize the Sunday weekday heading and Sunday date cells in the Tata Ibadah calendar.
- Use theme-aware styling for light and dark themes.
- Retain selected-date and today indicators.

### Out of scope

- Changing date defaults, selection, navigation, submission, or popover placement.
- Changing other date pickers.

## Domain rules

- Sunday dates are visibly more prominent than other dates in the calendar.
- Existing selected-date and today states remain visible and recognizable when they occur on a Sunday.
- The calendar continues to display and submit the same dates as before.

## Acceptance scenarios

### Scenario: Sunday dates stand out

- **Given** the Tata Ibadah date picker is open
- **When** I scan the month grid
- **Then** Sunday dates and the Sunday weekday heading are visually emphasized compared with other weekdays
- **And** the Sunday emphasis is legible in both light and dark themes

### Scenario: Sunday emphasis preserves date states

- **Given** today or the selected date is a Sunday
- **When** the calendar is displayed
- **Then** the existing today and selected-date indicators remain visible and distinguishable
- **And** selecting dates continues to submit the same ISO date values

## Traceability

- Domain/app tests: N/A; no date-domain behavior changes.
- E2E: `tests/e2e/test_editor.py::EditorE2ETests.test_date_picker_emphasizes_sundays_in_light_and_dark_themes` — starts from home and navigates in-page; compares Sunday/weekday computed styles in both themes, checks the Sunday heading, selected-date hover priority, keyboard focus, ISO selection, and an unselected Sunday-today border.
- Regression verification: eight focused date-picker E2Es and five `tests.test_design_tokens.TokenContrastTests` passed (13 tests total). Existing Sunday defaults, popover overlap/viewport anchoring, keyboard/clear behavior, ISO submission, edit, and validation rerender remain covered. Full browser suite is deferred to push verification.
- Rendered verification: home → Tata Ibadah → Add → date picker at 1440×900 and 390×844 in light/dark themes; Sunday dates use weight 700 versus weekday weight 500, with no horizontal overflow and the calendar within the viewport. Unselected Sunday text contrast on its tinted background measures 6.27:1 (light) and 6.05:1 (dark).
- Implementation: `static/web/date-picker.js` marks Sunday dates; `multimedia/web/templates/reading/_editor_form.html` marks the Sunday heading; `static/styles/design/components.css` applies theme-aware accents while preserving selected/today/focus states.