# Contracts: none

**Slice**: `specs/137-reading-text-wrap`

This slice exposes no interface. It changes how the browser lays out text it already receives:

- no endpoint, request or response changes;
- no template variable, payload key or stored value changes;
- no CSS class is added to a template, so nothing another component selects on moves.

The nearest thing to a contract is the stylesheet's own: `overflow-wrap` is inherited, and the three
roots (`.read`, `.search-results`, `.preview`) are what a future reading surface must render inside
to get the behaviour. That is recorded in `plan.md`'s Design and in `data-model.md`'s roots table,
not as an interface.

Stated explicitly rather than left absent, per SDD-12.
