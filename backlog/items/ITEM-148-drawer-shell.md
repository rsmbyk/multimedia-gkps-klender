---
id: ITEM-148
status: in-progress
title: 'On a small screen the sidebars are a drawer stack; a phone gets a toolbar'
type: feat
priority: P1
effort: L
created: 2026-10-27
updated: 2026-10-27
spec: specs/138-sidebar-overlay-stack/spec.md
branch: feat/138-sidebar-overlay-stack
pr:
issue:
closed_at:
closed_reason:
bump: minor
release_version: 1.22.0
---

# ITEM-148: On a small screen the sidebars are a drawer stack; a phone gets a toolbar

## Summary

Below 1272px the three columns still push each other, so a 768px window spends 440px on the rail
and the service list and squeezes the reading pane into 328px; on a 425px phone the icon strip costs
a tenth of the width and its glyphs are unlabelled.

The sidebars become drawers over the page: one section's stack at a time, the second level covering
the first, a backdrop that closes them, a rail that reopens the level last used. A phone swaps the
strip for a top toolbar — control, logo, theme — whose control opens the menu and closes whatever is
open, with the rail itself as a labelled menu drawer.

## Notes

- Owner request with two screenshots (768px and 425px), refined over five rounds against a live
  prototype: the parent edge, the phone inset, the toolbar's order and the control's glyphs, the
  phone's menu contents, the Project control, the service-list behaviour, the edit control's
  visibility and the row's two lines.
- The desktop above 1272px is untouched.
- The shell's own state: `data-nav`, `data-ch`, and two new attributes `data-rail` and
  `data-drawer-open`.
- A row's edit control was hover-only even under a touch pointer — the exemption the entry controls
  already had was never extended to `.row-edit`.

## Acceptance sketch

- At 1024 and 768 the stage keeps its width while a drawer opens; at 1440 the columns still push.
- The second level covers the first exactly; both slide out from under the rail.
- The backdrop and Escape close the stack; the rail reopens the level last used.
- A phone shows one toolbar, a full-width menu drawer with names, and full-width drawers.
- A service on a phone offers no contents drawer; its rows open the page and close the drawer.
- A row's pencil is always visible on touch, and the row stacks its date under its name.

## Links

- Spec: [138](../specs/138-sidebar-overlay-stack/spec.md)
- Related items: ITEM-145 (the contents rows' clamp), ITEM-136 (the sidebar's date buckets)
