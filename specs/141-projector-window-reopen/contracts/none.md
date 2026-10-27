# Contracts: none

**Slice**: `specs/141-projector-window-reopen`

This slice exposes no interface. It adds a control to a page the server already renders, and the act
it performs is a browser-local one:

- no endpoint, request or response changes;
- no template variable or payload key is added — the control's URL comes from the existing
  `web-projector` route;
- no stored value changes: the display state is read, never written;
- the DOM attributes it adds are read only by `static/web/display.js` and the stylesheet that draws
  the control, both recorded in `data-model.md`.

The nearest thing to a contract is spec 119's: `/projector` without a parameter renders the stored
state. This slice depends on it and does not change it.

Stated explicitly rather than left absent, per SDD-12.
