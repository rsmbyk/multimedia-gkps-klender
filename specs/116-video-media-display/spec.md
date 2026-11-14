# Spec: Display Video media entries

- **ID:** 116
- **Status:** Accepted (owner, 2026-10-19)
- **Item:** ITEM-116
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [Owner-approved interactive preview](./preview.html) (2026-10-19)
- **Bump:** minor

## Intent

Let an operator inspect a locally available Video service entry and present that exact file from its position in the Tata Ibadah projector sequence. Playback starts manually, uses fullscreen for the active projector video when the browser allows it, and stops cleanly when the operator pauses or leaves the entry.

## Scope

### In scope

- Video-family service entries already registered in the Media Library with immutable SHA-256 references.
- The Tata Ibadah service-entry Preview action and existing projector sequence, position cue, and display-off behavior.
- Local companion retrieval, browser video decoding, Preview and projector playback, seeking, fullscreen transitions, idle controls, and unavailable states.

### Out of scope

- Image behavior changes; audio behavior changes; PDF, PPT, or PPTX rendering; OBS projection; upload, identity, deduplication, cloud-sharing, or date-based download-policy changes; transcoding; captions; playlists; looping; and changing an entry's saved file reference.

## Domain rules

- `MediaIdentity.family == Video` is authoritative. A Video entry receives Video Preview and one Video projector screen at its current service-order position. Its title, canonical filename, inspected family, and SHA-256 reference remain unchanged. Other media families do not receive Video controls.
- Fetch only the entry's SHA-256 from the companion's verified `GET /v1/files/<sha>` endpoint. Never construct a path from the filename, read deployment storage, or substitute a same-name file. Create a Blob URL using the inspected Video MIME type; Django and Vercel never proxy the media bytes.
- Opening Preview or selecting a projector Video entry does not autoplay. Preview controls let the operator start, pause, and seek the actual local video. Reopening Preview starts paused at the beginning.
- Starting Video from the projector requests fullscreen on the Video stage and starts playback from the operator gesture. If fullscreen is unsupported or denied, continue playback in the normal projector safe area. Do not fail playback solely because fullscreen is unavailable.
- Pausing or ending playback exits fullscreen and returns to the normal projector view. Exiting fullscreen with Escape pauses playback and returns to the normal view. Leaving the Video entry, turning the display off, closing/leaving the page, or changing to another surface stops the video and resets it to `0:00`.
- Space toggles Video playback in Preview and on the selected projector Video entry. While Video is actively playing in fullscreen, projector left/right screen-navigation shortcuts are prevented from changing the service entry. When fullscreen has exited or playback has paused, the existing projector navigation works normally. On Audio entries, the existing Audio Space behavior remains; on all other projector entries, Space retains Show/Hide Words.
- In fullscreen, only the seek bar and elapsed/total timer are shown as controls; the center play/pause button and service cue are not displayed. The seek bar accepts pointer click and drag. It is hidden in normal projector mode. Fullscreen idle controls hide after two seconds without pointer or keyboard activity and return on activity; hiding controls never pauses the video.
- Local bytes are unavailable when the companion is disconnected, the exact SHA is absent, the response fails, or the browser cannot decode/play the returned video. Never display an incorrect file by matching its filename. A later local copy of the exact bytes restores the original entry on the next open/selection. Do not start a Cloudflare/R2 transfer merely because Preview or the projector opens.
- Preview reports `Video unavailable on this computer` with a video-specific missing icon. The projector clears prior content and displays only the very muted video-specific missing icon, without a filename or error text for the congregation. The existing projector position cue continues to identify the service position in normal projector mode.
- A pending read or decode from an older selection cannot overwrite a newer selection or begin playback after navigation. Release Blob URLs and event handlers when no longer needed. Only the selected Video entry can play.

## UI details

The owner-approved [interactive preview](./preview.html) is the visual reference. The 12-second generated clip, sample Tata Ibadah entries, and preview-only state buttons are demonstration data, not product features.

