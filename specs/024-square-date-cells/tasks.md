# Tasks 024: Make Tata Ibadah calendar date cells square

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts Spec 024 and confirms 1:1 proportions with rounded corners retained
- [x] Create `chore/024-square-date-cells` from the current develop-based work without losing pending changes
- [x] Red — `tests/e2e/test_editor.py`: geometry failed at the expected 39.42×34 px baseline before the CSS change
- [x] Green — `static/styles/design/components.css`: responsive square cells without default padding/min-height distortion
- [x] Verify Sunday/selected/today/focus states and existing date-picker interaction/overlap regressions
- [x] Verify geometry at desktop/mobile/narrow/short viewports and Sunday styling in light/dark themes
- [x] Fill Traceability in `./spec.md`
- [x] Prepare patch bump metadata for ITEM-026/027; the combined PR uses 1.0.0 because accepted ITEM-015 carries the higher major bump
- [x] Update ITEM-026 and `backlog/board.md` alongside implementation
- [x] Commit and open draft PR #275; full browser CI runs when the PR becomes ready

## Done when

- [x] Acceptance scenarios hold and targeted tests pass
- [x] No unrelated date behavior or component styling changed
- [ ] Board, tasks, and version land with the implementation in the same PR
