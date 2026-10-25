# Contracts: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`

No new endpoint, payload, field or event. The only interface that changes is the **refusal** of an existing
endpoint for one `kind`, and it is refused with the response an unknown kind already gets.

## The writing endpoints, for `kind=3`

| Method | Path | Request | Before | After |
| --- | --- | --- | --- | --- |
| `GET` | `/editor/entry/new/?kind=section_break&tatib=N` | — | `200`, a one-field form | `404` |
| `POST` | `/editor/entry/new/save/?tatib=N` | `kind=3`, optional `after`, optional `title` | `200 {"ok":true,"id":<pk>,"kind":"entry"}` | `404`, no row |
| `GET` | `/editor/entry/<pk>/edit/` (a break's pk) | — | `200`, the same one-field form | `404` |
| `POST` | `/editor/entry/<pk>/save/` (a break's pk) | any body | `200 {"ok":true,...}` | `404`, row unchanged |
| `POST` | `/editor/entry/<pk>/delete/` (a break's pk) | — | `200 {"ok":true}` | unchanged |
| `POST` | `/editor/entry/reorder/` | `{entry, order_number}` pairs | `200` | unchanged |

The `404` body is Django's own (`Http404('Unknown kind.')`), the same as for a mistyped kind today; no client
reads it. The browser treats any non-OK response as a failed save (the existing toast), so a stale page needs
no new handling.

## Surfaces that must agree

| Surface | File | Offers |
| --- | --- | --- |
| server page | `multimedia/web/templates/reading/tatib.html` | `scripture`, `song`, `text`, `media` |
| rebuilt empty state | `static/web/entries.js` (`EMPTY_ADD_*`, `emptyAddButton`) | the same four |
| saved page | `static/web/offline-render.js` (`addButtons`, `emptyAddButtons`) | the same four |

The parity between the three is a test, not a shared module: each renders in a different environment (Django,
the live shell, the cached shell) and spec 130 already sets that precedent.
