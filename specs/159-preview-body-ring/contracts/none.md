# Contracts: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md`

## Interfaces exposed by this slice

**none** — no endpoint, payload, template variable, stored value, DOM event or public script API is
added, removed or re-shaped. The preview dialog's markup is unchanged, the space listener keeps its
existing signature and the player's `toggle()` is called exactly as before.

## Not exposed

The suppression is internal to `static/web/preview.js` plus one declaration in
`static/styles/design/components.css`. Its observable surface is what a browser paints, which is what
`tests/e2e/test_preview_body_ring.py` reads through `getComputedStyle`, and what a person can see in
`specs/159-preview-body-ring/preview/preview.html`.

## Compatibility

Nothing here is consumed outside the page. The one class name this slice introduces, `is-shortcut`, is
scoped to `.preview__body` and is not a styling hook any other module reads — the module's own
`is-image-preview` / `is-audio-preview` / `is-video-preview` classes live on the dialog and stay
untouched.
