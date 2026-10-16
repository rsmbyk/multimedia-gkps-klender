# Tasks 095: Immediate editor opening during form loads

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Continue on the owner-requested `feat/092-offline-library-sync` branch
- [x] Red — add focused E2E tests in `tests/e2e/test_immediate_editor_open.py` covering songbook, song, Tata Ibadah, current/legacy service entries, immediate opening, duplicate activation, cancellation/stale responses, success/focus, failure, and retry
- [x] Green — implement shared active-load coordination and immediate loading UI in `static/web/editors.js` and `static/web/entries.js`
- [x] Run the focused E2E tests and relevant JavaScript syntax checks
- [x] Verify light/dark themes, reduced motion, narrow modal sizing, Cancel/Esc/backdrop behavior, and that the loaded form remains unchanged
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
