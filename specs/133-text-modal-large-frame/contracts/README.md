# Contracts: A text entry is written and edited in the media modal's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`

## Interfaces exposed by this slice

`none — the slice adds no endpoint, no parameter and no payload field.`

The only interface it touches already existed and is unchanged in shape:

| Existing interface | Kind | Defined in | How this slice relates |
| --- | --- | --- | --- |
| `GET /editor/entry/new/?kind=<kind>&tatib=<id>` | HTML fragment | `multimedia/web/reading/views.py::entry_form` | renders two more attributes on the form; response status, fields and names unchanged |
| `GET /editor/entry/<pk>/edit/` | HTML fragment | same view | as above |

## Not exposed

Nothing new is published. `data-editor-size` and `data-editor-grow` are styling hooks on a
server-rendered fragment — they are not read by any request, script or stored value, and no client
outside this stylesheet consumes them. A consumer added later would make them an interface; today the
only reader is `static/styles/design/components.css`.
