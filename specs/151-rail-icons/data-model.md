# Data model — the rail's marks and the stage's own

**Spec**: `specs/151-rail-icons/spec.md` · **Date**: 2026-10-29

**No stored data.** This slice changes drawn markup only: no model, no migration, no request, no
response, no template variable, no stored value.

## The marks, as the code holds them

| Mark | Path set (24-unit grid) | Drawn at | Ink | Source |
| --- | --- | --- | --- | --- |
| **Bible** | open book + Latin cross | 24px rail · 24px tile · 20px kind mark · 48px panel empty state | `currentColor` | `base.html`, `_entry_kind_icon.html`, `tatib.html`, `entries.js` |
| **Song** | beamed pair | 24px rail · 24px tile · 20px kind mark · 48px panel empty state | `currentColor` | same |
| **Tata Ibadah** | clipboard | 24px rail · 48px panel empty state | `currentColor` | `base.html` |
| **Audio** | five-bar waveform | 23px stage chip · 23px library row · 22px service-media row · 27px upload preview | `currentColor` | `media-stage.js` |

## Invariants the tests hold

1. **One path per kind.** The Bible's three places and the song's three places are string-identical
   (`d` attributes concatenated in DOM order).
2. **Two sizes, no third.** A rail mark is 24 × 24 in its 44 × 44 button; a kind mark is 20 × 20 at
   `row + 24`; the tile's glyph is 24 × 24; the chip's is 23 × 23 in its 42 × 42 box.
3. **The marks are not data.** No mark is stored, translated, personalised or fetched; the same markup
   is served on every page and in both themes.
4. **No mark is a family mark.** The five rail paths and the six `gkpsMediaIcon` paths share no string.

## What is *not* modelled

- The service's entry kinds, the media families and the media identities are unchanged; the slice
  reads `family` and `kind` and draws a different path for two of their values.
- No state (missing, unavailable, disconnected, empty) changes; each keeps the treatment it had.
