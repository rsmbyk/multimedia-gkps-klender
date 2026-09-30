# Tasks 006: Song bookmarks and setlists

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `SONGS-BM` → NNN 006). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/006-songs-bookmarks/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `SONGS-BM` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/songs/song-bookmarks/tasks.md`)</summary>

# Tasks: SONGS-BM — Song bookmarks (setlists)

Spec: [`spec.md`](spec.md) (`SONGS-BM`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **SONGS-BM-T1 — Document bookmark API + OBS activate EARS**
  - Touch: this folder
  - Verify: Align with bookmarks pytest + OBS bookmark storage tests
  - Covers: `SONGS-BM-AC1`–`AC16`

- [ ] **SONGS-BM-T2 — Keep bookmark API tests green**
  - Touch: `multimedia/bookmarks/tests/test_api.py`
  - Verify: `pytest multimedia/bookmarks/tests/test_api.py`
  - Covers: `SONGS-BM-AC2`–`AC12`

## Done when

- Spec matches as-built bookmarks; API tests remain the proof.


</details>
