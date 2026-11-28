# HTTP contract: expected version and conflict

**Spec**: `specs/254-entity-versioning/spec.md`

## Write request

- Form endpoints: add `expected_version` as a hidden field in the existing POST body.
- JSON endpoints: add `expected_version` as an integer member of the existing JSON body.
- Creates: no expected version for the new row; a create inside a service carries the parent service's version under `expected_parent_version`.

## Success

The existing success body is unchanged. The stored row's version increases by one only if stored values changed.

## Conflict

Status `409`, content type `application/json`:

```json
{
  "error": "conflict",
  "message": "This record changed. Reopen it and try again.",
  "current_version": 6
}
```

`current_version` is the version actually stored when the request was refused. No field is written.

## Deletion refusal

Verse, song and songbook deletion with a non-zero referencing-service count keeps the existing refusal status and gains the shared notice text `Used in <count> Tata Ibadah — delete unavailable`.
