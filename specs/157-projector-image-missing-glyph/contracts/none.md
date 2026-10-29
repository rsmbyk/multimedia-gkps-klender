# Contracts: the projector's image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`

## Interfaces exposed by this slice

**none** — no endpoint, payload, template variable, stored value or DOM event is added, removed or
re-shaped. The page keeps fetching `GET http://127.0.0.1:63174/v1/files/<sha256>` and keeps rendering the
same three nodes; what changes is which of them is visible.

## Not exposed

The state is internal to `static/web/projector.js`. Its observable surface is the projector's own DOM —
the active screen's `<img>` and its `<svg class="screen__image-missing">` — which
`tests/e2e/test_image_display.py` reads and the preview draws. The `[hidden]` attribute is a rendering
detail, not a contract another surface consumes: `static/web/obs-overlay.js` and `display.js` read the
display state, not this element.
