# Tasks 025: Avoid automatic row outlines after modal close

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts Spec 025
- [x] Continue on the active dirty branch `feat/026-live-projection-editing`; no separate branch created or switched during this verification
- [x] Regression coverage — `tests/e2e/test_editor.py` exercises Escape/Enter cancellation and real create/edit saves for songbooks, songs, and Tata Ibadah, including kind-aware focus after refresh
- [x] Green — shared close/refresh focus restoration, scoped visual suppression, and correct kind-aware saved-row target
- [x] Focused service-entry, legacy-item, and delete-confirmation regressions pass in `tests/e2e/test_entries.py` and `tests/e2e/test_old_rows.py`
- [x] Unsaved-order modal is no longer present in the current worktree; Spec 026's immediate-save flow has no modal focus-restoration path. The direct-save/no-prompt reorder tests pass.
- [x] Deliberate Tab focus, genuine hover, and date-picker keyboard interaction retain visible indicators
- [x] Pointer close/save and validation-rerender regressions pass
- [x] Fill Traceability with the tested modal/close matrix and actual outcomes
- [x] Prepare patch bump metadata for ITEM-027; the combined PR uses 1.0.0 because accepted ITEM-015 carries the higher major bump
- [x] Update ITEM-027 and `backlog/board.md` alongside implementation
- [x] Commit and open draft PR #275; full browser CI runs when the PR becomes ready

## Done when

- [x] Acceptance scenarios hold and targeted tests pass with real saves on isolated test records
- [x] No blanket focus-outline removal or focus stranded on detached/hidden nodes
- [ ] Board, tasks, and version land with the implementation in the same PR
