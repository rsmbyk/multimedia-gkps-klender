# Research: A Go To still names itself with no service under it

## Decisions

### D001 — Check the detour before the empty-stage return

`renderCue()` in `static/web/projector.js` opens with `if (!cue || !entries.length) return;`, then
clears running labels and dispatches to `renderDetourCue()`. `renderDetourCue()` already handles a
missing return entry (`entryAt(current) === null` → `back to service`), so the detour needs no new
code — only to be reached. The fix splits the guard: `if (!cue) return;`, clear labels, check
`detour`, then `if (!entries.length) return;`.

**Rationale**: one dispatcher owns the cue; the detour has its own renderer and its own label and
controls, independent of the service's screen list.

**Alternatives**: call `renderDetourCue()` from `renderDetour()` directly (rejected — a second call
site would double-clear labels and drift from the dispatcher); delete the empty return (rejected —
a blank service would then paint an empty prefix, progress and Back over its empty stage).

### D002 — Pin the behaviour with E2E, not a JS unit test

The repo has no JS unit runner; user-visible acceptance is Playwright through
`StaticLiveServerTestCase`. The existing `tests/e2e/test_goto_shared_state.py` already builds a
no-service fixture and drives the real projector and display state.

**Rationale**: the defect is a rendered DOM state, and the read-back is the contract.

**Alternatives**: a new standalone test file (rejected — duplicates the fixture); a DOM stub in a
unit test (rejected — would test the guard, not the cue).

### D003 — Create the empty service from a worker thread inside the E2E case

Playwright's sync driver keeps an event loop running in the test thread, so Django 4.0 rejects an
ORM write there with `SynchronousOnlyOperation`. Writing the extra service in `setUp` would add it
to every case in the module; a `ThreadPoolExecutor` worker writes it and closes its connection
before returning.

**Rationale**: keeps the new fixture local to one case and lets Django drop the test database at
teardown.

**Alternatives**: move the fixture into `setUp` (rejected — changes every other case's service
list); `database_sync_to_async` (rejected — needs a coroutine the sync test cannot await).

## Provenance

- `static/web/projector.js:909–914, 1687–1715` — the guards and the existing detour cue renderer.
- `docs/spec/projector.md` R2 — the empty-service and Go To-over-empty scenarios.
- `tests/e2e/test_goto_shared_state.py` — the no-service fixture and the three-surface state seam.
- Red run (before): 2 failures, `AssertionError: 'Matius 5' not found in ''` and
  `AssertionError: 'NKB 43' not found in ''`. Green run (after): 2 tests `OK` in 5.754s; the
  related lane of 25 tests `OK` in 89.035s.
