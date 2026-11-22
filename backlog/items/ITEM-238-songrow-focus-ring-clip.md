---
id: ITEM-238
status: in-progress
title: 'The song-row focus ring is clipped at the top of the list'
type: fix
priority: P2
effort: S
created: 2026-11-22
updated: 2026-11-22
spec: 223-songrow-focus-ring-clip
branch: fix/223-songrow-focus-ring-clip
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-238: The song-row focus ring is clipped at the top of the list

## Summary

On a reading page with the songs list open, a keyboard-focused first row shows a focus ring whose
top edge is cut off. Measured at 900×700 on the local page: the row's top and `#chBody`'s top are
both y=130, `#chBody` has `padding-top: 0`, and the browser's `auto 1px` outline with a 1px offset
needs 2px above the row. The list is not scrolled — `scrollTop = 0` and `scrollHeight =
clientHeight = 570` — so the ring, not the content, is what the scrollport clips.

## Notes

- The ring appears on Tab, or when any key is pressed while a pointer click's focus is still on the
  row: focus alone does not match `:focus-visible`.
- Two candidates are previewed: reserve 3px of top space in the scrollport with the browser
  outline unchanged, or draw a 2px `--focus` ring inside the row with `outline-offset: -2px`.
- Owner authorised this card to enter Speccing directly on 2026-11-22.
- Out of scope: the first sidebar's rows, other focusable controls, and any change to row content,
  ordering, hover or selected state.

## Acceptance sketch

- Focus the first song row by Tab and by key-after-pointer-click; the complete ring is visible in
  both, including its top edge.
- Unfocused rows, hovered rows and the selected row keep their current appearance and boxes.
- The same holds in both themes at 1440×900, 900×700 and 390×844, and at the bottom of the list.

## Links

- Spec: [223-songrow-focus-ring-clip](../../specs/223-songrow-focus-ring-clip/spec.md)
- Related items: ITEM-171 (preview body's shortcut ring), ITEM-211 (sidebar date focus)
