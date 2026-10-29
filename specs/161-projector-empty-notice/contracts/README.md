# Contracts: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`

## Interfaces exposed by this slice

none — the slice adds no route, payload, header, event or stored field. The projector page's
response and every script it loads keep the interface they have today; the change is the paint state
of one server-rendered paragraph inside that page.

## Not exposed

- `syncEmptyNotice()` — an internal function of `static/web/projector.js`'s IIFE; nothing outside the
  page can call it, and no other file reads the notice's `hidden`.
