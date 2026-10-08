# Tasks 044: Add a TB/SIM toggle to the passage modal book picker

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`feat/044-passage-translation-toggle`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): the modal renders the toggle; the fragment
      carries both translations' names/ids per book
- [ ] Green — implementation (`multimedia/web/templates/reading/_entry_form.html`,
      `static/web/entries.js`, `static/styles/design/components.css`)
- [ ] Red — E2E (`tests/e2e/test_entry_pickers.py`): toggling swaps the names; the choice is stored;
      the chapter / verse controls are unchanged
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
