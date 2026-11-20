# Fold: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md`  
**Date**: 2026-11-19  
**Status**: Converged

## Capabilities touched

| Capability | Operation | Before | After |
| --- | --- | --- | --- |
| `dock` | modified | R14 has one clause about hover fill; open headers carry no wash | R14 adds the open‑header wash clause: 4 % rail‑and‑ink, half the hover step, source order after base and before hover |

## Operations

- **Modified** `dock/R14` — one added clause:
  - An open header SHALL wear one flat wash of its rail mixed 4 % ink —
    `color-mix(in srgb, var(--rail-bg) 96%, var(--ink))` — for as long as its block stands open, a
    step softer than the hover face so the pointer stays the louder state; the wash rides the row's
    own 200 ms background ease and adds none of its own, and the live row's selected fill always
    outranks it (spec 198, wash spec 206).
- **Added** scenarios:
  - **an open header wears the wash** — when a non-live header's block stands open, then its whole
    line, chevron included, carries the 4 % rail‑and‑ink wash — softer than the hover face, which
    replaces it under the pointer — and closing the block returns it to bare rail.

## Before / after counts

- R14 was 4 acceptance scenarios; now it is 5.
- Capability rule count: 14 → 14 (one modified, not added).
- No other capability file is touched.

## Notes

- The rule is `color-mix(in srgb, var(--rail-bg) 96%, var(--ink))`, following the same expression
  pattern as `.nextband:hover` (92 % / 8 %).
- No new token. The rule is one consumer of the value; a token would name a number that nothing else
  shares.
- The live row is always `aria-expanded="true"`, so its `[aria-current="true"]` rule must stay after
  the open rule — source order is the cascade. The preview proved this the hard way: appended after
  the sheet, the rule beat hover and the live row; spliced in at its shipping position, all three
  states compute correctly.
- The wash is a state, not a transition: it belongs to a header while its block is open. The row's
  existing `background var(--ease)` carries the tint on and off; the slice adds no new transition.
- Reduced motion already governs the row's background; no new reduce rule is owed.