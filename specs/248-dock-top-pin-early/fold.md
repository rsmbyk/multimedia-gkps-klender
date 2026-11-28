# Fold: earlier top pin for the live header

**Capability**: `docs/spec/dock.md`
**Folded at**: 2026-11-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R19` | Full replacement block: the top pin now takes over when the live header's own top reaches the scrollport (`li.top <= box.top + 0.5`) rather than when the whole block clears the fold; the source row is hidden with `visibility: hidden` while the clone owns the edge; the earlier one-header assumption and the stale "no service pin during a Go To" claim are recorded as superseded. Scenarios 3 → 4 (added "the whole block clears the fold"). |

## Drift guard

- **Files changed in this capability**: `docs/spec/dock.md` (R19 replacement block, header date and
  slice list); production changes are `static/web/obs-dock.js` and `static/styles/design/obs-dock.css`,
  with E2E evidence in `tests/e2e/test_dock_top_pin.py`.
- **Declared no behaviour change**: no — visible behaviour changed at the owner's request; the
  boundary is earlier and the native header is covered while the clone owns the edge.
- **Before → after**: 19 requirements → 19 requirements; 75 scenarios → 76 scenarios; R19's ID is
  preserved.

## Evidence

- Converge: `converge.md` — one pass, zero gaps, one MED finding kept as a retraction (D006).
- Verification split: 9 test · 4 inspection · 1 manual; targeted modules 7/7 and 23/23 green,
  boundary probe 490 frames with 0 mismatches.
- `VERSION`/`CHANGELOG.md`, the board card and its close are delivery-step artifacts and are
  deliberately absent here.
