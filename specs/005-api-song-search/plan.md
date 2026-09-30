# Plan 005: Song lyric search

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `API-SEARCH` from `specs/api/song-search/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/api/song-search/{spec,plan,tasks}.md` into `specs/005-api-song-search/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/api/song-search/plan.md`)</summary>

# Plan: API-SEARCH — Song lyric search API

Spec: [`spec.md`](spec.md) (`API-SEARCH`)

## Approach

As-built DRF list view using Postgres `SearchVector` / phrase `SearchQuery` on
verse lyrics with custom pagination page size 50.

## Touch points

| Area | Files / modules |
|------|-----------------|
| API | `multimedia/api/search/` |
| Tests | `multimedia/api/tests/test_search.py` |
| Consumer | `multimedia/obs/static/obs/songs/dock/tabs/search.js` |

## Contracts

- Query param `q` min length 3.
- Phrase match (quoted or plain multi-word).
- Page size 50.

## Risks and rollout

- SQLite cannot satisfy FTS tests — suite uses Postgres (`TEST-COV`).

## Non-goals

- Title/number search; Elasticsearch.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `API-SEARCH` — intended; follow-up may update them.
