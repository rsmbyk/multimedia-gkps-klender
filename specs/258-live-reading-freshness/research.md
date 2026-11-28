# Research: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`
**Unknowns remaining**: 0

## D001 — Separate polling endpoints
- **Decision**: one endpoint returns the open page's version; three endpoints return one fingerprint each for songbooks, songs and services.
- **Rationale**: the owner chose separate endpoints; the read paths differ and can be polled independently.
- **Alternatives considered**: one combined response (rejected by owner); polling full pages from the client (wastes bandwidth).
- **Provenance**: `owner decision; research inconclusive`

## D002 — List fingerprint
- **Decision**: SHA-256 of compact JSON of the ordered `(id, version)` pairs for the scope.
- **Rationale**: detects membership, order and row-version changes without a persisted list entity.
- **Alternatives considered**: a persisted list counter (new schema and writes); latest row version alone (a deletion can lower it).
- **Provenance**: `owner decision; research inconclusive`

## D003 — Scope parameters
- **Decision**: songs are scoped by `book`; services by `mode=service|template`; songbooks have no parameter.
- **Rationale**: matches the sidebar scopes, so a template change cannot alter the dated-service fingerprint.
- **Alternatives considered**: one fingerprint for all services (mode isolation untestable).
- **Provenance**: research

## D004 — Poll cadence
- **Decision**: 10 s while visible, at most one in-flight request per endpoint.
- **Rationale**: owner ruling and the existing dock/overlay cadence.
- **Alternatives considered**: 3 s (more requests); focus-only (not continuous).
- **Provenance**: `owner decision; research inconclusive`

## D005 — Page invalidation
- **Decision**: a client flag closes every dialog, disables controls in place and shows the badge.
- **Rationale**: slice 254's 409 is the real guard; invalidation stops the operator starting refused work.
- **Alternatives considered**: hiding controls (layout shift); a blocking overlay (hides the stage).
- **Provenance**: research

## D006 — Reload
- **Decision**: the badge Reload calls the existing in-place navigation refresh for the current URL.
- **Rationale**: page-only reload was the owner's ruling and the shell already has that path.
- **Alternatives considered**: `location.reload()` loses shell state.
- **Provenance**: `owner decision; research inconclusive`

## D007 — Sidebar reconciliation
- **Decision**: on fingerprint change, fetch the fresh fragment and reuse `reconcileChildren` keyed by row id; reapply existing order and filters; animate inserted rows only.
- **Rationale**: the product already has reconciliation and order reapplication.
- **Alternatives considered**: replace the whole list (loses focus and scroll); render from JSON (duplicates templates).
- **Provenance**: research

## D008 — Animation
- **Decision**: inserted rows animate 180 ms `cubic-bezier(.2,.8,.2,1)` from opacity 0 and `translateY(-6px)`.
- **Rationale**: measured in the preview; one continuous motion.
- **Alternatives considered**: no animation (owner asked for one); longer flourish (reads as jaggy).
- **Provenance**: `owner decision; research inconclusive`

## D009 — Persistence
- **Decision**: no new tables or columns; versions come from slice 254 and fingerprints are derived per request.
- **Rationale**: reading and presenting state, not new domain data.
- **Alternatives considered**: persisted list-version table (write amplification).
- **Provenance**: research

## D010 — Test seams
- **Decision**: Django test client for the poll endpoints; Playwright for badge, disabled controls and animated insert.
- **Rationale**: owner-approved existing seams.
- **Alternatives considered**: new unit seam for the fingerprint helper (implementation test).
- **Provenance**: `owner decision; research inconclusive`

## Open

