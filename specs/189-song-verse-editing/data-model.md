# Data Model: song verse editing on the song page

**Spec**: `specs/189-song-verse-editing/spec.md`

## Entities

### Song

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | integer | pk | — |
| `book` | FK `Book` (PROTECT) | — | — |
| `number`, `sub_number`, `title` | existing | unchanged | FR-014 |
| `is_hymn_book` (via `book`) | bool | hymn → read-only | FR-001 |

**Relationships**: `Song` 1—n `Verse` (CASCADE, live set = `is_deleted=False`, ordered by `number`).
**Validation**: None changed.
**State transitions**: none.

### Verse (`songs.Verse`)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | integer | pk — the stable reference | FR-008 |
| `song` | FK `Song` (CASCADE) | — | — |
| `number` | pos int ≥1 | unique among live rows of the song; renumbered 1…n on every write | FR-007, FR-012 |
| `lyric` | text | non-blank on save; untouched by number-only writes | FR-005, FR-014 |

**Relationships**: referenced by `ServiceEntry.verses` as IDs; legacy setlist `SongBookmarkItem.verse` stays number-based and may drift.
**Validation**: Each write leaves the live set numbered 1…n with no gap/duplicate; reorder payload must be a full permutation of the live IDs.
**State transitions**: `live → soft-deleted` via `soft_delete()`; delete only when unreferenced (FR-010).

### ServiceEntry (kind song)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `verses` | JSON list | was list of numbers, becomes list of verse IDs; each ID belongs to `entry.song` | FR-008, FR-016 |
| `song` | FK | — | — |

**Relationships**: resolves via `Verse.objects.filter(pk__in=verses, is_deleted=False).order_by('number')`; label/body use current numbers in that order.
**Validation**: Picker values are IDs, labels are current numbers; stale-form save refused by choice validation.
**State transitions**: none.

### SongBookmarkItem (legacy, not modelled)

- **Not modelled**: `SongBookmarkItem.verse` (comma-separated numbers, 829 items) is deliberately untouched per owner: no migrate/write/payload change (FR-015).

## Invariants

- Live verses of a song are 1…n with no gap/duplicate after every add/edit/delete/reorder (FR-012).
- A referenced verse `is_deleted` never goes true while any `ServiceEntry.verses` contains its id (FR-010).
- A hymn song or restricted reader draws no verse controls; endpoints refuse writes (FR-001, FR-013).
- Reorder payload is exactly the live ID set; otherwise whole write refused (Edge Cases).
- Tombstones never occupy a live row's number (unique among live).

## Not modelled

- The verse row/grip/edit/controls: presentation, not entity (FR-004, FR-006).
- Revision/optimistic-concurrency token: stale writes refused by live-set mismatch check, not a version field.
- Display-state identity beyond lyric text (service body unchanged across reorder).
