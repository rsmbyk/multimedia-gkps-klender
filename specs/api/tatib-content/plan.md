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
