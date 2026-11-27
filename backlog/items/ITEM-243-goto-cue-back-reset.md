---
id: ITEM-243
status: done
title: 'Back leaves the Go To information in the cue over an empty stage'
type: fix
priority: P1
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 228-goto-cue-back-reset
branch: fix/228-goto-cue-back-reset
pr: 598
issue: 597
closed_at: 2026-11-23
closed_reason: merged into develop (PR #598)
bump: patch
release_version: 1.37.3
---

# ITEM-243: Back leaves the Go To information in the cue over an empty stage

## Summary

After spec 227, the corner cue names the Go To over a projector with no service or no entries.
Leaving it does not clear the cue: the empty-stage early return in `renderCue()` leaves the detour's
label, flip, baits and Back in place while the state and the stage are already back to idle.

## Notes

- Measured on the merged code at `4ea9a6ab`: with `goto: null`, `detour: false` and zero screens the
  cue still reads `· HAL 1 Jahowa Sihol Pujionku ·12345671/2 back to service` with seven baits.
- The clear belongs in `renderCue()`'s empty branch: `leaveDetour()`, the dock's Back via
  `applyGoto()`/`paintIdle()`, and `rereadSession()` all reach it.
- The idle cue shows no visible text; the `.cue-service` button stays as the operator's controls
  surface.
- Spec 227's detour cue is unchanged; only its removal is fixed.
- Revision: the idle empty stage also hides the cue's centre-dot separator and its next button's
  lone arrow, disables the edge and centre mouse zones and stops cursor auto-hide; fullscreen,
  service list, keys and find stay.

## Acceptance sketch

- Back over no service, or over a service with no entries, clears the passage or song label, flip,
  baits, progress and Back from the cue.
- Back from the dock clears the projector's cue through the shared state.
- The idle empty stage also drops the cue's centre dot and phantom mouse zones, keeping fullscreen
  and the cue's own controls.

## Links

- Spec: [228](../specs/228-goto-cue-back-reset/spec.md)
- Related items: ITEM-242 (spec 227, the cue that now needs clearing)
