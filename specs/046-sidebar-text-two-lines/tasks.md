# Tasks 046: Show the first two text lines in the service sidebar

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/046-sidebar-text-two-lines`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): a text entry's TOC label is its first two
      lines; a single-screen text entry's too; other kinds unchanged
- [ ] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/_toc.html`,
      `static/styles/design/components.css`)
- [ ] Red — E2E (`tests/e2e/test_reading.py`): the row shows two lines; the grip is centered
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
