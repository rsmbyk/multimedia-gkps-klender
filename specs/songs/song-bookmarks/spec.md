# Spec: SONGS-BM — Song bookmarks (setlists)

| Field | Value |
|-------|--------|
| **Spec ID** | `SONGS-BM` |
| **Area** | `songs` |
| **Status** | `as-built` |
| **Folder** | `specs/songs/song-bookmarks/` |

## Problem / goal

Operators build service setlists (bookmarks) of songs with selected verses,
reorder them, filter by date/active state, and drive the OBS Songs Display tab
from an activated bookmark.

## User stories

- **SONGS-BM-US1:** As an OBS operator, I want to create and activate a bookmark,
  so that the Display tab plays through a prepared setlist.
- **SONGS-BM-US2:** As an operator, I want unique active bookmark names per date
  (including undated), so that setlists do not collide.
- **SONGS-BM-US3:** As an operator, I want reorder and verse selection on items,
  so that the live order matches the service plan.

## Acceptance criteria (EARS)

### API resources

- **SONGS-BM-AC1:** THE system SHALL expose CRUD at
  `/api/bookmarks/songs/bookmarks` and `/api/bookmarks/songs/items`, plus
  `POST /api/bookmarks/songs/items/reorder`.
- **SONGS-BM-AC2:** WHEN an unauthenticated client creates a bookmark, THE
  system SHALL return HTTP 201 (`API-ACCESS`).
- **SONGS-BM-AC3:** WHEN a client filters bookmarks with `has_date`, `month`,
  `year`, and/or `is_active`, THE system SHALL return matching rows.
- **SONGS-BM-AC4:** WHEN listing bookmarks with `ordering=name`, THE system
  SHALL order by name.

### Uniqueness (active only)

- **SONGS-BM-AC5:** IF an active bookmark with the same `name` and null `date`
  already exists, THEN creating/updating another active bookmark that way SHALL
  return HTTP 400 (`"This bookmark name already exists"`).
- **SONGS-BM-AC6:** IF an active bookmark with the same `name` and same non-null
  `date` already exists, THEN THE system SHALL return HTTP 400
  (`"This bookmark name on this date already exists"`).
- **SONGS-BM-AC7:** THE system SHALL allow reusing a name when the conflicting
  row is inactive.
- **SONGS-BM-AC8:** WHEN updating a bookmark without changing its unique
  name+date identity, THE system SHALL accept the update (exclude self).

### Items

- **SONGS-BM-AC9:** WHEN creating a bookmark item, THE system SHALL
  auto-assign `order_number = max+1` for that bookmark.
- **SONGS-BM-AC10:** THE `verse` field SHALL be a comma-separated integer list;
  IF invalid, THEN THE system SHALL return HTTP 400 on `verse`.
- **SONGS-BM-AC11:** WHEN returning an item, THE system SHALL include
  `verse_info` (per number `{number, lyric}`; missing verse → `lyric: ""`) and
  `song_info` (`book_number`, `title`, `is_untitled`). For hymn books,
  `book_number` SHALL be `"{short_name} {number}{sub_number}"`; for non-hymn,
  `book_number` SHALL be null.
- **SONGS-BM-AC12:** WHEN a client POSTs a valid reorder payload to
  `/api/bookmarks/songs/items/reorder`, THE system SHALL persist order numbers
  and return HTTP 200.

### OBS integration (Bookmarks tab)

- **SONGS-BM-AC13:** WHEN the operator Activates a bookmark in the OBS Songs
  Bookmarks tab, THE dock SHALL load items
  (`GET …/items?bookmark=`) and initialize Display at song index 0.
- **SONGS-BM-AC14:** WHEN bookmark items become empty/null, THE Display tab
  SHALL idle (placeholders, inactive).
- **SONGS-BM-AC15:** WHEN a single-song activate (paste / song detail) runs
  WHILE a bookmark was active, THE manager SHALL stash a pending bookmark and
  offer Reactivate.
- **SONGS-BM-AC16:** WHEN reordering in bookmark-detail, THE dock SHALL POST
  `/api/bookmarks/songs/items/reorder`.

## Out of scope

- Full Songs Display/hotkey behavior (`OBS-SONGS`).
- Bookmarks web content-admin UI (does not exist; use OBS + `WEB-ADMIN`).

## Constraints

- Models: `multimedia/bookmarks/`. API: `multimedia/api/bookmarks/`.
- Related: `OBS-SONGS`, `API-SONGS`, `API-ACCESS`, `TEST-COV`.

## Notes

- Pytest: `multimedia/bookmarks/tests/test_api.py`.
- Vitest: `…/songs/dock/common/bookmark-storage.test.js`.
- OBS builds `verse` via `JSON.stringify(selectedVerses).slice(1, -1)`.
