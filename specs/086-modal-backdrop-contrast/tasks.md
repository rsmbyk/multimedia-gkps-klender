# Tasks 086: Separate the modals from the page behind them

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`chore/086-modal-backdrop-contrast`)
- [x] Red — E2E: `tests/e2e/test_entry_preview.py` and `tests/e2e/test_editor.py` assert the backdrop's
      computed background (`rgba(31, 31, 29, 0.38)` before, `rgba(20, 20, 18, 0.52)` after), that the
      scrim is a paint of its own, that the dialog's lift resolves through `--shadow-dialog`, and that
      a pixel of the page really changes under the scrim
- [x] Green — `tokens.css` gains `--backdrop` and `--shadow-dialog` in both themes; `components.css`
      points both `::backdrop` rules and `.preview__confirm-layer` at `--backdrop` and gives both dialogs
      the 1px `--divider` edge and `--shadow-dialog`. The hairline rides in `box-shadow`, not a border,
      so no width or measurement inside the dialog moves.
- [x] Confirm `tests/test_design_tokens.py` still passes unchanged
- [x] Confirm `tests/e2e/test_tatib_hover.py` still passes (origin highlight readable behind the scrim)
- [x] Run the targeted suites only: `tests/test_design_tokens.py`, `tests/e2e/test_entry_preview.py`,
      `tests/e2e/test_editor.py`, `tests/e2e/test_tatib_hover.py`
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] Tests named above are green
- [x] Board, tasks, and version (if any) are complete in this PR
