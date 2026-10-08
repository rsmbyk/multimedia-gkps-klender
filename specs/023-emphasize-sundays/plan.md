# Plan 023: Make Sundays more prominent in the Tata Ibadah date picker

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-025
- **Bump:** patch

## Why

The calendar is used to schedule weekly Tata Ibadah, and new services default to Sunday, but Sunday dates currently look like every other day. Give Sundays a clear, consistent visual cue so they are quicker to spot.

## Scope / edges

**In:**

- Visually distinguish the Sunday weekday heading and Sunday date cells in the Tata Ibadah editor calendar.
- Use the existing theme tokens so the emphasis works in light and dark themes.
- Preserve existing selected-date and today indicators; do not let Sunday styling obscure them.

**Out:**

- Changing which date is selected, date navigation, calendar positioning, or date submission.
- Styling date pickers outside Tata Ibadah forms.

## Approach

Mark Sunday date buttons from their local calendar date and style Sunday dates and the Sunday heading with a stronger weight and a subtle theme-aware accent. Keep selected and today states visually distinct. Add a focused E2E assertion comparing an unselected Sunday with a weekday and checking the Sunday heading.

## TDD

- Domain/app tests: N/A; no date-domain behavior changes.
- E2E: `tests/e2e/test_editor.py` — Sunday markers and visible contrast against weekday dates, without changing date selection.

## Risks

- The Sunday emphasis must remain discernible in both themes and not compete with the selected-date or today indicators.