# Tasks 005: Song lyric search

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `API-SEARCH` → NNN 005). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/005-api-song-search/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `API-SEARCH` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/api/song-search/tasks.md`)</summary>

# Tasks: API-SEARCH — Song lyric search API

Spec: [`spec.md`](spec.md) (`API-SEARCH`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-SEARCH-T1 — Document search API EARS**
  - Touch: this folder
  - Verify: Align with `multimedia/api/tests/test_search.py`
  - Covers: `API-SEARCH-AC1`–`AC6`

- [ ] **API-SEARCH-T2 — Keep pytest green on search**
  - Touch: `multimedia/api/tests/test_search.py`
  - Verify: `pytest multimedia/api/tests/test_search.py` (Postgres)
  - Covers: `API-SEARCH-AC2`–`AC5`

## Done when

- Spec matches as-built search; Postgres tests remain the proof.


</details>
