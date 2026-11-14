# Tasks 036: Keep the add bar out of the item hover

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/036-add-bar-outside-item-hover`)
- [x] Red — domain/app tests (N/A per spec out-of-scope)
- [x] Green — implementation (`static/styles/design/components.css`)
- [x] Red — E2E (`tests/e2e/test_tatib_entry_controls.py`): hovering the add bar leaves the item
      un-highlighted with controls hidden; the buttons show; hovering the item still reveals it
- [x] Green — E2E
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
