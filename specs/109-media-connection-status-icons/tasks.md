# Tasks 109: Show distinct connection icons in the Media Library status row

- **Status:** Accepted (2026-10-17)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order after the Draft is accepted. -->

## Checklist

- [x] Spec Accepted by the project owner on 2026-10-17
- [x] Branch from the current media feature base as `fix/109-media-connection-status-icons`
- [x] Red — E2E assertions for connected, unavailable, and refreshed icon states in `tests/e2e/test_media_library.py` (confirmed failing before implementation)
- [x] Green — render and update the state icon in `multimedia/web/templates/reading/media_library.html` and `static/web/media-library.js`
- [x] Green — style both icon states in `static/styles/design/components.css`; preserve the accepted preview and reduced-motion behavior
- [x] Run the targeted Media Library E2E module (19 passing) and `git diff --check`
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` and release version 1.14.6 on the ITEM and spec; update `VERSION` and `CHANGELOG.md`
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in PR #359 (In review while open; Done before merge)
- [x] Conventional Commit + draft PR #359 linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All three acceptance scenarios in `spec.md` hold in the Media Library status popover.
- [x] The E2E assertions named above pass.
- [x] Board, tasks, and version metadata are complete in the same PR.
