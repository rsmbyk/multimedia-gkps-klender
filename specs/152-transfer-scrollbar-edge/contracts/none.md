# Contracts: The Transfers scrollbar sits at the dialog's edge

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md`

## Interfaces exposed by this slice

`none` — the slice adds no HTTP endpoint, no template context variable, no companion route, no
JavaScript API and no class name. The companion's `GET /v1/transfers` response and the page's routes
are unchanged; `media-handoff.js` keeps querying `#mediaTransfersList`, whose element, id and class
are untouched. The whole of the change is one CSS rule on that element.

## Not exposed

- The list's box — an internal layout detail of the dialog; only the engine's scrollbar and the rows
  depend on it.
- The bar's drawing — owned by spec 087's global rules in `static/styles/design/components.css` and
  not specialised here.
