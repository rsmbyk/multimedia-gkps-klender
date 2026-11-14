# Plan 114: Display image media entries

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-114
- **Bump:** minor

## Why

The local Media Library and temporary handoff now make image files available on an operator computer, but an image entry still has no content in Preview or on the projector. An operator needs to inspect the actual image and show it to the congregation from the existing service sequence.

## Scope / edges

**In:** Image-entry Preview; one projector screen per image entry; fit without cropping; missing/unavailable/decode-failure states; local companion byte retrieval; existing screen navigation and display-off behavior. The [approved visual preview](./preview.html) governs the look.

**Out:** Audio/video playback, PDF display, PPT/PPTX rendering, OBS-specific sources, cloud streaming, image editing, captions/overlays, and changes to Media Library import or sharing.

## Approach

Keep the existing SHA-256 service reference and local companion as the sole image-byte source. The Django server emits image identity and family in the existing stage and projector data, never the bytes. The browser requests a verified local file only for an image it is about to show, wraps the response in a validated image Blob, and releases the object URL when no longer needed. The companion's exact-origin policy continues to apply. A local miss, disconnected companion, or failed image decode resolves to the approved unavailable state without falling back to the cloud or showing the previous screen.

Use the existing Preview dialog, but size its image variant to the image's aspect ratio within the viewport. Place each image in one projector screen inside the existing `32px 32px 64px` safe area, preserving the current keyboard/mouse navigation and bottom position cue. Opening/closing Preview gets the short morph; Escape and backdrop dismiss it. The projector icon for a missing image is intentionally low contrast.

## TDD

- Domain/app tests: projector screen construction, ordering, image-only scope, and safe identity metadata.
- Targeted browser E2E: image Preview and projector, aspect fitting, local miss and late availability, navigation/display-off, keyboard/modal behavior, light/dark Preview and narrow layout.

## Risks

- The current companion serves verified bytes as `application/octet-stream` with `nosniff`. Rendering must use an image-typed Blob object URL after the verified response; pointing `<img>` straight at the endpoint may be blocked by the browser.
- A 200 MB image can be expensive to decode. Load only the current image, release Blob URLs promptly, and leave neighboring screens blank until selected.
- Browser-local access can fail even when the server's image reference exists. The screen must make that failure local and must not leave prior projector content visible.
