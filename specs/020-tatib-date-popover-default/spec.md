# Spec 020: Use a date popover with a Sunday default

- **ID:** 020
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-022
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make Tata Ibadah date selection compact in the editor and ready for the nearest Sunday when creating a service.

## Scope

### In scope

- Show the existing custom calendar as a dropdown/popover anchored beneath the date field.
- Preselect the nearest Sunday in create forms: today when today is Sunday, otherwise the upcoming Sunday.
- Keep date clearing, keyboard access, and ISO form submission.

### Out of scope

- Changing dates or blank-date meaning on edit forms.
- Changing date validation or other product date fields.

## Domain rules

- Opening the date control shows its calendar below the field without shifting the surrounding form layout.
- A new service's initial date is the nearest Sunday in the application-local timezone; Sunday itself is included.
- Existing service dates remain selected on edit; an undated service remains undated until the owner selects a date.
- Clearing submits an empty date, and choosing a date submits ISO `YYYY-MM-DD`.

## Acceptance scenarios

### Scenario: Create on a weekday

- **Given** the create form opens on a day before Sunday
- **When** I open its date picker
- **Then** the date field is preselected to the upcoming Sunday and the calendar is a dropdown beneath the field

### Scenario: Create on Sunday

- **Given** the create form opens on Sunday
- **Then** today is preselected, not the following Sunday

### Scenario: Edit an existing service

- **Given** I edit a dated or undated service
- **Then** its stored date or blank value is preserved as the initial selection

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`).
- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`).
- Implementation: `multimedia/web/reading/editors.py`, `multimedia/web/templates/reading/_editor_form.html`, `static/web/date-picker.js`, and `static/styles/design/components.css`.
