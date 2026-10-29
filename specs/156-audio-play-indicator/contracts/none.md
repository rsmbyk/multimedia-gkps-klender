# Contracts: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`

## Interfaces exposed by this slice

`none` — no HTTP endpoint, no template context variable, no companion route, no JavaScript API. The
projector page's response, its `projectorEntryData`/`projectorScreenData` payloads and the companion's
`/v1/files/<sha>` route are unchanged; the audio element still reads its bytes from the same place.

The slice changes one page-internal seam: a capture-phase click listener (`projector.js:909`) now returns
early when the click's target is inside `[data-audio-play]`. That is a behaviour of the page, not an
interface — nothing outside the page can observe or call it.

## Not exposed

- The markup of the audio player — unchanged; the control was already `<span data-audio-play>` in
  `projector.html:47`.
- `media-audio.js`'s `attach()` handle and its `onPlayback` option — unchanged; the idle timer keeps
  reading the same handle.
- The media companion's origin allowlist and file route — untouched by this slice.
