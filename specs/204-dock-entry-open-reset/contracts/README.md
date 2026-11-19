# Contracts: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`

## Interfaces exposed by this slice

none — client-only. One page-memory map is emptied on an existing internal path; no HTTP endpoint,
serializer, channel verb, storage key, display-record field, DOM id or class changes. The dock's
existing internal names (`openService`, `entryOverrides`, `effectiveOpen`, `#entryList`,
`.entryinner`, `aria-expanded`) are one document's own machinery and are recorded in
`data-model.md` and `plan.md`, not offered as an interface.

## Not exposed

- The reset is not broadcast: the projector and the overlay have no entry blocks, and an open
  already writes no display state (measured byte-identical across 10 opens).
- No override is persisted, and no debug hook or query parameter is added to the product. The
  preview's `?behaviour=` switch exists only in `preview/`, never in `static/web/obs-dock.js`.
- The re-read contract (`dock/R13`) and the crossing contract (`dock/R14`) are unchanged: a
  consumer of either sees exactly today's behaviour.
