# Fold: 221-empty-reading-stage

**Spec**: `specs/221-empty-reading-stage/spec.md` (Accepted, Gate 1 2026-11-22)
**Converge**: `specs/221-empty-reading-stage/converge.md` — Converged, no accepted gaps
**Date**: 2026-11-22

## Capabilities touched

| Capability | Operation | Requirement |
| --- | --- | --- |
| `reading` | `modified` | `R41` — the on-stage delete no longer swaps to a search landing; it keeps reading mode with a centred nothing-open stage, URL flag and history replacement. |

## Operations

- **modified `reading/R41`**: complete replacement of the paragraph's landing clause and of the
  "a confirmed delete lands" scenario, plus a new "the deleted record was on stage" scenario. The row
  removal, neighbour focus, guarded endpoints, soft-delete rules and history replacement all survive.
- **Header**: `last folded` stays `2026-11-22`; `221-empty-reading-stage` prepended to `slices`.
- **No additions or removals**: `reading/R50` and the rest of the tree are untouched.

## Before / after counts

| Measure | Before | After |
| --- | --- | --- |
| `reading` requirements | 50 | 50 |
| `R41` paragraphs | 1 | 1 (replaced) |
| `R41` scenarios | 4 | 5 |
| `slices` entries | 46 | 47 |
