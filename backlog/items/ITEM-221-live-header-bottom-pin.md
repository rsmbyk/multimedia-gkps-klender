---
id: ITEM-221
status: in review
title: 'The live entry header pins to the bottom when it would be cut off'
type: feat
priority: P2
effort: M
created: 2026-11-20
updated: 2026-11-20
spec: specs/208-dock-stuck-corner/spec.md
branch: fix/208-dock-stuck-corner
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/551
issue:
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-221: The live entry header pins to the bottom when it would be cut off

## Summary

The owner's ask (2026-11-20, while spec 208 sat at gate 1): "can you also do the same when the
live-entry headers going partially out of screen at the bottom (pin it to the bottom)". Today the
live header pins only at the top edge; when the operator scrolls above the live entry (browsing)
or projects a far-down entry without re-centring, the header sits partially cut at the bottom
edge. The live label should stay fully visible, pinned flush at the bottom edge, with the same
corner treatment the top pin wears — flat edge while pinned, round in flow.

## Notes

- **Mechanism finding (measured against the DOM, 2026-11-20):** the header node itself cannot
  bottom-pin. A sticky element pins only toward room inside its containing block: the header is
  the entry's FIRST child (room below → top pin works; an upward shift would leave the li, which
  sticky forbids). The NEXT band is the LAST child (room above → `bottom: -10px` pin works).
  The feasible shape is the dock's own proven band pattern: a bottom-pinned strip carrying the
  live entry's label, shown when the header would be cut at the bottom edge — visually the
  header pinned to the bottom.
- Builds on spec 208's `updateStuck()` per-frame tracking: the bottom state is the same
  geometry read at the other edge, and the flat-bottom corner class mirrors `.is-stuck`.
- Open design points for Clarify: (1) the NEXT band wants the same edge in that state (the live
  block extends below the viewport, which is the band's show condition) — stack the band above
  the live strip, or hide the band while the strip is up; (2) trigger scope — partially cut only
  (the owner's words) or also fully off below (the 15 s idle re-centre already covers fully-off);
  (3) the strip's click — re-centre the live row (return to following) is the natural act;
  (4) reduced motion and the yield rule when the header scrolls back into full view.
- Sequence: **folded into spec 208 before gate 1** (owner's ruling, 2026-11-20) — US4 of
  `specs/208-dock-stuck-corner/spec.md`, on the same branch; the fix stories' gate-1 acceptance
  stands, the combined pack awaits a fresh gate-1 showing.

## Acceptance sketch

- With the live header partially below the bottom edge, the live label stands fully visible,
  flush at the edge, flat bottom corners; scrolling it back into full view returns the round
  corners and removes the pinned representation — per frame, no hand scroll needed.
- The NEXT band and the bottom pin never paint over each other; one ruled interaction.
- The top pin and its corner state (spec 208) are unchanged.

## Links

- Spec: — (awaits the owner's pick and sequencing)
- Related items: ITEM-219 (spec 208 — the corner state follows the pin), ITEM-210 (spec 200 —
  following and the named centring acts), ITEM-208 (spec 198 — the header/block anatomy)
