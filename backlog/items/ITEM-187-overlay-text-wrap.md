---
id: ITEM-187
status: in_review
title: 'A long run in the overlay''s text is painted past its panel instead of wrapping'
type: fix
priority: P1
effort: S
created: 2026-11-02
updated: 2026-11-02
spec: specs/183-overlay-text-wrap/spec.md
branch: fix/183-overlay-text-wrap
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/486
issue:
closed_at:
closed_reason:
bump: patch
release_version: 1.26.1
---

# ITEM-187: A long run in the overlay's text is painted past its panel

## Summary

The OBS caption overlay never breaks a word: `obs-overlay.css` declares no `overflow-wrap` on the
stage, the plate or the caption, so any run without a space is painted straight out of the panel it
belongs to. Measured on develop (1.26.0) at 1920×1080:

| screen | what | ink past its own box | ink past the panel |
| --- | --- | --- | --- |
| a liturgy text, body `a very looo…o untitled text` (120-char run) | `.obs-overlay__line` | 735px | **710px** |
| the same, with a pasted 140-char URL after a speaker mark | `.obs-overlay__line` | 746px | **722px** |
| a song lyric with a 66-char run | `.obs-overlay__caption` | **2,035px** | 2,035px |
| a passage whose verse title is one long run | `.obs-overlay__title` | 232px | **207px** |
| the same passage's body | `.obs-overlay__line` | 718px | **694px** |

The panel is `width: fit-content` between `min-width: 34%` and `max-width: 90%`, so a run narrower
than the 90% cap is absorbed by the panel growing (only the right padding is eaten) and a run wider
than it is painted out of the panel entirely — which is what the owner met, with the words running
across the frame. The caption has no width to grow into at all.

The reading surfaces got this rule in spec 137 and that spec's assumptions say the projector and the
OBS dock already break words; the overlay was left out, and spec 180 then added the plate on top of
it without one.

## Notes

- Every text on the overlay is affected: the plate's kicker, title and body lines, its speaker-mark
  words column, and the song caption — one inherited declaration reaches all of them from the stage.
- The scope was first agreed as the plate's body alone and widened at gate 2 by the owner (*"do the
  word-break on the song captions and the panel's header/title as well"*); the reversal is recorded in
  the spec's clarifications.
- The boxes must not change their measuring: the plate sizes itself to its content, so the fix must
  not cap or clamp it, only break a run that cannot fit.
- A 64-character entry title (the plate's kicker, at `.5em`) cannot outgrow the plate — the panel
  absorbs it — so that state is measured as unchanged rather than as wrapping.

## Acceptance sketch

- At 1920×1080, 1280×720 and 960×540, no part of any text on any overlay state is painted past the
  box that owns it (0 px spill; from 710 / 722 / 2,035 / 207 / 694 at 1080p).
- Text that already fits draws the same number of rows in the same box at the same position,
  including both controls and the 64-character kicker.
- The panels keep their measuring: a short liturgy is 823.72 × 201.13 at 1920×1080, and the caption
  keeps weight 800, its outline, its centring and balanced lines.

## Links

- Spec: [183](../specs/183-overlay-text-wrap/spec.md)
- Related items: ITEM-147 (the same defect on the reading surfaces, spec 137), ITEM-180 (the plate,
  spec 180)
