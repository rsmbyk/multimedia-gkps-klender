# Implementation Plan: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md`
**Branch**: `feat/155-audio-presentation-lock`
**Bump**: `patch` — 1.22.16 → 1.22.17
**Preview**: `specs/155-audio-presentation-lock/preview/` — live at `/projector?service=144`, probe `preview/probe_lock.py`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5, IIFE modules) in `static/web/projector.js`, `static/web/media-audio.js`, `static/styles/design/projector.css` |
| Primary dependencies | none added; the browser's own Fullscreen API, which the video path already uses |
| Storage | none; the locked state is derived from the live `<audio>` element, never written |
| Testing | Playwright (Python) in `tests/e2e/test_audio_display.py`, next to the video path's own three fullscreen cases |
| Target platform | every browser the projector runs in, including a browser that refuses fullscreen |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; one boolean read per keydown/click, no request added |
| Constraints | the video path's behaviour must not move; the preview dialog's audio player must not enter fullscreen; the dock channel stays authoritative; no new markup in `projector.html` |
| Scale / scope | two script modules, one CSS rule, one E2E class's new cases, one board card, one capability requirement |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
`Constraints` row above stands in its place.

Re-checked after Phase 1: pass — the design adds no entity, no request, no route and no markup.

## Phase 0 — Research

