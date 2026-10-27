# Data Model: The stage's entry links read as text until hovered

**Spec**: `specs/140-stage-link-affordance/spec.md`

## Entities

None. The slice changes one CSS rule's presentation; no field, record, model, endpoint or stored
state is added, removed or renamed.

## Invariants

- A stage entry title's resting colour equals its heading's colour, because the rule inherits rather
  than names a value (FR-001).
- The link's box is unchanged by any state: underline and colour are paint, not layout (FR-002,
  FR-003).

## Not modelled

- Which entries have a link at all. That is decided server-side (`item.jump` in `tatib.html`) and is
  untouched; an entry without a jump renders a `span` with the same class and therefore the same
  resting appearance.
