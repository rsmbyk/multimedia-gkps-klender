# Data Model: the copy confirmation as a dialog of its own, and the copy's name

**Spec**: `specs/215-copy-template-dialog/spec.md`

## Entities

### TataIbadah

Unchanged in shape — no field added, no field removed, no constraint changed, **no migration**.

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `name` | `CharField(64)` | required, not unique | FR-003, FR-005, FR-007 |
| `kind` | `SmallIntegerField` | `service` \| `template`, set once | FR-005 (unchanged) |
| `date` | `DateField(null=True)` | `null` exactly when `kind = template` | unchanged |
| `created_at` | `DateTimeField` | `auto_now_add` | unchanged |

**Relationships**: `TataIbadah` 1—n `ServiceEntry`, unchanged; the copy is a new `TataIbadah` with its own entries, which spec 167 already governs.

**Validation**: the only new rule is on the copy's `name` — trimmed, non-empty, at most 64 characters (FR-007). It is enforced in the endpoint, not in the model, because the model's own writers (the editor form, the API) already validate `name` through `TataIbadahForm` and the DRF serializer; a second model-level rule would change what those two accept, which this slice does not do.

**State transitions**: unchanged. A copy is created as `kind = template` with `date = null`, and never transitions.

## Invariants

- **A copy is a template with no date** — `kind = template`, `date is null`; guaranteed by the existing `tatib_kind_matches_date` check constraint and unchanged by this slice.
- **The source is untouched** — every write the endpoint makes is on the new row; the source's `name`, `kind`, `date` and entries are read only (FR-005).
- **The copy's name fits the field** — at most 64 characters, so the default `<source> (Copy)` is trimmed to 57 + 7 rather than posted over-long (FR-003, SC-009).
- **Names are not unique** — two Tata Ibadah may share a name, including a copy that keeps its source's (FR-005's edge case, and spec 167's rule this slice does not change).

## Not modelled

- **The name field's default.** It is derived (`<source name trimmed to 57> (Copy)`) and recomputed per request; storing it would let it disagree with the source after a rename.
- **The copy's provenance.** Nothing records which Tata Ibadah a copy came from. Spec 167 decided a copy is an independent template, and this slice renames it, not links it — a `copied_from` FK would be a new capability, not this requirement.
- **The confirmation's own state.** Open/closed and the typed name live in the DOM for the length of one dialog; nothing is persisted before accept.
