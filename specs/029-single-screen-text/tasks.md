# Tasks 029: Single-screen text entry

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/029-single-screen-text`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): `clean()` requires text; `kind_name()`
      round trip; `_projector_screens()` yields one screen with blanks preserved; the projector
      marks the screen as single-fit; the editor form is offered
- [ ] Green — implementation (`multimedia/tatib/models.py` + migration,
      `multimedia/web/reading/entries.py`, `multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`,
      `multimedia/web/templates/reading/projector.html`)
- [ ] Red — E2E (`tests/e2e/test_projector.py`): one screen; font shrinks; ellipsized at the floor,
      never overflowing
- [ ] Green — E2E (`static/web/projector.js`, `static/web/entries.js`)
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
