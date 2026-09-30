# Tasks 004: Tatib REST content

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `API-TATIB` → NNN 004). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/004-api-tatib-content/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `API-TATIB` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [ ] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/api/tatib-content/tasks.md`)</summary>

# Tasks: API-TATIB — Tata ibadah content REST API

Spec: [`spec.md`](spec.md) (`API-TATIB`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-TATIB-T1 — Document tatib API EARS**
  - Touch: this folder
  - Verify: Align with `multimedia/tatib/tests/test_api.py`
  - Covers: `API-TATIB-AC1`–`AC9`

- [ ] **API-TATIB-T2 — Keep pytest green on tatib API**
  - Touch: `multimedia/tatib/tests/test_api.py`
  - Verify: `pytest multimedia/tatib/tests/test_api.py`
  - Covers: `API-TATIB-AC2`–`AC9`

## Done when

- Spec matches as-built API; tests remain the living proof.


</details>
