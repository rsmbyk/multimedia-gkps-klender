# Tasks 035: Give the section break a clear separation

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/035-section-break-separation`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): a `section_break` entry renders the
      divider with its label; the legacy END_OF_SECTION renders the same shape
- [ ] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`,
      `static/styles/design/components.css`)
- [ ] Red — E2E (`tests/e2e/test_tatib_section_break.py`): the divider separates, both themes; the
      divider stays editable
- [ ] Green — E2E
- [ ] Amend spec 006: the `section_break` pane rendering
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
