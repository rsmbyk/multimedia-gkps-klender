# Spec 043: Fix the passage modal book picker's search filter

- **ID:** 043
- **Status:** Draft
- **Item:** ITEM-045
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the book picker's search box actually filter the books, and match both the TB and SIM names the
picker shows.

## Scope

### In scope

- The passage modal's book picker: typing hides non-matching books; clearing restores them.
- Matching on the TB name and the SIM name.

### Out of scope

- The song picker's search, the chapter / verse selects.

## Domain rules

- **It filters.** While a query is entered, only matching books are visible; a non-match is hidden,
  not merely marked.
- **Clear restores.** Emptying the search shows every book again.
- **Both names match.** A query matches the book's TB name or its SIM name.
- **The hint follows.** The "No matching books" hint shows only when nothing matches.

## Acceptance scenarios

### Scenario: Filtering

- **Given** the passage modal's book picker
- **When** I type a book's name
- **Then** only the matching books remain visible

### Scenario: Clearing

- **Given** a query that hides some books
- **When** I clear the search
- **Then** every book is visible again

### Scenario: The SIM name

- **Given** a book whose SIM name differs from its TB name
- **When** I type the SIM name
- **Then** the book matches

### Scenario: No matches

- **Given** a query that matches no book
- **Then** the "No matching books" hint shows and no book remains

## Traceability

- Domain/app tests: N/A (client-side filtering; fragment markup unchanged).
- E2E: `tests/e2e/test_entry_pickers.py`.
- Implementation: `static/styles/design/components.css`, `static/web/entries.js`.
- Related: spec 041 (the picker's TB/SIM names).
