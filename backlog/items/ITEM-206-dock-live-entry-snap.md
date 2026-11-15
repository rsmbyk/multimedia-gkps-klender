---
id: ITEM-206
status: in-progress
title: 'The runner keeps its live entry in view'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: specs/196-dock-live-entry-snap/spec.md
branch: feat/196-dock-live-entry-snap
pr:
issue: 525
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-206: The runner keeps its live entry in view

## Summary

The dock's runner re-centres its live entry on every state notice — unless a hand has been on the
list, which cancels a pending centring. A member of the team who scrolls away leaves the on-air
entry entirely off the screen, and nothing brings it back until the next state change. The request
(2026-11-15, chat, three screenshots): when the live entry is entirely out of the scroll area — far
off the top or far off the bottom — it should snap into view edge-aligned, the way a long entry
pins while it is on screen.

## Notes

- Today `scheduleCenter()` re-centres on every sync with `live && !morphing`
  (`static/web/obs-dock.js`); a crossing morph brings its own 230 ms curve instead, and a hand on
  the list (`wheel` / `pointerdown`) cancels any pending centring or glide.
- The pinned look already exists: `.entryrow[aria-current="true"]` is `position: sticky; top: -4px`,
  flush at the list's top edge, with its `.entryinner` block open beneath it.
- The bottom end-state leaves the sticky `.nextband` — labelled with the next entry — pinned at the
  list's bottom edge and visible above the live entry's foot.
- The centring rule spec 119 pinned ("recenters the current row vertically on every move, 190 ms
  ease-out, clamped at the ends") was never folded into `docs/spec/dock.md`; this slice folds a full
  rule for the scroll behaviour, citing spec 119.
- The open semantics — what moments fire the snap, what a partial exit keeps — are the slice's
  Clarify questions, not settled here.

## Acceptance sketch

- With the live entry entirely above the scroll area, the runner scrolls so its entry row sits
  flush at the list's top edge, its block open beneath it.
- With the live entry entirely below the scroll area, the runner scrolls so its foot sits just
  above the NEXT band at the list's bottom edge.
- A live entry that is even partly in view keeps today's centring.

## Links

- Spec: [196](../specs/196-dock-live-entry-snap/spec.md)
- Related items: ITEM-119 (the runner itself, spec 119), ITEM-189 (the runner's Go To, spec 185),
  ITEM-191 (the dock's keyboard grammar, spec 187), ITEM-177 (the dock fills its panel, spec 164)
