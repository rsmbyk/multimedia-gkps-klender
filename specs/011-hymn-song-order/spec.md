# Spec: Sort hymn book songs by number and sub-number

- **ID:** 011
- **Status:** Accepted (owner, 2026-10-06)
- **Item:** ITEM-012
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Hymn songs are identified by a numeric song number and optional sub-number. Display hymn-book songs in that citation order in the public Kidung reader, independent of their modification timestamps or title text.

## Scope

### In scope

- Order songs in the public song list for a selected hymn book by numeric `number`, then case-insensitive `sub_number`.
- Put a blank sub-number before suffixed variants; put any legacy null-number songs after numbered songs.
- Preserve the existing absence of a sort control for hymn books.
- Preserve all current non-hymn song-list ordering and sort-toggle behavior.

### Out of scope

- Database/schema or song data changes.
- OBS, API, search-result, editor, or bookmark ordering.
- Any change to non-hymn song ordering or UI.

## Domain rules

- Compare hymn `number` values numerically in ascending order (for example, 2 precedes 10).
- For the same number, compare `sub_number` case-insensitively in ascending order; an empty sub-number precedes lettered variants (for example, 12, 12a, 12b).
- Null-number legacy rows follow all numbered rows.
- Hymn books keep no song-sort toggle. Non-hymn song lists retain their existing last-modified default and alphabetical toggle.

## Acceptance scenarios

### Scenario: Hymn songs follow numeric number and sub-number order

- **Given** a hymn book contains songs created out of order with numbers 10, 2, 12b, 12a, and 12
- **When** I open that book in the public Kidung reader
- **Then** the song rows appear as 2, 10, 12, 12a, 12b
- **And** the comparison is by the numeric number field, not the displayed citation or title

### Scenario: Legacy hymn songs without a number do not interrupt numbered songs

- **Given** a hymn book contains numbered songs and a legacy song whose number is null
- **When** I open that book in the public Kidung reader
- **Then** the numbered songs appear first in number and sub-number order
- **And** the numberless row appears after them

### Scenario: Existing song-list controls and non-hymn ordering stay unchanged

- **Given** a hymn book and a non-hymn songbook
- **When** I open either song list
- **Then** the hymn list has no sort toggle and follows number/sub-number order
- **And** the non-hymn list retains its existing last-modified default and alphabetical toggle

## Traceability

- Domain/app tests: `multimedia/web/tests.py` (`ReadingViewTests`).
- E2E: `tests/e2e/test_reading.py` (public home/index to Kidung book flow).
- Implementation: `multimedia/web/reading/views.py` (`_song_rows`).
