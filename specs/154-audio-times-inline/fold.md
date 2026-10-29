# Fold: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Date**: 2026-10-29

## Capabilities touched

| Capability | File | Operation | Detail |
| --- | --- | --- | --- |
| `reading` | `docs/spec/reading.md` | `added` | **R27 — An audio file's Preview reads its times as `current / total`**, with five scenarios (the pair, playing and seeking, read aloud, a long file, the file cannot be served) |

No `modified`, `removed` or `renamed` block: no existing requirement stated the times line's shape, so
nothing was superseded. `media-library.md` and `projector.md` were read and left alone — the projector's
own audio bar is named in R27 as explicitly unchanged, and it belongs to the same capability as before.

## Counts

| | before | after |
| --- | --- | --- |
| `reading` requirements | 26 | 27 |
| `media-library` requirements | 1 | 1 |
| `projector` requirements | 2 | 2 |

## Header

`docs/spec/reading.md`: `last folded` moved 2026-10-28 → 2026-10-29, and `154-audio-times-inline`
prepended to `slices`.

## Idempotence

Re-running this fold writes the same `R27` block and the same two header fields: the block is keyed on the
requirement ID, and the header is set from this slice's ID rather than appended to.
