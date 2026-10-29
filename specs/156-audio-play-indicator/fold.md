# Fold: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`
**Capability**: `projector`
**Folded**: 2026-10-29

## Operations

| Operation | Requirement | Before | After |
| --- | --- | --- | --- |
| `added` | `projector/R4` — the audio screen carries its playback control | the capability held R1 (the Go To) and R2 (the page renders from its own response); nothing stated what an audio screen paints | R4 with five scenarios: at rest, playback starts and stops, the chrome settles, the control is pressed, the local copy is missing |

**Renumbered at delivery.** Slice 155 (`feat/155-audio-presentation-lock`, PR #438) was in flight on the
same screen and folded `projector/R3` for its takeover before this slice reached the merge; this
requirement moved from R3 to R4 so the two can land in either order without a shared number.

## Counts

| | before | after |
| --- | --- | --- |
| requirements | 2 | 3 |
| scenarios | 7 | 12 |

## What did not fold

- Nothing: Converge closed with one accepted gap whose subject is SC-004's wording in the slice, not a
  behaviour. `R4` states the behaviour that shipped — the control hides with the chrome and its space stays
  reserved — so the wording gap has nothing to fold.
- The seek bar's unchanged clickability is out of scope by the spec's own assumption and stays unstated in
  the capability: it is existing behaviour, not new.

## Header

`**last folded**` 2026-10-26 → 2026-10-29; `**slices**` now begins `156-audio-play-indicator`.
