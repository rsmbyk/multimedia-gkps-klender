# Tasks 038: Remove the label from section-break entries

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/038-drop-section-break-label`)
- [x] Red — domain/app tests (`multimedia/tatib/tests.py`, `multimedia/web/tests.py`): the
      section-break form has no `title` field; the model `resolve()` returns no label; the pane
      shows no label for a break; a text entry keeps its title
- [x] Green — implementation (`multimedia/web/reading/entries.py`, `multimedia/tatib/models.py`,
      `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/_entry_form.html`)
- [x] Red — E2E (`tests/e2e/test_tatib_section_break.py`): a break's divider carries no label; a
      legacy row's note still shows
- [x] Green — E2E
- [x] Amend spec 035: the divider shows no label for an entry break
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
