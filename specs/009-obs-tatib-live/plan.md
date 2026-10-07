# Plan 009: OBS Tatib dock and source

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `OBS-TATIB` from `specs/tatib/obs-tatib-live/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/tatib/obs-tatib-live/{spec,plan,tasks}.md` into `specs/009-obs-tatib-live/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/tatib/obs-tatib-live/plan.md`)</summary>

# Plan: OBS-TATIB — OBS Tatib dock and source

Spec: [`spec.md`](spec.md) (`OBS-TATIB`)

## Approach

As-built two-tab dock (list + display) over `API-TATIB`. Item order is
API-owned; OBS focuses on activate/step/paste/project.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Templates/JS | `multimedia/obs/templates/tatib/`, `static/obs/tatib/` |
| Tests | tatib BC/hotkeys/storage Vitest |

## Contracts

- Channels in `OBS-TATIB-AC2`.
- item_type 0/1 + synthetic `--- END ---` marker.
- As-built double-post on end markers documented in AC11.

## Risks and rollout

- Documentation-only; end-marker posting quirk is intentional as-built.

## Non-goals

- Adding OBS reorder; changing item_type enum.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `OBS-TATIB` — intended; follow-up may update them.
