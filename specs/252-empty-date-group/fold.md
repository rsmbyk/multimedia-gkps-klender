# Fold: No empty groups after the last row is deleted

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-28
**State**: Converged in one pass; gate 2 accepted after all five analysis findings were fixed.

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R64` | A grouped sidebar retires its `section.group` when the last row goes, hides it when a filter has hidden every survivor, and no renderer emits an empty bucket or `Templates` group. Four scenarios cover the bucket, templates, songbooks and the filtered case. |

## Operations

- Header `last folded`: `2026-11-27` → `2026-11-28`.
- Header `slices`: `252-empty-date-group` prepended; the `246…` entry and all older entries unchanged.
- Body: one `added` block (`R64`), before Fold there were `63` requirements; after Fold there are `64`.
  The new requirement carries four scenarios, matching the four cases in the accepted spec.
- No requirement was modified, removed or renamed. No other capability was touched.
- The number `252` and card `ITEM-269` were checked against `origin/develop` and all unmerged refs at
  Specify and again at Fold; no retake was needed. `VERSION` stays `1.37.9` — the `patch` bump is applied
  in the pre-merge delivery commit per VER-04.
- Earlier premature commit (`bd75845b`) was reset to base before gate 1; it exists only in the reflog as
  an undo trail. This slice's branch has zero commits before Fold.

## Drift guard

- **Files changed in this capability**: `docs/spec/reading.md` (header + `R64` block).
- **Declared no behaviour change**: no — deleting the last row now removes the heading section too,
  and a template-mode reload with no templates renders no group. The other eight grouped surfaces were
  inspected and left untouched.
- **Not folded**: the manual production check (T023) and delivery (T025) are not spec facts.
