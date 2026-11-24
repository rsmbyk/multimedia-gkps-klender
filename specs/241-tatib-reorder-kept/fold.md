# Fold: reordered Tata Ibadah keeps every entry

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R57` | Full replacement block: only a row carrying the sorter's song data is a song row; a contents row, chapter row or break divider is never reordered, and non-song rows keep their places when song rows trade. Adds the "contents list after a save" scenario. |
| `added` | `R60` | A reordered service keeps every entry; one write; sidebar and stage agree on the same order; a cancelled gesture restores the pre-drag order; legacy rows, breaks and options keep their places. Three scenarios. |

Header: `last folded` moves to 2026-11-24 and `241-tatib-reorder-kept` is prepended to `slices`.

## Drift guard

- **Files changed in this capability**: `static/web/reading.js`, `static/web/reorder.js`,
  `tests/e2e/test_reorder.py`, `docs/spec/reading.md`, `specs/241-tatib-reorder-kept/`,
  `backlog/items/ITEM-256-tatib-reorder-kept.md`, `backlog/board.md`, `CHANGELOG.md`, `VERSION`.
- **Declared no behaviour change**: no — both requirements describe the corrected client behaviour;
  the spec pack, board card and release record are bookkeeping for the same change.

## Before / after

| | Before | After |
| --- | --- | --- |
| reading `R<n>` count | 59 (after the develop merge) | 60 |
| `slices` entries | 57 | 58 |
| spec packs under `specs/` (this branch) | 234 max | 241 added |

## Number collision

The slice planned `R58`; while it was open, develop folded spec 236 as `R58` and spec 238 as `R59`.
The develop merge therefore folded this slice's requirement as **`R60`**. No behaviour changed —
only the capability number recorded here and in `spec.md`.

## Not folded

No requirements were excluded — Converge reported no accepted gaps.
