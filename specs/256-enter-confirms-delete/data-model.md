# Data Model: Enter accepts a delete confirmation

**Spec**: `specs/256-enter-confirms-delete/spec.md`

## Entities

No new entity, field, relation or migration. The only new artifact in the browser is a marker
attribute on an existing control:

- **Destructive control** — any visible, enabled element with `data-enter-delete`, inside an open
  confirmation. Its identity is the DOM node; the existing handler on that node decides what delete
  means (FR-003, FR-006).

## Invariants

- A control without `data-enter-delete` is never activated by the Enter handler (FR-003, FR-007).
- At most one `keydown` produces at most one `.click()`; the default action is prevented before the
  click so a focused button cannot fire a second time (FR-005).
- The handler never writes to the network itself: the target's existing click/submit handler owns
  the request, its feedback and its focus restoration (D005).
- A closed `<dialog>`, a hidden layer and a disabled control produce no activation (FR-004).

## Not modelled

- **In-flight state** — reused from `feedback.setDialogBusy` and each surface's existing guard; the
  slice adds no second "is deleting" flag.
- **Keyboard preferences** — no setting or persistence; the rule is global to the reading app.
- **Retired modals** — no compatibility state for routes that already redirect (D001).
