# Fold: a text screen arrives as fast as the entries beside it

**Date**: 2026-11-22
**Capabilities touched**: `projector`

## Operations

| Capability | Operation | Requirement | What the reader now sees |
| --- | --- | --- | --- |
| `projector` | `added` | `R14 — A screen of words is fitted where it rests, and before it is asked for` | The projector fits a screen at the geometry it comes to rest in, so an advance and a resize agree; it walks the sizes from the top down because a refusal is not monotone; the screens either side are fitted in idle time and a screen already fitted is not fitted again on arrival; every remembered fit is discarded when the bundled faces arrive; and a single-screen body too long for any size is cut by halving, keeping the same rows and characters. |

The requirement is new because nothing in `projector/R1`–`R13` says when a screen is fitted. The
behaviour it protects existed before this slice and was never folded: the fitting has walked the sizes
from the top down since spec 006, and the single-screen cut since spec 031.

## Counts

- Requirements before: 13 · after: 14.
- Slices listed in the header: 12 entries before (with repeats), 13 after.
- `last folded` moved 2026-11-14 → 2026-11-22.

## Not folded

- Nothing. Converged with no accepted gaps (`converge.md`).
