# Tasks 045: Make the passage modal's chapter/verse dropdowns custom

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`refactor/045-custom-chapter-verse-dropdowns`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): the fragment renders chapter / verse_start
      / verse_end as the custom picker markup with values POSTing, in add and edit
- [x] Green — implementation (`static/web/entries.js`,
      `multimedia/web/templates/reading/_entry_form.html`,
      `static/styles/design/components.css`)
- [x] Red — E2E (`tests/e2e/test_entries.py`): each control opens and picks; the to-verse
      disables with its note; the form saves the right chapter/verses
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
