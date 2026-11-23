# Data Model: A passage cue carries its current and end verse

**Spec**: `specs/229-cue-verse-counter/spec.md`

## Entities

### Projector scripture entry (existing dict in `_projector_data()`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `verse_start` | int or null | first verse of the passage; null becomes 1 | FR-001, FR-003 |
| `verse_end` | int or null | last verse of the passage; null becomes `verse_start` | FR-001, FR-003 |

**Relationships**: one entry owns the screens from `start` to `end - 1`; its final screen is the
built-in blank rest and is not a verse.
**Validation**: `verse_end >= verse_start` is already enforced by the entry editor; the renderer
never prints a counter whose end is below its current number.
**State transitions**: none — the entry is read-only data on the projector page.

### Projector scripture screen (existing dict from `_scripture_screens()`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `verse` | int | the verse this screen prints; absent on blank screens | FR-001, FR-002 |

### Passage Go To detour (existing browser object)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `verse` | int | the verse currently painted | FR-004, FR-005 |
| `editions` | map of code → `{name, verses: [{n, title, text}]}` | already fetched for the chapter | FR-004 |
| `translation` | code | edition in use; selects the list that supplies the end number | FR-004 |

## Invariants

- The counter's end number is never below its current number (FR-003, FR-004).
- A screen that is `blank: true` never contributes a verse number (FR-006).
- No new field is written to `gkps-display`: the counter is derived from data already loaded (FR-005).

## Not modelled

- No database migration, model field or endpoint: the two new payload fields are derived from
  columns already stored on `ServiceEntry` and `Verse`.
- No "last verse seen" state: the Go To counter is recomputed on every render from the loaded
  chapter, so a step, a flip and a fresh boot agree without new persistence.
