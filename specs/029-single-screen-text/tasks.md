# Tasks 029: Single-screen text entry

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/029-single-screen-text`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): `clean()` requires text; `kind_name()`
      round trip; `_projector_screens()` yields one screen with blanks preserved; the projector
      marks the screen as single-fit; the editor form is offered
- [x] Green — implementation (`multimedia/tatib/models.py` + migration,
      `multimedia/web/reading/entries.py`, `multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`,
      `multimedia/web/templates/reading/projector.html`)
- [x] Red — E2E (`tests/e2e/test_projector.py`): one screen; font shrinks; never overflows
- [x] Green — E2E (`static/web/projector.js`, `static/web/entries.js`)
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
