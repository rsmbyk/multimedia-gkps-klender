# Spec 013: Remove songbook language and merge duplicate songbooks

- **ID:** 013
- **Status:** Accepted (owner, 2026-10-07)
- **Item:** ITEM-015
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** major

## Intent

Remove language as a songbook property and consolidate same-name songbooks while retaining every song and its dependent data.

## Scope

### In scope

- Remove `Book.lang` from the Django model, database schema, editor forms, admin, API responses, ordering, search/display code, and fixtures; remove `songs.Language` when it has no remaining consumers.
- Merge existing books with exactly equal names and enforce globally unique songbook names after the merge.
- Preserve all Song and Verse records and all song-based references.

### Out of scope

- Bible language/version behavior.
- Renaming songbooks, changing the keeper's short name/hymn flag, or rewriting song/verse IDs.
- Changing the existing API routes beyond removal of the `lang` field from book payloads.

## Domain rules

- Songbook names are compared exactly and case-sensitively for migration grouping; after migration, a name is globally unique.
- For a duplicate-name group, keep the lowest-ID non-deleted Book if one exists; otherwise keep the lowest-ID Book. The keeper retains its metadata, including short name and hymn-book flag.
- Reassign every song from duplicate Books to the keeper, including soft-deleted songs. Preserve each Song's primary key, title, key, flags, modification/deletion metadata, and all Verse rows and their IDs/fields. Existing service-entry/bookmark references continue resolving through the unchanged Song IDs.
- If a moved song's `(number, sub_number)` conflicts in the keeper, assign the next available integer greater than the current maximum and keep its existing sub-number. Resolve multiple conflicts deterministically by duplicate Book ID then Song ID, considering earlier assignments when finding the next free number.
- Remove duplicate Book rows only after their songs have been reassigned. Do not otherwise change song/verse soft-delete state.
- No songbook form, model, or book API payload contains a language field. The book API key set is pinned without `lang`.

## Acceptance scenarios

### Scenario: Merge duplicate songbooks and preserve all songs

- **Given** two songbooks with the same exact name and songs with non-conflicting numbers
- **When** the migration runs
- **Then** one songbook remains, every song and lyric verse remains, and every song points to the keeper
- **And** song IDs and song-based foreign-key references remain unchanged

### Scenario: Allocate a free number for a collision

- **Given** same-name songbooks contain songs with the same number and sub-number
- **When** the migration merges them
- **Then** the keeper's song keeps its number, and the moved colliding song gets the next available integer above the merged maximum with its sub-number preserved
- **And** the moved song's lyrics, metadata, ID, and references remain intact

### Scenario: Select a stable keeper

- **Given** a duplicate-name group with active and soft-deleted books
- **When** the migration runs
- **Then** the lowest-ID active book is the keeper; if all are soft-deleted, the lowest ID is the keeper
- **And** the keeper's short name and hymn flag are unchanged

### Scenario: Remove language from songbook contracts

- **Given** an active songbook
- **When** I use the editor or read its book API resource
- **Then** no language field is rendered or returned
- **And** creating two books with the same name is rejected regardless of their former languages

### Scenario: Keep song references resolvable

- **Given** a bookmark or service entry points to a song in a duplicate book
- **When** the migration completes
- **Then** the same Song ID still resolves through the keeper, with all lyric verses available

## Traceability

- Domain/app tests: `multimedia/songs/tests.py`; fixtures and reference regressions in `multimedia/tatib/tests.py`, `multimedia/api/bookmarks/tests.py`, `multimedia/api/search/tests.py`; editor contract in `multimedia/web/tests.py`.
- API contract: `multimedia/api/songs/tests.py` (exact book key set before/after).
- E2E: `tests/e2e/test_editor.py`.
- Implementation: `multimedia/songs/models.py`, `multimedia/songs/migrations/0015_merge_duplicate_books_remove_language.py`, `multimedia/songs/admin.py`, `multimedia/api/songs/serializers.py`, `multimedia/web/reading/editors.py`, `multimedia/web/reading/views.py`, `multimedia/obs/static/obs/songs/dock/tabs/songbooks.js`, `multimedia/web/static/web/songs/books/`, `multimedia/web/templates/reading/_books.html`, `scripts/songs_seeder.py`, and all affected fixtures.
