# Spec: Display image media entries

- **ID:** 114
- **Status:** Accepted
- **Item:** ITEM-114
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [Approved interactive preview](./preview.html) (owner approved 2026-10-18)
- **Bump:** minor

## Intent

Let an operator Preview an Image service entry and present that image directly through the Tata Ibadah projector page. The local Media Library remains the source of bytes. An absent image must be visible to the operator and quiet for the congregation.

## Scope

### In scope

- Image-family service entries detected and stored by the existing Media Library.
- The existing service-entry Preview action and dialog, plus the existing projector sequence and bottom position cue.
- Browser retrieval of the referenced SHA-256 file from the local companion, including disappearance, disconnection, and decode failure.

### Out of scope

- Preview or presentation of audio, video, PDF, PPT, or PPTX contents.
- New image controls such as zoom, pan, rotation, crop, captions, or full-size download.
- A new cloud streaming path or an OBS-specific projection surface.
- Changes to service-entry identity, editability, deduplication, sharing, or automatic download eligibility.

## Domain and display rules

- A media entry whose authoritative `MediaIdentity.family` is Image gains Preview and exactly one image projector screen at its existing position in Tata Ibadah order. Its title, saved filename, type icon, and file reference do not change. Other media families retain the current blank-content behavior and do not gain this image Preview.
- The browser requests only this entry's SHA-256 from the companion's verified `GET /v1/files/<sha>` endpoint. It must not form a path from the filename, read deployment storage, or accept a mismatched file. The companion's exact-origin policy remains in force. A successful verified response is converted to an image-typed Blob object URL for browser decoding; the server and Vercel never proxy image bytes.
- The complete image is visible, preserving aspect ratio. Scaling up or down is allowed; cropping, stretching, rotation, and automatic page scrolling on the projector are not. A landscape, portrait, or square image uses the same fit rule.
- An image is unavailable if the companion is disconnected, the referenced SHA-256 is absent, the response fails, or the browser cannot decode the returned bytes. Do not substitute another file with the same name. A later verified local copy of the same bytes restores the original entry without editing it.
- When an image is unavailable, Preview shows the missing-image icon and `Image unavailable on this computer`. The projector clears the previous content and shows only a very muted, centered missing-image icon in the image area. It shows no filename, error reason, or action to the congregation. Its existing bottom operator position cue remains governed by the current projector behavior.
- An image becoming available or unavailable while Preview/projector is open is reconciled on opening/selecting the entry and on the existing local-library availability update; stale successful or failed requests cannot overwrite a newer selected entry. Do not automatically fetch from R2 merely because the projector opened. Existing date-based automatic/manual downloads operate unchanged.
- Navigating off an image, turning the display off, closing Preview, or leaving the page prevents its bytes from remaining on a visible screen. Release object URLs when no longer needed. The existing projector sequence controls, blank screens, and display-off state keep their semantics.

## UI details

The approved [interactive preview](./preview.html) is the visual reference. Its surrounding Tata Ibadah rail, list panels, stage, and separate projector page represent the existing app layout; this spec changes only the image-specific elements.

