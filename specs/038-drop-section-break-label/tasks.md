# Tasks 038: Remove the label from section-break entries

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/038-drop-section-break-label`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): the section-break form has no `title`
      field; a posted `title` is ignored; the pane shows no label for a break; a text entry keeps its
      title
- [ ] Green — implementation (`multimedia/web/reading/entries.py`,
      `multimedia/tatib/models.py`, `multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/_entry_form.html`)
- [ ] Red — E2E (N/A per spec out-of-scope)
- [ ] Green — E2E (N/A)
- [ ] Amend spec 035: the divider shows no label for an entry break
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
