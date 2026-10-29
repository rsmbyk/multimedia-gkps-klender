# Contracts: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`

## Interfaces exposed by this slice

**none** — no HTTP endpoint, payload, template variable, stored value or DOM event is added, removed or
re-shaped. The page keeps calling the companion's `/status`, `/files` and `/references`, the same-origin
`/media-library/references/` view and its `media:status` listener exactly as it does today; only the
order in which the response is applied to the page changes.

## Not exposed

The refresh/render sequence is internal to `static/web/media-library.js`. Its one observable surface is
the sequence of frames the page paints, which is what `tests/e2e/test_media_library.py` samples — that
is a behaviour, not an interface.
