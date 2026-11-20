# Contracts: the dock's entry headers toggle their own block

**Spec**: `specs/198-dock-entry-toggle/spec.md`

## Interfaces exposed by this slice

none — the slice is client-side behaviour of the dock's own page. The only new attribute
contract (`aria-controls="entryinner-<index>"` → the inner's `id`) is internal to one document;
no endpoint, no channel message, no payload, no template contract changes.

## Not exposed

- The projection path (`projectScreen`, the `OBS-*` channel, `gkps-display`) is consumed exactly
  as today — FR-004 keeps it bit-for-bit; the slice only removes one *trigger* (the header).
- `entryOverrides` is page memory; nothing outside `obs-dock.js` can read or write it.
