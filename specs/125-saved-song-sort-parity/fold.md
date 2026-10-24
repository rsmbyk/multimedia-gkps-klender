# Fold: A saved hymn song page never shows the song sort control

**Capability**: `n/a — this repo has no docs/spec/ capability tree (owner decision at gate 2, 2026-10-24);
starting the tree is its own slice, not a renderer fix`
**Folded at**: 2026-10-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| none | — | no capability tree to apply a delta to; the behaviour lives in `specs/125-saved-song-sort-parity/spec.md` and in `CHANGELOG.md` under `[Unreleased]` |

## Drift guard

- **Files changed in this capability**: `static/web/offline-render.js`,
  `tests/e2e/test_saved_render_parity.py`
- **Declared no behaviour change**: no — the changes are FR-001…FR-005 themselves
- **Guard result**: `n/a — the guard compares changed files against tree deltas, and there is no tree. When
  the tree is created, this slice's requirements enter it as the initial saved-reading entries.`
