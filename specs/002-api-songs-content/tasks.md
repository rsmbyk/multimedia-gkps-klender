# Tasks 002: Songs REST content

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `API-SONGS` → NNN 002). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/002-api-songs-content/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `API-SONGS` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/api/songs-content/tasks.md`)</summary>

# Tasks: API-SONGS — Songs content REST API

Spec: [`spec.md`](spec.md) (`API-SONGS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-SONGS-T1 — Document songs API EARS from as-built tests**
  - Touch: this folder
  - Verify: Criteria align with `multimedia/songs/tests/test_api.py`
  - Covers: `API-SONGS-AC1`–`AC14`

- [ ] **API-SONGS-T2 — Keep pytest green on songs API**
  - Touch: `multimedia/songs/tests/test_api.py`
  - Verify: `pytest multimedia/songs/tests/test_api.py`
  - Covers: `API-SONGS-AC2`–`AC14`

## Done when

- Spec matches as-built API; tests remain the living proof.


</details>
