# Contracts: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`

`none` — no endpoint, payload, schema, event or module boundary changes.

The interfaces this slice relies on are internal to the reading shell and already exist:

- the two DOM ids `#panelEmpty` and `#chEmpty`, which `reading.js`, `entries.js` and `offline-render.js`
  already looked up;
- `window.shellListEmpty(element, any, total)`, published by `reading.js` for the two scripts that sit
  beside it (a page-local helper, not an API);
- the `reconcileNode` helper `reading.js` already uses for the Tata Ibadah mode switch.
