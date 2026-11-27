# Contracts: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`

none — the slice adds browser-event listeners inside `static/web/projector.js`. It exposes no HTTP
endpoint, message, storage key or DOM attribute to another component; the `fullscreenchange` and
`(display-mode: fullscreen)` events are browser interfaces consumed by this file alone, and the
inline `font-size` it writes is the same output the existing fit already writes.

## Not exposed

The fitter's `dataset.fitted` key stays an internal cache, and the page's projection channel
messages (`show` / `hide` / `release`) are unchanged.
