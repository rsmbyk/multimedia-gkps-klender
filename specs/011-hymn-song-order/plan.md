# Plan 011: Sort hymn book songs by number and sub-number

- **Status:** Accepted (owner, 2026-10-06)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-012
- **Bump:** patch

## Why

The accepted public-site contract says hymn books keep number order, but the public song-list query currently applies the non-hymn last-modified order to every book. Sort hymn songs by their structured numeric number and sub-number so the displayed order matches their hymn citations.

## Scope / edges

**In:**

- Public Kidung song lists for hymn books: numeric song number ascending, then sub-number ascending.
- Place a song with no sub-number before its lettered variants; keep any legacy song with no number after numbered songs.
- Keep hymn lists without a sort toggle.
- Preserve the existing non-hymn default and alphabetical toggle behavior.

**Out:**

- Changes to song data, schema, APIs, OBS song pickers, editing rules, or the search result order.
- Changes to non-hymn song sorting or the existing song-list UI.

## Approach

Choose the query ordering based on `book.is_hymn_book` in the public reading list builder. For hymns, order by numeric `number`, normalized `sub_number` (case-insensitive), then title as a deterministic tie-break; put legacy null numbers last. Leave the non-hymn last-modified ordering unchanged. Cover the ordering through the real Django reading view and a browser-visible Kidung list assertion.

## TDD

- Domain/app tests: `multimedia/web/tests.py` (`ReadingViewTests`), with deliberately out-of-order numbers and sub-numbers.
- E2E (tool named after stack exists): `tests/e2e/test_reading.py`, verify visible order through the home/index flow.

## Risks

- Database backends differ in default null ordering and text collation; specify null placement and normalize suffix comparison so the result is consistent.
- Existing spec 004 promises number order, so retain its no-sort-toggle behavior while correcting the query ordering.
