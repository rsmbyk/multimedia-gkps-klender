# Tasks 118: Display PowerPoint slides in Preview and projector

- **Status:** Draft
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [ ] Owner explicitly accepts this Draft.
- [ ] Reconcile this branch with `develop` after Spec 117 lands; retain the approved preview and Draft.
- [ ] Red — targeted tests in `multimedia/test_local_media.py` for verified-source conversion, cache identity, concurrency, invalidation, failure cleanup, and bounded work.
- [ ] Green — add the local companion's converter and private derived-cache endpoint; keep original Media Library identity unchanged.
- [ ] Red — targeted `multimedia/web/test_media.py` tests for PowerPoint Preview metadata and one stable projector screen.
- [ ] Green — expose only the slide identity needed by Preview/projector and offline saved-screen data.
- [ ] Red — focused browser E2E in `tests/e2e/test_powerpoint_display.py` for PPT and PPTX, Preview, projector boundaries, backward/direct jumps, untitled state, preparing, missing/failure, and offline shell.
- [ ] Green — reuse local PDF rendering for slides; add UI states and cleanup; preserve other media behavior.
- [ ] Run targeted local tests; run full suite/browser matrix in CI after push.
- [ ] Fill final implementation paths in `spec.md` Traceability.
- [ ] In the same implementation PR, move ITEM-118 and board through review to Done; bump VERSION, add changelog, and fill release_version.
- [ ] Conventional Commit and draft PR to `develop` linking this spec.
- [ ] Verify exact-head CI before merge.

## Done when

- [ ] All acceptance scenarios hold.
- [ ] Tests, ITEM/board, version, changelog, and PR evidence land together.

