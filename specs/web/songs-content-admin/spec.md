# Spec: WEB-SONGS — Songs content admin (web)

| Field | Value |
|-------|--------|
| **Spec ID** | `WEB-SONGS` |
| **Area** | `web` |
| **Status** | `as-built` |
| **Folder** | `specs/web/songs-content-admin/` |

## Problem / goal

Editors manage non-hymn song content in the browser: books → songs → verses,
with live lyric preview. Hymn books are treated as read-mostly in this UI.

## User stories

- **WEB-SONGS-US1:** As a content editor, I want to browse books and songs, so
  that I can find and open a song’s verses.
- **WEB-SONGS-US2:** As a content editor, I want CRUD modals for non-hymn books,
  songs, and verses, so that I can maintain custom content.
- **WEB-SONGS-US3:** As a content editor, I want a verse lyric preview with
  chunked lines, so that I can check projection-sized chunks.

## Acceptance criteria (EARS)

### Pages and access

- **WEB-SONGS-AC1:** THE system SHALL serve `/` as a hub linking to Songs and
  Tata Ibadah admin.
- **WEB-SONGS-AC2:** THE system SHALL serve `/songs/books`,
  `/songs/books/<id>`, and `/songs/songs/<id>` (and redirect `/songs/` → books).
- **WEB-SONGS-AC3:** THE songs content-admin pages SHALL be reachable without
  login (`API-ACCESS`).

### API usage

- **WEB-SONGS-AC4:** THE UI SHALL load books via `GET /api/songs/books` and
  songs via `GET /api/songs/songs?book=<id>`.
- **WEB-SONGS-AC5:** WHEN creating a song, THE UI SHALL POST `/api/songs/songs`
  with `book_id`, `title`, `number` (may be null), `sub_number`, `is_untitled`.
- **WEB-SONGS-AC6:** THE UI SHALL load/create/update/delete verses via
  `/api/songs/verses` filtered by `song`.

### Hymn vs non-hymn UX

- **WEB-SONGS-AC7:** WHILE a book has `is_hymn_book === true`, THE UI SHALL hide
  Add Song / Add Verse and hide edit/delete hover actions on books/songs/verses
  (read-mostly).
- **WEB-SONGS-AC8:** WHILE a book is non-hymn, THE UI SHALL offer full CRUD via
  modals, with client-side name/title charset and max-length checks before
  write.

### Browse and preview

- **WEB-SONGS-AC9:** WHEN the operator uses song list search, THE UI SHALL
  filter by title and book number (Semantic UI search, `minCharacters: 1`).
- **WEB-SONGS-AC10:** WHEN the operator opens verse preview, THE UI SHALL show
  lyrics chunked by pairing adjacent lines (`joinAdjacentLyricLines`), with
  prev/next navigation in the preview.

## Out of scope

- API validation rules themselves (`API-SONGS`).
- OBS Songs dock (`OBS-SONGS`).
- Bible/bookmarks web admin (not built).

## Constraints

- Templates/JS: `multimedia/web/songs/`, `multimedia/web/static/web/songs/`.
- Related: `API-SONGS`, `API-ACCESS`, `WEB-TATIB`.

## Notes

- Vitest: `multimedia/web/static/web/api-paths.test.js`,
  `…/songs/verses/lyric-chunks.test.js`.
