# Spec 044: Add a TB/SIM toggle to the passage modal book picker

- **ID:** 044
- **Status:** Draft
- **Item:** ITEM-046
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Let the operator flip the passage modal's book picker between the TB and SIM translations in place,
using the same toggle the reading page shows.

## Scope

### In scope

- A TB/SIM toggle in the add and edit passage modals.
- Toggling swaps the book dropdown's main and secondary names at once and points it at the selected
  translation.
- The stored value is the selected translation's `BookTranslation`.

### Out of scope

- A new form field.
- The chapter / verse controls.
- The song modal and other editors.

## Domain rules

- **Not a field.** The toggle adds no form field; the existing `book_translation` stores the choice.
- **Reflected at once.** Changing the toggle swaps the book dropdown's main and secondary names
  immediately.
- **The choice is stored.** Selecting a book stores the translation the toggle is on.
- **The rest is still.** The chapter and verse controls do not change with the toggle.
- **Both names remain searchable.** The picker's filter matches either name in either state
  (spec 043).

## Acceptance scenarios

### Scenario: The toggle is present

- **Given** the add passage modal, and the edit passage modal
- **Then** each shows a TB/SIM toggle

### Scenario: Switching swaps the names

- **Given** the picker showing TB as the main name
- **When** I switch to SIM
- **Then** SIM becomes the main name and TB the secondary, at once

### Scenario: The choice is stored

- **Given** the toggle on SIM
- **When** I pick a book and save
- **Then** the entry stores the SIM translation of that book

### Scenario: The other dropdowns stay

- **Given** the toggle
- **When** I switch it
- **Then** the chapter and verse controls are unchanged

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_entry_pickers.py`.
- Implementation: `multimedia/web/templates/reading/_entry_form.html`,
  `static/web/entries.js`, `static/styles/design/components.css`.
- Related: spec 041 (the picker's TB/SIM names), spec 043 (the filter).
