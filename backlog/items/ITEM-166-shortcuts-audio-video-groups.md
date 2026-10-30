---
id: ITEM-166
status: in-review
title: 'The shortcuts sheet names Audio and Video on their own'
type: feat
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-30
spec: specs/160-shortcuts-audio-video-groups/spec.md
branch: feat/160-shortcuts-audio-video-groups
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/477
issue: 476
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-166: The shortcuts sheet names Audio and Video on their own

## Summary

The projector's shortcuts sheet lists one row, `Audio/Video Play/Pause`, inside the `Display` group —
beside `Show or Hide Words`, which is the other Space behaviour. The sheet's other groups name the
thing the keys act on (`Service`, `Song`, `Passage`, `Library passage`), so a combined row hides
which key applies to what and reads as a footnote to Display.

Give audio and video each a group of its own, `Audio` and `Video`, each holding its Play/Pause row,
and take the combined row out of `Display`.

## Notes

- Owner request, 2026-10-29: "add play/pause to keyboard shortcuts modal for audio and video" →
  "move it to their own groups of 'Audio' and 'Video'".
- The sheet is `#key-list` in `multimedia/web/templates/reading/projector_controls.html`; its rows
  are static markup, so the change is markup only — no script, no new CSS.
- The sheet is three columns of groups (`.stack` × 3) whose height is set by the tallest column.
  Measured on the running develop page at 1920×1080 and 1280×720: 676.5×1124px, tallest column
  634.5px, middle column 380px. Two one-row groups added to the tallest column would take the sheet
  to 775px and make it scroll at 720p; in the middle column the sheet keeps its 676.5px height.

## Acceptance sketch

- `Display` holds `Show or Hide Words`, `Show or Hide Corner` and `Keyboard Shortcuts`, and no
  play/pause row.
- A group headed `Audio` and a group headed `Video` each hold one row: `Play/Pause`, with the Space
  chord the sheet already draws.
- The sheet's box is unchanged in height at 1080p and 720p, no group row changes its pitch, and
  nothing else in the sheet moves.
- The projector's Space behaviour is untouched: it still toggles the audio or video that is showing,
  and toggles the words otherwise.

## Links

- Spec: [160](../specs/160-shortcuts-audio-video-groups/spec.md)
- Related items: ITEM-115 (audio display), ITEM-116 (video display) — both shipped the row this
  card regroups
