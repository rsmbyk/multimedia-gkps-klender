# Contracts — spec 215

**Spec**: `specs/215-copy-template-dialog/spec.md`

One external interface changes: the copy endpoint starts taking a name. The editor fragment's context
gains one key, which is internal but is the seam `_copy_confirm.html` renders from.

## `POST /tatib/<service_id>/copy-as-template/` — `web-tatib-copy`

Unchanged: method, route, permissions, the 403 for a restricted editor, the 405 for a non-POST.

**Request body** — optional JSON object:

```json
{"name": "9 Agustus 2026 (Copy)"}
```

| Case | Behaviour |
| --- | --- |
| body absent, or a JSON object with no `name` key | the copy is named `<source name trimmed to 57> (Copy)` (D004) |
| `name` present, a string | trimmed; the copy takes the trimmed value |
| `name` present, not a string | `400 {"ok": false, "error": "Malformed request."}` |
| `name` trimmed to `""` | `400 {"ok": false, "error": "A name is required."}` |
| `name` longer than 64 characters after trimming | `400 {"ok": false, "error": "A name can be at most 64 characters."}` |
| body is not JSON | `400 {"ok": false, "error": "Malformed request."}` |

**Response** — unchanged on success:

```json
201 {"id": 317, "url": "/tatib/317/?mode=template"}
```

**Guarantees**: the source's `name`, `kind`, `date` and entries are not written; the copy is a
`template` with `date = null`; every failure leaves no row behind (the whole copy is one
`transaction.atomic()` block, as today).

## Editor fragment context — `_editor_fragment_context`

One key added, present only for a Tata Ibadah that has a `pk` (the same condition as `copy_url`):

| Key | Value |
| --- | --- |
| `copy_name` | `f"{source.name[:57]} (Copy)"` — the field's default value (FR-003) |

`_copy_confirm.html` renders it as the Name field's `value`, so the default the person sees and the
default a nameless request produces (D004) come from one rule.

## DOM contract — the confirmation

The hooks `editors.js` addresses. All already exist except the three marked *new*.

| Hook | Element | Behaviour |
| --- | --- | --- |
| `[data-copy-open]` | the header button, `data-copy-url` | opens the confirmation |
| `[data-copy-confirm]` | the layer | `hidden` when closed; `position: fixed; inset: 0` when open |
| `[data-copy-name]` *new* | the Name field | holds `copy_name`; click selects all; `input` re-evaluates accept |
| `[data-copy-accept]` | the accept button | disabled while the name is blank; posts `{"name": …}` |
| `[data-copy-cancel]` | the cancel button | closes the confirmation only |
| layer itself | a click whose target is the layer | closes the confirmation only |

**Unchanged**: `[data-copy-open]`'s `data-copy-url`, the `X-Requested-With: fetch` and `X-CSRFToken`
headers, the `announce()` failure path, and the navigation to `result.data.url` on success.
