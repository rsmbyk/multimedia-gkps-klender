# Tasks 052: Collapse the hidden add rows and tighten the section break

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/052-collapse-hidden-add-rows`)
- [x] Red — E2E (`tests/e2e/test_tatib_entry_controls.py`): rest state reserves no vertical space
      between entries; hovering/focusing an entry expands the rows above and below; a revealed row
      stays enterable and keeps only itself shown; tabbing onto a collapsed row's button expands
      it; a coarse-pointer/no-hover context shows the rows outright; the break sits at 16px
      margins. The "no overlap" box comparison moved to the collapsed resting state.
- [x] Green — implementation (`static/styles/design/components.css`: grid 0fr/1fr collapse,
      coarse-pointer rule, `.tatib__eos` margins 34px → 16px; `static/web/entries.js`: the
      coordinate guard that stops a shifting short item from oscillating; the clipped
      `.entry__add-inner` in `multimedia/web/templates/reading/tatib.html`).
- [x] Regression — `tests/e2e/test_entries.py`, `tests/e2e/test_reorder.py`,
      `tests/e2e/test_tatib_section_break.py`, `tests/e2e/test_old_rows.py` green (they click the
      rows through).
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
