# Plan 116: Play Video media entries

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-116
- **Bump:** minor

## Why

The Media Library can store verified Video files, but a Video service entry still cannot be inspected or presented. Operators need to check the exact local file and present it at its place in the Tata Ibadah sequence. Playback must remain under operator control, and a missing file must not leave old media on screen.

## Scope / edges

**In:** Video-family service entries; the existing Preview dialog and projector sequence; local verified file retrieval; manual playback, pause, seek, fullscreen playback, idle controls, contextual keyboard behavior and shortcut-sheet documentation, and missing/undecodable states.

**Out:** PDF and slide rendering, OBS sources, upload/signature changes, transcoding, captions, playlists, looping, audio controls, Cloudflare/R2 retrieval changes, and replacing a service entry's file reference.

## Approach

Use the entry's authoritative `MediaIdentity` and SHA-256 reference. Retrieve the selected file directly from the local companion's verified file endpoint, create a Video-typed Blob URL, and let the browser's video element decode and play it. Django/Vercel must not proxy media bytes. Release object URLs and stop playback on navigation, display-off, Preview dismissal, and page exit; guard async responses so an old selection cannot replace the current screen.

Projector playback starts only after an operator action. A Play action requests fullscreen on the video stage and starts playback. Pause returns to the normal projector view; playback ending, leaving the entry, turning the display off, or exiting fullscreen with Escape also returns to the normal view. While a Video is playing fullscreen, arrow navigation is suppressed. Space toggles Video playback and the projector shortcut sheet documents contextual Audio/Video playback beside Show/Hide Words. Only fullscreen playback shows the seek bar and timer; after two seconds without operator input they hide until activity resumes.

If browser fullscreen is unavailable or denied, playback continues in the normal projector area with the same center Play/Pause control and idle behavior. The fullscreen seek bar/timer remain hidden, and ordinary projector navigation stays available.

## TDD

- **Domain/app tests:** `multimedia/web/test_media.py` — Video-only Preview metadata and exactly one Video projector screen at the original service position, with other media families unchanged.
- **E2E:** `tests/e2e/test_video_display.py::VideoDisplayE2ETests` — real local video playback, modal controls and dismissal, fullscreen entry/exit, pause/end/navigation/display-off cleanup, keyboard behavior, idle controls, missing/undecodable files, and landscape/portrait fitting.

## Risks

- A file classified as Video by signature may use a codec the current browser cannot decode. Show the unavailable state on load, decode, or playback failure; never substitute a same-name file.
- Fullscreen requires a user gesture and may be blocked by the browser. Keep playback usable in the normal projector area when the request fails.
- Local file retrieval must stay between the browser and companion; do not route large media through Django or Vercel.
