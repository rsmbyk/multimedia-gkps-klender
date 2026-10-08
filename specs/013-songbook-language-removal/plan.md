# Plan 013: Remove songbook language and merge duplicate songbooks

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-015
- **Bump:** major

## Why

Songbook language no longer distinguishes the public corpus. Remove the field and merge exact-name duplicates without losing songs, lyric verses, or references.

## Scope / edges

**In:**

- Remove `Book.lang` and the now-unused `songs.Language` model/table.
- Merge existing songbooks with the same exact name before enforcing global name uniqueness.
- Preserve all songs, their lyric verses, IDs, metadata, references, and soft-delete state; resolve `(book, number, sub_number)` collisions by allocating the next available integer above the merged book's current maximum while preserving the sub-number.
- Remove language from songbook forms, serializers, API payloads, sorting, search, admin, and tests where it is a songbook property.

**Out:**

- Renaming songbooks or changing short-name/hymn metadata beyond the keeper rule.
- Rewriting song, verse, bookmark, or Tata Ibadah entry identities.
- Changing Bible language/version data.

## Approach

- The data migration groups songbooks by exact `name`. The keeper is the lowest-ID non-deleted book when any exist, otherwise the lowest ID. The keeper retains its short name, hymn flag, and other book metadata.
- Process duplicate books and songs deterministically by ID. Repoint every song (including soft-deleted songs) to the keeper before removing duplicate books. If a song's number/sub-number tuple conflicts, assign the next free integer above the current maximum and retain its sub-number; do not alter song or verse primary keys or other fields.
- Apply a global unique constraint to `Book.name` after consolidation, then remove the language relation and model. Update every caller and pin the changed API key set.

## TDD

- Domain/app tests: `multimedia/songs/tests.py` (migration preservation, duplicate-number allocation, and global name uniqueness); `multimedia/web/tests.py` (editor form); `multimedia/api/songs/tests.py` (exact book payload); `multimedia/tatib/tests.py`, `multimedia/api/bookmarks/tests.py`, `multimedia/api/search/tests.py` (fixtures and retained song references).
- E2E: `tests/e2e/test_editor.py` (create/edit songbook form without language).

## Risks

- This is a destructive, externally visible schema/API change. Confirm a production backup and migration rehearsal before applying it.
- Merging makes active songs from a soft-deleted duplicate book children of the selected active keeper. The migration preserves each song's own soft-delete fields unchanged.
- Number collisions change the affected song citation; references remain valid because song IDs do not change.
