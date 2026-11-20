# Contracts: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`

## Interfaces exposed by this slice

| Interface | Kind | Defined in | Consumed by |
| --- | --- | --- | --- |
| `POST /editor/tatib/new/save/` and `/editor/tatib/<id>/save/` | internal JSON | `contracts/save-response.md` | `static/web/editors.js`, `static/web/reading.js` |

The response gains two additive fields; no route, method or status code changes.

## Not exposed

No public HTTP API, message channel or persisted state is added. The `editor:saved` DOM event keeps
its existing detail shape plus the two additive fields; its other listeners ignore them.
