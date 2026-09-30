# Tasks 003: Bible REST content

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `API-BIBLE` → NNN 003). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/003-api-bible-content/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `API-BIBLE` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [ ] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/api/bible-content/tasks.md`)</summary>

# Tasks: API-BIBLE — Bible content REST API

Spec: [`spec.md`](spec.md) (`API-BIBLE`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-BIBLE-T1 — Document bible API EARS**
  - Touch: this folder
  - Verify: Align with `multimedia/bible/tests/test_api.py`
  - Covers: `API-BIBLE-AC1`–`AC8`

- [ ] **API-BIBLE-T2 — Keep pytest green on bible API**
  - Touch: `multimedia/bible/tests/test_api.py`
  - Verify: `pytest multimedia/bible/tests/test_api.py`
  - Covers: `API-BIBLE-AC2`–`AC6`

## Done when

- Spec matches as-built API; tests remain the living proof.


</details>
