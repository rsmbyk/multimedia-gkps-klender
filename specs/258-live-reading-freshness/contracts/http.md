# HTTP contract: freshness polls

**Spec**: `specs/258-live-reading-freshness/spec.md`

## `GET /freshness/page/`

Query: `kind=service|song`, `id=<positive integer>`.
Response: `{"version": <int>}` with HTTP 200; unknown or wrong-kind id returns 404.

## `GET /freshness/songbooks/`

Response: `{"fingerprint": "<sha256 hex>"}`.

## `GET /freshness/songs/`

Query: `book=<positive integer>`.
Response: `{"fingerprint": "<sha256 hex>"}`; unknown book returns 404.

## `GET /freshness/services/`

Query: `mode=service|template`.
Response: `{"fingerprint": "<sha256 hex>"}`; absent mode defaults to `service`.

## Fingerprint definition

The server serialises the ordered `(id, version)` pairs of the rows in that scope as compact JSON — no spaces, keys `id` then `version` — and returns the SHA-256 hex digest. A scope with no rows fingerprints the empty array.

All four endpoints are read-only and never mutate state.
