# Contracts: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`

## Interfaces exposed by this slice

**none** — no endpoint, payload, template variable, stored value or DOM event is added, removed or
re-shaped. The page keeps calling `POST /v1/references` with `X-GKPS-Media-Token`; what moves is *when*
the page obtains the value it sends.

## Not exposed

The refresh's ordering is internal to `static/web/media-library.js`. Its observable surface is the request
the page sends, which `tests/e2e/test_media_library.py` captures and the live page can be watched for.
