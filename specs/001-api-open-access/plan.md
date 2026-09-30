# Plan 001: Open product API and web access

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `API-ACCESS` from `specs/api/open-access-policy/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/api/open-access-policy/{spec,plan,tasks}.md` into `specs/001-api-open-access/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/api/open-access-policy/plan.md`)</summary>

# Plan: API-ACCESS — Open product access policy

Spec: [`spec.md`](spec.md) (`API-ACCESS`)

## Approach

Document the as-built open-access policy. No code changes in this backfill.
Other API/web/OBS specs link here for auth assumptions.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Settings | `multimedia/settings.py` (`REST_FRAMEWORK`) |
| Router | `multimedia/api/routers.py` (`OptionalTrailingSlashRouter`) |
| URLs | `multimedia/urls.py` — `/api/`, `/admin/`, web routes |
| Tests | `multimedia/*/tests/test_api.py` unauthenticated cases |

## Contracts

- Unauthenticated AllowAny for product API.
- Staff auth only for `/admin/`.
- Optional trailing slash on API routes.

## Risks and rollout

- Risks: Deploying publicly without network controls exposes write APIs —
  accepted as-built; call out in ops notes if needed.
- Documentation-only backfill.

## Non-goals

- Adding authentication.
- Changing CSRF or session settings.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `API-ACCESS` — intended; follow-up may update them.
