# Fold: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md`
**Date**: 2026-11-24
**State**: Converged on pass 1; no accepted gaps

## Capabilities touched

- `reading` — `R49` (A contents row states its entry's kind in a column after the number).

## Operations

- **modified** (`reading/R49`): the mark's requirement now says it "SHALL share the number's
  vertical centring on every row, including the drag copy of a row", where it previously only
  said the mark "SHALL be 16px". The number's own centring sentence and the label's clamp are
  unchanged. The requirement's spec footer moves from `(spec 214)` to `(spec 214, 237)`.
- **added** (one scenario under `R49`): "the mark shares the number's centre" — a one-line row,
  a row with a `Bait` line, and a row wrapped at a 390px pane all keep the mark's box centre
  within 1px of the row's and the number's, with the slot badge on the mark's corner.
- **header**: `last folded` stays 2026-11-24; `slices` gains
  `237-sidebar-mark-centering` as the newest entry, ahead of the existing list.

Nothing was removed or renamed. No behaviour change outside `R49` is declared.

## Before / after counts

| Measure | Before | After |
| --- | --- | --- |
| `### R<n>` blocks in `docs/spec/reading.md` | 58 | 58 |
| `#### Scenario:` blocks | 250 | 251 |
| File characters | 114,540 | 114,951 |

## Not folded

None. T014 (version bump, changelog line, card close) is a delivery step, not a capability
operation, and stays open until the delivery word.

## Evidence

- Targeted E2E `tests.e2e.test_sidebar_mark_centring`: 4/4 green after a 4/4 red-on-base run.
- Existing `tests.e2e.test_sidebar_kind_marks`: 12/12 green.
- Converge pass 1: 14/14 traceability rows met, 0 gaps.
