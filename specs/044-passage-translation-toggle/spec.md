# Spec 044: Add a TB/SIM toggle to the passage modal book picker

- **ID:** 044
- **Status:** Accepted
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
- Each book option exposes both translation IDs and names; a new form starts on TB, while edit and
  validation-error forms reflect their currently selected `BookTranslation`.
- If a book has neither TB nor SIM, preserve the existing primary-translation fallback on the default
  side so it remains selectable.
- Toggling swaps the book dropdown's main and secondary names and updates the selected book's hidden
  `book_translation` to the active translation.
- The stored value is the active translation's `BookTranslation`.

### Out of scope

- A new form field.
- Re-fetching chapter/verse options solely because the toggle changed.
- The song modal and other editors.

## Domain rules

- **Not a field.** The toggle adds no form field; the existing `book_translation` stores the choice.
- **Reflected at once.** Changing the toggle swaps the book dropdown's main and secondary names
  immediately.
- **The choice is stored.** Switching the active side updates the selected book's hidden value; a
  book picked afterward stores that side's `BookTranslation`.
- **The edit state is truthful.** An edit or validation-error form starts on the edition of its
  selected `BookTranslation`; a new passage starts on TB.
- **The rest is still.** Toggling preserves chapter/verse controls, their options, and their selected
  values. Picking another book follows the existing cascade for the active translation.
- **Both names remain searchable.** The picker's filter matches either name in either state; this is
  implemented by spec 041 (spec 043 was superseded by spec 041).
- **Legacy fallback remains usable.** If a book has neither TB nor SIM, keep its existing primary
  translation selectable on the default side.

## Acceptance scenarios

### Scenario: New passage starts on TB

- **Given** the add passage modal
- **When** its scripture form opens
- **Then** TB is active and the picker shows TB as the main name

### Scenario: A book without TB or SIM keeps its fallback

- **Given** a book has neither TB nor SIM and the existing book index provides a primary fallback
- **When** I choose that book in a new passage's default state
- **Then** the fallback remains selectable and is stored in `book_translation`

### Scenario: Editing an existing SIM passage

- **Given** a saved passage that uses the SIM translation
- **When** I open its editor without choosing another book
- **Then** the same book remains selected, SIM is active, and its saved translation remains unchanged

### Scenario: Switching swaps names and the selected value

- **Given** a selected book with TB active
- **When** I switch to SIM
- **Then** SIM becomes the main name, TB becomes the secondary, and the hidden value becomes that
  book's SIM `BookTranslation`

### Scenario: Picking a book stores the active translation

- **Given** the toggle on SIM
- **When** I pick a book and save
- **Then** the entry stores the SIM translation of that book

### Scenario: Chapter and verse controls stay put on toggle

- **Given** the chapter and verse controls have selected values
- **When** I switch the translation toggle
- **Then** their options and selected values remain unchanged
- **When** I pick a different book
- **Then** the existing cascade loads that book's chapter and verse options for the active translation

### Scenario: Filtering works on either side

- **Given** the picker's filter
- **When** I type either the TB or SIM name with either side active
- **Then** the book matches

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_entry_pickers.py`.
- Implementation: `multimedia/web/reading/entries.py`,
  `multimedia/web/templates/reading/_entry_form.html`, `static/web/entries.js`,
  `static/styles/design/components.css`.
- Related: spec 041 (TB/SIM names and the two-name filter), spec 040 (picker menus past the modal).
  Spec 043's filter proposal was superseded by spec 041.
