# Contracts: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`

## Interfaces exposed by this slice

| Interface | Kind | Defined in | Consumed by |
| --- | --- | --- | --- |
| Write endpoints with `expected_version` | HTTP endpoint | `contracts/http.md` | sidebar editors, entry editor, verse editor, reorder scripts |
| HTTP 409 conflict body | HTTP endpoint | `contracts/http.md` | write callers; later invalidation slice |

## Not exposed

No new public API route and no change to DRF serializer field lists. The version is an internal guard for the product's own write paths; the later live-surface slices consume it through their own poll endpoints.
