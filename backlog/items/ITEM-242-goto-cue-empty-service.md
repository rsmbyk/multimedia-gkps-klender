---
id: ITEM-242
status: in-progress
title: 'A Go To with no service under it has no cue'
type: fix
priority: P1
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 227-goto-cue-empty-service
branch: fix/227-goto-cue-empty-service
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-242: A Go To with no service under it has no cue

## Summary

Opening a Go To while the projector has no service, or a service with no entries, paints the detour
but leaves the corner cue blank. `renderCue()` returns on an empty entry list before it reaches the
detour branch, so the passage or song label and its controls are never drawn.

## Notes

- The defect is guard order in `static/web/projector.js` `renderCue()`: `!entries.length` returns
  before `if (detour) { renderDetourCue(); return; }`.
- `renderDetourCue()` already handles a missing return entry by naming `service`; no change is needed
  in it.
- Both cases reproduce at 420×800: the detour is active and the cue prefix reads empty.
- The empty-service notice is a stage sibling and is hidden while the detour is up; it is not a
  signal for whether the cue may paint.

## Acceptance sketch

- A projector with no service, or on a service with no entries, still names the Go To in the cue.
- A passage offers its translation flip; a song offers one bait button per bait; Back reads
  `back to service`.
- The populated-service cue path and the empty notice's return after Back are unchanged.

## Links

- Spec: [227](../specs/227-goto-cue-empty-service/spec.md)
- Related items: ITEM-174 (the shared Go To state, spec 187), ITEM-210 (the dock's live block)
