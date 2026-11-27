# Data Model: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`

## Entities

`n/a — no entity changes. The slice moves one script include between two templates; no model,
field, migration or context value is added, removed or renamed.`

## Invariants

- A direct song load has exactly one `songs_verse.js` include (FR-005).
- The verse button's markup and box stay byte-identical (FR-006).

## Not modelled

- The script's own state (drag, editor form) is unchanged and remains in browser memory; no
  durable state is introduced.
