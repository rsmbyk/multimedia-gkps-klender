# Plan 000: Multimedia GKPS Klender baseline

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `APP` from `specs/app/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/app/{spec,plan,tasks}.md` into `specs/000-multimedia-baseline/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/app/plan.md`)</summary>

# Plan: APP — Multimedia GKPS Klender (product overview)

Spec: [`spec.md`](spec.md) (`APP`)

## Approach

Document the as-built product as a map of surfaces and domains. No new runtime
behavior. Feature-level contracts live in the registry specs; this plan only
orients readers to where code and docs already live.

## Touch points

| Area | Files / modules |
|------|-----------------|
| URL roots | `multimedia/urls.py` — `/`, `/admin/`, `/api/`, `/obs/` |
| Domain apps | `multimedia/{songs,bible,tatib,bookmarks,obs,web}/` |
| API package | `multimedia/api/` |
| Settings | `multimedia/settings.py`, `multimedia/settings_test.py` |
| Deploy | `vercel.json`, `docker-compose.yml`, `docs/DEPLOY.md` |
| Specs index | `specs/README.md`, this tree |

## Contracts

- Surface map: API + OBS + web content admin + staff admin (see `APP-AC1`–`AC4`).
- Spec ID scheme: [`docs/SDD.md`](../../docs/SDD.md#spec-ids).
- Open access: `API-ACCESS`.

## Risks and rollout

- Risks: Spec drift if feature folders are not updated with behavior changes —
  mitigated by constitution + SDD rule.
- Migrations / backfill: documentation only.
- Rollout: merge via `chore/backfill-feature-specs` into `develop`.

## Non-goals

- Implementing missing UIs (bible/bookmarks web admin).
- Changing auth, deploy topology, or SemVer scheme in this backfill.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `APP` — intended; follow-up may update them.
