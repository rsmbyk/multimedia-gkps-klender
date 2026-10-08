# Tasks 039: Show the short full title for a hymn song in the service sidebar

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [ ] Spec Accepted by the project owner
- [ ] Branch from the current base (`chore/039-hymn-song-sidebar-title`)
- [ ] Red — domain/app tests (`multimedia/web/tests.py`): a hymn song labels the sidebar with its
      short full title; a non-hymn song is unchanged; a title-less hymn song falls back; the filter
      text carries the words
- [ ] Green — implementation (`multimedia/web/reading/views.py`)
- [ ] Red — E2E (N/A per spec out-of-scope)
- [ ] Green — E2E (N/A)
- [ ] Amend spec 006: the song entry's sidebar label
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
