# Fold: Add verse sits beside Project in the song header

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-11-23

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R56` | A song's Add verse sits beside Project in the header while verses exist; the empty song keeps its centred invitation |

## Drift guard

- **Files changed in this capability**: `multimedia/web/templates/reading/song.html`,
  `static/styles/design/components.css`, `multimedia/web/reading/test_verse_add_gate.py`,
  `tests/e2e/test_add_verse_header.py`
- **Declared no behaviour change**: no — all four files carry the placement change described by `R56`.
