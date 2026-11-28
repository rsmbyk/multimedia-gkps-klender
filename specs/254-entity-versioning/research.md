# Research: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`
**Unknowns remaining**: 0

## D001 — Version field

- **Decision**: one `version` integer per tracked row, default 1, increasing by 1 only when stored values change.
- **Rationale**: the owner asked for an incremental object version; an integer matches every existing primary key and needs no new table.
- **Alternatives considered**: a UUID/etag on each write (no human-readable increment); a separate history table (the owner explicitly deferred history). Both lose the requested visible counter.
- **Provenance**: `owner decision; research inconclusive`

## D002 — Expected version transport

- **Decision**: form POSTs carry a hidden `expected_version`; JSON endpoints carry `expected_version` in the body. Creates carry no expected version for the new row but must carry the parent service's version when they land inside a service.
- **Rationale**: the existing editors are ModelForm POSTs and the reorder endpoints are JSON, so this follows the seams already present instead of adding a new transport.
- **Alternatives considered**: a header on every write (invisible to form markup and harder to test); global session token (does not identify the row the operator opened).
- **Provenance**: research

## D003 — No-op detection

- **Decision**: compare the stored field values with the submitted values before writing; compare ordered ID lists for reorder. Identical values leave both fields and version untouched.
- **Rationale**: the owner ruled that a no-op save is not a change; `auto_now` timestamps are not a reliable dirty signal.
- **Alternatives considered**: always bump on save (rejected by owner); hash the whole row (cannot tell which field changed and still needs a comparison).
- **Provenance**: `owner decision; research inconclusive`

## D004 — Propagation to services

- **Decision**: a single helper, called after any accepted song or verse write, increments every active `TataIbadah` — dated service or template — that has a song-kind entry naming a live verse of that song. It locks the affected services in primary-key order.
- **Rationale**: the owner confirmed that any song/verse change propagates; service rows are the unit the later invalidation surfaces will poll. Inactive rows are no longer projected and are excluded.
- **Alternatives considered**: per-entry version only (would miss changes made on the song page); lazy bump on next read (the server version would not be ahead when another operator writes).
- **Provenance**: `owner decision; research inconclusive`

## D005 — Distinct-service refusal count

- **Decision**: one helper returns the number of distinct active `TataIbadah` records whose song-kind entries name a live verse of the target. The verse modal, song confirmation and songbook confirmation all use it.
- **Rationale**: the owner ruled that verse, song and songbook notices all count distinct Tata Ibadah, including templates. The current verse count loops entries and can overcount.
- **Alternatives considered**: keep entry counts for verse and use services only for song/book (rejected — the owner wants one rule everywhere).
- **Provenance**: `owner decision; research inconclusive`

## D006 — Conflict response

- **Decision**: HTTP 409 with `{"error": "conflict", "message": "<stable text>", "current_version": <int>}`. Presentation of the response is out of scope for this slice.
- **Rationale**: existing write refusals return JSON `error` bodies with explicit status codes; this keeps the same shape and gives the later invalidation slice the current version.
- **Alternatives considered**: 200 with an error flag (cannot be distinguished from success by generic clients); 422 (the request is well-formed, the state is stale).
- **Provenance**: research

## D007 — Atomicity

- **Decision**: version comparison and the write share one transaction with `select_for_update()` on the target row; propagated service rows are locked in primary-key order.
- **Rationale**: without a lock, two writers can both read version 5 and both succeed. Ordered locking avoids deadlocks when one song touches several services.
- **Alternatives considered**: compare-then-update without a lock (race remains); unconditional `UPDATE ... WHERE version = ?` (works for the row but not for multi-row propagation).
- **Provenance**: research

## D008 — Delete confirmation width

- **Decision**: the delete confirmation is `min(560px, calc(100vw - 32px))`.
- **Rationale**: measured in the preview — at 520px the song notice wraps, at 540px the song fits but the songbook does not, at 560px both notices are one line with the default buttons.
- **Alternatives considered**: keep 480px and drop the note to two lines (owner asked for one); shrink button labels (changes product wording).
- **Provenance**: `owner decision; research inconclusive`

## D009 — Test seams

- **Decision**: endpoint tests through the Django test client are the rules seam; the existing Playwright verse-notice E2E is the user-visible seam, extended to the song and songbook confirmations.
- **Rationale**: the owner approved these seams; they are already used by the repo and need no new harness.
- **Alternatives considered**: new unit seam around the version helper (would test implementation, not behaviour); E2E for every conflict (UI handling belongs to a later slice).
- **Provenance**: `owner decision; research inconclusive`

## D010 — API surface

- **Decision**: no new public API endpoint; DRF serializers keep their current field lists.
- **Rationale**: the version is an internal concurrency guard for product write paths, not a client-facing resource.
- **Alternatives considered**: expose `version` on every serializer (widens the API contract without a requirement).
- **Provenance**: research

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
