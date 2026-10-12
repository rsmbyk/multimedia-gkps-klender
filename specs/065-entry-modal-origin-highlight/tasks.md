# Tasks 065: Hold the service entry highlight while its modal is open

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner approved the state preview on 2026-10-12
- [x] Write Draft plan, spec, tasks, and ITEM-068; board → Speccing
- [x] Spec Accepted by the project owner on 2026-10-12
- [x] Branch started from `develop` as `fix/065-entry-modal-origin-highlight`
- [x] Red — browser tests show the origin entry losing its fill and controls while its modal is open
- [x] Green — `is-modal-origin` CSS state, marked on open and released on close in `preview.js` and `entries.js`
- [x] Verify Preview/Edit/Delete by pointer, keyboard open/close, only-origin held, legacy rows, and spec 061 after-close behaviour with `python manage.py test tests.e2e.test_tatib_hover.TatibHoverE2ETests`
- [x] Update Traceability with actual validation results
- [x] Set `VERSION` to 1.6.3, changelog section `[1.6.3]`, and ITEM `release_version: 1.6.3` (patch from integration 1.6.2)
- [ ] Conventional Commit and draft PR into `develop` using the repository template
- [ ] ITEM/board → In review with the PR in that same PR
- [ ] Merge by squash into `develop`; delete only the remote feature branch and keep the local branch intact

## Done when

- [x] All acceptance scenarios hold and targeted tests pass
- [ ] Fast checks and Browser E2E push/CI jobs pass
- [ ] Board, ITEM, tasks, and version metadata are complete in the same PR
