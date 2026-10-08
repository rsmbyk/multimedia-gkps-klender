# Tasks 031: Clamp a text entry in the Tata Ibadah pane

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/031-clamp-pane-text`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): more than three lines renders three plus
      "…"; blank lines count; three or fewer renders in full; legacy text rows clamp; `clipped` is
      set only when truncated
- [x] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`)
- [x] Red — E2E (N/A per spec out-of-scope)
- [x] Green — E2E (N/A)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
