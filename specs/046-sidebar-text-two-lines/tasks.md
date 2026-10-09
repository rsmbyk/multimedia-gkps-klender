# Tasks 046: Show the first two text lines for untitled service entries

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/046-sidebar-text-two-lines`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): untitled Text and Single-Screen Text show
      the first two literal lines (including a blank line); titled entries retain the title; the
      combined label is capped at 60 characters; legacy and other kinds are unchanged
- [x] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/_toc.html`,
      `static/styles/design/components.css`)
- [x] Red — E2E (`tests/e2e/test_reading.py`): an untitled row shows two lines and the grip is
      centered; a titled row keeps its title
- [x] Green — E2E
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
