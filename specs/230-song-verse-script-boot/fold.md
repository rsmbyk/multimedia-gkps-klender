# Fold: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`
**Date**: 2026-11-23
**State**: Converged (pass 1, zero gaps)

## Capabilities touched

- `docs/spec/reading.md` — `added` `R55`.

## Operations

- **added** — `reading/R55`, a full block with three scenarios, stating that a script owning
  controls on a swapped-in page is booted by the shell, not by the swapped fragment.
- **modified** — capability header: `last folded` moved to 2026-11-23 and `230-song-verse-script-boot`
  prepended to `slices`.

## Counts

| | Before | After |
| --- | --- | --- |
| Requirements in `reading.md` | 54 | 55 |
| Slices listed in header | 52 | 53 |

## Not folded

None. No behaviour was declared out of scope by this slice.

## Idempotence

Re-running Fold would find `R55` already present with the same text and make no change.
