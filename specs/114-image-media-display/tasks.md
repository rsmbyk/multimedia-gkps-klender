# Tasks 114: Display image media entries

- **Status:** In review
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Draft explicitly Accepted by the project owner
- [x] Branch from current `develop`: `feat/114-image-media-display`
- [x] Red — targeted Django tests in `multimedia/web/test_media.py` for image-only stage and projector screen construction, ordering, and missing identity.
- [x] Green — emit image-safe metadata and one image screen through `multimedia/web/reading/views.py` and the existing templates.
- [x] Red — focused browser E2E class under `tests/e2e/` for available/missing Preview, projector fit/sequence, Escape, backdrop, and narrow dark layout. Stale request handling is enforced by abort and token guards in both browser surfaces.
- [x] Green — retrieve verified local bytes and render/release image Blob URLs in `static/web/preview.js` and `static/web/projector.js`; apply focused image styles.
- [x] Verify targeted Django tests and single E2E class locally, including light/dark and narrow view; let CI run the full suite after push.
- [x] Fill traceability with final test paths and implementation files.
- [x] In the same implementation PR, update ITEM-114 and the board to In review, set the minor version bump and changelog/release_version, and check completed tasks before merge.
- [ ] Conventional Commit and draft PR to `develop` linking this spec.

## Done when

- [x] All acceptance scenarios in [spec.md](./spec.md) hold.
- [x] The owner has Accepted this Draft before implementation.
- [ ] Tests, board/ITEM, version, changelog, and PR evidence land together.
