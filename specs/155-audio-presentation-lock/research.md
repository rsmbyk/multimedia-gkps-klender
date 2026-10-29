# Research: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`
**Unknowns remaining**: 0

## D001 — Mirror the video's three fullscreen helpers instead of inventing a lock mode

- **Decision**: the audio path gets `requestAudioFullscreen(host)`, `exitAudioFullscreen(host)` and
  `syncAudioFullscreen()`, shaped exactly like `requestVideoFullscreen` (`static/web/projector.js:1287`),
  `exitVideoFullscreen` (`:1298`) and `syncVideoFullscreen` (`:1306`), plus one shared predicate
  `audioPlaying()`.
- **Rationale**: the video path has shipped this takeover, is pinned by
  `tests/e2e/test_video_display.py::test_projector_fullscreen_play_pause_and_navigation_guard`, and is
  the behaviour the owner asked for by name. Copying its shape means one navigation model, one
  fullscreen recipe, and the same stale-token discipline (a request that resolves after the host moved
  backs out).
- **Alternatives considered**: a boolean `locked` flag set on play and cleared on pause, with no
  fullscreen — it blocks the inputs but leaves the cue and the zones on screen, so the operator still
  sees controls that do nothing (refused by the owner's own direction); fullscreening the whole
  `.screen` — it would carry the header and lines of a text screen into the takeover, but an audio
  screen has neither, and the video precedent fullscreens the media box.
- **Provenance**: research (code read of `projector.js:1287-1322`, `tests/e2e/test_video_display.py:129-180`).

## D002 — `media-audio.js` needs the play-request hook the video module already has

- **Decision**: `toggle()` in `static/web/media-audio.js:50` calls `options.onPlayRequest()` before
  `audio.play()`, and the returned handle gains `pause()`.
- **Rationale**: `requestFullscreen` needs the user gesture that started playback, which only the
  module's own `toggle()` holds; `media-video.js:83` already does exactly this. `pause()` is needed by
  `syncAudioFullscreen` for the case where the browser leaves fullscreen by its own gesture — the
  video's equivalent reads `videoPlayer.video.paused` and calls `video.pause()` (`projector.js:1309`),
  and the audio element is not in the DOM, so it must be reached through the handle.
- **Alternatives considered**: `document.querySelector('audio')` from `projector.js` — the audio
  element is created with `new Audio()` and never appended, so it is unreachable from the DOM;
  requesting fullscreen from the `keydown` handler instead of the play hook — `Space` is a gesture, but
  the mouse's play path and the cue's would then need their own copies of the same call.
- **Provenance**: research (code read of `media-audio.js:28-85`, `media-video.js:80-147`).

## D003 — The lock is keyed on playback, not on the fullscreen request

- **Decision**: every guard asks `audioPlaying()`; none asks whether the fullscreen element is the
  audio box.
- **Rationale**: measured on the slice (preview probe, `requestFullscreen` denied): the recording still
  plays, and a browser that refuses fullscreen would otherwise be the one place a stray key kills it.
  The video path's guard does test `document.fullscreenElement === videoHost`, but the video's own
  fallback keeps navigation live too, and that asymmetry is deliberate here: an audio entry has no
  picture to watch, so playback itself is the fact worth guarding.
- **Alternatives considered**: follow the video exactly (guard only while fullscreen) — it leaves the
  refused-fullscreen operator unprotected, which contradicts the request's own words ("when an audio is
  playing … navigation should be disabled"); guard on `!audio.paused` read from the DOM — the element is
  detached, so the handle is the only source.
- **Provenance**: research + measurement (`specs/155-audio-presentation-lock/preview/probe_lock.py`,
  the `fullscreen_refused` block).

## D004 — The dock channel and `c`/`t` stay live

- **Decision**: `show` / `hide` / `release` / `stop` messages, the adopt path, the corner-hide key (`c`)
  and the translation key (`t`) are not part of the lock.
- **Rationale**: the channel is the authority that drives the projector from the dock (spec 119), and
  the existing tests pin that a `stop` message stops and releases the recording
  (`tests/e2e/test_audio_display.py::test_untitled_preview_and_projector_idle_display_off`). `c` and `t`
  change nothing about *which* screen is projected, and they are the operator's own display controls.
- **Alternatives considered**: blocking every key while playing — it would make the dock's own stop
  path inconsistent with the local one and would leave `c` unusable for 5 minutes mid-recording.
- **Provenance**: research (code read of `projector.js:1380-1420`, `:1245-1274`).

## D005 — No visible play/pause control in the fullscreen state

- **Decision**: the takeover adds no control. `Space` pauses; a held `Escape` exits fullscreen and
  pauses.
- **Rationale**: the video's own fullscreen hides its play button (`.screen__video-box:fullscreen
  .screen__video-play { display: none }`, `projector.css:129`), and the projector's audio screen never
  drew one (`.screen__audio-play` gets its 48×48 size from `components.css:2118`, which the projector
  page does not load — measured 0×0 on `develop`). A control that exists only in one media type's
  fullscreen is a second reflex for the same operator.
- **Alternatives considered**: a centred 58px play/pause button in fullscreen (the size of the video's
  own play affordance) — offered to the owner at gate 1 and not taken; a click anywhere to toggle —
  the seek bar already owns clicks on that surface.
- **Provenance**: owner decision at gate 1, 2026-10-29 (choice: "Accept as drafted — no visible
  control; Space pauses, held Escape exits (matches video)").
