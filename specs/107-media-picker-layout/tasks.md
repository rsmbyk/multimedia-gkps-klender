# Tasks 107: Polish media picker layout and tab feedback

- **Status:** Implemented and included in consolidated PR #359; 148 targeted tests passed, exact-head GitHub CI pending
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec Accepted by the project owner on 2026-10-17
- [x] Create implementation branch `feat/104-media-picker-layout` from the Spec 103 feature branch, which supplies the modal and companion integration this slice extends
- [x] Red — E2E coverage for connected-empty, unavailable, disabled Save, equal modal dimensions across tabs, footer alignment at the modal bottom, supported-files font sizing, and inactive-tab hover: `tests/e2e/test_media_library.py`
- [x] Green — render the empty-state markup and connection-specific state in `static/web/media-entry.js`
- [x] Green — keep the creation dialog's height stable, fill/scroll the active file panel, and style the quiet empty state in `static/styles/design/components.css`
- [x] Green — set the supported-files label to inherit the paragraph's 12 px size while preserving its semibold weight in `static/styles/design/components.css`
- [x] Green — give the inactive source tab the existing switch hover fill and text color, with the track and transition matching app tokens, in `static/styles/design/components.css`
- [x] Run the targeted Media Library E2E class (12 tests) and verify desktop, narrow, and short viewport behavior
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch`; update `VERSION` to 1.14.1, add the changelog entry, and set `release_version: 1.14.1`
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md)
- [x] Conventional Commit with Codex trailer and consolidated PR #359 to `develop` linking `./spec.md`

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] The targeted E2E coverage is green
- [x] Board, tasks, and version metadata are complete in the implementation PR
