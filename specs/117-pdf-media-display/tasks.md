# Tasks 117: Display PDF pages in Preview and projector

- **Status:** In review
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner explicitly Accepts the Draft spec.
- [x] Branch from current develop and prepare the page-by-page comparison preview.
- [x] Red — targeted Django tests in multimedia/web/test_media.py for PDF-only Preview metadata and one stable projector screen.
- [x] Green — emit PDF identity without routing bytes through Django.
- [x] Red — focused browser E2E in tests/e2e/test_pdf_display.py for real multi-page rendering, fitting, boundaries, jumps, and missing/corrupt files.
- [x] Green — bundle local PDF.js and worker; retrieve verified SHA bytes; render/cancel/release one page at a time in Preview and projector.
- [x] Preserve PDF identity in the saved offline-screen renderer and verify navigation while Django is unreachable.
- [x] Run targeted Django tests and one focused browser E2E class locally; full suite and browser matrix run in CI after push.
- [x] Fill Traceability in spec.md with final paths.
- [ ] In the same implementation PR, move ITEM-117 and board through review to Done, bump VERSION once, add changelog, and fill release_version.
- [x] Conventional Commit and draft PR to develop linking this spec.
- [ ] Verify exact-head CI before merge.

## Done when

- [ ] All acceptance scenarios hold.
- [ ] Tests, board/ITEM, version, changelog, and PR evidence land together.
