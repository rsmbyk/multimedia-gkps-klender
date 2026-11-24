# Contracts: none

**Spec**: `specs/239-media-filter-pill-hover/spec.md`

No external interface is added or changed. No endpoint, request/response shape, model
field, event name, stored format or script API is touched; the only product change is
one CSS rule in `static/styles/design/components.css`. Existing interfaces relied on
by the verification are:

- `multimedia/web/templates/reading/media_library.html`'s `[data-media-type]` buttons,
  `#mediaUnusedFilter`, `aria-pressed` and the separator span (read only);
- `static/web/media-library.js`'s click handler, which toggles `aria-pressed` (read only);
- theme tokens in `static/styles/design/tokens.css` (read only);
- the same-origin stylesheet rule read by `preview/probe.py` (read only).
