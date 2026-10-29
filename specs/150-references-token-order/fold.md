# Fold: the first refresh authenticates its references write

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-28

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R26` | The Media Library sends its references write with the token from the same refresh's `/status` response, so the page's first refresh is authenticated and its list is drawn once with its references; the head controls are still applied once, and nothing about the endpoint, payload, header or copy changes. Three scenarios: the first refresh, a later refresh, the token cannot be had. |

**Before**: `reading` held 24 requirements (R1…R24). **After**: 25 (R1…R26).

## Drift guard

- **Files changed in this capability**: `static/web/media-library.js` (the page's own script) and
  `tests/e2e/test_media_library.py` (its acceptance cases). No template, stylesheet, view or model.
- **Declared no behaviour change**: no — R26 is a new behaviour guarantee over the same request; the page's
  pixels, rows and copy are unchanged.
