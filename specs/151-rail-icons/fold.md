# Fold — the rail's marks and the stage's own

**Spec**: `specs/151-rail-icons/spec.md` · **Date**: 2026-10-29

## Capabilities touched

| Capability | Operations | Before | After |
| --- | --- | --- | --- |
| `reading` | `modified` R25 · `added` R29 | 28 requirements | 29 requirements |

## `reading` — modified R25

**A passage and a song carry a kind mark of their own.** The glyph is now named as the rail's own
mark — an open book with a Latin cross for a passage, the beamed pair for a song — instead of "an open
book" and "a single flagged note". Every clause about size, position, taupe ink, hidden assistive text,
no pointer and no added height is unchanged, and the scenarios say the row's mark is the rail's path.

The complete replacement block is in `docs/spec/reading.md`, which is the authority.

## `reading` — added R29

**The rail names its sections with the marks the stage draws.** One drawing per section, repeated
wherever the product draws it (rail, panel empty state, stage row, empty-stage tile); no rail mark
reuses a media family's mark, and audio files draw a five-bar waveform in all four places that mark is
drawn; every mark stays inline SVG on `currentColor`, in the box its surface already authors, hidden
from assistive technology; the rail keeps five destinations, and Search and Media Library are
untouched. Six scenarios: the Bible, a song, the service order, an audio file beside a song, the other
families, the theme.

## Not folded

Nothing. The slice converged with one partial finding (a wrong breakpoint in the spec's responsive
note), corrected in the spec before folding; no accepted gap.

## Header

`docs/spec/reading.md` — `last folded` moved to `2026-10-29`, and `151-rail-icons` was prepended to the
slice list.
