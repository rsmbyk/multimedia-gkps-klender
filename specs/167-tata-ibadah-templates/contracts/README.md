# Contracts: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md`
**Dependencies**: none new. The three endpoints below are same-origin, CSRF-checked, editor-only
(`editors.editors_allowed`) and answer JSON like the existing media endpoints do
(`views.py:340-380`).

Every request below carries `X-CSRFToken` (the pages already ship `{% csrf_token %}`), and every response
is `application/json`. Errors use the shape `{"error": "<sentence>"}` with the status shown; a validation
failure inside a slot uses `{"slots": [{"entry": <id>, "errors": {"<field>": "<sentence>"}}]}`.

## POST `/editor/entry/validate/`

Binds one kind's form against submitted data and writes nothing. Called by the New modal when it was opened
from a slot (the fragment's `data-slot-entry`), instead of `POST /editor/entry/new/save/`.

**Request** — form-encoded, exactly the fields `POST /editor/entry/new/save/?tatib=<id>` accepts today,
plus:

| Field | Type | Notes |
| --- | --- | --- |
| `tatib` | int | the **template's** id: the form uses it for querysets, never as a write target |
| `entry` | int | the fill-in or choice being settled |

**Response 200**

```json
{"ok": true,
 "value": {"label": "Fill-in · Song", "title": "Nyanyian Pembuka",
           "line": "KJ 152 — Ada Kuasa", "meta": "Bait 1, 2, 3"},
 "data": {"kind": "2", "song": "152", "verses": ["1", "2", "3"]}}
```

- `value` is what the row shows: the kind line, the slot's own title, the settled citation and its meta line
  (a song's verses, a passage's edition when it differs). It comes from `ServiceEntry.citation()` on an
  unsaved instance, so it cannot drift from what the page would render.
- `data` echoes the submitted form fields verbatim; the client keeps it and replays it at Create (D003).

**Response 400** — the form's own errors, keyed by field: `{"ok": false, "errors": {"verses": ["…"]}}`.
**Response 403** — editing is restricted or the request is not a POST.

## POST `/tatib/<int:template_id>/generate/`

Creates the dated service from a template in one transaction. Re-validates every slot; never writes to the
template.

**Request**

```json
{"name": "Ibadah Minggu",
 "date": "2026-11-01",
 "slots": [{"entry": 41, "kind": "song", "data": {"kind": "2", "song": "152", "verses": ["1", "2"]}}]}
```

- `slots` must cover **every** `FILL_IN` and `CHOICE` entry on the template, exactly once; the server does
  not trust **Next** (D004).
- `kind` is the option's stored kind name for a choice, and the fill-in's `fill_kind` name for a fill-in.

**Response 201** — `{"id": <new service id>, "url": "/tatib/<id>/"}`.

**Response 400** — `{"error": "…", "slots": [...]}`; nothing is created (the transaction rolls back).
**Response 403/404** — restricted editing; unknown or non-template id.

**Side effects** — one `TataIbadah(kind=SERVICE, date=…)` plus its entries, in the template's order:
ordinary entries copied, each fill-in replaced by its resolved entry, each choice by its chosen option,
legacy `TataIbadahItem` rows copied as legacy rows. The template's rows are not touched (FR-019).

## POST `/tatib/<int:service_id>/copy-as-template/`

Clones a service or a template into a new template.

**Request** — no body.

**Response 201** — `{"id": <new template id>, "url": "/tatib/<id>/?mode=template"}`.

**Side effects** — one `TataIbadah(kind=TEMPLATE, date=None)` with the same name and every entry in order;
a template source also brings its fill-ins, choices and options. Nothing is converted (FR-021). The
response's `url` is what the client opens, so the panel lands on Templates (FR-022).

## Unchanged surfaces

- `POST /editor/entry/new/save/`, `/editor/entry/<pk>/save/`, `delete/`, `reorder/` — untouched; a
  Service's own entries are still written exactly as today. They refuse `FILL_IN`/`CHOICE` (FR-010).
- `GET /media-library/references/` and `/media-library/cloud/manifest/` — untouched (D006).
- `GET /projector?service=<id>` — same URL and payload; a template's id renders the empty display (FR-012).
- The DRF `TataIbadahSerializer` — one added read-only key, `kind` (D011); no new route or verb.
