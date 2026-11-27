---
id: ITEM-237
status: done
title: 'Add song disappears when the songbooks sidebar is closed'
type: fix
priority: P1
effort: S
created: 2026-11-22
updated: 2026-11-22
spec: 222-add-song-parent-closed
branch: fix/222-add-song-parent-closed
pr: 584
issue: 583
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-237: Add song disappears when the songbooks sidebar is closed

## Summary

On a Kidung reading page, opening a songbook and then collapsing only the songbooks sidebar leaves the
songs list on screen but hides its `Add song` button. Reproduced on the local reading page at
1440×900: the root goes `data-nav="closed"` with `data-ch="open"`, `#chapters` stays visible, and
`#songAdd` computes `display: none` (height 0) where it measured `display: flex`, 38px high just
before the collapse.

## Notes

- Root cause is the shared hide rule for add controls: `[data-nav="mini"] .editor-add,
  [data-nav="closed"] .editor-add { display: none; }` in `static/styles/design/components.css`.
  It matches the button in the second sidebar as well as the one in the first.
- In scope: the second-level song list's add control while the first sidebar is mini or closed,
  at every breakpoint where the songs list itself is visible.
- Out of scope: hiding the first sidebar's `Add songbook` / `Add Tata Ibadah` control, which must
  still disappear when its own panel is mini or closed.

## Acceptance sketch

- Collapse only the songbooks sidebar with the songs list open: `Add song` stays visible, enabled
  for a real (non-hymn) songbook, and opens the same editor dialog as before.
- `Add songbook` is still hidden when the first sidebar is mini or closed; no add control paints
  on the search landing or when the songs list itself is closed.

## Links

- Spec: [222-add-song-parent-closed](../../specs/222-add-song-parent-closed/spec.md)
- Related items: ITEM-126 (saved song list renders a disabled `Add song`)
