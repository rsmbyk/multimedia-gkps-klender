# Spec 042: Sort and label the add-song picker like the hymn books

- **ID:** 042
- **Status:** Accepted
- **Item:** ITEM-044
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Make the song picker in the add / edit song modal read like its songbooks: hymnals in number order
shown by short reference and title, non-hymn songbooks in title order shown by title.

## Scope

### In scope

- Hymn books' songs ordered by number; non-hymn books' songs ordered alphabetically by title.
- Hymn songbooks first (by songbook id), then non-hymn songbooks (by name).
- Hymn option label `HAL 123 Some Title`; non-hymn option label the title alone.

### Out of scope

- The book picker, the sidebar, the projector.
- The picker's filter semantics.

## Domain rules

- **Hymns by number.** Songs of a hymn book are ordered by their number (sub-number as tiebreak).
- **Others by title.** Songs of a non-hymn book are ordered alphabetically by title.
- **Hymn groups first, by id.** The songbook groups list hymn songbooks first, ordered by songbook
  id, then non-hymn songbooks ordered by name.
- **Hymn label.** A hymn option shows the short reference and the title, e.g. `HAL 123 Some Title`.
- **Unnumbered hymn.** A hymn without a number follows numbered hymns, ordered by title. Its option
  shows the short reference and title without a number placeholder, e.g. `HAL Some Title`.
- **Non-hymn label.** A non-hymn option shows just the title.
- **Collapsed label.** After selection, the closed picker continues to show the title alone.

## Acceptance scenarios

### Scenario: A hymn book's songs

- **Given** a hymn book with numbered songs
- **When** I open the song picker
- **Then** that book's songs are listed in number order

### Scenario: A non-hymn book's songs

- **Given** a non-hymn songbook
- **Then** its songs are listed alphabetically by title

### Scenario: Group order

- **Given** the hymn and non-hymn songbooks
- **Then** the hymn songbooks appear first, ordered by songbook id, and the non-hymn songbooks
  follow, ordered by name

### Scenario: Hymn option label

- **Given** a hymn song numbered 123 titled "Some Title" in the book whose short name is "HAL"
- **Then** the option reads `HAL 123 Some Title`

### Scenario: Non-hymn option label

- **Given** a non-hymn song
- **Then** the option reads just its title

### Scenario: An unnumbered hymn

- **Given** a hymn book with numbered songs and two songs without numbers
- **When** I open the song picker
- **Then** the numbered songs appear first, followed by the unnumbered songs in title order
- **And** an unnumbered option shows the short book reference and title without `None`

### Scenario: The selected hymn label

- **Given** a hymn song has been selected
- **When** the picker is closed
- **Then** its trigger shows the song title alone


## Traceability

- Domain/app tests: `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_sort_and_label_by_songbook_type`.
- E2E: `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_sorts_and_labels_by_songbook_type`.
- Implementation: `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/_entry_song_options.html`, `static/web/entries.js`.
- Related: spec 041 (the book picker's names).
