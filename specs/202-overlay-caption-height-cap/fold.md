# Fold: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md`
**Date**: 2026-11-19
**Outcome**: folded (converged, no accepted gaps)

## Capabilities touched

| Capability | File | Operations | Before | After |
| --- | --- | --- | --- | --- |
| `overlay` | `docs/spec/overlay.md` | 1 `modified` (R2) + 1 `added` scenario, 1 scenario updated | R2 carried `clamp(11px, 3.75cqw, 80px)` rest, an 11px floor, a 1728×202/72px 1080p baseline and a 5-row/403.19px wrap baseline | R2 names a 5 % stage-height rest, a 2 % floor, the 6 % step and the accepted edge; the 1080p baseline is 1728×151.2 at (96, 874.8), 54 px; the wrap baseline is 33.81px/1 row; a new scenario pins 36px at 720p |

`R2`'s number is preserved — the rule it names changed, not the requirement's identity. `reading.md`
and the plate rules are untouched.

## Scenario delta

| R2 scenario | Operation |
| --- | --- |
| a two-line lyric at 1080p | `modified` — new box and size |
| the rest follows the stage height | `added` |
| a lyric that would wrap | `modified` — 6 % steps, 2 % floor |
| a lyric the floor cannot save | `modified` — floor is 2 % of the stage |
| a lyric with no space in it | `modified` — remeasured live |

## Counts

- Requirements in `overlay.md`: unchanged (R2 modified in place).
- Scenarios in R2: 6 → 7.
- Capability files touched: 1.
