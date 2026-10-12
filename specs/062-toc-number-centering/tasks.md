# Tasks 062: Center entry numbers vertically in the Tata Ibadah contents list

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner approved the alignment preview on 2026-10-12
- [x] Write Draft plan, spec, tasks, and ITEM-064; board → Speccing
- [x] Spec Accepted by the project owner on 2026-10-12
- [x] Branch from `develop` as `chore/062-toc-number-centering`
- [x] Red — domain/app tests: N/A (CSS only)
- [x] Red — E2E `tests/e2e/test_toc_number_centering.py` (`TocNumberCenteringE2ETests`):
      number/row centers for one-, two-, and three-line rows, text position, 404px
      and 280px widths, hover/selected, both themes, drag copy, songbook list unchanged
- [x] Green — `static/styles/design/components.css`: `align-self: center` on
      `.songrow__c` scoped to `:root[data-section="tatib"] #chList` and `.reorder__ghost`
- [x] Green — targeted E2E passes locally
- [x] Fill Traceability in `./spec.md`
- [x] Set `VERSION` to 1.5.2, changelog section `[1.5.2]`, and ITEM `release_version: 1.5.2` (patch from integration 1.5.1)
- [x] Conventional Commit + draft PR #316 into `develop` linking `./spec.md`
- [x] ITEM/board → In review with PR #316 in that same PR
- [x] All 15 browser E2E modules passed on code head `7a046a9` in run `38238514752`; Fast checks and `CI result` passed on `de3e0f2` in run `38238519022` (2026-10-12)
- [ ] Merge by squash into `develop`; delete only the remote feature branch and keep the local branch intact

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] `TocNumberCenteringE2ETests` is green
- [x] Board, tasks, and version are complete in this PR
