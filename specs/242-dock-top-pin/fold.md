# Fold — spec 242

**Date**: 2026-11-25 · **Slice**: `242-dock-top-pin` · **Converged**: see [converge.md](./converge.md)

## Capabilities touched

- `dock` — one operation: `added` — `dock/R19` (the live header's off-screen top pin) with three
  scenarios: the block passes above the fold, the real header takes the edge back, and the pin
  tracks the glide per frame.

## Header

- `last folded`: 2026-11-20 → **2026-11-25**.
- `slices`: prepended `242-dock-top-pin`; every incoming slice ID from the base header is kept in
  its original order.

## Counts

| Item | Before | After |
| --- | --- | --- |
| `docs/spec/dock.md` requirements | 18 (R1–R18) | 19 (R1–R19) |
| Slice IDs in the header | 10 | 11 |

## Operations

- Added a full requirement block after R18; no existing block was edited, removed or renamed.
- Capability IDs checked against `docs/spec/dock.md` at the slice's base (`56b3dcbf`): R19 was
  free; no unmerged sibling claims it (checked `develop`, `origin/develop`, local unmerged
  branches and untracked worktree packs).
- No behaviour change outside the added requirement: the bottom pin, NEXT band, corner state, go
  to strip and header wash are unchanged (inspection in Converge).

Idempotent: re-running Fold on the folded tree finds R19 already present and makes no second entry.
