# Contracts: none

**Spec**: `specs/221-empty-reading-stage/spec.md`

No external interface changes. No route, HTTP method, request or response schema, header, serializer,
webhook or event is added or altered. The existing sidebar delete endpoints keep their URLs, CSRF
guard and JSON `{"ok": true}` response; the only new input is an optional query flag on three existing
HTML pages, and the client change is confined to building that URL before the existing in-page navigation.
