---
id: ITEM-257
status: in-review
title: 'The live entry header leaves the top when its block goes off-screen'
type: feat
priority: P2
effort: S
created: 2026-11-25
updated: 2026-11-25
spec: specs/242-dock-top-pin/spec.md
branch: feat/242-dock-top-pin
pr: 622
issue: 621
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-257: The live entry header leaves the top when its block goes off-screen

## Summary

The runner's live header is sticky at the top only while its own entry block straddles the
scrollport; once that block is wholly above the fold the label is gone. The bottom half already
has a pinned representation (spec 208 / `dock/R18`). The owner asked for the same at the top:
"can you make the entry headers to stay pinned at the top when the entry is off-screen just like
the bottom pin?" Scope settled through the question tool: **live entry only**.

## Notes

- The header is the first child of its `li`, so sticky cannot keep it past the block; a
  list-level slot at the front of `#entryList` holds a faithful clone of the live header while
  the whole block is above the scrollport.
- The clone mirrors spec 208's bottom pin: selected face, flat top / round bottom, no
  `aria-current`, click = re-centre the live row and return to following, screen unchanged.
- The state is reconciled on every geometry path (scroll, sync, glide first paint, morph, resize)
  and instantly under reduced motion; the NEXT band and bottom pin are untouched.
- Gate 1 accepted 2026-11-25; the card moved from `Backlog` to `Ready` on that word. `bump: minor`
  is declared at Plan for the new `dock/R19`. Anchor issue #621 created at Ready (board custom).

## Acceptance sketch

- With the live block above the fold, one faithful header copy stands flush at the top edge,
  top radius 0 px, bottom radius 9 px; no second header while the real one is in view.
- Per frame, visibility equals the geometry; hand scroll and a click both return control to the
  native header with no screen write.
- Existing dock behaviour — the bottom pin, the always-visible NEXT band, the go to strip — stays
  as it is.

## Links

- Spec: `specs/242-dock-top-pin/spec.md`
- Related items: ITEM-219 / ITEM-221 (spec 208 — corner state and the bottom pin), ITEM-208 (spec
  198 — header/block anatomy), ITEM-210 (spec 200 — following and the centre act)
