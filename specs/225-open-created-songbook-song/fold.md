# Fold: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`
**Date**: 2026-11-23 · **Slice**: `225-open-created-songbook-song`

## Capabilities touched

- `reading` — one `added` operation.

## Operations

- `added` — `docs/spec/reading.md` `R53 — A newly created songbook or song opens as its row would`,
  with four scenarios: songbook opens in the sidebar, song opens on the stage, in-place and no
  other path changes, and a refused create changes nothing.
- Header — `last folded` moved to 2026-11-23; `225-open-created-songbook-song` prepended to `slices`.
- No `modified` or `removed` operation: `R46` (created service) and `R40` (song verses) keep their
  wording; FR-004 restates that those paths are unchanged.

## Counts

- `reading` requirements: **52 before → 53 after** (highest id `R52` → `R53`).
- Scenarios added: 4. Removed: 0. Renamed: 0.

## Not folded

- Gate-1 reproduction numbers and the in-page marker are measurement facts, not product behaviour.
- The save response fields are boundary data, already documented in `contracts/save-response.md`.
