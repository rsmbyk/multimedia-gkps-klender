# Plan 004: Tatib REST content

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `API-TATIB` from `specs/api/tatib-content/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/api/tatib-content/{spec,plan,tasks}.md` into `specs/004-api-tatib-content/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/api/tatib-content/plan.md`)</summary>

# Plan: API-TATIB — Tata ibadah content REST API

Spec: [`spec.md`](spec.md) (`API-TATIB`)

## Approach

As-built DRF viewsets with serializer `create` logic for append/`insert_after`
and a custom reorder action.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Models | `multimedia/tatib/models.py` |
| API | `multimedia/api/tatib/` (serializers `insert_after`) |
| Tests | `multimedia/tatib/tests/test_api.py` |

## Contracts

- Item types 0/1; server-assigned `order_number`.
- Reorder body: `{ items: [{ item, order_number }, ...] }`.
- Filters: `month`, `year`, `is_active`, `has_date`.

## Risks and rollout

- Documentation-only; `insert_after` scoping is a known correctness rule locked
  by tests.

## Non-goals

- OBS reorder UI (not present); web-only reorder UX details beyond API.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `API-TATIB` — intended; follow-up may update them.
