# Contracts: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`

## Interfaces exposed by this slice

`none` — the slice adds no HTTP endpoint, no template context variable, no companion route and no
JavaScript API. The companion's `GET /v1/transfers` response and the page's routes are unchanged; the
dialog keeps reading the same payload it reads today. The only new identifier is a CSS class
(`.media-transfers__list`) on an existing element, which is internal to the page.

## Not exposed

- The `#mediaTransfersList` element's structure — the script owns it (`media-handoff.js:36`), and the
  class added here is the stylesheet's handle on the same node.
- The seam's placement rule (`session` / `seen` / `viewed`) — unchanged and internal to the script.
