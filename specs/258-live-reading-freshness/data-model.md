# Data Model: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`

## Derived values

### Page version

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `version` | integer | current `TataIbadah.version` or `Song.version` | FR-001 |

**Relationships**: names the row the page loaded. **Validation**: mismatch invalidates the page; it never writes.

### List fingerprint

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `fingerprint` | SHA-256 hex string | derived from ordered `(id, version)` pairs in the scoped list | FR-002 |

**Relationships**: songbooks, songs by book, services by mode. **Validation**: identical scopes and rows produce identical strings.

### Invalidated page state

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `stale` | boolean | client-only; true until in-place reload | FR-004, FR-005 |

**State transitions**: `fresh → stale` on mismatch; `stale → fresh` after Reload.

## Invariants

- A stale page never writes: slice 254's 409 remains authoritative.
- Sidebar reconciliation never changes the stage or the open record.
- Filter, sort, scroll and panel state survive reconciliation unchanged.

## Not modelled

- No persisted list version, pending-change log or history table.
- No author attribution for the external edit.
