# Tasks 042: Sort and label the add-song picker like the hymn books

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/042-song-picker-sort-and-label`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): hymn songs in number order; non-hymn songs
      in title order; hymn groups first (by id) then non-hymn (by name); hymn option `HAL 123 …`;
      non-hymn option the title alone
- [ ] Green — implementation (`multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/_entry_song_options.html`, `static/web/entries.js`)
- [ ] Red — E2E (`tests/e2e/test_entry_pickers.py`): the option text and group order
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
