# Fold: An empty song names itself in the Verses section

**Date**: 2026-11-24
**Converged**: pass 1, zero gaps, zero accepted gaps.

## Capabilities touched

| Capability | Operation | Requirement |
| --- | --- | --- |
| `reading/R30` | `modified` | A picked song with no live verses shows the Verses section collapsed to its summary row instead of hiding it; spec 210's hidden-section answer is kept as a superseded note. |
| `reading/R48` | `modified` | The picker's empty state collapses the body rows under `data-empty="true"` with no second animation phase; the 200 ms reveal, tiles and mute rules are unchanged. |

## Before / after

- `R30`: 1 requirement block, 4 scenarios, 2 superseded notes → 1 block, 6 scenarios, 3 superseded notes.
- `R48`: 1 requirement block, 5 scenarios → 1 block, 6 scenarios; the empty-song clause and one scenario added.
- Header `last folded`: 2026-11-23 → 2026-11-24; slice `235-empty-song-verse-summary` prepended.
- No capability added, renamed or removed; no other file in `docs/spec/` touched.

## Not folded

None. Every converged requirement was folded; no accepted gaps exist.

## Merge-time note

- Spec 234 landed on `develop` while this slice was open and took patch 1.36.20; VERSION on this branch was re-taken to **1.36.21** before the merge. No card or spec number collided (ITEM-250 and spec 235 stayed free).
