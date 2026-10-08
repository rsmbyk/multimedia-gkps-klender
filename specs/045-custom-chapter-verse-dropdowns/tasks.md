# Tasks 045: Make the passage modal's chapter/verse dropdowns custom

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`refactor/045-custom-chapter-verse-dropdowns`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): the fragment renders chapter / verse_start
      / verse_end as the custom picker markup with values POSTing, in add and edit
- [ ] Green — implementation (`static/web/entries.js`,
      `multimedia/web/templates/reading/_entry_form.html`,
      `static/styles/design/components.css`)
- [ ] Red — E2E (`tests/e2e/test_entry_pickers.py`): each control opens and picks; the to-verse
      disables with its note; the form saves the right chapter/verses
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
