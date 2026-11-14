# Fold: Retired Addresses

**Capability**: `docs/spec/routing.md`
**Folded at**: 2026-11-14

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `routing/R1` | A retired address answers 302 to its successor — the old OBS docks to `/obs/dock`, the old OBS sources to `/obs/blank`, `/home/` and `/manage/…` to `/` — while `/songs/books*` keep their 301 and re-point at the reading pages. |
| `added` | `routing/R2` | The old version is reachable for one release at `/archive/…`, which answers the live successor in one hop and never a protocol-relative address. |
| `added` | `routing/R3` | `/obs/blank` is transparent and paints one watermark note: `Old OBS source` at 20% white, the live overlay's address on hover, no asset to load. |

The capability did not exist before this slice: `docs/spec/` had no `routing.md`, so all three
requirements are `added`, not `modified`.

## Drift guard

- **Files changed in this capability**: `multimedia/retirement.py`, `multimedia/urls.py`,
  `multimedia/obs/urls.py`, `multimedia/web/urls.py`, `multimedia/web/reading/views.py`,
  `multimedia/web/templates/reading/obs_blank.html`, `multimedia/web/tests.py`,
  `tests/e2e/test_retired_routes.py`
- **Declared no behaviour change**: no — the behaviour change is exactly the three `added` deltas
  above. No other capability's behaviour moved: `/songs/` and `/tatib/` answer as before, the live
  `/obs/dock` and `/obs/source/overlay` are untouched, and the editor pages keep their `/editor/…`
  routes. The `multimedia/web/manage/` package stays in the tree, unreachable.

## Capability counts

| Capability | Before | After |
| --- | --- | --- |
| `routing` | 0 requirements | 3 requirements |
