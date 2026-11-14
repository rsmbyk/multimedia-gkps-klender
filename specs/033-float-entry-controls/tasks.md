# Tasks 033: Float the entry controls over each item, top-right

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/033-float-entry-controls`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): the item element carries preview/Edit/
      Delete; the add bar no longer does
- [x] Green — implementation (`multimedia/web/templates/reading/tatib.html`,
      `static/styles/design/components.css`)
- [x] Red — E2E (`tests/e2e/test_tatib_entry_controls.py`): hover reveals over the text; keyboard
      focus reveals; the no-hover rule is present; no lingering reveal
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
