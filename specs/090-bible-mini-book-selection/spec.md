# Spec 090: Keep the Bible book sidebar mini when selecting a book

- **ID:** 090
- **Status:** Accepted
- **Item:** ITEM-093
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Selecting a Bible book from the mini book sidebar must leave that sidebar mini while opening the selected book's chapter list.

## Scope

### In scope

- Bible book tiles in the public reading shell.
- First-sidebar state, selected book, and chapter pane after an in-page book navigation.

### Out of scope

- Songbook and Tata Ibadah list selection; rail switches; search; layout, motion, color, or copy changes.
- Full page loads and no-JavaScript navigation, which continue to use the server page's initial state.

## Domain rules

- N/A; this changes browser state only.

## UI details

- A Bible book click preserves the first sidebar's live `open` or `mini` state. A mini panel remains the same width and position.
- The arriving page determines the selected book, chapter rows, and second-level pane state. Selecting a different book opens its chapter list.
- Clicking the already selected book keeps its existing in-place chapter-list toggle and leaves the first sidebar mini.
- The panel's expand control remains the way to open a mini book sidebar. Its state and accessibility labels continue to reflect the visible panel.

## Acceptance scenarios

### Scenario: Select another book from mini mode

- **Given** the Bible book sidebar is mini and one book's chapter list is open
- **When** the operator clicks another book tile
- **Then** the book sidebar remains mini, the other book is selected, and its chapter list is open with the correct title and rows.

### Scenario: Toggle the selected book in mini mode

- **Given** the Bible book sidebar is mini and the selected book's chapter list is open
- **When** the operator clicks that book tile
- **Then** the chapter list closes and the book sidebar remains mini.
- **When** the operator clicks that book tile again
- **Then** the same chapter list reopens and the book sidebar remains mini.

### Scenario: Explicitly expand the book sidebar

- **Given** the Bible book sidebar is mini after selecting another book
- **When** the operator uses the panel expand control
- **Then** the first sidebar opens and the selected book and its chapter list remain available.

### Scenario: Select a book while already open

- **Given** the Bible book sidebar is open
- **When** the operator selects another book
- **Then** the sidebar stays open and the selected book's chapter list opens.

## Traceability

- Domain/app tests: N/A.
- E2E: `tests/e2e/test_reading.py::SidebarStateOnItemOpenTests.test_selecting_a_bible_book_preserves_the_mini_panel` checks different-book selection, chapter rows, same-book toggling, explicit expansion, and open-state selection. The full class and `ReadingE2ETests.test_service_text_sidebar_shows_two_lines_and_centers_grip` pass together (7 tests).
- Implementation: `static/web/reading.js` — Bible book tile navigation uses `bible-book`, and `applyPage()` preserves `data-nav` for that kind while taking the arriving `data-ch`.
