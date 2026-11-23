# Data Model: Verse modal header draws one rule

**Spec**: `specs/226-verse-modal-header-rule/spec.md`

## Entities

None. The slice changes one CSS state rule over an existing dialog; no model, field, migration or
request shape is involved.

## Invariants

- The editor dialog's markup, fetch and save path stay byte-identical (FR-004).
- The large form marker remains the only switch between the compact and large dialog layouts.

## Not modelled

- Theme and viewport are runtime states of the existing shell, not stored data.
