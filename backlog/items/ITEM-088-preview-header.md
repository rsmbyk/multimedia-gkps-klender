---
id: ITEM-088
status: in-review
title: Show the entry's identity in the Preview header
type: feat
priority: P2
effort: M
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/085-preview-header/spec.md
branch: fix/085-preview-header
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/339
archived_at:
archive_reason:
bump: patch
release_version: 1.10.6
---

# ITEM-088: Name the entry in the Preview dialog's header

## Summary

The entry Preview dialog has no header (spec 032 built it headerless), so what is being previewed is
only shown by a line inside the scroller. Move each kind's identity into a fixed header — and a song's
verse tabs with it — leaving an untitled Text entry with no header at all.

## Notes

- Per kind: Text title, passage reference, song heading `HAL 3 — Sai puji Naibata`.
- The header sits outside the scroller; the body keeps the scroll, its padding, and its arrow-key
  handling.
- `wireTabs()` currently queries inside `#previewContent`; moving the tabs out means it has to widen its
  scope or the tab clicks die.
- No close button: Escape, the overlay, and the entry pane stay the ways out.
- Draft only — no implementation until the owner accepts Spec 085.

## Acceptance sketch

- A titled Text entry shows its title in the header and not in the body; an untitled one shows no header.
- A passage shows its reference; a song shows its heading and its verse tabs.
- The header does not scroll; dismissal and the origin highlight behave as before.

## Links

- Spec: [Spec 085](../../specs/085-preview-header/spec.md)
- Preview: [preview header](../../specs/085-preview-header/preview.html)
- Related items: ITEM-034 (entry preview modal), ITEM-076 (verse tabs), ITEM-073 (single-screen breaks)