- **Service entry:** Preserve the existing Video file icon, title or filename, subtitle, row spacing, and Edit/Delete actions. Add Preview in the existing previewable-entry action style. Keep Preview available for a missing file so the operator can see why it cannot play.
- **Preview dialog:** Center the existing morphing dialog at `min(920px, 100vw - 32px)` with `max-height: 100vh - 48px`, 14px radius, and 22px body padding (16px on narrow screens). Show the 16px semibold title header only when the entry title exists. Use a dark `#171613` Video frame. Keep the picture proportional with `object-fit: contain`, a 16:9 presentation area, and `max-height: calc(100vh - 210px)`; portrait and landscape videos must both fit without cropping or stretching.
- **Preview controls:** Center a 58×58px play/pause overlay on the Video frame, using `#514f48` with a quiet brightened hover state and a visible keyboard focus outline. When paused, show a 34×34px Play/Pause button below the frame, followed by a flexible seek track with 12px spacing; the controls row begins 14px below the frame. The seek target is 18px high with a 6px visible line; its 10px handle appears only on hover/focus. Put the canonical filename and 12px muted elapsed/total timer on the next row, 8px below the controls, with filename left and timer right. Do not include volume controls.
- **Preview unavailable:** Center a 38×38px video-specific missing icon over the 13px muted `Video unavailable on this computer` message in an area at least 270px high. Keep the title header rule above.
- **Normal projector:** Keep the dark `#171613` canvas and existing safe area (32px top/left/right, 64px bottom). Fit the complete video to the available stage with `object-fit: contain`, including portrait video. Show a centered 58×58px Play/Pause control in `#514f48`; hover brightens to `#68635b`. There is no projector seek bar or timer in this mode. The existing bottom service position cue remains visible.
- **Fullscreen projector:** The Video stage occupies the full viewport with the video fitted using `object-fit: contain`. Hide the center Play/Pause control, position cue, and other projector overlays. Place the seek target at the bottom so the center of its visible 6px line is `5vh` above the viewport bottom. The target is 18px high. Inset the row by 32px on both sides. Put the 16px muted timer inline to the right of the bar with a 14px gap. There is no play/pause icon in the row. The visible rail is `#34312b`, the fill and 10px hover-only handle are `#8e887b`. In fullscreen, the row is visible only while the operator is active.
- **Idle and active states:** While playing in the normal projector view (fullscreen fallback), hide the center control after 2 seconds of inactivity; return it on pointer or key activity. During fullscreen, fade the entire seek/timer row to opacity 0 after 2 seconds and disable its pointer target; restore it on activity. Projector control transitions are brief (160–260ms) and reduced-motion preference removes them. Clicking/tapping a play control gives a slight pressed scale effect; keyboard Space produces the same brief visual response in Preview. Hover and pressed feedback apply in Preview and in the normal projector view.
- **Fullscreen exit and navigation:** Pause exits fullscreen immediately and returns to normal projector view with the center control; ending playback also exits. Escape exits fullscreen, pauses the video, and restores normal projector navigation. While fullscreen playback is active, left/right screen navigation does nothing. Navigation remains available after pause or fullscreen exit.
- **Motion and responsive behavior:** Preview opens with the existing 210ms morph (`cubic-bezier(.2,.8,.2,1)`) and closes with the existing 170ms reverse morph; Escape and backdrop dismiss it. With reduced motion, modal and control motion is disabled. On narrow screens, the dialog stays within 16px viewport margins; controls and metadata shrink without horizontal overflow.

## Acceptance scenarios

### Scenario: Preview available Video

- **Given** a Video entry references verified local bytes
- **When** the operator opens Preview
- **Then** the modal names the entry, shows the full uncropped video, and begins paused at `0:00` with the filename and timer below the seek bar.
- **When** the operator clicks Play/Pause or presses Space, seeks by clicking or dragging, or focuses the seek bar and presses Left/Right
- **Then** playback or position changes as requested and the timer and seek bar remain synchronized.
- **When** the operator closes with Escape or by clicking the backdrop
- **Then** playback stops, its object URL is released, and the existing close morph/focus behavior is preserved.

### Scenario: Project Video in service order

- **Given** a Tata Ibadah has entries before, at, and after a Video entry
- **When** the projector selects the Video entry
- **Then** the video is paused and fitted in the normal projector safe area, with the normal service cue and no seek bar or timer.
- **When** the operator presses Space or clicks Play
- **Then** playback starts and the browser enters fullscreen when permitted.
- **When** the operator pauses
- **Then** fullscreen closes immediately and the normal projector view returns with the video paused at its current position.

