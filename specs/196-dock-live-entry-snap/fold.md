# Fold — dock live entry snap

**Date**: 2026-11-15 · **Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Converge**: pass 1

## Capabilities touched

| File | Operations | Before → After |
| --- | --- | --- |
| `docs/spec/dock.md` | `added` — `R14` (one block, eight scenarios); header moved `last folded` to 2026-11-15, slice prepended to `slices` | 13 rules → 14 rules |

No `modified`, `removed` or `renamed` operations.

## Not folded — accepted gaps

None. Converge pass 1 found no gaps in the shipped behaviour; C-005 (the
morph-finish trigger names a moment where "entirely out of view" cannot hold) is
accepted as vacuous, is recorded in `spec.md`'s Assumptions and in `converge.md`,
and changes no scenario in R14.

## Notes

- The rule was specified as `dock/R13` but lands as `dock/R14`: spec 195's
  hotfix batch folded its own `dock/R13` (a saved change re-reads the open
  service) into `develop` while this slice was in review, and `R<n>` is never
  reused or renumbered — this slice yielded. The pack's citations were updated
  in the same pass; the rule's content is unchanged.
- R14 also lands the centring rule spec 119 pinned but never folded into this
  file; the block cites spec 119 for the partly-visible case.
- The fold is idempotent by construction: the typed operation is `added` R14, and
  a re-run finds R14 already present with the same scenarios and stops.
- Gate 2 declared `bump: none`; `VERSION` and the `## [Unreleased]` line are
  untouched by this slice. (The merge with `develop` brought the 1.32.1
  release's `VERSION`/`CHANGELOG.md` into the branch; the slice itself ships
  no unreleased delta.)
