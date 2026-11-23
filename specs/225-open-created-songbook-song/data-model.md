# Data Model: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`

## Entities

No model, field or migration is added. The slice reads values already present at the save boundary.

### Created editor record

| Field | Type | Constraints | From |
| --- | --- | --- | --- |
| `id` | int | primary key of the saved row | existing save response |
| `kind` | str | `songbook` or `song` for this branch | existing save response |
| `created` | bool | true only when the form had no instance before save | existing save response |

**Relationships**: a created `Book` is the target of `/songs/book/<id>/`; a created `Song` is the
target of `/songs/<id>/`. No new relation.
**Validation**: the create flag comes from the server-side form, never from client input.
**State transitions**: `no record → saved record → record opened`; a refused save emits no event.

## Reading shell (existing)

`#panelBody .book[aria-current="true"]`, `#chList .songrow[aria-current="true"]`, `#readName`,
`data-ch` and `data-read` are the observable fields the E2E reads. The fresh rows are supplied by
the fetched page and reconciled by `applyPage`; no new state store or flag is introduced.

## Invariants

- A record opens only after a successful create (FR-001, FR-002, FR-005).
- Opening never reloads the document or changes `data-nav` (FR-003).
- Edits, verse/Tata Ibadah saves and the spec-209 service open keep their existing paths (FR-004).

## Not modelled

- No "just created" flag on `Book` or `Song`: the save response's `created` is a one-time fact.
- No dock or projector state; the reading shell is the only surface in scope.
