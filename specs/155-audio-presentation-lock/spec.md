# Feature Specification: A playing recording owns the projector screen until it pauses

**Slice**: `specs/155-audio-presentation-lock`
**Branch**: `feat/155-audio-presentation-lock`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1 and gate 2, 2026-10-29)
**Input**: "when an audio is playing in projector window, navigation should be disabled (either from keyboard or mouse)" — corrected in the same session to "i think it should enter similar fullscreen behavior kind of just like the video so that you need to pause to return to the normal projector screen"

## What the projector does today

An audio entry is one screen holding the player and nothing else
(`multimedia/web/reading/views.py:1238` builds `header: ''`, `lines: []` with `audio_sha256`),
and the projector wires that screen to `GKPSMediaAudio` at `static/web/projector.js:151`.
Nothing ties playback to navigation: `move()` (`:423`), `moveEntry()` (`:572`),
`moveBait()` (`:588`), `unitBoundary()` (`:592`) and the mouse-zone click handler (`:935`) all
run whatever the audio element is doing, and `renderAudioScreen()` tears the player down the
moment the active screen changes (`static/web/projector.js:102`).

Measured on the compose page serving `develop` @ `24a6d6d2` (`/projector?service=144`, the audio
entry on screen 85, a 5:02 MP3, headed Chromium 1440×900, dpr 1):

| action while the recording plays | result |
| --- | --- |
| `ArrowRight` | screen 85 → 86; the audio screen's player is torn down |
| `Ctrl+ArrowLeft` back to 85 | `data-playing="false"`, elapsed `0:00` — the recording stopped and lost its place |
| `Ctrl+ArrowRight` | 85 → 86 |
| right mouse zone (in fullscreen) | 85 → 86 |
| `g` | the Go To panel opens over the playing screen |
| `document.fullscreenElement` while playing | `null` — a recording never takes the screen, unlike a video |

The video path already solves the same problem: playing a video requests fullscreen on its
media box (`requestVideoFullscreen`, `:1287`), leaving fullscreen pauses it (`syncVideoFullscreen`,
`:1306`), and while the video is fullscreen and playing the navigation keys are swallowed
(`:1220`). Pinned by `tests/e2e/test_video_display.py::test_projector_fullscreen_play_pause_and_navigation_guard`.

## User Scenarios & Testing

### US1 — A playing recording cannot be stepped off (P1)

**Why this priority**: this is the report. During a service a recording (a choir track, an
offertory piece, a sermon MP3) runs for minutes; one stray arrow key on the mirrored display
stops it and loses the position, and the operator has to find the entry again mid-service.

**Independent Test**: play the audio entry, press every navigation key and click every mouse
zone, and read `data-current-screen`: it never leaves the audio screen.

**Acceptance scenarios**

1. **Given** an audio screen is showing, **When** the recording is played, **Then** the audio box
   becomes the fullscreen element (1440×900 at a 1440×900 viewport) and the corner cue is not
   inside it.
2. **Given** a recording is playing, **When** `ArrowRight`, `ArrowLeft`, `ArrowUp`, `ArrowDown`,
   `PageDown`, `PageUp`, `Home` or `End` is pressed — plain, `Shift+` or `Ctrl+` — **Then**
   `data-current-screen` and `data-playing` are unchanged and elapsed time keeps rising.
3. **Given** a recording is playing, **When** a mouse zone is clicked, or the cue's next, bait or
   entry-list control is clicked, **Then** the screen does not change.
4. **Given** a recording is playing, **When** `g` or `j` is pressed, **Then** neither the Go To nor
   the entry list opens.
5. **Given** a recording is playing, **When** `Space` is pressed, **Then** it pauses, the audio box
   leaves fullscreen, the normal projector screen returns showing `0:02`, and `ArrowRight` moves
   again.

### US2 — The screen comes back on its own (P2)

**Why this priority**: an operator who is not watching the screen should not be left in a
fullscreen player that once played a recording.

**Independent Test**: play to the end, and separately exit fullscreen with the browser gesture;
in both cases the projector is back on the normal screen, paused.

**Acceptance scenarios**

1. **Given** a recording is playing, **When** it reaches its end, **Then** the projector leaves
   fullscreen and returns to the normal audio screen, paused at the end.
2. **Given** a recording is playing fullscreen, **When** the browser leaves fullscreen (a held
   `Escape`), **Then** the recording pauses rather than playing on under the normal page.

### US3 — A refused fullscreen still locks the screen (P3)

**Why this priority**: the lock is about the recording, not about the browser's permission — a
kiosk or an embedded browser that refuses fullscreen must not become the one place a stray key
kills a recording.

**Independent Test**: deny `Element.prototype.requestFullscreen`, play, press the navigation keys.

**Acceptance scenarios**

1. **Given** fullscreen is refused, **When** a recording is played, **Then** it plays on the normal
   projector screen, every navigation input is still ignored, and pausing gives the keys back.

### Edge Cases

- **When** the recording is paused and resumed, **Then** the position continues (the pause keeps
  `currentTime`; only a screen change releases the player).
- **When** the display is turned off (`Space` has no audio on the active screen, or the dock sends
  `hide`/`stop`), **Then** the existing rule holds: the recording stops and resets (`:90`).
- **When** the dock adopts another Tata Ibadah mid-playback, **Then** the adoption releases the old
  service's media exactly as today (`:1401`); the lock only governs the operator's own inputs.
- **When** a video is playing instead, **Then** nothing in this slice changes: its own fullscreen
  guard and pause rules remain the only ones in force.
