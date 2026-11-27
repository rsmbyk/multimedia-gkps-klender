# Data Model: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`

No persisted entity is added. The slice reads fields that already exist and changes no schema.

## Entities

### Song sort choice (client state)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `songSort` | enum `m` \| `title` | initialized `m` on document load; changed only by `#songSort` | FR-003, US3/AC2 |

**Relationships**: drives the ordering of the `#chList` rows in the current document only.
**Validation**: the two values map to the two comparators in `applySongOrder()`; no third value is written.
**State transitions**: `m → title → m` on each sort click; survives every in-place refresh; resets to
`m` on a full document load.

### Song rows (existing `songs.Song`, read only)

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `modified` | datetime | set by `auto_now`; server sorts descending, nulls last | FR-001 |
| `title` | string | alphabetical comparator key; leading track number ignored | FR-001 |
| source order | number | tiebreak in both comparators | FR-001 |

**Relationships**: rows belong to one `Book` and appear in that book's child list.
**Validation**: none added — this slice never writes a song.
**State transitions**: none; only DOM order changes.

## Invariants

- After any in-place refresh, the DOM order of `.songrow` elements equals the order the current
  `songSort` comparator would produce (FR-001, FR-002).
- `applySongOrder()` only reorders `.songrow` children of `#chList`; chapter and service rows keep
  their own order (FR-004).
- Hymn songbooks offer no sort control and remain in number order (FR-004).

## Not modelled

- Browser persistence of the sort choice across a full reload — the owner chose in-place-refresh
  retention only, so the choice stays a document-lifetime variable.
- A server-side sort parameter — no new endpoint or query contract is introduced.
