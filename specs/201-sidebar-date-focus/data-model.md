# Data Model: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md`

## Entities

No entity is added, changed or removed: the slice edits one CSS selector pair. The existing
sidebar row (`<li data-editor-kind>` with its `.book` link and `.row-edit` / `.row-delete`
buttons) is the only structure involved, and it keeps its markup and identity.

## Invariants

- The date and Today badge stay in the DOM and in the row's `aria-label` in every reveal state
  (FR-004).
- The `@media (hover: hover)` guard and the touch/`hover: none` rules stay where they are (FR-003).
- Reveal state is derived only from `li:hover` or an action button's `:focus-visible`; no class or
  DOM state is introduced (FR-001, FR-002).

## Not modelled

- Sticky/clicked state: a click's effect on the rule is entirely where focus lands; there is no
  new state to persist or serialise.
