---
id: ITEM-251
status: speccing
title: 'The new/edit song entry modal paints a scrollbar on its own edge'
type: fix
priority: P2
effort: S
created: 2026-11-24
updated: 2026-11-24
spec: 236-song-modal-scrollbar
branch: fix/236-song-modal-scrollbar
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-251: The new/edit song entry modal paints a scrollbar on its own edge

## Summary

The shared editor dialog keeps the browser's default `overflow: auto`. The collapsed song-entry
Verses panel leaves a few clipped pixels past the dialog box, so the dialog itself scrolls and
paints a scrollbar on its rounded right edge even though every field is visible.

## Notes

The content wrapper is already the intended scrollport (`overflow-y: auto; min-height: 0`); the fix
is one declaration on `.editor`. The verse panel's animated collapse stays as it is. Spec 235 can
change what the collapsed panel shows without changing which element scrolls.

## Acceptance sketch

- New song: dialog gutter `0px`, computed `overflow-y: clip`, no wheel movement.
- Edit song with no verses: same; edit with verses keeps its box.
- Tall forms still scroll inside `.editor__content`; the fixed song results menu still escapes the dialog.

## Links

- Spec: [236-song-modal-scrollbar](../specs/236-song-modal-scrollbar/spec.md)
- Related items: —
