# Fold — spec 205 (dock centre pace)

**Date**: 2026-11-19
**Capabilities touched**: `dock` (`docs/spec/dock.md`).

## Operations

| Capability | Requirement | Operation | Detail |
| --- | --- | --- | --- |
| dock | R15 | modified | The centring motion sentence: 400 ms softened in-out (half sine, half smootherstep) → 200 ms sine in-out (half-cosine), shared by the glide and the crossing morph's carried scroll; hand block-toggle's 230 ms ease-in-out noted as separate (R14). The mode/trigger/idle rules of R15 are unchanged. |

## Counts

- `dock` requirements before: 15 (R1–R15) · after: 15. R15 modified in place; none added, removed or
  renamed.
- Header `last folded` moved 2026-11-18 → 2026-11-19; slice `205-dock-centre-pace` prepended.

## Not folded

None — the slice Converged with no accepted gaps. The per-crossing collapse-clamp reversal is a
behaviour this slice deliberately did not change (research D4), so there is no delta to fold for it.