### Scenario: Fullscreen controls, idle, and navigation

- **Given** a Video is playing fullscreen
- **Then** the progress bar is at `5vh` from the bottom, the timer is inline at its right, both have 32px side insets, and no center play/pause icon or service cue is visible.
- **When** two seconds pass without pointer or keyboard activity
- **Then** the progress bar and timer hide without pausing Video; operator activity brings them back.
- **When** the operator presses left/right while fullscreen playback continues
- **Then** the service entry does not change.
- **When** the operator pauses or exits fullscreen with Escape
- **Then** the normal projector returns and existing service navigation works.

### Scenario: Contextual Space and shortcuts sheet

- **Given** an available Video projector entry is selected and no higher-priority overlay or control owns the keyboard
- **When** the operator presses Space
- **Then** Video playback toggles once for that key press.
- **Given** Audio, Video, or another projector entry is selected
- **When** the operator opens the projector shortcuts sheet
- **Then** the Display section documents `Space — Audio/Video Play/Pause` alongside `Space — Show or Hide Words` for other entries.

### Scenario: Fullscreen request is unavailable

- **Given** the browser does not support or refuses fullscreen
- **When** the operator starts Video
- **Then** playback continues in the normal projector safe area, the center control follows the two-second idle behavior, and ordinary service navigation remains available.

### Scenario: Navigation and display lifecycle stop Video

- **Given** a Video is selected
- **When** the operator navigates away, turns the projector display off, leaves the projector page, or changes surface
- **Then** playback stops, the video resets to `0:00`, fullscreen exits, and no sound or moving frame continues on another service entry.
- **When** the operator returns to the Video entry
- **Then** it is paused at the start and requires a new Play action.

### Scenario: Missing, disconnected, and undecodable local video

- **Given** the exact file is absent, the companion is unavailable, the response fails, or the browser cannot decode/play it
- **When** Preview opens
- **Then** it displays the video-specific icon and `Video unavailable on this computer` message.
- **When** the projector selects the same entry
- **Then** prior content is cleared and only the very muted Video missing icon is shown, without a filename or error text.
- **When** the exact bytes later become available locally
- **Then** reopening/reselecting the unchanged entry restores Video playback.

### Scenario: Other service entries keep their behavior

- **Given** Image, Audio, PDF, PPT, and PPTX entries are in the same service
- **When** the operator navigates among them and the Video entry
- **Then** only the Video entry receives Video playback; each other family retains its own display and keyboard behavior, and navigation preserves the stored service order.

### Scenario: Stale response cannot replace a newer selection

- **Given** the Video file request is pending
- **When** the operator navigates to another entry or closes Preview before it resolves
- **Then** the old response cannot start playback or replace the current screen, and any no longer used object URL is released.

## Traceability

- **Domain/app tests:** `multimedia/web/test_media.py::VideoDisplayContractTests` — Video-only Preview metadata, screen identity/order, and unchanged other-family behavior.
- **Browser E2E:** `tests/e2e/test_video_display.py::VideoDisplayE2ETests` — local decode/playback, seek, title/untitled state, Space, fullscreen transitions, idle state, arrow-navigation guard, fullscreen fallback, missing/decode failure, and resource cleanup.
- **Implementation:** `multimedia/web/reading/views.py`; `multimedia/web/templates/reading/tatib.html`, `projector.html`, and `projector_controls.html`; `static/web/media-video.js`, `preview.js`, `projector.js`, and `offline-render.js`; `static/styles/design/components.css` and `projector.css`.

## Owner review points

- Video projector Play requests fullscreen; pausing returns to normal projector view while preserving the current frame/position.
- The fullscreen seek bar and timer share one row at the bottom; the progress line is 5vh from the bottom, with 32px side insets. The timer is at the end of the row; there is no play/pause icon in that row.
- Fullscreen playback suppresses left/right service navigation; normal navigation returns after pausing or exiting fullscreen.
- Space controls Audio/Video playback in context and the projector shortcuts sheet labels that context while retaining Show/Hide Words for other entries.
- A browser fullscreen denial keeps playback available in the normal projector area.
- Missing Video uses its own quiet projector icon and a readable operator Preview state.
