# Tasks 053: Give each entry the height of its floating controls

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/053-entry-controls-height`, stacked on spec 052's branch)
- [x] Red — E2E (`tests/e2e/test_tatib_entry_controls.py`): the controls' box never overlaps a
      title or first text line (titled and untitled entries); every entry with controls is at least
      band + first-line tall; the band tracks the controls' own condition (the section break
      reserves none). The over-the-text geometry assertion was rewritten.
- [x] Green — implementation (`multimedia/web/templates/reading/tatib.html` modifier class;
      `static/styles/design/components.css` band rule).
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
