# Plan 050: Search and label songs by songbook short name

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-052
- **Bump:** patch

## Why

The screenshot shows a query for `kj` in the New song picker, but its endpoint currently filters by song title and number only. It omits `book.short_name`, so a song can be missing when its abbreviation appears only in songbook metadata. The general `search_songs()` helper already matches book short names; the picker has its own query path. The result options already show a hymn's short name and number, but the closed picker and edit-form initial label show only the title.

## Scope / edges

**In:**

- Add case-insensitive substring matching against `Song.book.short_name` in the add/edit song-entry picker search.
- Show the existing hymn option reference (short name, number/sub-number when present, and title) in the selected picker label and edit-form initial label.
- Keep non-hymn selected labels title-only, and preserve the current title and number matching, result order/grouping, limit, and verse flow.

**Out:**

- Full songbook-name matching, changes to the public search or sidebar, and picker redesign.
- Changes to the result-option label format, picker result cap, or song ordering.

## Approach

- Extend `entry_song_options`'s existing OR filter with `book__short_name__icontains=query`.
- Reuse the hymn option's formatted label for the selected state and edit-form prefill; leave non-hymn labels unchanged.
- Add an endpoint regression whose query appears only in the related book's short name.
- Add E2E regressions for abbreviation search, the selected hymn label in add/edit forms, unchanged non-hymn labels, and verse loading.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — regression for matching a songbook short name when the title and number do not match.
- E2E: `tests/e2e/test_entry_pickers.py` — search by abbreviation in the add-song picker and verify the selected hymn reference remains visible in add/edit forms; retain non-hymn title-only and verse behavior.

## Risks

- Short-name substring matching may include overlapping abbreviations (for example, `KJ` also occurs in `PKJ`). This follows the existing case-insensitive substring behavior in `multimedia/songs/search.py`.
