---
id: ITEM-265
status: done
title: 'The live entry header pins at the top as soon as it is clipped'
type: fix
priority: P2
effort: S
created: 2026-11-28
updated: 2026-11-28
spec: specs/248-dock-top-pin-early/spec.md
branch: feat/248-dock-top-pin-early
pr: 640
issue: 639
closed_at: 2026-11-28
closed_reason: merged into develop (PR #640)
bump: patch
release_version: 1.37.9
---

# ITEM-265: The live entry header pins at the top as soon as it is clipped

## Summary

Spec 242 pinned the live header at the top only once its whole entry block had passed above the
runner's scrollport. The owner asked for the pin to start as soon as the header itself goes off
screen, mirroring spec 208's bottom pin. Through the question tool the boundary was settled as the
header's own top crossing the fold, with the clone taking over from the sticky header at that exact
point.

## Notes

- Measured on the live dock: first pin moved from scrollTop 1164 to 1056 (108 px earlier); at
  takeover the real header's top and the clone's top are both 0 px, so there is no hop.
- The clone keeps spec 242's face (flat top, 9 px round bottom, faithful label) and click act
  (re-centre, no screen write, following returns); the source is hidden with `visibility: hidden`
  while covered, keeping one painted header without moving the list.
- A carried-over Go To claim was found false on develop as well as the slice; it is recorded as a
  retraction in research D006, not silently rewritten.
- Gate 1 accepted 2026-11-28; gate 2 accepted 2026-11-28. `bump: patch` declared at Plan.
  Anchor issue #639 created at Ready (board custom).

## Acceptance sketch

- With a deep entry live, scrolling until the header reaches the fold shows the pinned clone while
  the block still straddles the list; the source header is hidden, so only one is painted.
- The clone holds at 0 px when the whole block clears the fold; scrolling back yields to the native
  sticky header on that frame.
- Bottom pin, NEXT band, go-to strip and the click act are unchanged; reduced motion lands the pin
  in the same paint.

## Links

- Spec: `specs/248-dock-top-pin-early/spec.md`
- Related items: ITEM-257 (spec 242 — the whole-block top pin), ITEM-221 (spec 208 — the bottom pin),
  ITEM-219 (spec 208 — the corner state), ITEM-210 (spec 200 — following and the centre act)
