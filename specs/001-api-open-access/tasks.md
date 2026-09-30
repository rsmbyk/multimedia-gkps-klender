# Tasks 001: Open product API and web access

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `API-ACCESS` → NNN 001). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/001-api-open-access/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `API-ACCESS` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/api/open-access-policy/tasks.md`)</summary>

# Tasks: API-ACCESS — Open product access policy

Spec: [`spec.md`](spec.md) (`API-ACCESS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-ACCESS-T1 — Document open-access EARS**
  - Touch: this folder
  - Verify: Spec matches settings + existing unauthenticated tests
  - Covers: `API-ACCESS-AC1`–`AC6`

- [x] **API-ACCESS-T2 — Cross-link from APP and API specs**
  - Touch: `specs/app/spec.md`, other `API-*` constraints
  - Verify: Related specs reference `API-ACCESS`
  - Covers: `API-ACCESS-AC6`

## Done when

- Policy is documented with IDs and linked from the registry.
- Existing pytest unauthenticated cases remain the verification baseline.


</details>
