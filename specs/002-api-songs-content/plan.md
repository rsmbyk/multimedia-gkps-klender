# Plan 002: Songs REST content

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `API-SONGS` from `specs/api/songs-content/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/api/songs-content/{spec,plan,tasks}.md` into `specs/002-api-songs-content/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/api/songs-content/plan.md`)</summary>

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


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `API-SONGS` — intended; follow-up may update them.
