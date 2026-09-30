# Spec: Tatib REST content

- **ID:** 004
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `API-TATIB` migrated from `specs/api/tatib-content/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `API-TATIB` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `API-TATIB` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/api/tatib-content/`
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

## Migrated as-built (verbatim from `specs/api/tatib-content/spec.md`)

# Spec: API-TATIB — Tata ibadah content REST API

| Field | Value |
|-------|--------|
| **Spec ID** | `API-TATIB` |
| **Area** | `api` |
| **Status** | `as-built` |
| **Folder** | `specs/api/tatib-content/` |

## Problem / goal

Web tatib admin and OBS Tatib dock need CRUD for tata ibadah documents and
ordered items, including append/`insert_after` ordering and bulk reorder.

## User stories

- **API-TATIB-US1:** As a content editor, I want to create tatibs and items with
  automatic order numbers, so that service orders stay sequenced.
- **API-TATIB-US2:** As a web admin, I want `insert_after` and reorder, so that
  I can insert and rearrange items without manual renumbering.
- **API-TATIB-US3:** As an OBS dock, I want filters for active/dated/undated
  tatibs, so that I can pick the right service order.

## Acceptance criteria (EARS)

### Tatibs

- **API-TATIB-AC1:** THE system SHALL expose CRUD at `/api/tatib/tatibs` and
  `/api/tatib/items`, plus `POST /api/tatib/items/reorder`.
- **API-TATIB-AC2:** WHEN an unauthenticated client creates a tatib, THE system
  SHALL return HTTP 201 (`API-ACCESS`).
- **API-TATIB-AC3:** WHEN a client filters tatibs with `has_date`, `month`,
  `year`, and/or `is_active`, THE system SHALL return matching rows
  (`has_date=true` → date not null; `has_date=false` → date null).
- **API-TATIB-AC4:** WHEN a tatib is created without `is_active`, THE system
  SHALL default `is_active` to true; `date` MAY be null.

### Items

- **API-TATIB-AC5:** THE system SHALL support item types `0` (TEXT) and `1`
  (END_OF_SECTION).
- **API-TATIB-AC6:** WHEN a client creates an item without `insert_after`, THE
  system SHALL assign `order_number` to `max(existing)+1` (or `1` if empty).
  `order_number` SHALL be read-only on the wire.
- **API-TATIB-AC7:** WHEN a client creates an item with `insert_after=N`, THE
  system SHALL shift only same-tatib items with `order_number > N` by +1, then
  assign the new item `order_number = N+1`. Other tatibs SHALL be unchanged.
- **API-TATIB-AC8:** WHEN a client POSTs
  `{ "items": [ { "item": <pk>, "order_number": <int> }, … ] }` to
  `/api/tatib/items/reorder`, THE system SHALL persist those order numbers and
  return HTTP 200.
- **API-TATIB-AC9:** WHEN a client lists
  `/api/tatib/items?tatib=<id>&ordering=order_number`, THE system SHALL return
  items for that tatib in ascending `order_number`.

## Out of scope

- OBS Tatib display/hotkeys (`OBS-TATIB`).
- Web UI month-calendar quirk (UI may not send `month`/`year` — see
  `WEB-TATIB`).

## Constraints

- Open access: `API-ACCESS`. `insert_after` is an **order_number**, not a PK.
- Related: `WEB-TATIB`, `OBS-TATIB`, `TEST-COV`.

## Notes

- Pytest: `multimedia/tatib/tests/test_api.py`.

