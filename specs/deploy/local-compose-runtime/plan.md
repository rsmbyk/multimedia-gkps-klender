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
