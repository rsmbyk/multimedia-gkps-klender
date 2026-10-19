# Spec: Display PDF pages in Preview and projector

- **ID:** 117
- **Status:** Draft
- **Item:** ITEM-117
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [Interactive comparison](./preview.html), Page by page selected by owner on 2026-10-19
- **Bump:** minor

## Intent

An operator can inspect the exact PDF referenced by a Tata Ibadah entry and project its pages one at a time. The congregation sees the complete page; the operator's existing navigation moves through the document and onward through the service. A missing file cannot substitute a same-name document or leave an earlier screen visible.

## Scope

### In scope

- PDF-family media entries already stored under immutable SHA-256 references.
- The existing Preview dialog, projector, service-order navigation, corner cue, and offline saved-screen renderer.
- Direct local-companion retrieval, page rendering, unavailable states, and cleanup.

### Out of scope

- PPT/PPTX display; changes to Image/Audio/Video; PDF editing, selection, search, hyperlinks, annotations, forms, zoom, pan, print, continuous scroll, and thumbnails.
- Upload, deduplication, identity, sharing, download-policy, or OBS changes.

## Domain and navigation rules

- The authoritative media family must be PDF. A PDF gains Preview and one server-side projector screen at its current entry position. Its title, filename, order, and SHA-256 remain unchanged. Other media families receive no PDF controls.
- The browser fetches only this SHA-256 from the companion's verified local file endpoint. It never uses a filename path, a same-name fallback, Django/Vercel proxying, or a new R2 download merely because Preview or projector opened.
- Locally bundled PDF.js decodes the verified bytes and renders one selected page to canvas. Honor each page's own aspect ratio and rotation; fit the whole page without cropping. Do not activate PDF links, forms, scripts, or other interactive content.
- Preview starts on page one, has Previous/Next bounded to the document, and has a page count. Closing and reopening resets it. Preview's page index is independent from the projector.
- Projector plain Previous/Next and equivalent pointer/keyboard controls step within the PDF while another page exists. Next from the final page enters the following service screen; Previous from page one enters the preceding screen. Entering the PDF from before starts on page one; entering by stepping backward from after starts on the final page once loaded. A direct service-entry jump starts on page one. Existing Shift/Ctrl entry/bait navigation bypasses intermediate pages.
- The PDF remains one service entry and one global screen identity. Its inner page index is browser-local and transient; the corner cue shows the entry and page N/M. The service-entry list contains one PDF row.
- While a PDF is loading, show a neutral pending state and let the operator navigate away. A late result cannot replace another page/entry or restore content after display-off.
- A disconnected companion, missing SHA, failed fetch, zero-page, encrypted, corrupt, or unrenderable PDF is unavailable. Preview shows a PDF-specific icon and “PDF unavailable on this computer.” The projector clears prior content and shows only a very muted PDF-specific missing icon, without filename or text. An unavailable PDF is one navigable screen.
- Restoring the exact bytes makes the original entry usable on a new open/selection. The existing service-date download rules remain the only automatic acquisition trigger.
- Saved offline projector data retains the PDF SHA so locally available pages work even when Django is unreachable. Release document, worker-related tasks, canvases, and buffers when no longer needed. Cap canvas backing pixels while maintaining full CSS fit.

## UI details

The Page by page mode of [the comparison preview](./preview.html) is the visual reference; its Scrollable toggle and sample pages are demonstration controls.

- **Service entry:** Keep the PDF icon, title or filename, existing subtitle, spacing, and Edit/Delete actions. Add Preview with the established action button, hover, focus-visible, and pressed styles. Preview remains available when the local file is missing.
- **Preview:** Reuse the 210 ms open/170 ms close morph, 14 px radius, and Escape/backdrop dismissal. Show the 16 px semibold header only for a titled entry. Width is at most 920 px and viewport width minus 32 px; height is at most viewport height minus 48 px. Use 22 px body padding, reduced to 16 px on narrow screens. Center one complete page on a neutral canvas. Below it, use a 42 px control row with 32 px square Previous/Next buttons and a 12 px muted N / M label. Disable the appropriate button at each bound; modal Left/Right also turns pages.
- **Projector:** Preserve the dark #171613 canvas and 32 px top/side, 64 px bottom safe inset. Center the entire PDF page, without congregation-facing filename or page buttons. Existing navigation controls turn pages. The corner cue shows page N/M beside the entry label. A page swap uses the existing quiet screen morph or a 160–260 ms fade.
- **Unavailable:** Center a 38 × 38 px PDF-specific missing icon and 13 px muted message in a Preview body at least 270 px high. The projector uses an 80 × 80 px PDF-specific missing outline in #3b3933, without text.
- **Responsive and accessible:** Shrink page and dialog to keep 16 px minimum viewport margins and no horizontal scroll. Announce page N of M and unavailability to assistive technology. Keep the projector icon decorative. Reduced-motion disables page transition animation.

## Acceptance scenarios

### Preview a multi-page PDF

- **Given** a verified three-page PDF exists locally
- **When** the operator opens Preview
- **Then** page one fits and the controls read 1 / 3.
- **When** Previous/Next or modal Left/Right is used
- **Then** one page changes at a time, bounds disable the relevant control, and the service entry stays selected.
- **When** Preview closes and reopens
- **Then** it starts on page one and prior asynchronous work cannot appear.

### Project through pages and adjacent entries

- **Given** a service has an entry before, a three-page PDF, and an entry after
- **When** the operator advances into and through the PDF
- **Then** pages one, two, and three appear in order, with a page N/3 corner cue; the next advance enters the following service screen.
- **When** the operator steps back from that following screen
- **Then** page three appears first, followed by pages two and one, then the preceding screen.
- **When** the operator directly jumps to the PDF
- **Then** page one appears.

### Missing or unreadable PDF

- **Given** the companion is unavailable, the exact SHA is absent, or decoding/rendering fails
- **When** Preview opens or projector selects that entry
- **Then** the operator gets the unavailable message and the projector shows only the quiet PDF icon, with previous content cleared.
- **When** the exact bytes later return
- **Then** a fresh open/selection renders them without changing the entry reference.

### Navigation, offline, and other media

- **Given** a page read/render is pending
- **When** the operator moves to another entry or turns display off
- **Then** the late page cannot replace the new/off screen and resources are released.
- **Given** the projector shell is saved and Django is unreachable
- **When** the local companion has the PDF
- **Then** the PDF pages still render and navigate.
- **Given** other media entries are present
- **When** the service renders
- **Then** their established behavior is unchanged.

## Traceability

- Domain/app tests: multimedia/web/test_media.py and focused projector tests.
- Browser E2E: tests/e2e/test_pdf_display.py.
- Implementation candidates: multimedia/web/reading/views.py, reading/projector templates, static/web/preview.js, static/web/projector.js, static/web/offline-render.js, a focused PDF renderer, local PDF.js assets, and focused styles.

## Owner review points

- Page-by-page navigation happens inside one service entry; a boundary move continues through the Tata Ibadah.
- Preview starts at page one and has no zoom or continuous scrolling.
- Missing/unreadable PDFs remain quiet on the projector and do not trigger a new transfer solely because opened.
