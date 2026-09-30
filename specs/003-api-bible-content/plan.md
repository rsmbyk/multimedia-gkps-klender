# Plan 003: Bible REST content

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `API-BIBLE` from `specs/api/bible-content/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/api/bible-content/{spec,plan,tasks}.md` into `specs/003-api-bible-content/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/api/bible-content/plan.md`)</summary>

# Plan: API-BIBLE — Bible content REST API

Spec: [`spec.md`](spec.md) (`API-BIBLE`)

## Approach

As-built DRF viewsets with nested serializers, Django filters used by OBS, and
DynamicFields `omit=` on translations/verses.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Models | `multimedia/bible/models.py` |
| API | `multimedia/api/bible/` |
| Tests | `multimedia/bible/tests/test_api.py` |

## Contracts

- Filters: translations by version / abbreviation + book name; verses by
  translation, chapter, verse, and nested abbreviation/book name.
- `omit=` comma-separated field names.

## Risks and rollout

- Documentation-only; write paths for versions/translations/verses are lightly
  tested compared to read/filter paths.

## Non-goals

- OBS browse/history UX; web bible admin.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `API-BIBLE` — intended; follow-up may update them.
