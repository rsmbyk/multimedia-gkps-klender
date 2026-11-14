# Spec: Keep projector Go To current while online

- **ID:** 120
- **Status:** Accepted
- **Item:** ITEM-120
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

An operator using projector Go To while online can find current Bible and song content without reloading the projector or manually syncing the offline library. Saved results continue to work offline.

## Scope

### In scope

- Go To suggestions for Bible references, TB/SIM names and abbreviations, songbook references, song titles, and matching detours.
- Refresh timing, stale/failed sync handling, and current-query protection.

### Out of scope

- Public reading navigation, service list transport, Media Library files, and a new search backend.

## Rules

- On an online Go To interaction, the library is checked or refreshed so the final suggestions and detour data reflect the current committed server generation without page reload.
- Do not synchronize the full library on every keystroke. One interaction may share an in-flight check; repeated queries use the result until another meaningful freshness trigger.
- While a check is pending, existing saved suggestions may remain usable. If it fails, keep saved content available and avoid presenting it as newly fetched data.
- An older asynchronous check or lookup cannot replace a newer query, close an active detour, or alter the currently projected service.
- Offline Go To continues to use one complete committed local generation and retains existing ranking, labels, keyboard behavior, and translation rules.

## Acceptance scenarios

### Scenario: Changed song appears without reload

- **Given** Go To has loaded an older saved song title and the server title changes
- **When** the online operator opens Go To and searches the new title
- **Then** the final suggestion shows the new title and can open its current detour without reloading the projector.

### Scenario: Changed Bible data appears without reload

- **Given** a saved Bible generation and a newer server verse or name
- **When** the online operator searches its reference or name
- **Then** the final suggestion and detour use the newer data while preserving TB/SIM matching rules.

### Scenario: Offline or failed refresh

- **Given** a complete saved generation and an unavailable or failing network
- **When** the operator opens Go To
- **Then** saved suggestions remain usable and the current projection state stays intact.

### Scenario: Query changes during refresh

- **Given** a pending freshness check for one query
- **When** the operator types another query or closes Go To
- **Then** the earlier result cannot replace the new query or reopen Go To.

## Traceability

- E2E: `tests/e2e/test_projector.py`.
- Implementation candidates: `static/web/projector-library.js`, `static/web/projector.js`, `static/web/offline-library.js`; confirm after failing test.
