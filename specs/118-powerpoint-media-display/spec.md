# Spec: Display PowerPoint slides in Preview and projector

- **ID:** 118
- **Status:** Draft
- **Item:** ITEM-118
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [Approved interactive preview](./preview.html), accepted by owner on 2026-10-19
- **Bump:** minor

## Intent

An operator can inspect and present each slide of a locally available PPT or PPTX referenced by a Tata Ibadah entry. The original file remains identifiable and shareable by its existing SHA-256. Missing or unreadable presentations cannot leave an earlier screen on the projector.

## Scope

### In scope

- Existing `slides`-family media identities, Tata Ibadah Preview, projector, corner cue, and saved offline projector shell.
- Local companion conversion to a static PDF derivative, local cache, retrieval, error states, and cleanup.
- The existing slide file icon, title/filename fallback, and entry position.

### Out of scope

- Editing presentations; transitions, builds, animation, embedded audio/video, narration, notes, or speaker view.
- Making a PPT/PPTX directly renderable by the browser, cloud-side conversion, a second media identity for the derivative, new upload/sharing rules, or OBS changes.

## Domain rules

- Only an existing `slides`-family entry gets PowerPoint Preview and projector display. Its source SHA-256, original filename, title, order, and relationship to the Media Library do not change. It remains one service entry and one server-side projector screen.
- The browser requests the exact source SHA from the local companion. The companion verifies the source bytes against that SHA before conversion. No filename lookup or same-name fallback is allowed. The original file is not sent through Django or Vercel merely to display it.
- The companion converts the verified PPT/PPTX with headless LibreOffice Impress to a PDF derivative. It stores the derivative privately in its own Docker volume, keyed by the original SHA plus converter version. The derivative is not a Media Library file: it is absent from file counts, sharing, transfers, deduplication, and service references. It can be deleted and regenerated without changing the source.
- Concurrent requests for one source share one conversion. Publish a derivative only after a successful complete conversion and validation that the output is a readable, nonempty PDF. Failed or interrupted output is removed. Conversion work has bounded time, memory, and temporary storage; the implementation records and tests the chosen limits.
- A cache hit can be used immediately. A cache miss begins local preparation; while waiting, Preview shows a neutral preparing state and the projector clears prior content. Navigating away, turning display off, or closing Preview cancels that caller's presentation, and any later result must not replace the current entry. The companion may finish a shared conversion for its cache.
- Once prepared, locally bundled PDF.js renders one whole slide at a time, honoring the source slide's aspect ratio without cropping. Each slide is a static result of the conversion. The app does not execute Office macros or PDF links, forms, scripts, or other active content.
- Preview starts at slide one with Previous, N / M, and Next. Closing and reopening resets to slide one. Modal Left/Right turns slides; Escape and backdrop close it. The Preview index is separate from the projector index.
- In the projector, plain Previous/Next and equivalent pointer/keyboard controls move through slides before crossing service-screen boundaries. Entering from before starts on slide one; stepping backward into the entry from after starts on its final slide; a direct entry jump starts on slide one. Existing Shift/Ctrl entry-level navigation bypasses intermediate slides. The corner cue shows slide N/M. The service sidebar still has one row for the entry.
- A missing source, disconnected companion, unsupported/corrupt presentation, conversion failure, or unreadable derivative is unavailable. Preview shows the PowerPoint-specific missing icon and “PowerPoint unavailable on this computer.” The projector shows only the muted PowerPoint-specific icon, no filename or message, and no stale previous content. An unavailable presentation is one navigable screen.
- Restoring the same source bytes or repairing the conversion environment allows a fresh open to retry. Opening Preview or projector does not independently trigger an R2 download; existing service-date transfer rules continue to decide automatic downloads.
- A saved offline projector shell can ask the same local companion to prepare and render slides without Django. Source deletion removes its derived cache. Obsolete converter-version caches are reclaimable. No derived PDF is uploaded to R2.

## UI details

The [approved preview](./preview.html) is the visual reference. Its top-right surface, example, and theme controls are demonstration controls only.

