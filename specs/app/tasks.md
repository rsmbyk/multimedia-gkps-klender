# Tasks: APP — Multimedia GKPS Klender (product overview)

Spec: [`spec.md`](spec.md) (`APP`) · Plan: [`plan.md`](plan.md)

As-built documentation backfill. Tasks are verification / scaffolding, not new
product implementation.

## Checklist

- [x] **APP-T1 — Write APP overview spec with registry**
  - Touch: `specs/app/spec.md`, `plan.md`, `tasks.md`
  - Verify: Registry lists all feature Spec IDs; links resolve
  - Covers: `APP-AC11`, `APP-US3`

- [x] **APP-T2 — Publish Spec ID conventions**
  - Touch: `docs/SDD.md`, `specs/README.md`, `specs/_templates/*`
  - Verify: Templates show `CODE-US*` / `CODE-AC*` / `CODE-T*` patterns
  - Covers: `APP-AC11`

- [x] **APP-T3 — Backfill feature specs in registry**
  - Touch: all `specs/<area>/<feature>/` rows in `spec.md` registry
  - Verify: Each folder has `spec.md` / `plan.md` / `tasks.md` with IDs
  - Covers: `APP-AC1`–`APP-AC12` (via feature specs)

- [ ] **APP-T4 — Keep registry in sync on future changes**
  - Touch: `specs/README.md`, `specs/app/spec.md`
  - Verify: New capabilities add a Spec ID row before or with the PR
  - Covers: `APP-AC11`

## Done when

- Feature registry is complete for the as-built product.
- Spec ID conventions are documented and used in templates.
- Changelog `## Unreleased` bullet added for this docs backfill.