See `research.md`. Five decisions, each read out of the shipped code or measured on the live route:
mirror the video's three fullscreen helpers (D001); give `media-audio.js` the play-request hook the
video module already has, plus a `pause()` (D002); key the lock on playback rather than on the
fullscreen request (D003); leave the dock channel and `c`/`t` alone (D004); add no visible control
(D005, accepted at gate 1). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entity, field or stored state`; it records the derived predicate and its
  three invariants instead.
- `contracts/` — `none` (`contracts/none.md`): no endpoint, no payload, no module signature removed.
  `GKPSMediaAudio.attach` gains one optional option and one method, both additive.
- `quickstart.md` — the isolated test command, the two E2E modules, the live preview and its probe.

### The design

`static/web/projector.js` already carries the video's three helpers. The audio path gets the same
three, plus one predicate the guards share:

```js
function audioPlaying() {
  return Boolean(audioHost && audioPlayer && !audioPlayer.audio.paused);
}
```

- `requestAudioFullscreen(host)` — called from `onPlayRequest`, inside the play gesture. It requests
  fullscreen on the `.screen__audio-box` and backs out if the host changed or playback stopped before
  the request resolved (the same stale-token guard `requestVideoFullscreen` uses).
- `exitAudioFullscreen(host)` — bumps the token and exits only when the fullscreen element is that
  box, so it never steals a video's or the page's fullscreen.
- `syncAudioFullscreen()` on `fullscreenchange` — records that it was fullscreen, and pauses the
  recording the moment fullscreen is left by any route (the browser's own `Escape` gesture included).

`media-audio.js` gains `onPlayRequest` in `toggle()` (mirroring `media-video.js:83`) and a `pause()`
on the returned object (mirroring `media-video.js:131`). The preview dialog calls `attach` without
that option, so it keeps its current behaviour untouched.

The guards, all reading `audioPlaying()`:

| where | today | after |
| --- | --- | --- |
| `projector.js:1266` keydown, after the video fullscreen guard | video fullscreen only | arrow/page/home/end swallowed; `g`/`j` swallowed |
| `projector.js:938` the mouse-zone click handler | moves | returns |
| `cueService` / `cueNext` / `baitList` / `chooseEntryList` click handlers | move | return |

`projector.css` gains one rule after the audio block: `.screen__audio-box:fullscreen` sized `100vw ×
100vh`, `background: #171613`, so the takeover is the viewport and the cue — outside the fullscreen
element — is not painted.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/projector.js` keydown guard | `test` → `tests/e2e/test_audio_display.py::test_projector_playing_audio_locks_navigation` | 10 key forms incl. Shift/Ctrl |
| FR-002 | `static/web/projector.js` mouse-zone + cue handlers | `test` → `tests/e2e/test_audio_display.py::test_projector_playing_audio_ignores_pointer_navigation` | next zone, cue next, cue entries |
| FR-003 | `static/web/projector.js` keydown guard | `test` → `tests/e2e/test_audio_display.py::test_projector_playing_audio_keeps_go_to_shut` | `g` and `j` |
| FR-004 | `requestAudioFullscreen` + `.screen__audio-box:fullscreen` | `test` → `tests/e2e/test_audio_display.py::test_projector_playing_audio_enters_fullscreen` | element identity, 1440×900, cue outside |
| FR-005 | `syncAudioFullscreen` + `onPlayback` | `test` → `tests/e2e/test_audio_display.py::test_projector_pausing_audio_returns_the_screen` | position kept |
| FR-006 | `syncAudioFullscreen` | `test` → `tests/e2e/test_audio_display.py::test_projector_escape_leaves_fullscreen_and_pauses_audio` | held Escape |
| FR-007 | `onPlayback(false)` from the `ended` event | `test` → `tests/e2e/test_audio_display.py::test_projector_audio_end_returns_the_screen` | |
| FR-008 | guards keyed on `audioPlaying()` | `test` → `tests/e2e/test_audio_display.py::test_projector_refused_fullscreen_still_locks_audio` | `requestFullscreen` denied |
| FR-009 | unchanged channel handler `:1380` | `test` → `tests/e2e/test_audio_display.py::test_untitled_preview_and_projector_idle_display_off` | existing case, re-run unchanged |
| FR-010 | no guard on `c`/`t` | `inspection` — the keydown guard lists no `c` or `t`; both handlers sit below it and read nothing from the audio state | |
| SC-001 | `projector.js` guards | `test` → the four lock cases above | 13 inputs, none moves the screen |
| SC-002 | `syncAudioFullscreen` | `test` → `::test_projector_pausing_audio_returns_the_screen` | `fullscreenElement === null`, screen kept, clock kept |
| SC-003 | `.screen__audio-box:fullscreen` | `test` → `::test_projector_playing_audio_enters_fullscreen` | 1440×900 at 1440×900, `rgb(23, 22, 19)` |
| US1 | `projector.js` + `projector.css` | `test` → the three lock cases | |
| US2 | `syncAudioFullscreen` | `test` → the escape and end cases | |
| US3 | guards keyed on playback | `test` → `::test_projector_refused_fullscreen_still_locks_audio` | |
| US1 (regression) | the video path's own helper trio | `test` → `tests/e2e/test_video_display.py::test_projector_fullscreen_play_pause_and_navigation_guard` | unchanged re-run: the audio helpers must not move it |

**Verification split**: 16 test · 1 inspection · 0 manual

### Reconciled with `develop` on 2026-10-29, before the merge

- **The card was renumbered ITEM-164 → ITEM-170**: spec 157's card had already taken ITEM-164 on
  develop (`9a318d8f chore(board): close ITEM-164 (157)`), so the file, its `id:`, the board row, the
  pack's references and the tracker anchor (#442, retitled) all moved. Spec 156's own notes record that
  its card was renumbered to ITEM-169 for the same reason, seen from the other side.
- **The version became 1.22.17** — develop is 1.22.16 after four slices landed since this branch was cut.
- **The requirement folded as `R5`, not `R3`**: develop had taken R3 (image placeholder, spec 157) and
  R4 (the audio screen's playback control, spec 156) in the meantime.
- **Spec 156's control is what a pointer uses** (D005): it landed on the audio screen while this slice
  was in flight, so the takeover keeps it visible instead of being keyboard-only. `R5` says the
  takeover is the audio screen's own box, which is the reading `R4`'s "the page does not enter
  fullscreen" leaves room for.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | | |

## Project Structure

### Documentation

```
specs/155-audio-presentation-lock/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/checklist.md  preview/README.md  preview/probe_lock.py
```

### Source

```
static/web/projector.js              + audio fullscreen helpers, the three guards
static/web/media-audio.js            + onPlayRequest in toggle(), pause() on the handle
static/styles/design/projector.css   + .screen__audio-box:fullscreen
tests/e2e/test_audio_display.py      + five cases in the existing class
```

### Structure Decision

Everything lands in the modules that already hold the video's equivalent — `projector.js` keeps one
navigation model, one fullscreen recipe and one place where input is read. No new file, no new route,
no new template: the audio screen's markup is unchanged, and the takeover is a CSS rule plus the
browser's own fullscreen.
