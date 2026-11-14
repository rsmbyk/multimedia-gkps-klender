# Spec 048: Make the passage book search hide non-matching books

- **ID:** 048
- **Status:** Accepted
- **Item:** ITEM-050
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Typing in the passage book picker's search should narrow the visible list to matching books, rather
than leave every book in the dropdown.

## Scope

### In scope

- The passage modal's book picker in add and edit flows.
- Filtering on either the TB or SIM book name.
- Hiding non-matching options and empty testament groups.
- Showing the no-match hint when appropriate and restoring the complete list when the query is
  cleared.

### Out of scope

- The song picker and the chapter / verse pickers.
- Changes to book ordering, labels, or the dropdown's visual design.

## Domain rules

- **Only matches remain visible.** A non-matching book option is hidden in the rendered menu, not
  merely marked in the DOM.
- **Both names match.** The filter searches the TB and SIM names, irrespective of the selected
  edition.
- **The empty state follows the results.** The no-match hint appears only when zero books match;
  testament groups with no visible book are hidden.
- **Clear restores the list.** An empty query makes every book option visible again.

## Acceptance scenarios

### Scenario: Filter to a matching book

- **Given** the passage book picker contains a matching and a non-matching book
- **When** I type text from the matching book's TB name
- **Then** only the matching book is visible

### Scenario: Match the SIM name

- **Given** a book whose TB and SIM names differ
- **When** I type text from its SIM name
- **Then** that book is visible and non-matching books are hidden

### Scenario: No matches

- **Given** the passage book picker is open
- **When** I type text that matches no book
- **Then** no book option is visible and the “No matching books” hint is shown

### Scenario: Clear the query

- **Given** a query hides some books
- **When** I clear the query
- **Then** every book option is visible again and the no-match hint is hidden

## Traceability

- Domain/app tests: N/A — client-side visibility behavior.
- E2E: `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_book_picker_filter_hides_nonmatching_books_and_restores_all`.
- Implementation: `static/styles/design/components.css`; existing filter logic in
  `static/web/entries.js` remains unchanged.
- Related: spec 041 (TB/SIM book names), spec 043 (original filter requirement, superseded by 041),
  spec 044 (translation toggle), and spec 045 (custom chapter / verse pickers).
