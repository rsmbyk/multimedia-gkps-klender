# Spec: Play audio media entries

- **ID:** 115
- **Status:** Accepted
- **Item:** ITEM-115
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Preview:** [Owner-approved interactive preview](./preview.html) (2026-10-19)
- **Bump:** minor

## Intent

Allow an operator to Preview a locally stored Audio service entry and play it from the Tata Ibadah projector page at its exact service-order position. The projector stays quiet until the operator starts playback, remains navigable with the existing keys, and never uses a different file when the referenced one is absent.

## Scope

### In scope

- Audio-family media entries already stored by the Media Library, with immutable SHA-256 service references and existing entry title/filename behavior.
- The existing service-entry Preview dialog, projector sequence, position cue, display-off state, and keyboard shortcuts sheet.
- Browser retrieval and playback of the verified file from the local companion, including disconnected, absent, failed-response, and browser decode/playback failure states.

### Out of scope

- Video, PDF, PPT/PPTX, OBS, cloud streaming, autoplay, playlists, looping, a volume control, waveform display, or replacing a media entry's file.
- Changes to Media Library upload, sharing, expiry, or automatic download eligibility.

## Domain and playback rules

- An entry whose authoritative `MediaIdentity.family` is Audio gains Preview and exactly one audio projector screen in its existing Tata Ibadah order. Other families do not gain audio controls. The entry's title, stored filename, SHA-256 reference, and edit rules remain unchanged.
- The browser fetches the entry's SHA-256 from the companion's verified `GET /v1/files/<sha>` endpoint. It must not use the filename as a path or accept another file with the same name. Convert the verified response to a Blob with the inspected Audio MIME type for browser playback. Django/Vercel never proxies the audio bytes.
- Playback is manual. Entering an Audio projector screen leaves the player paused at `0:00`, including when returning from another service entry. Leaving the screen, turning display off, or leaving the projector page stops audible playback. Re-selecting the entry starts at `0:00`; it does not resume or autoplay. A finished track remains stopped at its end until the operator replays or seeks it.
- Preview provides Play/Pause, a running elapsed clock, total duration, and a seek bar that accepts clicking, pointer dragging, and focused Left/Right arrows in five-second steps. Space also toggles Play/Pause while an available Audio Preview is open; holding Space does not toggle repeatedly. Close, Escape, or backdrop dismissal pauses playback. Reopening Preview never autoplays.
- The projector provides pointer Play/Pause and seek, plus Space for Play/Pause on the currently selected, available Audio entry. Its player elements do not take keyboard focus, so the existing plain/Shift/Ctrl navigation hierarchy continues to work. Space on non-Audio screens retains Show/Hide Words. When a projector overlay, search input, or another higher-priority control owns keyboard input, the Audio shortcut does not fire. The shortcuts sheet adds an Audio row for `Space — Play/Pause`, and keeps the Display row explaining Space on non-Audio screens.
- When local bytes are absent, the companion is unavailable, the response fails, or the browser cannot decode/play the file, Preview shows `Audio unavailable on this computer` with a missing-file icon. The projector clears prior entry content and shows only the established very-muted missing-media icon, without a filename or error text to the congregation. Later availability of the exact referenced bytes restores playback on reselecting/reopening the entry. Opening the projector does not itself trigger an R2 download.
- An in-flight fetch, decode, or playback event from a previous entry cannot replace or start audio on a newly selected screen. Release Blob URLs and event handlers when no longer needed. Only the selected Audio entry may be audible.

## UI details

The [approved interactive preview](./preview.html) is the visual reference. Its synthetic 24-second recording and demo-only navigation controls are not production features. Existing rail, stage, sidebar, bottom projector cue, and screen-navigation UI remain the app's own components.

- **Stage:** Retain the existing Audio type icon, entry title or saved filename, subtitle, spacing, and Edit/Delete actions. Add the same Preview action style and position used by previewable entries. The action remains available when the local file is missing so the operator can inspect the unavailable state.
- **Preview dialog:** Use the existing centered modal with `min(620px, 100vw - 32px)` width, 14px radius, and 28px vertical/26px horizontal body padding (24px/20px at narrow widths). Show the 52px-minimum title header only when the entry has a title; an untitled entry has no header, and its saved filename appears above the progress bar instead. A titled entry shows its title in the header and still shows the filename above the bar. Do not repeat file type or duration above the player and do not include volume UI.
- **Preview player:** Left 48×48px circular Play/Pause control; a flexible timeline to its right with a 14px semibold filename, 9px gap to a 6px-high track, and 12px muted elapsed/total time labels beneath. The control-to-timeline gap is 16px. The progress fill uses the app accent; its 10px circular handle is hidden at rest and appears only on track hover. Keep app-style hover/focus-visible feedback on the Play/Pause control and a clear focus-visible outline on the keyboard-seekable timeline. The bar accepts click, drag, and keyboard seeking without shifting the dialog.
- **Preview missing:** Center the existing missing-file outline icon (38×38px) above the 13px muted `Audio unavailable on this computer` message in a body at least 200px high. Preserve the titled/untitled header rule.
- **Projector:** Use the existing dark `#171613` screen and bottom position cue. Center Play/Pause, progress bar, and elapsed/total time as one vertical unit. The Play/Pause control is 48×48px in `#514f48`; the bar is at most 500px wide or 60vw, 6px high, with a dark `#34312b` rail and `#8e887b` fill; place it 30px below the button. Place the 16px muted timer 12px below the bar. Show no entry title, filename, audio-type label, or volume UI on the congregation screen. Its 10px handle appears only when the bar is hovered. Projector player controls are pointer-operable but not keyboard-focus targets; Space and existing navigation keys operate at screen level.
- **Playing idle state:** Only while audio is playing, after 3.5 seconds without pointer or keyboard activity, fade Play/Pause to opacity 0 and remove its pointer hit target; set bar opacity to 0.52 and timer opacity to 0.40. Any pointer movement/press or key press restores full opacity and restarts the timer. Paused and ended states keep all controls fully visible. Opacity changes take 260ms with `ease`; reduced-motion preference removes the transition. This idle state does not stop or change audio playback.
- **Motion and responsive behavior:** Preview retains the existing 210ms open and 170ms close morph, backdrop/Escape dismissal, and quiet focus restoration. The timeline shrinks within the modal at narrow widths without horizontal overflow; projector bar is capped at 60vw and the centered unit does not overlap the existing bottom cue. Light/dark Preview colors use current app tokens; the projector remains dark.

