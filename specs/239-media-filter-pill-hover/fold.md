# Fold: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md`
**Date**: 2026-11-24
**State**: Converged on pass 1; no accepted gaps

## Capabilities touched

- `media-library` — `R6` (new: the unpressed filter pills answer the pointer).

## Operations

- **added** (`media-library/R6`): a full requirement stating that the five file-type
  pills and the Unused pill take `--focus` border and `--icon-hover-bg` fill on hover,
  that a pressed pill keeps its accent fill, and that geometry, label, focus-visible
  outline, separator and filter behaviour do not change. Four scenarios cover hover in
  both themes, pointer leave, pressed hover and the frozen box/focus numbers.
- **header**: `last folded` moves from 2026-11-01 to 2026-11-24, and `slices` gains
  `239-media-filter-pill-hover` as the newest entry ahead of the existing list.

Nothing was removed, renamed or declared `modified`. No behaviour change outside
`R6` is declared: the only product diff is one CSS rule in the filter row.

## Before / after counts

| Measure | Before | After |
| --- | --- | --- |
| `### R<n>` blocks in `docs/spec/media-library.md` | 5 | 6 |
| `- **Given**` scenario lines | 24 | 28 |
| File characters | 10,306 | 11,625 |

## Not folded

None. T019 (VERSION bump, changelog line, card close) is a delivery step, not a
capability operation, and stays open until the delivery word. The card stays in
`Speccing`; promotion to `Ready` is the owner's.

## Evidence

- Targeted E2E `tests.e2e.test_media_filter_pill_hover`: 5/5 green after a red run with
  the shipped rule removed (14 subtest failures on the missing hover fill/border).
- Live probe after the test runs: light/dark hover and pressed values match the gate-1
  numbers frozen in `spec.md §UI/UX`.
- Converge pass 1: 14/14 traceability rows met, 0 gaps.
