# Tasks 107: Clarify Media Library controls and align media entry labels

- **Status:** Accepted (2026-10-17)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner explicitly accepted this Draft on 2026-10-17.
- [x] Create `fix/107-media-ui-polish` from the rebased media feature stack.
- [ ] Rebase after the dependent media feature and offline-entry branches integrate, resolving any markup changes.
- [x] Add targeted browser assertions for sort icon persistence and label changes, rail pictogram, upload guidance, and titled/untitled/missing service-entry alignment.
- [x] Implement the approved icons, text alignment, and copy with no change to file validation or sorting behavior.
- [x] Run the targeted Media Library E2E class (17 passing) and `git diff --check`.
- [x] Fill spec traceability with actual test and implementation references.
- [ ] Set the eventual patch version from the integration line in this PR: `VERSION`, `CHANGELOG.md`, and ITEM `release_version`.
- [ ] Move ITEM-107 through In review to Done and update [`backlog/board.md`](../../backlog/board.md) in the same PR.
- [ ] Conventional Commit with Codex trailer and open a draft PR against `develop` linking this spec.

## Done when

- [ ] All spec acceptance scenarios hold after rebasing onto the offline-entry work, including light and dark themes and the narrow breakpoint.
- [ ] Targeted browser checks pass; no upload or sorting behavior regresses.
- [ ] Board, tasks, and version metadata are complete in the same PR.
