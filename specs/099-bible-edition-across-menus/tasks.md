# Tasks 099: Keep the selected Bible Version across menu switches

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Regression coverage first; current develop already contains the behavior, so green needs no runtime edit. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from current `develop` (`fix/099-bible-edition-across-menus`)
- [x] Add E2E coverage in `tests/e2e/test_reading.py` for SIM and TB menu round trips through Kidung and Tata Ibadah, Back/Forward, unavailable SIM fallback, refresh reset, and separate-tab isolation
- [x] Add saved-copy menu round-trip coverage in `tests/e2e/test_offline_library.py`
- [x] Green — current `develop` already preserves the tab-local choice through menu and stage swaps in online and saved-copy reading; no runtime correction was needed
- [x] Verify explicit `?ed=sim` initial loads and no-JavaScript translation links retain their existing behavior
- [x] Run the targeted reading and offline-library E2E cases; do not run the full suite locally
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header
- [x] Update `VERSION`, changelog `## [X.Y.Z]`, and `release_version` in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] All acceptance scenarios in `spec.md` hold
- [x] Targeted reading and saved-copy E2E cases are green
- [x] Board, tasks, and version (if any) are complete in this PR