- **Service stage:** Keep the existing Image icon, heading/subtitle, entry spacing, and action-button style. Add the same `Preview` control used by previewable Text, Scripture, and Song entries to an Image entry's actions. Its hover, focus-visible, and pressed states match those existing controls; Edit/Delete keep their positions after it. The action is present even when the local file is missing so the operator can inspect its state.
- **Preview position and size:** Reuse the centered native Preview dialog and its header. The header contains the entry title, or saved filename when untitled, at the existing 16px/1.3 semibold style and minimum 52px height. The image variant's width follows the image's decoded aspect ratio and display size rather than the ordinary 44rem cap; the dialog remains within `100vw - 32px` and `100vh - 48px`. Retain 22px body padding and 14px dialog radius. Scale the image to the largest size that fits the available body rectangle while preserving its ratio; never expand the dialog beyond the viewport. Empty space uses the dialog canvas, without a decorative frame or caption.
- **Preview unavailable:** Center a 38×38px missing-image outline icon and the 13px `Image unavailable on this computer` line in a body area at least 280px high. Use the existing muted ink token, not danger red. Keep the header and its file identity visible.
- **Projector image:** Use the existing dark projector canvas (`#171613`) and safe area inset of 32px top/right/left and 64px bottom. Fit and center the image in that rectangle with `object-fit: contain`; no title or filename overlays it. Keep the existing bottom position cue. The normal display-off mode hides the image and the missing icon.
- **Projector unavailable:** Center an 80×80px outline missing-image icon in the image area, color `#3b3933` against the dark canvas. Do not show a message there. Clear the preceding image/text immediately on selecting the missing screen; the cue may still show the current position.
- **Motion and dismissal:** Preview opens with a 210ms opacity/scale/slight-rise morph using `cubic-bezier(.2,.8,.2,1)` and closes with a 170ms reverse morph. Backdrop opacity follows the same durations. Escape and clicking the backdrop close Preview and return focus to its opener using the existing quiet-focus behavior. With reduced motion, open/close is immediate.
- **Responsive/interaction:** At narrow widths the dialog keeps 16px minimum horizontal viewport margin and the image shrinks to fit; no horizontal scroll is required. The image has an accessible name based on the entry's title or filename, while the unavailable state exposes its message to assistive technology. Icon-only projector content is decorative; operator controls and cue retain existing keyboard/accessibility semantics.

## Acceptance scenarios

### Scenario: Preview a local image

- **Given** an Image entry refers to a verified file on this computer
- **When** the operator selects Preview
- **Then** the existing modal opens, names the entry, and displays the complete image at the largest size within the available viewport without distortion or cropping.
- **When** the operator presses Escape or clicks the backdrop
- **Then** the modal closes with the approved morph and focus returns to the Preview control.

### Scenario: Project a local image

- **Given** a service sequence has text, an Image entry, and another entry
- **When** the operator advances to the Image entry
- **Then** exactly one projector screen shows that image fitted in the existing safe area, without an image caption, and the position cue reflects the Image entry.
- **When** the operator advances, reverses, or turns display off
- **Then** the screen follows the existing sequence and visibility controls without leaving the image visible on a different or off screen.

### Scenario: Missing or undecodable local image

- **Given** an Image entry's SHA-256 is absent, its companion cannot be reached, or its verified response fails image decoding
- **When** Preview opens
- **Then** it shows the icon and `Image unavailable on this computer`, while the entry reference remains unchanged.
- **When** the projector selects that entry
- **Then** prior content is cleared and the muted centered missing-image icon appears without text or a filename.
- **When** the exact bytes later become locally available
- **Then** reopening/reselecting the entry shows the image without replacing or editing the service entry.

### Scenario: Other media remain unchanged

- **Given** audio, video, PDF, PPT, and PPTX entries are in the service
- **When** Preview and projector data are built
- **Then** none gains image rendering or image-specific controls, and their established blank projector behavior remains.

### Scenario: Slow or stale request

- **Given** an image request is pending
- **When** the operator moves to a different projector screen or opens another entry before it resolves
- **Then** the old response cannot replace the newly selected content, and its object URL is released when no longer displayed.

## Traceability

- Domain/app tests: `multimedia/web/test_media.py` covers image-only Preview data and projector screen identity/order.
- Browser E2E: `tests/e2e/test_image_display.py` covers available and missing local images, modal dismissal, and projector navigation.
- Implementation: `multimedia/web/reading/views.py`, Tata Ibadah and projector templates, `static/web/media-image.js`, `static/web/preview.js`, `static/web/projector.js`, and focused design styles.

## Owner review points

- Image entries gain a Preview action; other media types remain storage-only in this slice.
- The image variant may be wider than the ordinary 44rem Preview dialog, but never exceeds the viewport margins.
- Missing images use a readable operator state and a barely visible icon on the projector; there is no congregation-facing error text.
