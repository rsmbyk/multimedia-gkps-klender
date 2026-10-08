# Spec 041: Show TB/SIM book names in the passage modal's book picker

- **ID:** 041
- **Status:** Accepted
- **Item:** ITEM-043
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the passage modal's book dropdown read like the sidebar's book rows: the TB translation as the
main text and the SIM translation as the dimmed secondary on the right.

## Scope

### In scope

- The book picker (add and edit passage): one item per book, TB main, SIM secondary right.
- The picker's filter matching either name.
- A stored `BookTranslation` that resolves chapters and verses.

### Out of scope

- The chapter / verse selects, the song picker, and the sidebar.

## Domain rules

- **Like the sidebar.** Each book's picker item shows the TB name as the main text and the SIM name
  as the dimmed secondary at the right, mirroring `.book__n` / `.book__s`.
- **One book, one item.** A book appears once, whatever translations it has.
- **The stored value resolves.** Selecting a book stores a `BookTranslation` that yields the book's
  chapters and verses.
- **Keep an existing selection.** Editing an entry preserves its saved translation until a book is
  explicitly chosen; a new choice stores that book's primary `BookTranslation`.
- **Filterable by either name.** The picker's search matches the TB or the SIM name.

## Acceptance scenarios

### Scenario: A book with two translations

- **Given** a book with TB and SIM translations
- **When** I open the passage modal's book picker
- **Then** the book appears once, with the TB name as the main text and the SIM name dimmed on the
  right

### Scenario: Selecting still works

- **Given** a book selected in the picker
- **When** I pick a chapter and a starting verse
- **Then** the chapters and verses are offered as before

### Scenario: Editing an existing SIM passage

- **Given** a saved passage that uses the SIM translation
- **When** I open its editor without choosing another book
- **Then** the same book remains selected and its saved translation remains unchanged
- **When** I choose a book from the picker
- **Then** the book's primary translation is selected

### Scenario: Filtering

- **Given** the picker's filter
- **When** I type either the TB or the SIM name
- **Then** the book matches

### Scenario: No duplicates

- **Given** a book with more than one translation
- **Then** the picker lists it once

## Traceability

- Domain/app tests: `multimedia/web/tests.py`.
- E2E: `tests/e2e/test_entry_pickers.py`.
- Implementation: `multimedia/web/reading/entries.py`,
  `multimedia/web/templates/reading/_entry_form.html`,
  `static/styles/design/components.css`, `static/web/entries.js`.
- Related: spec 005 (entry modals), spec 040 (picker menus past the modal), spec 043 (the picker's
  filter must match both names), spec 044 (the TB/SIM toggle that decides which name is primary).
