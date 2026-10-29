---
id: ITEM-163
status: done
title: 'The audio preview splits its two times to the bar''s ends'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/154-audio-times-inline/spec.md
branch: feat/154-audio-times-inline
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/432
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/431
closed_at: 2026-10-29
closed_reason: merged into develop (432)
bump: patch
release_version:
---

# ITEM-163: The audio preview splits its two times to the bar's ends

## Summary

The Preview of an audio file prints the played time at the left end of the seek bar and the total at
its right end, 456.4px apart at the dialog's own width. Nothing says the left number belongs to the
bar it sits under: the pair reads as two unrelated labels, and the played time is the one an operator
watches.

The two times move together, right-aligned under the bar, as `current / total` — the shape every
video player uses.

## Notes

Measured on the compose page (develop, `/tatib/144/`, 1440×900, dpr 1, audio entry `e1`):

- dialog `#previewModal` 620×125 at x410;
- `.preview__audio .audio-player` 568×69 at x436, `.audio-player__timeline` x500→1004;
- `.audio-player__seek` x500→1004, y445.5, 504×14;
- `.audio-player__times` `display: flex; justify-content: space-between; margin-top: 7px;
  font-size: 12px; color: rgb(100, 99, 87)`;
- `[data-audio-elapsed]` x500→523.8 and `[data-audio-total]` x980.2→1004, both 23.8×18 at y466.5 —
  456.4px between them.

The projector's own audio bar already prints `0:00 / 0:00`
(`multimedia/web/templates/reading/projector.html:47`, `.screen__audio-times`), so the reading
surface is the one that deviates.

## Acceptance sketch

- The times line reads `current / total`, both numbers beside each other, right-aligned so the
  total's right edge is the seek bar's right edge.
- The played time no longer sits at the bar's left end.
- Nothing else moves: the dialog's 620px width, the 48px play button, the filename, the 6px bar and
  its 7px gap to the times line are unchanged; unavailable, empty and playing states are unchanged.

## Links

- Spec: [154](../../specs/154-audio-times-inline/spec.md)
- Related items: ITEM-115 (spec 115 — the audio preview and its local companion), ITEM-116 (spec 116
  — the video preview), ITEM-102 (spec 115's projector bar, which already reads `current / total`)
