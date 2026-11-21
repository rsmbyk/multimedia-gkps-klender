# Fold: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md`
**Date**: 2026-11-21 · **Slice**: `209-open-created-service`

## Capabilities touched

- `reading` — one `added` operation.

## Operations

- `added` — `docs/spec/reading.md` `R46 — A newly created service opens on the reading stage`, with
  four scenarios: creating from the sidebar, no reload and no panel change, Template/edit boundary,
  and a refused create.
- Header — `last folded` moved to 2026-11-21; `209-open-created-service` prepended to `slices`.
- No `modified` or `removed` operation: `R34`, `R36` and `R37` keep their wording; FR-006 restates
  that the generate/copy flows still navigate.

## Counts

- `reading` requirements: **45 before → 46 after** (highest id `R45` → `R46`).
- Scenarios added: 4. Removed: 0. Renamed: 0.

## Not folded

- The five pre-existing E2E errors recorded as F2 in `converge.md` are test-suite facts, not product
  behaviour; they stay out of the capability tree. The pointer-closed row-control error is reported
  for carding.
- `created` / `record_kind` are response fields, not a durable product behaviour; they stay in
  `contracts/save-response.md`.