- **Service entry:** Keep the existing 43 × 43 px PowerPoint icon block, 17 px title or filename, 12 px subtitle, 22 × 20 px row padding, and established Edit/Delete buttons. Add Preview with the same 12 px action-button style and existing hover/focus states. A missing original uses the established danger tint on the file icon.
- **Preview:** Reuse the 210 ms opening and 170 ms closing modal morph, 14 px radius, 52 px title band, 22 px body side padding, and Escape/backdrop dismissal. Show the entry title, or the original filename for an untitled entry. The dialog follows the converted slide's dimensions, with at least 16 px side and 24 px vertical viewport margins; sample slide is 16:9, but actual presentation aspect ratios must be honored. Center the complete slide, then center the Previous / N / M / Next controls vertically in the 74 px bottom band. Buttons are 32 px square, outlined, and visibly hover/focus; boundary buttons are disabled. Page count is 12 px muted text. The dialog smoothly resizes if slide geometry changes.
- **Projector:** Keep the dark `#171613` canvas and 32 px top/side, 64 px bottom safe area. Fit and center the entire static slide. No congregation-facing filename or slide buttons. Existing navigation turns slides; the corner cue shows N/M at its usual position. Use the existing quiet screen transition or a 160–260 ms slide fade.
- **Preparing and unavailable:** Preparing does not show old content or enable an incomplete page count. Unavailable Preview uses a centered 38 × 38 px PowerPoint-specific outline and 13 px muted message in a body at least 270 px high. The projector uses an 80 × 80 px outline in `#3b3933`, without text; hide the corner cue while unavailable.
- **Responsive/accessibility:** Fit slides and dialog within the viewport without horizontal scrolling. Announce slide N of M and unavailability to assistive technology. Make the projector icon decorative. Reduced-motion disables page and modal animation. Theme colors follow existing tokens; the projector remains dark.

## Acceptance scenarios

### Display an available PPT or PPTX

- **Given** a service entry references a verified three-slide PPT or PPTX on this computer
- **When** the operator opens Preview
- **Then** the original title or filename appears above a complete first slide and controls read 1 / 3.
- **When** the operator uses Previous/Next or modal Left/Right
- **Then** exactly one slide changes, controls stop at the ends, and the dialog fits the slide without cropping.
- **When** Preview closes and reopens
- **Then** it starts on slide one.

### Project through the service

- **Given** the service has an entry before and after the presentation
- **When** the operator advances into and through it
- **Then** all slides appear in order, the corner cue shows N/3, and the next step after the final slide enters the following screen.
- **When** the operator steps backward into it from the following screen
- **Then** the final slide appears first; a direct entry jump starts at slide one.
- **When** Shift/Ctrl entry navigation is used
- **Then** it can cross the entire presentation according to the existing shortcut hierarchy.

### Prepare once and preserve identity

- **Given** a verified original has no current derived PDF
- **When** Preview and projector request it concurrently
- **Then** the companion performs one bounded conversion, both callers can use its completed PDF, and the library still shows one original file with the same SHA and filename.
- **When** the original is deleted or the converter version changes
- **Then** the old derivative cannot be served as the current source; a present source can regenerate its display copy.

### Missing or failed conversion

- **Given** the original is missing, corrupt, or conversion fails
- **When** the entry is previewed or projected
- **Then** Preview shows the PowerPoint-specific unavailable state and the projector shows only its quiet icon, with prior content cleared.
- **When** the exact original later returns or the conversion fault is corrected
- **Then** a fresh open can render it without changing the service entry or fetching a same-name substitute.

### Offline and other media

- **Given** the saved projector shell is open without Django and the verified original is local
- **When** it selects the presentation
- **Then** the companion can prepare and provide slides for the same navigation flow.
- **Given** an image, audio, video, or PDF entry is selected
- **When** its Preview or projector runs
- **Then** its existing behavior is unchanged.

## Traceability

- Domain/app tests: `multimedia/test_local_media.py`, `multimedia/web/test_media.py`.
- Browser E2E: new focused `tests/e2e/test_powerpoint_display.py`.
- Likely implementation: `multimedia/local_media.py`, local Docker image/dependencies, `multimedia/web/reading/views.py`, relevant reading templates, `static/web/{media-pdf,preview,projector,offline-render,offline-library,service-worker}.js`, and component/projector styles. Final paths are recorded during implementation.

## Owner review points

- Slides are static. Animation, transitions, and embedded audio/video will not play.
- The original PPT/PPTX is kept; the local display copy is disposable and never shared online.
- The companion image grows because it must include a presentation converter.

