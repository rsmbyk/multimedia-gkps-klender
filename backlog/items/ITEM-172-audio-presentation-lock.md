---
id: ITEM-172
status: in-review
title: A playing recording owns the projector screen until it pauses
type: feat
priority: P1
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: 155-audio-presentation-lock
branch: feat/155-audio-presentation-lock
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/438
issue: 442
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-172: A playing recording owns the projector screen until it pauses

## Summary

Audio entries take over the projector the way a video already does: playing a recording
puts the audio screen into fullscreen, the corner cue and the mouse zones go off screen, and
no key or click moves the projector until the recording is paused. Today a stray arrow key or
a click on the edge zone jumps the projector to the next screen and tears the player down, so
the recording stops and its position is lost.

## Notes

- Spec 155 carries the measured behaviour and the requirement set.
- The mechanism is the one the video path already ships (`requestVideoFullscreen` /
  `syncVideoFullscreen` / the fullscreen navigation guard), mirrored for audio.
- The lock follows playback, not the fullscreen request: a browser that refuses fullscreen
  still keeps the navigation locked while the recording plays.

## Acceptance sketch

- Playing a recording enters fullscreen on the audio box (1440×900 at 1440×900 viewport).
- While it plays, Arrow/PageUp/PageDown/Home/End (plain, Shift, Ctrl), the mouse zones, the
  cue's next/bait/entry-list controls and `g`/`j` change nothing.
- Space pauses and the normal projector screen returns with the position kept; holding Escape
  exits fullscreen and pauses; the end of the recording returns on its own.

## Links

- Spec: [155](../specs/155-audio-presentation-lock/spec.md)
- Related items: ITEM-002 (projection controls), the video fullscreen slice.
