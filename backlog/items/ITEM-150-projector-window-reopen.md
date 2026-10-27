---
id: ITEM-150
status: ready
title: 'A closed projector window cannot be reopened without stopping the projection'
type: fix
priority: P1
effort: S
created: 2026-10-27
updated: 2026-10-27
spec: specs/141-projector-window-reopen/spec.md
branch: feat/141-projector-window-reopen
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-150: A closed projector window cannot be reopened without stopping the projection

## Summary

A Tata Ibadah service on air cannot be reopened after its projector window is closed. The service
page's only projection control is Stop projecting, which releases the display; the next Project opens
`/projector?service=<id>` and writes `show(service, 0)`, so the service restarts at its first screen
and the operator has to walk back to the screen they were on. Spec 119 removed the window-close
reaper on purpose — the display outlives every surface — but nothing on the page opens the projector
window again.

## Notes

- Owner report, 2026-10-27, with a screenshot of the service page showing Stop projecting.
- The bare `/projector` page already renders the stored state at the stored screen; only the control
  that reaches it is missing.
- Fix: a 34×34 icon-only control beside Stop projecting while this service is on air; it opens the
  window at the on-air screen and focuses it when it is already open. Icon-only because the pane is
  240 px at a 1280 window, where the live group with Media files already measures 238.4 px.

## Acceptance sketch

- With the service on air and the window closed, the control reopens the window at the screen on air.
- Pressing it changes no state and does not stop the projection; Stop projecting still releases.
- An already-open window is brought forward, not reloaded.
- The group never spills past the pane, at 1440 or 1280; neither control is drawn at the phone width.

## Links

- Spec: [141](../specs/141-projector-window-reopen/spec.md)
- Related items: [ITEM-119](./ITEM-119-obs-dock.md) (the display state and the removed reaper)
