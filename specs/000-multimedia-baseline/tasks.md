# Tasks 000: Multimedia GKPS Klender baseline

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `APP` → NNN 000). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/000-multimedia-baseline/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `APP` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/app/tasks.md`)</summary>

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


</details>
