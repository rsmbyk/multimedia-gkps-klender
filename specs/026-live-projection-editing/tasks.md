# Tasks 026: Keep editing while projecting, and keep the display in step

- **Status:** Accepted (owner, 2026-10-08)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Work on `feat/026-live-projection-editing` alongside the pending 013–025 docs
- [x] Amend spec 006 (lock rule + scenario; slice-3 mode rule + scenario) and spec 021 (superseded)
      so the contracts match this slice
- [ ] Red — `multimedia/web/tests.py`: the reorder pane still renders the endpoint carrier, and no
      longer renders `data-reorder-save` / `data-reorder-discard` / `data-reorder-confirm`
- [x] Green — (A) lift the ban: `static/web/entries.js`, `static/web/reorder.js`,
      `static/web/display.js`
- [x] Green — (B) reorder on drop: `static/web/reorder.js`,
      `multimedia/web/templates/reading/base.html`, `multimedia/web/templates/reading/tatib.html`,
      `static/web/reading.js`
- [x] Green — (C) display follows: `static/web/display.js`, `static/web/projector.js`
- [ ] Red — `tests/e2e/test_reorder.py`: a drop and a keyboard move persist with no Save; leaving
      never prompts
- [x] Green — `tests/e2e/test_reorder.py`
- [ ] Red — `tests/e2e/test_projector.py`: editing allowed while projecting; the display follows an
      add / edit / delete / reorder without Update; Update still works
- [x] Green — `tests/e2e/test_projector.py`
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR**
      (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in `spec.md` hold in the focused checks
- [x] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
