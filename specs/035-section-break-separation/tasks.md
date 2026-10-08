# Tasks 035: Give the section break a clear separation

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/035-section-break-separation`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): a `section_break` entry renders the
      divider with its label; the legacy END_OF_SECTION renders the same shape
- [x] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`,
      `static/styles/design/components.css`, `static/web/reorder.js`)
- [x] Red — E2E (`tests/e2e/test_tatib_section_break.py`): the divider spans the column; the
      divider stays editable
- [x] Green — E2E
- [x] Amend spec 006: the `section_break` pane rendering
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
