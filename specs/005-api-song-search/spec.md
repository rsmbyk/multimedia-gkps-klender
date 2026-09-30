# Spec: Song lyric search

- **ID:** 005
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `API-SEARCH` migrated from `specs/api/song-search/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `API-SEARCH` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `API-SEARCH` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/api/song-search/`
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

## Migrated as-built (verbatim from `specs/api/song-search/spec.md`)

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

