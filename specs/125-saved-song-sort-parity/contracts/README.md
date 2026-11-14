# Contracts: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`

## Interfaces exposed by this slice

none — the correction is an argument at one call site inside a browser renderer; no request, response,
event, or public function contract changes.

## Not exposed

`common()`'s `songListOpen` parameter stays private to `static/web/offline-render.js`; the slice changes
the value `songPage()` passes, not what the helper accepts or how any other caller uses it. The other
callers (`biblePage()`, `servicePage()`) are untouched and keep their current argument counts.
