# Tasks 040: Let the entry modal picker menus extend past the modal

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`fix/040-picker-menus-past-modal`)
- [ ] Red — domain/app tests (N/A per spec out-of-scope)
- [ ] Green — implementation (`static/styles/design/components.css`, `static/web/entries.js`)
- [ ] Red — E2E (`tests/e2e/test_entry_pickers.py`): the book/song menu extends past the dialog,
      stays in the window, flips up when there is no room below, and scrolls
- [ ] Green — E2E
- [ ] Fill Traceability in `./spec.md`
- [ ] Set `bump` on the ITEM and spec header
- [ ] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
