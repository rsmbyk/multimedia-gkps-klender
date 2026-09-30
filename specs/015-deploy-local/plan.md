# Plan 015: Local Compose runtime

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `DEPLOY-LOCAL` from `specs/deploy/local-compose-runtime/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/deploy/local-compose-runtime/{spec,plan,tasks}.md` into `specs/015-deploy-local/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/deploy/local-compose-runtime/plan.md`)</summary>

# Plan: DEPLOY-LOCAL — Local Docker Compose runtime

Spec: [`spec.md`](spec.md) (`DEPLOY-LOCAL`)

## Approach

Document the as-built Compose-first local runtime and env expectations from
README / `.env.example`.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Compose | `docker-compose.yml` |
| Env | `.env.example` |
| Seeders | `scripts/*seeder*`, `scripts/seeder.py` |
| Docs | `README.md` |

## Contracts

- Local Postgres via Compose; no production Neon for default local `.env`.
- App on port 8000.

## Risks and rollout

- Documentation-only; host Docker Desktop vs docker-vm is environment-specific.

## Non-goals

- Changing Compose service topology in this backfill.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `DEPLOY-LOCAL` — intended; follow-up may update them.
