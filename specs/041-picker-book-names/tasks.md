# Tasks 041: Show TB/SIM book names in the passage modal's book picker

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/041-picker-book-names`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): `scripture_books()` yields one row per
      book with TB/SIM names and the primary translation id; a two-translation book does not duplicate
- [ ] Green — implementation (`multimedia/web/reading/entries.py`,
      `multimedia/web/templates/reading/_entry_form.html`,
      `static/styles/design/components.css`, `static/web/entries.js`)
- [ ] Red — E2E (`tests/e2e/test_entry_pickers.py`): the option shows TB main and SIM right
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
