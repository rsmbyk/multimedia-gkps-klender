# Spec: API-SEARCH — Song lyric search API

| Field | Value |
|-------|--------|
| **Spec ID** | `API-SEARCH` |
| **Area** | `api` |
| **Status** | `as-built` |
| **Folder** | `specs/api/song-search/` |

## Problem / goal

OBS Songs Search tab needs phrase full-text search over verse lyrics so
operators can find songs by remembered lines.

## User stories

- **API-SEARCH-US1:** As an OBS operator, I want to search lyrics with a short
  query, so that I can find a song without knowing its number.
- **API-SEARCH-US2:** As a client, I want paginated results, so that large hit
  lists remain usable.

## Acceptance criteria (EARS)

- **API-SEARCH-AC1:** THE system SHALL expose `GET /api/search/songs`.
- **API-SEARCH-AC2:** IF `q` is missing or shorter than 3 characters, THEN THE
  system SHALL return HTTP 400 with field `q`.
- **API-SEARCH-AC3:** WHEN `q` length is at least 3, THE system SHALL run
  Postgres phrase full-text search on `Verse.lyric` (`SearchQuery` phrase type)
  and return matches ordered by descending rank.
- **API-SEARCH-AC4:** THE system SHALL paginate results with page size 50
  (`count`, `next`, `previous`, `results`).
- **API-SEARCH-AC5:** EACH result SHALL include verse fields and a nested
  `song` object.
- **API-SEARCH-AC6:** WHEN an unauthenticated client searches with a valid `q`,
  THE system SHALL allow the request (`API-ACCESS`).

## Out of scope

- Non-Postgres search backends.
- Searching titles/book numbers (lyrics only as-built).
- OBS Search tab UX details beyond calling this API (`OBS-SONGS`).

## Constraints

- Requires Postgres FTS (local Compose / production Neon; pytest per
  `TEST-COV` / `docs/TDD.md`).
- Related: `API-SONGS`, `OBS-SONGS`.

## Notes

- Pytest: `multimedia/api/tests/test_search.py`.
