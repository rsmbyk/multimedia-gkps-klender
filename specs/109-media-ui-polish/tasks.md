# Tasks 109: Clarify Media Library controls and align media entry labels

- **Status:** Implemented and included in consolidated PR #359; 148 targeted tests passed, exact-head GitHub CI pending
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner explicitly accepted this Draft on 2026-10-17.
- [x] Create `fix/107-media-ui-polish` from the rebased media feature stack.
- [x] Integrate the accepted offline-entry dependency (Spec 106) and resolve markup against the current `develop` base.
- [x] Add targeted browser assertions for sort icon persistence and label changes, rail pictogram, upload guidance, and titled/untitled/missing service-entry alignment.
- [x] Implement the approved icons, text alignment, and copy with no change to file validation or sorting behavior.
- [x] Run the targeted Media Library E2E class (17 passing) and `git diff --check`.
- [x] Fill spec traceability with actual test and implementation references.
- [x] Set the patch release version in `VERSION`, `CHANGELOG.md`, and ITEM release metadata.
- [ ] Move ITEM-109 to Done and update [`backlog/board.md`](../../backlog/board.md) in consolidated PR #359.
- [x] Include this spec in the conventional-commit history and consolidated PR #359 to `develop`.

## Done when

- [x] All spec acceptance scenarios hold with the offline-entry work included, including light and dark themes and the narrow breakpoint.
- [x] Targeted browser checks pass; no upload or sorting behavior regresses (included in the 148-test consolidated run).
- [x] Board, tasks, and version metadata are complete in consolidated PR #359.
