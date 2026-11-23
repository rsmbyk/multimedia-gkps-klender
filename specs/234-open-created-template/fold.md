# Fold: a created Template opens on the reading stage

**Date**: 2026-11-23
**Slice**: `specs/234-open-created-template`

## Capabilities touched

- `docs/spec/reading.md` — `reading` — one `modified` operation on `reading/R46`.

## Operations

- **modified `reading/R46`** — complete replacement block: both created kinds open on the stage,
  the Template at `/tatib/<id>/?mode=template`; in-place navigation, focus and no-reload clauses
  carry over; edits and other kinds keep the list-refresh rule. The superseded Template clause and
  its scenario are kept visible as a dated retraction, not deleted.
- The capability header keeps `last folded: 2026-11-23` (same day as the previous fold) and prepends
  `234-open-created-template` to the slices list.

## Counts

- Requirements before: 57 · after: 57 · added 0 · removed 0 · renamed 0 · modified 1.
- No undeclared behaviour change: the only code change is the create branch's destination for
  `record_kind === 1`; no other surface moved.

## Evidence

- Converged at pass 1 (`converge.md`), zero findings, zero accepted gaps.
- Targeted E2E: 12 tests OK (six new spec 234 cases, six existing spec 209/215/167 regressions);
  five of the new cases were proven red against base `reading.js` first.
- Full browser suite deferred to the push step, per the owner's verification preference.
