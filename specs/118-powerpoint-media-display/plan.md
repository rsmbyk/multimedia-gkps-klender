# Plan 118: Display PowerPoint slides in Preview and projector

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-118
- **Bump:** minor

## Why

PPT/PPTX files can be stored, shared, downloaded, and referenced by Tata Ibadah entries, but their slides cannot yet be displayed. The owner approved the slide-by-slide Preview and projector layout on 2026-10-19. This slice makes those existing entries presentable without replacing their immutable file reference.

## Scope / edges

**In:** Local conversion of a verified PPT/PPTX into a disposable display PDF, Preview and projector slide navigation, fitting, local/offline use, missing and conversion-failure states, conversion cache ownership, and resource cleanup.

**Out:** PowerPoint editing; native animation, transitions, embedded audio/video or narration; uploading/converting on Vercel; changing media identity or transfer policy; Office macros; OBS; a general document conversion service.

## Approach

Keep the original PowerPoint bytes and SHA-256 as the only Media Library identity. Extend the Docker media companion with a bounded, headless LibreOffice Impress conversion path. The companion reads its verified local original, writes a PDF to a private derived cache keyed by source SHA and converter version, and exposes only that derivative to the allowed browser origin. A cache miss or a newly downloaded file can be converted locally; no conversion is required on the cloud server. A derived PDF is never listed, shared, counted as a user file, or treated as a new service-entry reference. Rebuild it if missing, stale, or unreadable, and remove it when its source is deleted.

Reuse the locally bundled PDF.js rendering and page-navigation rules from Spec 117, but label the pages as slides. The conversion is static: no PowerPoint animation, transitions, or embedded playback. A neutral preparing state appears while conversion runs. Conversion errors and unavailable originals use the approved quiet missing-content UI, with a fresh attempt possible after the source or environment is corrected.

The branch is based on the accepted Spec 117 implementation because slide rendering depends on its PDF viewer. Before the implementation PR, reconcile it with current `develop` after the PDF PR lands.

## TDD

- Domain/app: companion tests for exact-SHA lookup, cache key/invalidation, concurrent requests, bounded conversion, failure cleanup, and source deletion; Django tests for one stable service screen and PowerPoint-only Preview metadata.
- Browser E2E: PPT and PPTX examples covering Preview, projector slide boundaries, direct/backward entry, untitled name, missing/corrupt source, conversion failure, and saved offline shell.
- Local runs remain targeted; full browser matrix and database suite run in CI after push.

## Risks

- LibreOffice can render fonts or advanced Office features differently. Document this limit and preserve the original for re-export outside the app.
- Conversion can consume CPU, memory, and temporary disk. Use bounded work, one conversion per source at a time, atomic cache publication, and cleanup of failed output.
- Companions may run different converter versions. Key the derivative by source identity and converter version; never assume a display cache can be transferred with the original.

