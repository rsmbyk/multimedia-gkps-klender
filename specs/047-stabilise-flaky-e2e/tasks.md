# Tasks 047: Stabilise the flaky E2E tests

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`test/047-stabilise-flaky-e2e`)
- [x] Red — the two tests fail intermittently (observed on `#278`'s and `#283`'s develop push runs)
- [x] Green — implementation (`tests/e2e/test_editor.py`, `tests/e2e/test_reading.py`)
- [x] E2E — both pass repeatedly (4 runs locally)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
      (bump is `none` — test-only)
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
