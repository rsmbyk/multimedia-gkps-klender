# Plan 014: Vercel production

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `DEPLOY-VERCEL` from `specs/deploy/vercel-production/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/deploy/vercel-production/{spec,plan,tasks}.md` into `specs/014-deploy-vercel/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/deploy/vercel-production/plan.md`)</summary>

# Plan: DEPLOY-VERCEL — Vercel production hosting

Spec: [`spec.md`](spec.md) (`DEPLOY-VERCEL`)

## Approach

Capture as-built production constraints from `docs/DEPLOY.md` into a numbered
spec so agents treat routing/env rules as acceptance criteria, not folklore.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Config | `vercel.json`, `.python-version` |
| Entry | `multimedia/wsgi.py` (`app`) |
| Settings | `multimedia/settings.py` (`VERCEL` branches) |
| Docs | `docs/DEPLOY.md` |

## Contracts

- Legacy builds + catch-all routes → WSGI `app`.
- Env and WhiteNoise behavior per deploy doc.

## Risks and rollout

- Changing `vercel.json` can take production down with opaque 404s — require
  tested plan.

## Non-goals

- Hosting migration; Docker production.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `DEPLOY-VERCEL` — intended; follow-up may update them.
