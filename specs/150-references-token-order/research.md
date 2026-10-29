# Research: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`
**Unknowns remaining**: 0

## D001 — Assign the token, do not move `setStatus`

- **Decision**: in `refresh()`, after `/status` and `/files` resolve, assign `token = next.status.write_token`
  (guarded), and leave `setStatus(next.status)` and `render()` where they are at the end.
- **Rationale**: `write()` (`static/web/media-library.js:21`) builds its header from the module's `token`,
  which today only `setStatus` assigns (`:37`). Moving `setStatus` earlier would also move the head
  controls and the Files / Total size readout — which read the module-level `files` array, still the
  previous list at that moment — so the page would paint a stale count before its single draw. Assigning
  the one value the write needs keeps one visible update and authenticates the request.
- **Alternatives considered**: `write('/references', …, next.status.write_token)` — a second way to pass
  a token, and every later write would still depend on `setStatus`; calling `setStatus` before the write
  — splits the head controls from the list and paints a stale count; a retry after a 403 — hides the
  ordering bug behind a second request and doubles the write.
- **Provenance**: research (code read of `media-library.js:21`, `:28-41`, `:153-172`; the 403 measured on
  the live page).

## D002 — The E2E stub refuses what the companion refuses

- **Decision**: `_sampled_library`'s companion stub answers a `/references` POST whose
  `X-GKPS-Media-Token` is not `test-token` with `403 {'error': 'Not authorized.'}` — the companion's own
  reply at `multimedia/local_media.py:515`.
- **Rationale**: the stub answered 200 for every request, so a tokenless write was indistinguishable from
  an authenticated one and six cases were green against a page that fails on the real companion. The
  fixture is the reason this shipped; making it refuse the same request is the fix for that reason.
- **Alternatives considered**: a note in the spec asking reviewers to check headers — not a test; a
  separate unit test of `write()` — it would pass, because `write()` is correct: the defect is *when*
  the token exists, which only the page's own sequence can show.
- **Provenance**: research (`tests/e2e/test_media_library.py:977-990`; `local_media.py:514-515`).

## D003 — A case names the header, not only the consequence

- **Decision**: one new case, `test_the_first_refresh_writes_its_references_with_the_token`, captures the
  page's `/references` request and asserts its `X-GKPS-Media-Token` is the token `/status` returned, and
  that the first draw already carried the references.
- **Rationale**: the stricter stub makes the six cases red, which proves the page recovers — but not that
  *the first* refresh sent the token; a page could recover on a second refresh and still pass them. The
  new case pins FR-001 itself.
- **Alternatives considered**: asserting the 403 never happens — an absence assertion that passes if the
  write is never sent at all.
- **Provenance**: research.

## D004 — The live readout is a post-merge step

- **Decision**: SC-001 (the live page's `worst jolt: 0px`) is a `manual` row with steps, taken after the
  merge.
- **Rationale**: a worktree server cannot reach the companion — `local_media.py:447` admits only the
  origins in `GKPS_MEDIA_ALLOWED_ORIGINS`, and the compose `web` service serves the `develop` checkout
  (the same finding spec 148 recorded). The E2E harness is the pre-merge evidence; the live readout is
  the post-merge one, with exact commands.
- **Alternatives considered**: changing the companion's allow-list to include a dev port — a change to a
  running service's security boundary for a test, well outside this slice.
- **Provenance**: research (spec 148's `converge.md`, pass 1).

## Open

<!-- empty: Phase 0 finished, zero unknowns -->
