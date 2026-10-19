# Tasks 118: Display PowerPoint slides in Preview and projector

- **Status:** In review
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner explicitly accepts this Draft.
- [ ] Reconcile this branch with `develop` after Spec 117 lands; retain the approved preview and Draft.
- [x] Red — targeted tests in `multimedia/test_local_media.py` for verified-source conversion, cache identity, concurrency, invalidation, and failure cleanup.
- [x] Green — add the local companion's converter and private derived-cache endpoint; keep original Media Library identity unchanged.
- [x] Red — targeted `multimedia/web/test_media.py` tests for PowerPoint Preview metadata and one stable projector screen.
- [x] Green — expose only the slide identity needed by Preview/projector and offline saved-screen data.
- [x] Focused browser E2E in `tests/e2e/test_powerpoint_display.py` for Preview, projector boundaries, untitled state, missing/failure, and offline shell; real local conversion test covers both PPT and PPTX.
- [x] Green — reuse local PDF rendering for slides; add UI states and cleanup; preserve other media behavior.
- [x] Run targeted local tests; full suite/browser matrix remains for CI after push.
- [x] Fill final implementation paths in `spec.md` Traceability.
- [x] Move ITEM-118 and board into review; bump VERSION, add changelog, and fill release_version in the implementation branch. Move to Done after merge.
- [ ] Conventional Commit and draft PR stacked on Spec 117, then retarget `develop` after Spec 117 lands.
- [ ] Verify exact-head CI before merge.

## Done when

- [ ] All acceptance scenarios hold.
- [ ] Tests, ITEM/board, version, changelog, and PR evidence land together.
