# Plan: API-SONGS — Songs content REST API

Spec: [`spec.md`](spec.md) (`API-SONGS`)

## Approach

As-built DRF ModelViewSets over `Book`, `Song`, `Verse` with DjangoFilterBackend
and custom short-name uniqueness validation.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Models | `multimedia/songs/models.py` |
| API | `multimedia/api/songs/` |
| Router | `multimedia/api/routers.py` → `/api/songs/` |
| Tests | `multimedia/songs/tests/test_api.py` |

## Contracts

- Write song with `book_id`; read nested `book`.
- Filters: `songs?book=`, `verses?song=`.
- Blank `short_name` allowed to duplicate; non-blank globally unique.

## Risks and rollout

- Documentation-only for this backfill.
- Uniqueness of `(book, number, sub_number)` is model-level; keep tests green.

## Non-goals

- Search endpoint; bookmark APIs; web UI rules.
