---
id: ITEM-223
status: in-review
title: 'A speaker''s continuing line hangs under the words, not under the mark'
type: fix
priority: P2
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: specs/211-overlay-turn-hang/spec.md
branch: feat/211-overlay-turn-hang
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/556
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-223: A speaker's continuing line hangs under the words, not under the mark

## Summary

In the OBS overlay, a liturgy line that follows a speaker's marked line already carries that
speaker's voice (spec 059), but it is painted flush at the plate's leading edge — under the mark.
The owner's screenshot shows `L. Aku percaya kepada Allah` with `Bapa yang mahakuasa…` starting
under `L.` instead of under `Aku`, so the turn reads as a ragged stack. The continuing line should
hang at the same words column the marked line uses.

## Notes

- The voice is already right; `voice_lines` carries it across lines and screen breaks. The defect
  is the overlay's row layout: only a row with both a mark and words joins the mark grid.
- R5 gives the marked lines one column sized by the widest mark. The continuation is the same
  turn, so it belongs in that column with the mark cell empty.
- A screen that begins mid-turn and carries no mark has no column; its lines stay flush left.
- A cue (`Nyanyian: …`), an ordinary line, and a body with no speaker have an empty voice and are
  unchanged.
- A speaker token alone on its line is a different gap, recorded as ITEM-224.

## Acceptance sketch

- At 1280×720 the continuation's first glyph begins at the marked line's words x (±1px).
- A wrapped continuation keeps every visual row at that x and inside the plate.
- A no-mark screen keeps its lines flush at the plate's content edge.
- The voice classes and the existing overlay behaviour are unchanged.

## Links

- Spec: [specs/211-overlay-turn-hang/spec.md](../../specs/211-overlay-turn-hang/spec.md)
- PR: [#556](https://github.com/rsmbyk/multimedia-gkps-klender/pull/556) (draft)
- Related items: [ITEM-061](./ITEM-061-speaker-colors.md) (spec 059), [ITEM-224](./ITEM-224-token-only-line.md)
