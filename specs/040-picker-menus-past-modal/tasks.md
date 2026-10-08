# Tasks 040: Let the entry modal picker menus extend past the modal

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/040-picker-menus-past-modal`)
- [x] Red — domain/app tests (N/A per spec out-of-scope)
- [x] Green — implementation (`static/styles/design/components.css`, `static/web/entries.js`)
- [x] Red — E2E (`tests/e2e/test_entry_pickers.py`): the book/song menu is fixed, in the window,
      and follows the content's scroll
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
