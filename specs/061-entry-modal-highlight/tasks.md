# Tasks 061: Clear stale service entry highlight after modal dismissal

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner approved the state preview on 2026-10-12
- [x] Write Draft plan, spec, tasks, and ITEM-063; board → Speccing
- [x] Spec Accepted by the project owner on 2026-10-12
- [x] Branch started from `develop` as `fix/058-entry-modal-highlight`; Specs 058-060 merged concurrently, so this slice was renumbered to 061 before merge
- [x] Red — reproduced the stale background after closing Preview in the browser test
- [x] Green — refine entry selectors and retain keyboard modal return across save/delete refresh
- [x] Verify hover, keyboard return/navigation, both themes, touch controls, edit refresh, successful deletion, and legacy paths with `python manage.py test tests.e2e.test_tatib_hover.TatibHoverE2ETests`
- [x] Update Traceability with actual validation results
- [x] Set `bump: patch` intent on ITEM and spec
- [x] Set `VERSION` to 1.5.1, changelog section `[1.5.1]`, and ITEM `release_version: 1.5.1` (patch from integration 1.5.0)
- [x] Conventional Commit and draft PR #314 into `develop` using the repository template
- [x] ITEM/board → In review with PR #314 in that same PR
- [x] Remote Fast checks, CI result, and all browser E2E modules passed on synchronized PR code head `d200907` in run `38231116716` (2026-10-12)
- [ ] Merge by squash into `develop`; delete only the remote feature branch and keep the local branch intact

## Done when

- [x] All acceptance scenarios hold and targeted tests pass
- [x] Fast checks and Browser E2E push/CI jobs pass on synchronized PR code head `d200907`
- [x] Board, ITEM, tasks, and version metadata are complete in the same PR

Full Fast checks and every browser E2E module passed on synchronized PR code head `d200907` in run `38231116716`, including the modal-highlight and entry-control suites. Production release/tag follows the repository's owner-triggered Git Flow release process.
