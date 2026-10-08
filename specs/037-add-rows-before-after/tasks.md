# Tasks 037: Reveal the add rows before and after a hovered item

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/037-add-rows-before-after`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): the pane renders a bar after each item and
      the leading start bar
- [ ] Green — implementation (`static/web/entries.js`,
      `static/styles/design/components.css`,
      `multimedia/web/templates/reading/tatib.html`)
- [ ] Red — E2E (`tests/e2e/test_tatib_entry_controls.py`): hovering an item reveals the bars above
      and below; focus does the same; hovering a bar shows only that bar with no item highlight
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
