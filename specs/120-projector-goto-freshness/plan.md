# Plan 120: Keep projector Go To current while online

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-120
- **Bump:** patch

## Why

Projector Go To searches a snapshot of the committed browser library. In a controlled browser test, after the library saved a song and the server renamed it, Go To found no match for the new title and made no lookup request. Calling library sync made the new title appear. Reloading the projector also triggered sync and eventually showed it. Thus an online operator can need a refresh or manual sync before Go To reflects current data.

## Scope / edges

**In:** Projector Go To Bible/song suggestions and detours, online freshness, saved offline fallback, pending lookup state.

**Out:** Public reading navigation (Spec 119), service screen transport, a new server search API, and Media Library files.

## Approach

Retain the committed library as the offline source and refresh it when online Go To needs current data. Avoid making each keystroke start a full sync. Preserve the current suggestion ordering, TB/SIM behavior, keyboard/click selection, and protection against old lookup results replacing a newer query. Show saved results while a refresh is unavailable; do not silently claim current data after a failed sync.

## TDD

- Domain/app: no new model rule expected.
- E2E: rename/add a Bible or song record after initial save, open Go To while online, verify eventual current suggestions without page reload, and verify offline/failure fallback and query-race behavior.

## Risks

- The library sync can be expensive; bound its triggers and avoid a sync per keypress.
- New data can arrive after a query changes; refresh must not replace the current query's results with an older one.
