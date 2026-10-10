# Tasks 054: Label song entries by their short hymn reference and show the selected verses

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/054-song-entry-label-and-verses`, from `develop`)
- [x] Red — domain/app tests (`multimedia/tatib/tests.py`, `multimedia/web/tests.py`): the hymn
      citation (with title, title-less, sub-number, non-hymn unchanged); the stage heading; the
      verse line shown / hidden / non-hymn / deleted target; the modal heading (numbered-hymn
      short form; others unchanged). Six spec-006-era assertions that encoded the old wording
      were updated — `'Kidung Jemaat 152'` resolves at `multimedia/tatib/tests.py` (×3), the
      stage references at `multimedia/web/tests.py` (×2), and the modal's `'Kidung Jemaat'`
      header (×1).
- [x] Green — implementation (`multimedia/tatib/models.py`, `multimedia/web/reading/views.py`,
      `multimedia/web/templates/reading/tatib.html`, `static/styles/design/components.css`)
- [x] Red/Green — E2E (`tests/e2e/test_entry_preview.py`): the song modal's header reads the
      short form; a partial selection shows its `Bait …` line on the stage
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while
      open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
