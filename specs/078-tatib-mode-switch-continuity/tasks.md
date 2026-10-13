# Tasks 078: Preserve the open Tata Ibadah during list-mode switches

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec 078 Accepted by the project owner
- [x] Branch from current `develop` as `fix/078-tatib-mode-switch-continuity`
- [x] Red — add view-context tests in `multimedia/web/tests.py` for both mode directions and contextual row identity
- [x] Red — add mode-switch sidebar/stage/scroll cases in `tests/e2e/test_reading.py`
- [x] Green — preserve service context and render the selected row in `multimedia/web/reading/views.py` and `multimedia/web/templates/reading/_tatib_panel.html`
- [x] Green — keep second-level state and reveal the selected first-panel row in `static/web/reading.js`
- [x] Verify first-filter edge, second-filter preservation, narrow layout, and reduced motion
- [x] Fill Traceability in `./spec.md`
- [x] Update ITEM-081 and `backlog/board.md` in the same PR
- [x] Set `VERSION`, changelog entry, and `release_version` in the same PR
- [x] Conventional Commit with Codex co-author trailer; draft PR into `develop` linking this spec

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Targeted view and browser checks are green
- [ ] Board, ITEM, tasks, version, and changelog are complete in the same PR
