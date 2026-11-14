# Plan 115: Play audio media entries

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-115
- **Bump:** minor

## Why

The Media Library can store and transfer Audio files, but an Audio service entry still has no usable Preview or projector content. Operators need to check the actual recording before a service and start or pause it at the right point without losing the established projector navigation keys.

## Scope / edges

**In:** Audio-entry Preview and one projector screen per Audio entry; play/pause, elapsed/total time, pointer seek and drag; local verified byte retrieval; missing and decode-failure states; projector idle treatment; playback lifecycle across navigation and display-off; contextual Space shortcut and projector shortcuts sheet. The owner-approved [interactive preview](./preview.html) governs the visual design.

**Out:** Video/PDF/slides, playlists, autoplay, looping, volume UI, waveform, changing the saved file reference, OBS sources, cloud streaming, and replacing the existing non-audio projector Space action.

## Approach

Keep the existing SHA-256 service reference and local companion as the byte source. Use the browser's media engine to decode and play the verified local audio; do not proxy bytes through Django/Vercel. Load only the selected Audio entry, release local object URLs when no longer needed, and guard asynchronous loads against navigation to another entry. Match the approved Preview player and centered projector transport. A local miss or decode failure shows the unavailable state without advancing the service automatically.

The projector's existing screen navigation continues to own arrows and service-entry movement. On an Audio entry, Space plays or pauses instead of toggling words; non-Audio screens retain their Space behavior. Update the projector shortcuts sheet to explain that context. Pausing or leaving an entry must not leave audio audible behind another screen.

## TDD

- Domain/app tests: Audio-only Preview metadata, screen identity/order, and no change to other media families.
- Targeted browser E2E: actual local audio Preview and projector playback, time/seek, title and untitled states, Space context, keyboard navigation, reset on return, missing/decode failures, idle/paused states, and modal behavior. Use the repository's existing focused test harness and let CI run the full suite.

## Risks

- The companion returns verified bytes as `application/octet-stream` with `nosniff`; use a Blob with the inspected Audio MIME type before passing an object URL to the browser's audio decoder.
- A file may be valid Audio by signature but unsupported by the current browser codec. Treat playback/decode failure as unavailable rather than claiming it will play.
- The existing projector binds Space to Show/Hide Words and overlays can own keyboard input. The Audio override must run only for the active, available Audio entry when no overlay or text input owns the key.
- Avoid loading large Audio files through the app server; revoke object URLs and stop playback on navigation, display-off, modal dismissal, and page unload.
