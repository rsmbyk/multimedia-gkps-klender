---
id: ITEM-169
status: in-review
title: 'The audio projector screen shows its play/pause control'
type: feat
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/156-audio-play-indicator/spec.md
branch: feat/156-audio-play-indicator
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/448
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/443
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-169: The audio projector screen shows its play/pause control

## Summary

An audio entry on `/projector` prints its seek bar and its two times and nothing else: the screen
never says whether the audio is playing or paused, and there is nothing to click. The play/pause mark
the page carries (`<span class="screen__audio-play" data-audio-play>`) has no size on the projector —
its geometry and its glyph live in `components.css`, which the projector page does not load — so it
paints 0×0, and the idle rule would fade it out anyway once playback starts.

The audio screen gets the mark the app's own audio player uses: a 48px round play/pause control above
the seek bar, its triangle or its two bars following the audio, visible in every state and clickable.

## Notes

Measured on the compose page serving `develop` @ `24a6d6d2` (`/projector?service=144`, audio entry,
1920×1200, dpr 1): `.screen__audio-play` is **0×0** at x 960, y 549.05, with no `::before` content;
`document.styleSheets` lists only `fonts.css`, `tokens.css` and `projector.css`.

## Acceptance sketch

- The control is a 48×48 box at opacity 1 whenever the chrome is up, and opacity 0 with the box
  unchanged when the chrome settles; the bar and times dim, the control shows and hides.
- Its mark is a triangle while paused and two bars while playing.
- A click toggles playback; the seek bar, the times and every other screen keep their geometry.

## Links

- Spec: [156](../specs/156-audio-play-indicator/spec.md)
- Related items: ITEM-115 (spec 115, the audio media display this completes)
