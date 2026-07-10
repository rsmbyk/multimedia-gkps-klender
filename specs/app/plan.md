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
