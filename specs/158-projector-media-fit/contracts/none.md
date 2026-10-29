# Contracts: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`

**None** — the project exposes no interface this slice changes: no URL, no endpoint, no request body, no
response shape, no stored data. `T`, the drag and the wheel are page events, and the fit is computed in
the page.

One interface does move inside the page, and it is recorded here because two of the project's own
scripts share it:

```js
// static/web/media-pdf.js — the 7th argument is optional and additive
GKPSMediaPDF.paint(document, page, canvas, availableWidth, availableHeight, signal, options)

// options omitted            → today's behaviour: fit, and never a scale above 1
//                             (preview.js, the reader's dialog, unchanged)
// {fit: 'width'}             → the page's width fills the box, the height follows and overflows
// {fit: 'height'}            → the height fills the box, the width follows
// {fit: 'contain', upscale: true}  → the smaller ratio, above 1 allowed (the projector's default)
```

`paint()` returns the same `{width, height}` it returns today; with a fit that overflows, those numbers
are the painted size the projector clamps its pan against. `GKPSMediaImage.load()` is unchanged — the
projector already receives `{url, width, height}`.
