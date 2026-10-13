# Tasks 083: Give the translation switch the same hover as the screen-mode switch

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/083-language-switch-hover`)
- [x] Red — E2E: `tests/e2e/test_reading.py` (reading header) and `tests/e2e/test_entry_pickers.py`
      (passage picker): the unselected option's computed background changes on hover and the selected
      option's does not
- [x] Green — `static/styles/design/components.css`: `.read__lang` hover takes `--icon-hover-bg` for
      unselected options only; the enhanced transition list gains `background`
- [x] Run the targeted suites only: `tests/e2e/test_reading.py` (the language cases) and
      `tests/e2e/test_entry_pickers.py` (the translation toggle)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open;
      Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
