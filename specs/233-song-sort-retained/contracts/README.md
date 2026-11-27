# Contracts: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`

## Interfaces exposed by this slice

none — the slice adds no endpoint, payload, event or shared function signature. It calls the
existing `applySongOrder()` from the existing `update()` path; the `#songSort` control's markup,
`aria-label`, `title` and `data-order` attribute stay as they are.

## Not exposed

The sort choice remains a document-lifetime variable in `static/web/reading.js`; no storage key,
URL parameter or server session value is introduced, and nothing outside the reading shell reads
it.
