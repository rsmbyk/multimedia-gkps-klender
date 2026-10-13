# Tasks 071: Scroll Preview text with arrow keys

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Draft accepted by the project owner
- [x] Start `fix/071-preview-keyboard-scroll` from current `develop`; its shared Preview dialog already supports this fix
- [x] Add a failing browser test for arrow-key scrolling after clicking text in `tests/e2e/test_entry_preview.py`
- [x] Make the Preview body focusable, focus it on non-interactive content clicks, and guard keyboard scrolling at its edges
- [x] Verify tabs, Escape, and backdrop dismissal in the targeted browser module; preserve the existing opener restoration path
- [x] Fill Traceability in `./spec.md` with exact paths
- [x] Set `bump: patch` on ITEM-074 and this spec
- [x] Include `VERSION`, changelog, and `release_version` in the implementation PR
- [x] Update ITEM-074 and [`backlog/board.md`](../../backlog/board.md) in the same PR
- [x] Conventional Commit and draft PR linking `./spec.md`

## Done when

- [x] All acceptance scenarios hold
- [x] Targeted browser test passes locally and required remote checks pass
- [x] Board, tasks, version, and PR traceability are complete
