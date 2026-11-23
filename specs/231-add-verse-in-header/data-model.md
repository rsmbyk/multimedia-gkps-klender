# Data Model: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`

## Entities

None. The slice edits one server-rendered template block and one scoped CSS rule; `Song`, `Verse`,
`Book`, `ServiceEntry`, the editor endpoints and all permission helpers are untouched.

## Invariants

- Each song page paints exactly one `[data-add-verse]` node (FR-004, SC-003).
- The header control is drawn only when `can_edit_verses` and at least one live verse exist
  (FR-001, FR-003).
- Project keeps its own `verse_rows` gate and is never converted to a Stop control (FR-006).

## Not modelled

- No new state is stored: button placement is derived from `verse_rows` and `can_edit_verses` on
  every render, so an in-place song swap paints the same header as a direct load.
