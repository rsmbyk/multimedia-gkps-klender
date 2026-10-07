# Spec: Songs REST content

- **ID:** 002
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `API-SONGS` migrated from `specs/api/songs-content/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `API-SONGS` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `API-SONGS` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/api/songs-content/`
- **When** comparing with this `NNN` pack
- **Then** problem/goal, user stories, and acceptance criteria are preserved verbatim below

### Scenario: suite stays green

- **Given** docs-only migration
- **When** running `pytest` and `npm test`
- **Then** existing suites pass with no behavior change

## Traceability

- Domain/app tests: existing `pytest` suite (`multimedia.settings_test`) and Vitest suite — no new tests for migration.
- E2E: N/A (docs-only migration).
- Implementation: this migration (adopt PR).

---

## Migrated as-built (verbatim from `specs/api/songs-content/spec.md`)

# Spec: API-SONGS — Songs content REST API

| Field | Value |
|-------|--------|
| **Spec ID** | `API-SONGS` |
| **Area** | `api` |
| **Status** | `as-built` |
| **Folder** | `specs/api/songs-content/` |

## Problem / goal

OBS docks and the web songs admin need CRUD access to hymn books, songs, and
verses. This API is the canonical content store for the songs domain.

## User stories

- **API-SONGS-US1:** As a web/OBS client, I want to list and filter books, songs,
  and verses, so that I can browse worship music content.
- **API-SONGS-US2:** As a content editor, I want to create/update/delete songs
  and verses via REST, so that non-hymn content stays maintainable.
- **API-SONGS-US3:** As a client, I want song writes via `book_id` and nested
  `book` on read, so that payloads stay convenient.

## Acceptance criteria (EARS)

### Resources and access

- **API-SONGS-AC1:** THE system SHALL expose ModelViewSet CRUD at
  `/api/songs/books`, `/api/songs/songs`, and `/api/songs/verses`.
- **API-SONGS-AC2:** WHEN an unauthenticated client lists books, THE system
  SHALL return HTTP 200 (`API-ACCESS`).
- **API-SONGS-AC3:** WHEN a client requests `/api/songs/books` with or without a
  trailing slash, THE system SHALL treat both as the same endpoint.

### Books

- **API-SONGS-AC4:** WHEN a client POSTs a valid book (`lang`, `name`, optional
  `short_name`, `is_hymn_book`), THE system SHALL return HTTP 201.
- **API-SONGS-AC5:** IF a client POSTs/PATCHes a non-blank `short_name` that
  already exists on another book, THEN THE system SHALL return HTTP 400 with
  field `short_name`.
- **API-SONGS-AC6:** THE system SHALL allow multiple books with blank
  `short_name` to coexist.
- **API-SONGS-AC7:** THE system SHALL enforce unique `(lang, name)` for books.

### Songs

- **API-SONGS-AC8:** WHEN a client POSTs a song with `book_id`, THE system SHALL
  return HTTP 201 and include a nested `book` object (not `book_id`) in the
  response body.
- **API-SONGS-AC9:** WHEN a client GETs `/api/songs/songs?book=<id>`, THE system
  SHALL return only songs for that book.
- **API-SONGS-AC10:** THE system SHALL enforce unique `(book, number, sub_number)`
  for songs and restrict `key` to the allowed pitch set
  `{c,des,d,es,e,f,ges,g,as,a,bes,b}`.
- **API-SONGS-AC11:** WHEN a client PATCHes a song then DELETEs it, THE system
  SHALL return HTTP 200 then HTTP 204 respectively.

### Verses

- **API-SONGS-AC12:** WHEN a client creates verses and GETs
  `/api/songs/verses?song=<id>`, THE system SHALL return those verses for the
  song.
- **API-SONGS-AC13:** IF a client submits verse `number` less than 1, THEN THE
  system SHALL return HTTP 400.
- **API-SONGS-AC14:** THE system SHALL enforce unique `(song, number)` for verses.

## Out of scope

- Song lyric full-text search (`API-SEARCH`).
- Song bookmarks (`SONGS-BM`).
- Hymn-book UI read-only rules in the web admin (`WEB-SONGS`).

## Constraints

- Follow constitution; open access per `API-ACCESS`.
- Models: `multimedia/songs/models.py`; API: `multimedia/api/songs/`.
- Related: `WEB-SONGS`, `OBS-SONGS`, `API-SEARCH`, `TEST-COV`.

## Notes

- Pytest: `multimedia/songs/tests/test_api.py`.

