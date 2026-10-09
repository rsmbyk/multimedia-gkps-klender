# Spec 051: Search songs by songbook reference and title

- **ID:** 051
- **Status:** Accepted
- **Item:** ITEM-053
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Let people find songs in the New song picker by naming a songbook — its abbreviation, its full name, or any distinctive part of either — and by the common book-and-number reference, so `kj`, `kidu`, `maat`, `kidung jemaat`, `kj 123`, and `Kidung Jemaat 235` all lead to the intended songs. Song-title text keeps working, alone or after a reference.

## Scope

### In scope

- Search in the song picker used by the add and edit song-entry forms.
- Match the query as a case-insensitive substring of a **hymn** songbook's short name or full name, so `kj`, `kidu`, `maat`, or `kidung jemaat` lists that songbook's songs alongside songs whose title matches.
- Match a hymn songbook's short name or full name followed by a song-number prefix, case-insensitively: `kj 123`, `Kidung Jemaat 235`, and `kj 12` (which also matches KJ 123 and PKJ 12/123 because the book phrase is a substring). A one-letter sub-number suffix can be included, e.g. `kj 12a`.
- Allow title text after the reference, so `KJ 123 <song title>` still finds that referenced song.
- Preserve existing free-text title and number matching, option labels, grouping, ordering, the result limit, active/deleted filtering, selected labels, and verse-loading behavior.

### Out of scope

- Changes to public cross-corpus search, sidebar search, or song data.
- Fuzzy typo correction, picker redesign, or changes to result ordering or the result limit.
- Filtering non-hymn songbooks by name (`lagu` keeps matching titles only).
- New matching against lyrics.

## Domain rules

- Free-text matching is case-insensitive and substring-based, and covers song title, song number, and hymn songbook short name or full name. Those fields are OR-ed, so a book reference returns that songbook's songs *in addition to* any song whose title matches the query.
- Only hymn songbooks are matched by name. A non-hymn book's name is never a filter, so `lagu` does not list the *Lagu* songbooks' songs — it matches titles alone.
- Because matching is substring-based, one query may match several hymn songbooks: `kidu` also matches *Nyanyikanlah Kidung Baru* and *Pelengkap Kidung Jemaat*; `maat` also matches *Pelengkap Kidung Jemaat*; `kj` also matches the `PKJ` short name. That breadth is accepted — the existing order decides what the person sees first.
- A trimmed query whose leading phrase is a substring of an active hymn songbook's short name or full name, followed by a song-number prefix, is one combined, case-insensitive reference. It matches songs from every hymn songbook containing that book phrase; e.g. `kj 12` can match KJ and PKJ because `kj` occurs in both short names. The book phrase is not a literal substring that must occur in a single song field.
- Without a sub-number letter, the numeric part is a prefix of the song's number: `kj 12` matches number 12, number 12 with any sub-number, and numbers 120–129. A zero query matches number 0 exactly. If the query includes one letter after the number (`kj 12a`), match that exact base number and case-insensitive sub-number; do not match 12B or 120.
- If title words follow a recognized reference, the matching song must satisfy the book substring, number-prefix (and optional sub-number), and title conditions, so a different book/number cannot match solely because its title shares the words.
- If several songs in a matching book share a number through sub-number variants, a numeric-only prefix includes all of them in the existing order.
- The picker's 200-song result limit is unchanged and applies to every query, including book filters; a number in the query narrows the list but may still match a prefix range.
- Result grouping and every other picker behavior are unchanged.

## Acceptance scenarios

### Scenario: Filter songs by songbook abbreviation or name

- **Given** hymn songbooks *Kidung Jemaat* (`KJ`) and *Pelengkap Kidung Jemaat* (`PKJ`), and a song in another book whose title contains the query
- **When** I type `kj`, `kidu`, `maat`, or `kidung jemaat` in the add-song picker search field
- **Then** the songs of every matching hymn songbook appear, grouped under their songbook label
- **And** the song whose title matches appears in the same result set

### Scenario: A non-hymn songbook's name is not a filter

- **Given** a song in the non-hymn *Lagu* songbook whose title does not contain the query
- **When** I type `lagu` in the add-song picker search field
- **Then** that song does not appear
- **And** songs whose title contains `lagu` still do

### Scenario: Find songs by a book-and-number prefix, including sub-numbers

- **Given** songs in KJ and PKJ numbered 12, 123, and KJ songs numbered 12A and 12B
- **When** I type `kj 12` in the picker
- **Then** KJ 12, KJ 123, PKJ 12, and PKJ 123 appear, as do the KJ 12A and KJ 12B variants
- **And** KJ 130 does not appear
- **When** I type `kj 12a`
- **Then** KJ 12A appears and KJ 12B does not
- **And** `kj 12` also finds songs whose number begins with 12 when searching in the edit-song picker

### Scenario: Find a song by full book name and number prefix

- **Given** songs in Kidung Jemaat numbered 235 and 235A
- **When** I type `kidung jemaat 235`
- **Then** both songs appear under their existing songbook group

### Scenario: Include the song title with the reference

- **Given** a Kidung Jemaat song numbered 235 with a known title
- **When** I type `Kidung Jemaat 235` followed by that song's title
- **Then** the referenced song appears
- **And** a song from a different book or with a different number does not match solely because its title contains the same words

### Scenario: Preserve existing picker behavior

- **Given** a query that matches more than 200 songs, such as a hymn songbook's name
- **When** I search for and select a result
- **Then** at most 200 results show, in the existing order
- **And** existing grouping, labels, selection, and verse loading are unchanged

## Traceability

- Domain/app tests:
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_filter_songs_by_songbook_name`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_filter_songs_by_songbook_name_substring`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_book_filter_keeps_title_matches`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_book_filter_ignores_non_hymn_book_names`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_book_filter_keeps_the_result_limit`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_reference_zero_does_not_match_other_single_digit_numbers`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_reference_number_is_a_prefix`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_reference_book_part_is_a_substring`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_reference_number_prefix_can_include_the_sub_number`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_match_short_name_and_number`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_match_full_book_name_and_number`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_match_reference_followed_by_title`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_match_accented_title_after_reference`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_ignore_non_decimal_reference_number`
  - `multimedia/web/tests.py::ServiceEntryViewTests.test_song_options_ignore_out_of_range_reference_number`
- E2E:
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_filters_songs_by_songbook_name`
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_searches_by_short_and_full_songbook_reference`
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_reference_number_prefix_includes_sub_number`
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_reference_can_include_the_title`
  - `tests/e2e/test_entry_pickers.py::EntryPickerE2ETests.test_song_picker_searches_by_reference_when_editing`
- Implementation: `multimedia/web/reading/views.py`.
