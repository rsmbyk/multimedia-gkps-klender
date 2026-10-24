# Data Model: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`

## Entities

### Songbook (existing — `songs.Book`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | integer | primary key | FR-001 |
| `name` | string | required; the A–Z key's source | FR-002 |
| `short_name` | string | optional; rendered on hymn rows only | FR-003 |
| `is_hymn_book` | boolean | decides the group | FR-001 |
| `is_deleted` | boolean | soft delete; a deleted songbook is not in the panel | FR-005 |
| `song_total` | integer | annotation: non-deleted songs; hymn order only | FR-002 |

**Relationships**: Songbook 1—n Song — the count that orders the hymn group.
**Validation**: unchanged; this slice adds no field and no constraint.
**State transitions**: none — the slice reads the row, it does not write it.

### Panel group (computed, not persisted)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| rows | list of songbook rows | hymn group first, ordinary group second | FR-001 |
| separator | CSS, not data | the second `.group`'s `border-top`; absent when either side is empty | FR-003, FR-005 |

**Relationships**: the panel renders zero, one or two groups — one when a side is empty, never a group with no
rows.
**Validation**: no heading element (`group__head`) inside the Kidung panel; one separator at most.
**State transitions**: `present → filtered-empty → dropped` when the panel filter removes a group's last row.

## Invariants

- Every hymn songbook precedes every ordinary songbook in the panel (FR-001).
- Ordinary songbooks are ordered by the folded name and the original name only; no other field participates (FR-002).
- At most one separator exists, and only between two non-empty groups (FR-003, FR-005).
- The server and the saved renderer produce the same order for the same names (FR-007).

## Not modelled

- No new model, field, migration or API: the grouping is a presentation concern over rows that already exist.
- The separator's pixels are CSS, not data; they are pinned by the plan's traceability and the E2E measurement.
