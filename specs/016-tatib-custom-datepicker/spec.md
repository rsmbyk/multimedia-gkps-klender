# Spec 016: Use a custom date picker for Tata Ibadah forms

- **ID:** 016
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-018
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Replace the native date-picker control in Tata Ibadah create/edit forms with a custom, accessible calendar that submits the same optional date to Django.

## Scope

### In scope

- Custom calendar UI for the date field in Tata Ibadah create and edit modals.
- Month navigation, day selection, keyboard interaction, accessible naming/selected state, and a clear-date action.
- Correct initialization from an existing date; no dependency and no native date-picker input/UI.
- Submit selected dates in ISO `YYYY-MM-DD` format through the existing form contract.

### Out of scope

- Changing the optional-date meaning (an empty date remains a recurring template).
- Changing the Tata Ibadah page's date header formatting or projection controls.
- Replacing date controls elsewhere in the product.

## Domain rules

- The form does not use `input[type=date]` or browser-native picker UI.
- Selecting a day updates the form's submitted value to ISO `YYYY-MM-DD` and displays the selected date in the custom control.
- Clearing the date submits an empty value and preserves recurring-template behavior.
- The calendar has previous/next month controls; day choices are keyboard reachable and expose the selected day and accessible date labels.
- The create form opens on a sensible current month. The edit form opens on the month containing its saved date, with that day selected.
- After a server-rendered validation error, the picker remains usable and reflects the submitted date.

## Acceptance scenarios

### Scenario: Select a date while creating

- **Given** I open the Tata Ibadah create form
- **When** I navigate months and select a day
- **Then** the custom control shows the chosen date and the form submits its ISO value

### Scenario: Edit or clear an existing date

- **Given** I edit a dated Tata Ibadah
- **Then** the calendar starts on its saved month and identifies the saved day
- **When** I select another day or clear the date and save
- **Then** the saved service reflects the selected date or remains an undated recurring template, respectively

### Scenario: Operate the calendar without a pointer

- **Given** the custom calendar is open
- **When** I use keyboard navigation to move between dates and select one, or press Escape to close
- **Then** selection and close behavior work without losing an understandable focus position
- **And** the calendar exposes accessible labels and selected state

### Scenario: No native date picker is present

- **Given** either Tata Ibadah editor form
- **Then** it contains no `input[type=date]` and date selection is provided by the custom calendar

## Traceability

- E2E: `tests/e2e/test_editor.py` (`EditorE2ETests`).
- Domain/app tests: `multimedia/web/tests.py` (`EditorViewTests`).
- Implementation: Tata Ibadah form markup, `static/web/editors.js`, and `static/styles/design/components.css` (or a dedicated custom date-picker module under `static/web/`).
