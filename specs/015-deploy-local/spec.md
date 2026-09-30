# Spec: Local Compose runtime

- **ID:** 015
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `DEPLOY-LOCAL` migrated from `specs/deploy/local-compose-runtime/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `DEPLOY-LOCAL` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `DEPLOY-LOCAL` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/deploy/local-compose-runtime/`
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

## Migrated as-built (verbatim from `specs/deploy/local-compose-runtime/spec.md`)

# Spec: DEPLOY-LOCAL — Local Docker Compose runtime

| Field | Value |
|-------|--------|
| **Spec ID** | `DEPLOY-LOCAL` |
| **Area** | `deploy` |
| **Status** | `as-built` |
| **Folder** | `specs/deploy/local-compose-runtime/` |

## Problem / goal

Developers need a single supported local app runtime: Docker Compose with local
Postgres, without pointing day-to-day work at production Neon.

## User stories

- **DEPLOY-LOCAL-US1:** As a developer, I want `docker compose up` to run the
  app + Postgres, so that local URLs match production shapes.
- **DEPLOY-LOCAL-US2:** As a developer, I want `.env.example` guidance, so that
  required secrets/URLs are obvious.
- **DEPLOY-LOCAL-US3:** As a developer, I want optional seeders, so that songs/
  bible/users data can be loaded for manual testing.

## Acceptance criteria (EARS)

- **DEPLOY-LOCAL-AC1:** THE supported local app runtime SHALL be Docker Compose
  (`web` + Postgres), not a host-only Django run as the primary path.
- **DEPLOY-LOCAL-AC2:** Compose SHALL inject a local `DATABASE_URL` for the `db`
  service; local development SHALL NOT point at production Neon by default.
- **DEPLOY-LOCAL-AC3:** THE repository SHALL provide `.env.example` documenting
  required variables such as `DJANGO_SECRET_KEY` / database-related settings.
- **DEPLOY-LOCAL-AC4:** THE app SHALL be reachable at `http://127.0.0.1:8000/`
  when Compose is up (as documented in README).
- **DEPLOY-LOCAL-AC5:** Optional seed scripts under `scripts/` (e.g. `seeder.py`,
  songs/bible/users seeders) MAY load sample data inside the `web` container.
- **DEPLOY-LOCAL-AC6:** On this maintainer machine, Docker SHALL use the
  VirtualBox `docker-vm` context (not Docker Desktop) per project Docker notes;
  the Compose files themselves remain standard.

## Out of scope

- Production Vercel topology (`DEPLOY-VERCEL`).
- Making pytest’s Postgres requirement identical to Compose app networking
  details (`TEST-COV` / `docs/TDD.md`).
- Guaranteeing seeders’ content completeness.

## Constraints

- Related: `DEPLOY-VERCEL`, `APP`, README quick start.
- Files: `docker-compose.yml`, `.env.example`, `scripts/`.

## Notes

- Optional Neon→local copy script may exist for ops; treat as helper, not
  required for everyday boot.

