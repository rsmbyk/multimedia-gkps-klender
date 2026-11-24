# Fold: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md`
**Date**: 2026-11-24
**State**: Converged on pass 1; no accepted gaps

## Capabilities touched

- `reading` — `R10` (modified: the large-frame title band is restored and the
  headerless/head-bearing distinction is made explicit).

## Operations

- **modified** (`reading/R10`): the block already pinned the 840×760 frame, the
  `20px 26px` title inset and the 1px divider; spec 226 moved those declarations to
  `.editor__head`, which the entry form does not render. The replacement block adds the
  rule that a headerless large form carries the inset and the one rule on its title,
  while head-bearing editors keep the zero-padding title under spec 226's single head
  rule, plus a scenario naming the three affected dialogs and the narrow numbers.
- **header**: `last folded` stays 2026-11-24; `slices` gains
  `240-entry-modal-title` as the newest entry ahead of the existing list.

Nothing was added as a new `R<n>`, removed or renamed. No behaviour change outside
`R10` is declared: the product diff is one scoped CSS rule and its narrow override.

## Before / after counts

| Measure | Before | After |
| --- | --- | --- |
| `### R<n>` blocks in `docs/spec/reading.md` | 58 | 58 |
| `- WHEN` scenario lines | 255 | 256 |
| File characters | 115,451 | 116,113 |

## Not folded

None. The VERSION bump, changelog line and card/board close are delivery bookkeeping,
not capability operations. The card's `Done` close (`closed_at`, `closed_reason`) and
board row were made on the same PR, #617, with no follow-up board PR.

## Evidence

- Red on the gate-1 CSS edit temporarily removed: four assertion failures naming the
  missing 26px/18px text inset and 1px divider, with no timeouts.
- Green with the edit restored: `tests.e2e.test_entry_modal_title` 2/2; together with
  `test_entry_modal_frame` and `test_verse_modal_header`, 11/11 targeted tests green.
- Live probe readbacks at 1440×900 and 390×844 match the gate-1 numbers in §UI/UX.
- Converge pass 1: 14/14 traceability rows met, 0 gaps.

## Delivery state

| Item | Value |
| --- | --- |
| Version | `1.36.26` (was `1.36.25` on `origin/develop`; spec 238 still holds `1.36.24` unmerged) |
| Card | `ITEM-255` — `ITEM-253` was taken by spec 238 mid-flight |
| Branch | `fix/240-entry-modal-title`, based on `origin/develop` at `3aa1810e` after merging spec 239 |
| Push / PR | pushed as PR [#617](https://github.com/rsmbyk/multimedia-gkps-klender/pull/617); the card's `Done` close and board row carry the same PR number |
