# Tasks 059: Distinct song label typography

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Spec Accepted by the project owner on 2026-10-12 (approved preview and Draft 004; renumbered 059 on current develop)
- [x] Identify the current sidebar and record renderer/style paths
- [x] Branch from the current Spec 057 line using `fix/059-song-label-typography`
- [x] Add Playwright acceptance coverage in `tests/e2e/test_song_label_typography.py`
- [x] Implement separate reference, title, and lyric verse styles in the renderer/styles
- [x] Verify normal, hover, selected, missing-reference, long-title, narrow-width, and theme contrast cases in Playwright
- [x] Run focused E2E and service-entry regressions; 2 browser E2E cases and 99 service-entry tests pass on PostgreSQL
- [x] Fill implementation traceability in spec.md
- [x] Set patch bump on ITEM and spec
- [x] Update VERSION to 1.3.24, CHANGELOG, and ITEM release_version in this PR
- [x] Update ITEM and board in the same PR
- [ ] Conventional Commit with Codex attribution and draft PR to develop using the repository template

## Done when

- [ ] All acceptance scenarios hold
- [ ] Named tests pass and visual inspection confirms the hierarchy
- [ ] Board, tasks, and version metadata are complete in the implementation PR
