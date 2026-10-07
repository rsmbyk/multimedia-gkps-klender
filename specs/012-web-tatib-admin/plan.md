# Plan 012: Web tatib content admin

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `WEB-TATIB` from `specs/web/tatib-content-admin/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/web/tatib-content-admin/{spec,plan,tasks}.md` into `specs/012-web-tatib-admin/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/web/tatib-content-admin/plan.md`)</summary>

# Plan: WEB-TATIB — Tatib content admin (web)

Spec: [`spec.md`](spec.md) (`WEB-TATIB`)

## Approach

As-built TemplateViews + axios modules over `API-TATIB`. Document the list
filter quirk explicitly so agents do not “fix” it without a product decision.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Views | `multimedia/web/tatib/` |
| JS | `multimedia/web/static/web/tatib/` |
| Tests | `api-paths.test.js`, `reorder.test.js` |

## Contracts

- Reorder payload builder covered by Vitest.
- `insert_after` is order_number from the row.

## Risks and rollout

- Calendar vs `month`/`year` mismatch is intentional as-built documentation.

## Non-goals

- Wiring calendar to API month/year filters unless a future spec asks for it.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `WEB-TATIB` — intended; follow-up may update them.
