# Tasks 066: Always show a song entry's verses on the Tata Ibadah stage

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner OKed the approach in chat on 2026-10-12 (no new look; reuses spec 054's style)
- [x] Write Draft plan, spec, tasks, and ITEM-069; board → Speccing
- [x] Branch started from `develop` as `fix/066-stage-song-verse-line`
- [x] Spec Accepted by the project owner on 2026-10-12
- [x] Red — full-selection, verse-added, and stage/sidebar agreement tests fail against the spec 054 rule
- [x] Green — `_tatib_stage` builds one verse string for the stage `subtitle` and the sidebar `verse_line`
- [x] Verify with targeted `multimedia.web.tests` and `tests.e2e.test_entry_preview`
- [x] Update Traceability with actual validation results
- [x] Set `VERSION` to 1.6.4, changelog section `[1.6.4]`, and ITEM `release_version: 1.6.4` (patch from integration 1.6.3)
- [x] Conventional Commit and draft PR #319 into `develop` using the repository template
- [x] ITEM/board → In review with the PR link in that same PR
- [ ] Merge by squash into `develop`; delete only the remote feature branch and keep the local branch intact

## Done when

- [x] All acceptance scenarios hold and targeted tests pass
- [ ] Fast checks and Browser E2E push/CI jobs pass
- [x] Board, ITEM, tasks, and version metadata are complete in the same PR
