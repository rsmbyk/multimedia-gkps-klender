# Data Model: <short title>

**Spec**: `specs/NNN-slug/spec.md`

## Entities

### <Entity>

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | uuid | primary key | FR-001 |

**Relationships**: <Entity> 1—n <Entity> — <what the relationship means>
**Validation**: <rules traceable to a requirement>
**State transitions**: `created → active → archived` — <what triggers each>

## Invariants

- <a statement that must always hold, and which requirement says so>

## Not modelled

- <what the spec mentions but the model deliberately does not represent, and why>
