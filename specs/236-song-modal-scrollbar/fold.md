# Fold: song entry modal scrollbar

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R58` | The shared editor dialog is never a scroll container in a song-entry state; overflow is clipped at its edge (computed `overflow-y: clip`, 0px gutter) while `.editor__content` remains the scrollport; box, radius, verse-panel animation and fixed results menu unchanged |

Header: `last folded` moved to 2026-11-24 and `236-song-modal-scrollbar` was prepended to `slices`.

## Drift guard

- **Files changed in this capability**: `static/styles/design/components.css`,
  `tests/e2e/test_song_modal_scrollbar.py`, `docs/spec/reading.md`, `specs/236-song-modal-scrollbar/`,
  `backlog/items/ITEM-251-song-modal-scrollbar.md`, `backlog/board.md`, `CHANGELOG.md`, `VERSION`.
- **Declared no behaviour change**: no — the one declaration changes which element scrolls; `R58`
  records it. The spec pack, board card and release record are bookkeeping for the same behaviour.
- `CHANGELOG.md` and `VERSION` are written in the delivery commit, after the push has given the
  card its PR number; they are not part of this Fold commit.

## Before / after

| | Before | After |
| --- | --- | --- |
| reading `R<n>` count | 57 | 58 |
| `slices` entries | 57 | 58 |
| spec packs under `specs/` (this branch) | 235 max (in flight) | 236 added |

## Not folded

No requirements were excluded — Converge reported no accepted gaps.
