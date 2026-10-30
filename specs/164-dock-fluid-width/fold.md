# Fold: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md` · **Capability**: `reading`

## Capabilities touched

| Capability | File | Operation | Requirement |
| --- | --- | --- | --- |
| reading | `docs/spec/reading.md` | `added` | R33 — The dock fills whatever size it is given |

## The delta

- **added — R33**: the operator dock's panel takes the dock viewport's full width and height at every
  width of 320px and up; the picker stays one column whose rows span the body's content width; the
  bucket head keeps sticking; no other metric moves and every box at 560px or less equals spec 119's.
  Four scenarios: a wide dock, four buckets in a wide dock, a narrow dock, the scroller.
- **modified** — none.
- **removed** — none.
- **renamed** — none.

## Counts

| | before | after |
| --- | --- | --- |
| requirements in `reading.md` | 32 | 33 |
| scenarios in `reading.md` | (unchanged elsewhere) | +4 |

## Not folded

- Nothing — Converge closed with 0 findings, so every row of the traceability table is folded.

## Header

`last folded` stays `2026-10-29` (the same day); `164-dock-fluid-width` is prepended to the `slices`
list.

## Idempotence

Re-running this fold against the same spec finds R33 already present with the same text and changes
nothing.
