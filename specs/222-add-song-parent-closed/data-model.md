# Data Model: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`

## Entities

None — the change is a CSS selector boundary over existing buttons. No model, field, migration or
endpoint is added or changed.

## Invariants

- A control inside `aside.panel` is hidden when the first sidebar is mini or closed; a control
  inside `aside.chapters` is not governed by that first-sidebar state (FR-001, FR-003).
- Hymn songbooks still render no add control at all; no CSS rule can create one (FR-005).

## Not modelled

- Focus, DOM state snapshots and sidebar transitions are browser state, not stored entities.
