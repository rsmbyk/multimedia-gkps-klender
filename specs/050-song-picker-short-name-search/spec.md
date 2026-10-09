# Spec 050: Search and label songs by songbook short name

- **ID:** 050
- **Status:** Accepted
- **Item:** ITEM-052
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Let people find songs in the New song picker by typing a songbook abbreviation such as `KJ`, and keep the hymn-book reference visible after choosing a song.

## Scope

### In scope

- Search in the song picker used by both add and edit song-entry forms.
- Match the query case-insensitively against the associated songbook's `short_name`, in addition to the existing song-title and number matches.
- For hymn-book songs, show the same short-name/number/title reference in the selected picker label and edit-form initial label as is already shown in the result option. Keep non-hymn selected labels title-only.
- Preserve existing song grouping, ordering, result limit, active/deleted filtering, and verse-loading behavior.

### Out of scope

- Matching the songbook's full name as a new search field.
- Changes to the public song search, songbook sidebar, result-option labels, grouping, or result limit.
- Changes to which songs are active or selectable.

## Domain rules

- A trimmed, non-empty query matches a song when it occurs case-insensitively in the song title, the song number, or its book's short name.
- These match fields are combined with OR semantics. A book short-name match must find its songs even when the title and number do not contain the query.
- Selecting a hymn-book song shows its existing formatted reference (short name, number/sub-number when present, and title) in the closed picker. Editing that entry shows the same reference. Non-hymn song labels remain title-only.
- Clearing the query and selecting a result keep their current behavior, including verse loading.

## Acceptance scenarios

### Scenario: Find a song by its book abbreviation

- **Given** a song in a book whose short name is `KJ`, and the song's title and number do not contain `KJ`
- **When** I type `kj` in the add-song picker search field
- **Then** the song appears under its existing songbook group
- **And** the search behaves the same in the edit-song picker

### Scenario: Keep the hymn-book reference visible after selection

- **Given** a hymn-book song whose option label is `KJ 152 Ada Kuasa`
- **When** I select it, or open an existing entry that already uses it
- **Then** the closed picker label shows `KJ 152 Ada Kuasa`, not only `Ada Kuasa`
- **And** a non-hymn song's selected label remains its title

### Scenario: Preserve existing song searches and verse selection

- **Given** songs that match by title, number, or book short name
- **When** I search and select a result
- **Then** all matching fields continue to work together
- **And** the selected song's verses load as before

## Traceability

- Domain/app tests:
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_the_song_options_match_the_songbook_short_name`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_edit_fragment_shows_the_hymn_reference_as_its_label`
- E2E:
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_searches_by_songbook_short_name`
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_sorts_and_labels_by_songbook_type`
  - `tests/e2e/test_entries.py::EntryModalE2ETests.test_editing_a_hymn_song_shows_its_reference`
  - `tests/e2e/test_entries.py::EntryModalE2ETests.test_the_song_pick_searches_and_the_verses_start_all_checked`
- Implementation: `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/_entry_form.html`, `multimedia/web/templates/reading/_entry_song_options.html`, and `static/web/entries.js`.
