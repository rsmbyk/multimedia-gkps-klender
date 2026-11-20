# Fold: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`
**Date**: 2026-11-16
**Outcome**: folded (converged with one observed consequence, no accepted gap)

## Capabilities touched

| Capability | File | Operations | Before | After |
| --- | --- | --- | --- | --- |
| `reading` | `docs/spec/reading.md` | 1 `modified` (R33) | R33 carried "a bucket head SHALL keep sticking to the top of the picker's scroller" and listed the head's padding among the metrics that must not change | R33 states that the head owns the strip above its label (its box starts at the scroller's own top edge, 14px top padding, no body top padding, the label 14px below the divider at rest and pinned, the foot unmoved, the 37px reserve), and that consecutive buckets carry 12px of air on the section; the "no other metric" list drops the head's padding, which this slice changes |

`R33`'s number is preserved — the behaviour it names changed, not the identity of the requirement. `dock.md`
is not touched: the runner, the go to and the display state are unchanged, and the picker's requirements have
lived in `reading.md` since spec 164.

## Scenario delta

| R33 scenario | Operation |
| --- | --- |
| the scroller | `modified` — the head's box starts at the scroller's top and no row paints above it; the label's 14px is named |
| two buckets meet | `added` |

## Counts

- Requirements in `reading.md`: unchanged (R33 modified in place).
- Scenarios in R33: 4 → 5.
- Capability files touched: 1.

## Not folded

Nothing — the converged slice had no accepted gap. The one observed consequence (`converge.md` finding 1: the
picker's empty-state line sits 4px higher because it shares the scroll body) changes no requirement, so there
is nothing to fold and nothing to list as an accepted gap.