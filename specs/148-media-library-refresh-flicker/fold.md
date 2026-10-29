# Fold: the Media Library list holds still while it refreshes

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R24` | The Media Library page draws its file list once per refresh and holds still: no intermediate pass without the service references, no row moves during a refresh, the first load appears complete in one draw, a failed references read still draws the placeholder once, and the 2s poll stays visually inert. Four scenarios: a refresh from an action, the first load, references unavailable, a running transfer. |

**Before**: `reading` held 23 requirements (R1…R23 — 145, 146 and 147 folded theirs first).
**After**: 24 (R1…R24; the number was R22 until 146 took R22 and R23 on `develop`).

## Drift guard

- **Files changed in this capability**: `static/web/media-library.js` (the page's own script, which
  draws the list this requirement is about) and `tests/e2e/test_media_library.py` (its acceptance
  cases). No template, no stylesheet, no view, no model.
- **Declared no behaviour change**: no — the delta above is the behaviour change, and it is the only
  one. `render()`'s output is byte-identical to before; what changed is how many times it runs.
