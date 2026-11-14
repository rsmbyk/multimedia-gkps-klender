# Plan 117: Display PDF pages in Preview and projector

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-117
- **Bump:** minor

## Why

The Media Library stores and verifies PDFs, but Tata Ibadah cannot inspect or present their pages. The owner chose page-by-page display after comparing it with scrolling. The PDF must remain one immutable media entry shared across computers.

## Scope / edges

**In:** PDF Preview, projector pages, local verified-byte retrieval, page-boundary navigation, fitting, unavailable states, offline saved-screen support, and cleanup.

**Out:** PPT/PPTX, PDF search/text editing, links/forms/annotations, zoom/pan, printing, continuous scrolling, OBS, cloud streaming, and changes to file identity or download policy.

## Approach

Keep one server-side projector screen for the PDF entry. Fetch its SHA-256 bytes directly from the local companion, never through Django/Vercel. Bundle Mozilla PDF.js and its worker locally; load the verified bytes, read the page count, and render only the currently visible page to canvas. Its official examples show document loading, page lookup, and canvas rendering; it is Apache-2.0 licensed ([examples](https://mozilla.github.io/pdf.js/examples/index.html), [license](https://github.com/mozilla/pdf.js/blob/master/LICENSE)).

Use a transient browser page index inside the projector entry. Plain Next/Previous moves through the pages and crosses to adjacent service screens at the ends. A direct jump starts at page one. Entering from the following service screen by moving backward starts at the PDF's final page. The corner cue displays the inner page count. If unavailable, the PDF occupies one quiet missing-content screen that navigation can cross in one step.

Abort stale fetch/render operations. Destroy the PDF document and release large buffers when Preview closes or the projector leaves the entry. The local PDF.js worker must be present in production and the saved offline shell, with no CDN dependency.

## TDD

- Domain/app tests: multimedia/web/test_media.py and focused projector tests for PDF identity and one stable service screen.
- Browser E2E: tests/e2e/test_pdf_display.py for a real multi-page file, page navigation, direct jumps, offline rendering, missing/corrupt files, and cleanup.

## Risks

- The page count is local and asynchronous, so browser navigation must be safe while loading and must ignore late results after a screen change.
- A large PDF can consume memory or produce oversized canvases. Render one page at a time and cap backing-canvas pixels without cropping its visible page.
- Encrypted or corrupt files may pass signature checks but fail decoding; show unavailable rather than a password prompt or stale page.
