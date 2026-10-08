---
id: ITEM-042
status: done
title: 'Let the entry modal book/song menus extend past the modal'
type: fix
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/040-picker-menus-past-modal/spec.md
branch: fix/040-picker-menus-past-modal
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/292
archived_at:
archive_reason:
bump: patch
release_version: 1.3.8
---

# ITEM-042: Let the entry modal book/song menus extend past the modal

## Summary

The book picker (add / edit passage) and song picker (add / edit song) dropdowns are capped to the
dialog's own scroll area, so a menu near the modal edge is squeezed and its options scroll inside a
tiny box. Let the menu overlap the dialog's edge — capped to the viewport, the way the date picker
already does (ITEM-024 / spec 022).

## Notes

- **Why it is capped.** `.editor__picker-menu` is `position: absolute` inside `.editor__picker`, and
  the scroll container `.editor__content` has `overflow-y: auto`, so anything past the dialog's box is
  clipped. `placeMenu()` in `static/web/entries.js` measures `.editor__content` and clamps each menu's
  `max-height` to the room inside it, flipping up or down.
- **The precedent.** The date picker already escapes the dialog: `.editor__date-calendar` is
  `position: fixed; z-index: 20`, positioned by JS (`static/web/date-picker.js`), with
  `max-height: calc(100vh - 16px)` (ITEM-024 / spec 022).
- **The change.** Make the picker menu `position: fixed`, positioned from the trigger's rectangle,
  capped to the viewport rather than the dialog; keep the up/down flip and the scrolling options.
  Cover both the add and edit modals (the same fragment and JS serve both).
- **Coherence.** The menu must sit above the dialog's backdrop and stay anchored while the dialog's
  content scrolls, or close on scroll.

## Open questions

- Does the verses picker (the song modal's second dropdown) get the same treatment, or only book and
  song?
- On the dialog's content scrolling, reposition the fixed menu or close it?
- Keep the current 268px cap, or use the viewport room on the chosen side?

## Acceptance sketch

- The book and song menus can overlap the dialog's edge and never leave the window.
- A menu with no room below flips above the trigger, and its options scroll.
- The menus in both the add and edit modals behave the same.
- The menu is never clipped by the dialog's scroll area.

## Links

- Spec: [040 — Let the entry modal picker menus extend past the modal](../../specs/040-picker-menus-past-modal/spec.md)
- Related items: ITEM-024 / spec 022 (date picker over the modal), ITEM-006 / spec 005 (entry modals)
