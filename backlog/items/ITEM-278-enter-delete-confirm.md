---
id: ITEM-278
status: in review
title: 'Enter accepts a delete confirmation'
type: feat
priority: P1
effort: S
created: 2026-11-28
updated: 2026-11-29
spec: specs/256-enter-confirms-delete/spec.md
branch: feat/256-enter-confirms
issue: 655
pr: 656
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-278: Enter accepts a delete confirmation

## Summary

Pressing Enter while a delete confirmation is open activates its destructive control, wherever focus
sits. The same rule covers the sidebar record, stage entry, stage old row, verse and Media Library
removal confirmations; non-destructive confirmations keep their own Enter behaviour.

## Notes

- The live before/after probe measured 0 to 1 delete POST on the stage, sidebar and verse confirmations
  and 0 to 1 Remove-file click in the Media Library, with one press and focus away from the control.
- One capture-phase `keydown` handler in `static/web/enter-delete.js` activates the single visible
  `[data-enter-delete]` control; each control keeps its existing delete handler, feedback and focus
  restoration. Guards cover hidden/closed/disabled controls, repeated keys, modified chords and
  already-prevented events.
- The old Fomantic/OBS delete modals are retired by spec 194 and their addresses redirect, so no live
  page carries the rule there.
- Gate 1 and gate 2 were accepted on 2026-11-28 with `bump: patch`. The tracker anchor and PR number
  are filled on the push that opens the PR.

## Acceptance sketch

- Enter with focus away from Delete sends exactly one delete request and closes the confirmation.
- Enter with focus on Cancel still deletes; Enter on a non-destructive confirmation changes nothing.
- Repeat, modifier chords, disabled controls and closed or hidden layers produce no activation.

## Links

- Spec: [256](../specs/256-enter-confirms-delete/spec.md)
- Related items: [ITEM-277](ITEM-277-modal-scroll-containment.md) (other modal rule), [ITEM-190](ITEM-190-sidebar-delete.md) (sidebar delete).
