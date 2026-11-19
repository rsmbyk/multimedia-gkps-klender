# Fold: The first sidebar's idle rule, restored and set to fifteen minutes

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-18
**Outcome**: folded (converged, no accepted gap)

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R44` | The first sidebar rests fifteen quiet minutes: the armed conditions, the closed six-event activity surface on the rail and first panel, `scroll` in capture so descendant scrollers count, focusout, the hidden tab, the mini/closed outcomes, and the absence of a setting. Restores the rule spec 072 accepted but never folded. |
| `added` | `R45` | The four deferral conditions, the 1 s re-check, and the full interval that restarts the moment the last condition clears — from the condition's state, never from a seventh activity event. Completes spec 072's second clause. |

`R44` and `R45` are new numbers; the capability tree previously ended at `R43`. Existing
requirements are untouched — spec 072's sentence was never folded into `reading.md`, so this slice
adds the rule rather than modifying a requirement that does not exist there.

## Drift guard

- **Files changed in this capability**: `docs/spec/reading.md` (header's `last folded` and `slices`
  line, plus the two appended requirements).
- **Declared no behaviour change**: no — the idle delay moves from 60 000 ms to 900 000 ms, a
  descendant `scroll` now restarts the interval, and a deferral ending restarts it immediately.
  All three are stated in the two added requirements and covered by the traceability table.

## Counts

- Requirements in `reading.md`: 43 → 45.
- Scenarios added: 6 (three in R44, three in R45).
- Capability files touched: 1.

## Not folded

Nothing — the converged slice had no accepted gap. The one test still red in
`tests.e2e.test_reading.py` reproduces on unmodified develop and is carded separately as ITEM-137;
it is not a behaviour of this slice.
