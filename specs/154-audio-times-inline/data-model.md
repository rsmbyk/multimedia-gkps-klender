# Data model: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Created**: 2026-10-29

No stored entity changes: no model, no field, no migration, no API payload.

## The times line (view state only)

| Field | Kind | Source | Lifetime |
| --- | --- | --- | --- |
| played | string `m:ss` | `clock(audio.currentTime)` | rewritten on every `timeupdate` |
| separator | literal `/` | markup | static |
| total | string `m:ss` | `clock(audio.duration)` | rewritten on `loadedmetadata` and every `timeupdate` |

The three children are `.audio-player__times` → `[data-audio-elapsed]`, `.audio-player__separator`,
`[data-audio-total]`, in that order. Laid out by `display: flex; justify-content: flex-end;
align-items: baseline; gap: 5px`.

## Invariants

1. **Same two selectors.** `[data-audio-elapsed]` and `[data-audio-total]` still exist, once each, in the
   line — `media-audio.js:33-34` finds them by those attributes.
2. **Order is played → separator → total.** Nothing else may sit between them; a fourth child would take a
   fifth gap.
3. **The pair's right edge is the seek bar's right edge** — both are children of
   `.audio-player__timeline`, so the bar's width is the pair's container width.
4. **Nothing here is persisted.** A reload starts at `0:00 / total` once metadata lands.
