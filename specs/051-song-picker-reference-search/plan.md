# Plan 051: Search songs by songbook reference and title

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-053
- **Bump:** patch

## Why

The song picker applies the whole query to single fields: title, number, and the book's short name. Typing a songbook's full name (`kidung jemaat`) matches nothing, because only `short_name` is searched. A combined reference (`kj 123`, `Kidung Jemaat 235`) also fails because no single field contains both the book and the number. The picker additionally treats the number as exact, so `kj 12` cannot find `KJ 123`. The public cross-corpus search already resolves book references; the picker has its own endpoint and does not.

## Scope / edges

**In:**

- Match a hymn songbook's full name as well as its short name, case-insensitively and as a substring, so a book reference lists that book's songs alongside title matches.
- Recognize a hymn songbook name substring followed by a song-number prefix (with an optional one-letter sub-number suffix) and optional trailing title text.
- Keep songbook-name filtering restricted to hymn books; preserve current free-text title and number matching, result grouping/order/limit, active/deleted filtering, option labels, selected labels, and verse-loading behavior.

**Out:**

- Changes to public cross-corpus search, sidebar search, or song data.
- Fuzzy typo correction, new search UI, or changes to song ordering or the result limit.
- Filtering non-hymn songbooks by name.

## Approach

- Extend the picker's free-text filter in `entry_song_options` to OR hymn-book `short_name` and `name` substring conditions with title and number matching. Restrict both book-name fields to hymn books so `lagu` does not list non-hymn songbooks.
- Keep combined-reference matching on its own path (`_entry_song_reference_filter`), which runs first for a multi-word query and falls back to free text when the query is not a reference. Parse the first numeric token after a leading phrase, match that phrase as a normalized substring of active hymn-book names/short names, then filter by decimal number prefix (including longer numbers and sub-number variants). A one-letter suffix instead selects that exact base number and sub-number.
- Keep title words after a reference as an additional condition; preserve the existing 200-song slice and ordering.
- Add endpoint regressions for the book-name filter (full name, name substring, title matches kept, non-hymn names ignored, limit kept), then cover the add/edit picker in E2E.

## TDD

- Domain/app tests in `multimedia/web/tests.py` cover full-name/substring filtering, title matches, hymn-only book names, the 200-result cap, exact zero, number-prefix matching across KJ/PKJ, book-phrase substring matching, sub-number suffixes, title suffixes, non-decimal tokens, and out-of-range values. The number-prefix and sub-number regressions failed against the exact-number parser.
- E2E tests in `tests/e2e/test_entry_pickers.py` cover book-name filtering, short/full references, number prefixes and sub-number suffixes, title suffixes, and the edit picker.

## Risks

- **Query breadth within hymn books.** Name substring matching means `kidu` lists *Kidung Jemaat*, *Pelengkap Kidung Jemaat*, and *Nyanyikanlah Kidung Baru* (≈1050 songs, of which the first 200 show). Likewise `kj` matches *PKJ*. Number prefixes such as `12` return 12, 12A/12B, and 120–129 for every matching book. This breadth is accepted; existing ordering and the 200-song cap remain in force.
- **Truncated book listings.** A hymn book can exceed the 200-song cap (Kidung Jemaat has 502 songs, Haleluya 507), so `kj` reaches KJ 1–200 only. A number prefix in the query can reach later songs.
- **Reference/title overlap.** A query that begins with a book-name substring and a number, such as a song titled `Haleluya 2`, reads as a reference rather than as title text. Existing behavior for `kj`-style queries is unchanged.
