# Fold: song list keeps its chosen order

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-23

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R57` | The song list keeps the operator's chosen order across every in-place refresh; the control agrees with the rows; default load stays last-modified; hymn books and non-song lists untouched |

Header: `last folded` stays 2026-11-23 and `233-song-sort-retained` is prepended to `slices`.

## Drift guard

- **Files changed in this capability**: `static/web/reading.js`, `tests/e2e/test_song_sort_retained.py`,
  `docs/spec/reading.md`, `specs/233-song-sort-retained/`,
  `backlog/items/ITEM-247-song-sort-retained.md`, `backlog/board.md`, `CHANGELOG.md`, `VERSION`.
- **Declared no behaviour change**: no — the client change and its E2E coverage carry `R57`; the
  spec pack, board card and release record are bookkeeping for the same behaviour.

## Before / after

| | Before | After |
| --- | --- | --- |
| reading `R<n>` count | 56 | 57 |
| `slices` entries | 56 | 57 |
| spec packs under `specs/` (this branch) | 231 max | 233 added |

## Not folded

No requirements were excluded — Converge reported no accepted gaps.