- **When** the preview dialog plays audio, **Then** nothing changes: the lock is the projector's.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | While an audio entry's recording is playing, no page-change key moves the projector: `ArrowLeft`/`ArrowRight`/`ArrowUp`/`ArrowDown`, `PageUp`/`PageDown`, `Home`/`End`, in plain, `Shift` and `Ctrl` forms. | `projector/R3` |
| FR-002 | The same lock covers the pointer: the three mouse zones and the cue's next, bait and entry-list controls change nothing while the recording plays. | `projector/R3` |
| FR-003 | The Go To shortcuts (`g`, `j`) do not open while the recording plays. | `projector/R3` |
| FR-004 | Playing a recording makes the audio box the fullscreen element, filling the viewport, so the corner cue and the mouse zones are off screen. | `projector/R3` |
| FR-005 | `Space` pauses the recording; the audio box leaves fullscreen and the normal projector screen returns with the position kept. | `projector/R3` |
| FR-006 | Leaving fullscreen by the browser's own gesture pauses the recording; it never plays on under the normal page. | `projector/R3` |
| FR-007 | When the recording reaches its end, the projector leaves fullscreen and returns to the normal screen, paused at the end. | `projector/R3` |
| FR-008 | When the browser refuses fullscreen, the recording plays on the normal projector screen and the navigation lock still holds while it plays. | `projector/R3` |
| FR-009 | The display channel stays authoritative: a dock `hide`/`release`, a `show` naming another screen, and an `update` still stop and release the recording exactly as today. | `projector/R3` |
| FR-010 | `c` (corner hide) and `t` (translation) keep their behaviour while a recording plays: neither moves the projected screen off its entry. | `projector/R3` |

### Pins that flip

`tests/e2e/test_audio_display.py::test_projector_space_navigation_and_reset` asserted that
`Ctrl+ArrowRight` leaves a **playing** audio screen — the player count drops to 0. FR-001 forbids
exactly that, so the case now pauses first and then navigates; its other claims are unchanged (Space
toggles playback, a screen change releases the player, returning resets the clock to `0:00`).
`::test_untitled_preview_and_projector_idle_display_off` is not changed by this slice: its final
`stop`-broadcast assertion fails because the page has never handled a `stop` message — it reads `show`,
`hide`, `release`, `flip` and `update` only (`static/web/display.js:19`) — so that assertion is red on
`develop` too (card ITEM-140), and the case was re-run unchanged.

### Key Entities

- **Audio screen** — one `.screen` whose `data-media-audio` carries the recording's sha256; no
  header and no lines, so the player is the whole content. No new entity or field is introduced.
- **Locked state** — derived, never stored: "an audio player exists on the active screen and its
  audio element is not paused". Both the key guard and the pointer guard read it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No navigation input moves the projector during playback | probe over 8 key forms + 3 mouse zones + `g`/`j`: `data-current-screen` unchanged in all 13, against 0 of them blocked today |
| SC-002 | One key gets the screen back, with the place kept | `Space` → `document.fullscreenElement === null`, `data-playing="false"`, `data-current-screen` still `85`, elapsed `0:02` |
| SC-003 | The takeover is the whole viewport | `.screen__audio-box` bounding box 1440×900 at a 1440×900 viewport, background `rgb(23, 22, 19)`, `document.fullscreenElement` that box |

## UI/UX

No new component, icon, label or type: the fullscreen state is the audio screen's existing
player on the existing dark stage, with the corner cue and the mouse zones off screen. Values
measured on the slice's live preview at 1440×900:

- **Layout / position**: `.screen__audio-box:fullscreen` is `display:flex` filling `100vw ×
  100vh`; the player stays centred — `.screen__audio-player` at x 470→970, y 415→485 (500×69.9).
- **Size / spacing**: the player keeps its `min(500px, 60vw)` width; the seek bar keeps its 6px
  height and 30px top margin; the time line keeps `16px` and its 12px top margin.
- **Colour / typography**: the fullscreen background is `#171613`; the seek fill `#8e887b` on
  `#34312b`; the times `#8e887b` — the values the screen already uses.
- **States**: playing (fullscreen, cue absent) · paused (normal screen, cue back) · idle after
  3.5s (existing `.is-idle` dimming, unchanged) · fullscreen refused (normal screen, locked) ·
  ended (normal screen, paused at the end).
- **Motion**: none added. Fullscreen is the browser's own transition; no fade, no scale.
- **Responsive**: the player's `min(500px, 60vw)` already narrows with the viewport; the
  fullscreen box is the viewport at every size.

## Assumptions

- **The lock follows playback, not the fullscreen request.** A browser that refuses fullscreen
  keeps the recording locked (FR-008). The video path only guards while its fullscreen element is
  active; an audio entry has no picture to watch, so its playback is the fact worth guarding.
- **`Space` stays the pause control**, as it is today on an audio screen; the lock removes nothing
  from it. `Escape` keeps the app's existing hold-to-exit gesture.
- **No visible play/pause control is added to the fullscreen state.** The video's own fullscreen
  hides its play button, and the projector's audio screen has never drawn one (`.screen__audio-play`
  is a 0×0 box outside `components.css`'s shared rule); a mouse operator pauses with `Space`.
  Raised for the owner rather than invented.
- **The preview dialog's audio player is out of scope** — it is a dialog with its own close button,
  not a projected screen.

## Clarifications

### Session 2026-10-29

- Q: Does "navigation disabled" mean the page simply ignores the inputs, or something more? →
  A: the recording takes the screen the way a playing video does: "enter similar fullscreen
  behavior kind of just like the video so that you need to pause to return to the normal projector
  screen".
