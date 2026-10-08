# Tasks 039: Show the short full title for a hymn song in the service sidebar

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/039-hymn-song-sidebar-title`)
- [x] Red — domain/app tests (`multimedia/web/tests.py`): a hymn song labels the sidebar with its
      short full title; a non-hymn song is unchanged; a title-less hymn song falls back
- [x] Green — implementation (`multimedia/web/reading/views.py`)
- [x] Red — E2E (N/A per spec out-of-scope)
- [x] Green — E2E (N/A)
- [x] Amend spec 006: the song entry's sidebar label
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
