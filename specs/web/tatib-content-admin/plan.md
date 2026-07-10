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
