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
