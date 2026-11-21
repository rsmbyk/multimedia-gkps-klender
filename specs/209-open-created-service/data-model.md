# Data Model: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`

## Entities

No model or field is added. The slice reads three existing values at the save boundary:

### Created editor record

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | int | primary key of the saved row, present in today's JSON answer | existing save response |
| `kind` | str | `tatib`, `songbook`, `song`, `verse`; present today | existing save response |
| `created` | bool | new; true only when the form had no instance before save | FR-001/FR-004 |
| `record_kind` | int | new on `tatib` saves; `0` Normal, `1` Template | FR-001/FR-004 |

**Relationships**: a `created` Normal `TataIbadah` is the target of `/tatib/<id>/`; no new relation.
**Validation**: `record_kind` comes from `TataIbadahForm.chosen_kind()`, never from client input.
**State transitions**: `no record → saved record → stage shows saved record`; a refused save leaves
the first state and does not emit `created`.

## Reading stage (existing)

`#readName`, the `aria-current` row in `#panelBody` and `data-ch` on the reading root are the three
observable fields the E2E asserts. They are read from the freshly fetched `/tatib/<id>/` page by
`applyPage`; this slice adds no state store.

## Invariants

- A stage opens only for a confirmed create of a Normal service (FR-001, FR-004, FR-005).
- Opening a service never reloads the document and never changes `data-nav` (FR-002, FR-003).
- The template-generate and copy-as-template flows keep navigating to their created record (FR-006).

## Not modelled

- No flag on `TataIbadah` marking it "just created": the response field is a one-time fact about the
  save, not a property of the record.
- No dock or projector state: the owner chose the reading stage only.
