# Fold: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Date**: 2026-11-21 · **Slice**: `211-overlay-turn-hang`

## Capabilities touched

- `overlay` — one `modified` operation.

## Operations

- `modified` — the complete replacement block for `docs/spec/overlay.md` `R5 — A speaker mark sits
  in a column of its own`. Its rule now carries the continuation line at the same column and gap,
  the no-mark flush case and the wrapped-continuation constraint; the existing mark and widest-mark
  wording is preserved. Citation moved from `(spec 180)` to `(spec 180, 211)`.
- One `added` scenario inside that block: `the turn continues on an unmarked line`.
- Header — `last folded` moved to 2026-11-21; `211-overlay-turn-hang` prepended to `slices`.

## Counts

- `overlay` requirements: **5 before → 5 after** (highest id `R5` unchanged).
- Scenarios in R5: **2 before → 3 after**. Removed: 0. Renamed: 0.

## Not folded

- The speaker-token-alone shape (`Paragenda:` on its own line) stays with ITEM-224; its classifier
  is unchanged by this slice.
- The preview's scroll override and the E2E fixture setup are tooling facts, not product behaviour;
  they stay in `preview/index.html` and `tests/e2e/test_obs_overlay.py`.
