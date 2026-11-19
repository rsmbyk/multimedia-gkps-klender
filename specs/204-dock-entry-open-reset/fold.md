# Fold: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`
**Converged**: 2026-11-19, pass 1 (`converge.md`)
**Capability touched**: `dock` (`docs/spec/dock.md`)

## Operations

| Capability | Requirement | Operation | What changed |
| --- | --- | --- | --- |
| `dock` | R14 — An entry header expands its block; only an item jumps | **modified** | the override's lifetime: hand-opened blocks now survive a crossing **and a re-read**, and do not survive an **explicit open of a service** (picker click, picker `Enter`, on-load resume) nor a reload. The open starts every block shut except the live entry's, whose liveness is read from the display state; the reset writes no state, broadcasts nothing and animates nothing. Two scenarios added: *a service is opened after a hand-open*, *the on-air service is opened*. The citation becomes `(specs 198, 204)`. |

No requirement was added, removed or renamed: R14 already owned the header's disclosure behaviour
and the override's lifetime, so the delta is a modification of its block, written in full.

## Header

- `last folded`: 2026-11-19 (unchanged date — spec 205 folded earlier the same day).
- `slices`: `204-dock-entry-open-reset` prepended.

## Counts

| | before | after |
| --- | --- | --- |
| requirements in `dock.md` | 16 (R1–R16) | 16 (R1–R16) |
| scenarios under R14 | 4 | 6 |
| capabilities touched | — | 1 (`dock`) |

## Not folded

Nothing. Every converged row maps to R14's modification; the two base-identical reds in
`test_obs_dock_follow.py` are `ITEM-215`'s demand, not behaviour this slice changed, and the
preview's revision marker is a preview affordance, not product behaviour.

## Idempotence

Re-running this fold finds R14's block already carrying the open-reset rule and the two scenarios,
and the slice id already in the header: no further change.
