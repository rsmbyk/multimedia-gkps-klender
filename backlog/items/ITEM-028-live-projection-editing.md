---
id: ITEM-028
status: in_progress
title: 'Keep editing while projecting, and follow every change'
type: feat
priority: P1
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/026-live-projection-editing/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: minor
release_version: 0.12.0
---

# ITEM-028: Keep editing while projecting, and follow every change

## Summary

Let the operator keep working while a Tata Ibadah is on screen: add, edit, delete and reorder are no
longer refused during projection; a reorder is written the moment it is dropped (no Save/Discard);
and the projector follows every add, edit, delete and reorder without the operator pressing Update.

## Notes

- The current edit ban is client-side only (`gkpsDisplay.locked()` in `display.js`, consulted by
  `entries.js` and `reorder.js`); the server has no projection guard. Lifting it is a shell change.
- The reorder mode's Save/Discard strip, leave-confirm dialog, and unsaved-leave guard are removed;
  a drop and a keyboard move persist at once, with writes serialised to the newest order.
- The display stays a same-browser popup over the existing channel — no server push, no new deps.
  OBS browser sources and second-laptop fan-out are deliberately out of scope.
- Supersedes ITEM-023 / spec 021 (which kept the lock and only hid its explanation) and amends the
  spec 006 lock and reorder-mode rules.

## Acceptance sketch

- With a Tata Ibadah projecting, adding, editing, deleting and reordering an entry are all allowed.
- Dropping an entry reorders it immediately; reloading the service returns the dropped order.
- Leaving or switching pages after a reorder never prompts.
- The open projector reflects an add, edit, delete and reorder without pressing Update; Update still
  works.

## Links

- Spec: [026 — Keep editing while projecting](../../specs/026-live-projection-editing/spec.md)
- Related items: ITEM-007 (service entries), ITEM-023 (projection-lock note, superseded),
  ITEM-020 (projection button styles), ITEM-002 (projection source + controls)
