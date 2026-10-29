---
id: ITEM-171
status: done
title: 'Space paints the Preview dialog''s focus ring when it plays or pauses'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/159-preview-body-ring/spec.md
branch: fix/159-preview-body-ring
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/456
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/457
closed_at: 2026-10-29
closed_reason: merged into develop (PR #456)
bump: patch
release_version:
---

# ITEM-171: Space paints the Preview dialog's focus ring when it plays or pauses

## Summary

Space is the Preview's play/pause shortcut, and it also repaints the dialog's edge with the
keyboard focus ring. `showModal()` hands DOM focus to `.preview__body` — the dialog's scroll
region, `tabindex="0"` — and the first key press flips Chrome's `:focus-visible` on that
already-focused element. In audio and video previews the body is laid out edge to edge over the
dialog (measured: dialog and body both 920×852 at 296,24), so its inset ring reads as a 2px
`#1C5C3C` border around the whole modal. It appears on the first space press and stays.

## Notes

- Measured on the compose page at 1.22.10: `:focus-visible` false after a pointer open, true
  immediately after one space, still true after a second space and after a click inside the body.
  Clicking the body cannot clear it, because the click handler's `focus()` call is a no-op once
  the element already holds focus.
- The ring is the deliberate keyboard indicator for the scroll region (spec 071); opening with
  Enter should still show it.
- Two slices met here: `tabindex` + the ring from spec 071 (ITEM-074), the space shortcut from #364.
- Nothing in the space handler touches focus — it only `preventDefault()`s and toggles the player.

## Acceptance sketch

- Pressing space to play or pause a preview paints nothing on the dialog's edge, whether the
  dialog was opened by pointer or by keyboard.
- Tabbing into the dialog still shows every keyboard indicator it shows today, the body's included.
- Escape, the seek bar and the player behave exactly as they do now.

## Links

- Spec:
- Related items: ITEM-074 (the body's focus ring), ITEM-016 (focus lifecycle)
