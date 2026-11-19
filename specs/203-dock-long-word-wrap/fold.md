# Fold: A long word wraps in the dock runner

**Capability**: `docs/spec/dock.md`
**Folded at**: 2026-11-19

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R16` | The runner's text wraps at its own box — the service title, every entry header shape and a screen row inside an open block; the body does not scroll sideways because of text; a run that fits keeps its line count, height, width and row geometry; no clamp; the Next band's and off-strip's labels keep their one-line `…` cut and the picker keeps its own wrap. Six scenarios. |

Nothing modified, removed or renamed. `R1`–`R15` are untouched: the slice changes where a run of text
breaks, not what any control does. The reading page's own wrap requirement (`reading/R13`, spec 137) is
the sibling this one mirrors on the dock; it is not modified.

## Drift guard

- **Files changed in this capability**: `static/styles/design/obs-dock.css` (three declarations),
  `tests/e2e/test_dock_text_wrap.py` (new).
- **Declared no behaviour change**: no — the behaviour change is the wrap itself, declared as `R16`.
- **Counts**: `dock` 15 requirements before → 16 after; header `last folded` 2026-11-18 → 2026-11-19,
  `203-dock-long-word-wrap` prepended to `slices`.

## Not folded

None. Converge reported zero gaps, so the whole delta folds.
