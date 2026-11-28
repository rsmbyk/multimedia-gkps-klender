# Data Model: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`

## Entities

### Versioned row

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `version` | positive integer | default 1; increments by 1 on a accepted change; never decreases | FR-001, FR-002, FR-014 |

**Applies to**: `TataIbadah`, `TataIbadahItem`, `ServiceEntry`, `Book`, `Song`, `Verse`.
**Relationships**: unchanged — this slice adds one column to each model.
**Validation**: a write carrying an expected version that differs from the stored version is refused with 409 (FR-003).
**State transitions**: `version n → n+1` only when stored values actually change.

### Expected version

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `expected_version` | positive integer | supplied by every write to an existing row | FR-003, FR-005 |

**Relationships**: carried by form POSTs and JSON bodies, never persisted.
**Validation**: must equal the stored version at the moment of the write.

### Referencing service count

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `count` | non-negative integer | distinct active `TataIbadah` records, dated services and templates | FR-011 |

**Relationships**: derived from song-kind `ServiceEntry` rows whose `verses` list names a live verse of the target.
**Validation**: never counts two entries in one service twice; inactive services are excluded.

## Invariants

- A tracked row's version never moves without a stored-value change (FR-002).
- A write that read version `n` cannot be applied when the stored version is `n+1` or higher (FR-003).
- Every song or verse change that succeeds is reflected in one increment on each active referencing service (FR-006, FR-007).
- A non-zero referencing-service count makes deletion unavailable at the server and in the UI (FR-008–FR-012).

## Not modelled

- No history table, diff or rollback: the owner deferred entity history; `version` is a guard, not an archive.
- No author attribution: public writes are a standing product decision and the notice does not name an editor.
- No version on `MediaIdentity` or `MediaShare`: their identity is SHA-256 and their state changes are machine-driven.
