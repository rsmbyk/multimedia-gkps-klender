# Fold: Keep Add song when the songbooks sidebar is closed

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-22

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `reading/R51` | The second-level song list's add control follows its own sidebar, not the first sidebar's mini/closed state. |

## Drift guard

- **Files changed in this capability**: `docs/spec/reading.md` (header slices and `R51`)
- **Declared no behaviour change**: no — the collapsed-parent state now keeps `Add song` visible.
