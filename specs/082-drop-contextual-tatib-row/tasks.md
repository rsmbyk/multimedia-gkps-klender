# Tasks 082: Drop the extra Tata Ibadah row for the open service

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/082-drop-contextual-tatib-row`)
- [x] Red — domain/app tests: `multimedia/web/tests.py`
      - [x] replace `test_open_service_has_one_contextual_row_in_opposite_mode` with the new rule
      - [x] no synthetic row and no `Currently open` copy in either mode
      - [x] an in-list open service keeps its single highlighted row and its edit control
- [x] Green — `_tatib_groups()` drops the append block and the `contextual` flag;
      `_tatib_panel.html` drops the flag, the suffix, and the edit-control exemption
- [x] Red then green — E2E: `tests/e2e/test_reading.py`
      - [x] `test_tatib_mode_switch_keeps_open_service_and_reveals_its_row`
      - [x] `test_tatib_mode_switch_keeps_template_and_no_page_state`
- [x] Run the targeted suites only: `multimedia/web/tests.py` (`ServiceEntryViewTests`) and
      `tests/e2e/test_reading.py` (the mode-switch cases)
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