## Acceptance scenarios

### Scenario: Preview titled and untitled Audio

- **Given** an Audio entry references a verified local file
- **When** the operator opens Preview
- **Then** the actual file is playable and shows its filename, live elapsed/total time, and seekable progress bar, without file-type/duration duplication or volume control.
- **And** a titled entry shows its entry title in the header; an untitled entry has no header and still names the file inside the player.
- **When** the operator presses Space, clicks Play/Pause, clicks or drags the bar, or focuses the bar and presses Left/Right
- **Then** playback or position changes once as requested and the time/bar stay synchronized.
- **When** the operator closes the modal via Escape or backdrop
- **Then** playback pauses and the existing close morph/focus behavior applies.

### Scenario: Project audio in service order

- **Given** a service has entries before and after an Audio entry
- **When** the operator navigates to that Audio entry
- **Then** its one screen shows the centered, paused player at `0:00` without a title or filename, and the bottom cue shows its normal service position.
- **When** the operator clicks Play/Pause or presses Space
- **Then** the actual file plays or pauses and the time/bar follow it, without a focused projector player element stealing navigation keys.
- **When** the operator leaves and later returns to the Audio entry
- **Then** prior audio is no longer audible and the player is paused at `0:00`.

### Scenario: Contextual Space and shortcuts sheet

- **Given** an available Audio projector entry is selected and no overlay owns the keyboard
- **When** the operator presses Space
- **Then** only Audio Play/Pause toggles, once per key press.
- **Given** a non-Audio projector screen is selected
- **When** the operator presses Space
- **Then** the existing Show/Hide Words behavior remains.
- **When** the operator opens the projector shortcuts sheet
- **Then** it documents Audio `Space — Play/Pause` alongside the existing Display shortcut.

### Scenario: Idle only during playback

- **Given** projector audio is playing
- **When** 3.5 seconds pass without keyboard or pointer activity
- **Then** Play/Pause becomes hidden and the bar/timer dim to their specified opacities, while audio continues.
- **When** the operator moves the pointer, presses a key, or pauses playback
- **Then** the controls reappear; while paused or ended they remain fully visible regardless of inactivity.

### Scenario: Missing, undecodable, and stale audio

- **Given** an Audio entry's exact SHA-256 is absent, inaccessible, or not playable by the browser
- **When** Preview or projector selects it
- **Then** the operator sees the unavailable Preview state and the projector shows only the muted missing-media icon, with no previous audio continuing.
- **When** the exact file later becomes locally available
- **Then** reselecting the unchanged entry restores playback.
- **When** an old file request finishes after navigation to another entry
- **Then** it cannot play or replace the current screen.

### Scenario: Other media remain unchanged

- **Given** Image, Video, PDF, PPT, and PPTX entries are present
- **When** Preview and projector data are built
- **Then** Image retains its accepted image behavior, and the other families gain no audio player or Audio-specific keyboard action.

## Traceability

- Domain/app tests: `multimedia/web/test_media.py::AudioDisplayContractTests` coverage for Audio-only metadata and projector sequence construction.
- Browser E2E: `tests/e2e/test_audio_display.py::AudioDisplayE2ETests` for Preview, actual playback, projector navigation, contextual keys, idle state, missing file, and display-off.
- Implementation targets: `multimedia/web/reading/views.py`, reading Preview/projector templates, `static/web/preview.js`, `static/web/projector.js`, `static/web/media-audio.js`, and focused component/projector styles.

## Owner review points

- Projector audio starts manually and resets on every navigation back to the entry.
- Space changes meaning only on an available Audio screen (and plays/pauses in the Audio Preview); other projector screens retain their existing meaning.
- The synthetic clip and neighboring demo entries are preview scaffolding; production uses the service's real local Audio file and running order.
