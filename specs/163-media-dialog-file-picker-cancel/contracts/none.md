# Contracts: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`

## Interfaces exposed by this slice

**none** — no endpoint, payload, template variable, DOM attribute or event is added, removed or
re-shaped. The page keeps listening for `cancel` on `#editorModal`; what changes is that it no longer
treats a descendant's event as its own.

## Not exposed

The discriminator is internal to `static/web/media-entry.js`. Its observable surface is whether the dialog
is still open after a dismissal — which `tests/e2e/test_media_library.py` asserts in the browser and a
person can see on the live route.
