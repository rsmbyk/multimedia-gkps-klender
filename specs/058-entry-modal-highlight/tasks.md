# Tasks 058: Clear stale service entry highlight after modal dismissal

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner approved the state preview on 2026-10-12
- [x] Write Draft plan, spec, tasks, and ITEM-060; board → Speccing
- [x] Spec Accepted by the project owner on 2026-10-12
- [x] Branch from current `develop` as `fix/058-entry-modal-highlight`; carry only this slice's Draft files to that branch
- [x] Red — reproduced the stale background after closing Preview in the browser test
- [x] Green — refine entry selectors and retain keyboard modal return across save/delete refresh
- [x] Verify hover, keyboard return/navigation, both themes, touch controls, edit refresh, successful deletion, and legacy paths with `python manage.py test tests.e2e.test_tatib_hover.TatibHoverE2ETests`
- [x] Update Traceability with actual validation results
- [x] Set `bump: patch` intent on ITEM and spec
- [x] Set `VERSION` to 1.4.1, changelog section `[1.4.1]`, and ITEM `release_version: 1.4.1` (patch from integration 1.4.0)
- [ ] Conventional Commit and draft PR into `develop` using the repository template
- [ ] ITEM/board → In review with PR link in that same PR
- [ ] Required remote CI green for the exact PR head; complete metadata before authorized squash merge
- [ ] On merge, delete only remote feature branch and keep local branch intact

## Done when

- [x] All acceptance scenarios hold and targeted tests pass
- [ ] Required push/CI checks pass
- [ ] Board, ITEM, tasks, and version metadata are complete in the same PR

The targeted E2E class is green locally. Push/CI and PR metadata remain. Production release/tag follows the repository's owner-triggered Git Flow release process.
