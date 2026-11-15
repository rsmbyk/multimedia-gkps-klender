# Fold — dock live entry snap

**Date**: 2026-11-15 · **Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Converge**: pass 1

## Capabilities touched

| File | Operations | Before → After |
| --- | --- | --- |
| `docs/spec/dock.md` | `added` — `R13` (one block, eight scenarios); header moved `last folded` to 2026-11-15, slice prepended to `slices` | 12 rules → 13 rules |

No `modified`, `removed` or `renamed` operations.

## Not folded — accepted gaps

None. Converge pass 1 found no gaps in the shipped behaviour; C-005 (the
morph-finish trigger names a moment where "entirely out of view" cannot hold) is
accepted as vacuous, is recorded in `spec.md`'s Assumptions and in `converge.md`,
and changes no scenario in R13.

## Notes

- R13 also lands the centring rule spec 119 pinned but never folded into this
  file; the block cites spec 119 for the partly-visible case.
- The fold is idempotent by construction: the typed operation is `added` R13, and
  a re-run finds R13 already present with the same scenarios and stops.
- Gate 2 declared `bump: none`; `VERSION` and the `## [Unreleased]` line are
  untouched (they belong to the pre-merge commit, if the owner ships one).
