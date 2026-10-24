---
id: ITEM-125
status: done
title: 'Keep a chapter''s verse text when both Bible editions share a book name'
type: fix
priority: P1
effort: S
created: 2026-10-24
updated: 2026-10-24
spec: specs/124-bible-edition-block-identity/spec.md
branch: fix/124-bible-edition-block-identity
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/373
issue:
closed_at:
closed_reason:
bump: patch
release_version: 1.20.2
---

# ITEM-125: Keep a chapter's verse text when both Bible editions share a book name

## Summary

Opening a chapter of a book whose TB and SIM names match (Rut, Ezra, Nehemia, …) in the reading sidebar
leaves the stage blank until a reload, and the translation switch stops responding. The in-place
reconciler keyed both rendered edition blocks by the shared book label, so it merged the hidden SIM block
into the TB block and dropped the visible text.

## Notes

- The fix is one identity ordering in `static/web/reading.js` (`data-ed` before `data-name`).
- The saved library renders the same blocks and inherits the fix; no separate change.

## Acceptance sketch

- Opening such a chapter in place shows its verse text, as a direct load does.
- Moving between its chapters and switching TB/SIM keep working.
- Books whose names differ, direct loads, and the saved copy behave as before.

## Links

- Spec: [124](../../specs/124-bible-edition-block-identity/spec.md)
- Related items: ITEM-119, ITEM-122
