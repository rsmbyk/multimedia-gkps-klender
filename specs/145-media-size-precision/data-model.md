# Data Model: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`

## Entities

None added or changed. `MediaIdentity.byte_count` and the companion's `size` / `total_size` already carry
the exact byte count, which stays the source of truth.

## Invariants

- A label is a pure function of its byte count: the same count always prints the same string on every
  surface (`FR-003`).
- A label's value is in `1`–`999.9`; a value that would reach `1000` belongs to the next unit (`FR-002`).
- A nonzero byte count never prints a zero value (`FR-001`).

## Not modelled

- The label itself — it is derived at paint time and never stored, so a formatter change needs no
  migration.
- Locale — the product prints `id-ID` dates but Latin digits and a full stop decimal everywhere already;
  this slice does not introduce a second numeric locale.
