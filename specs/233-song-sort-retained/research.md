# Research: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`
**Unknowns remaining**: 0

## D001 — Where the chosen order is re-applied

- **Decision**: re-apply `applySongOrder()` inside the shell's shared page-update path, directly
  after `reconcileChildren(chList, doc.querySelector('#chList'))`, before the arriving state is
  written to the document root.
- **Rationale**: this is the single place every in-place list refresh passes through. A probe E2E
  showed the base commit produces `['Beta', 'Zebra', 'Alpha']` with the button still reading
  `title`; re-sorting at the reconciliation point produces `['Alpha', 'Beta', 'Zebra']` and keeps
  the button truthful, with `performance.timeOrigin` unchanged.
- **Alternatives considered**: (a) re-sort only in the create handler — rejected by the owner, who
  chose the root-cause scope covering edits, deletes and row clicks; (b) ask the server for a
  sorted fragment — rejected because the shell intentionally refreshes in place and a URL/param
  change would break spec 225's no-reload guarantee; (c) CSS `order` — rejected because it would
  not keep the DOM order used by keyboard navigation and the list index controls.
- **Provenance**: research (code read and in-page measurement, 2026-11-23).

## D002 — Which sort states are re-applied

- **Decision**: call `applySongOrder()` unconditionally after the reconciliation, for both `m`
  and `title`; when there are no song rows the function is a no-op.
- **Rationale**: the `m` comparator uses the same modification stamps and source order as the
  server query, so re-applying it cannot diverge from the incoming order. A single unconditional
  call avoids a branch that would let the button and the rows disagree if the server's tiebreak
  ever changes.
- **Alternatives considered**: re-apply only when `songSort === 'title'` — narrower, but leaves a
  second code path whose correctness depends on the server and client comparators staying
  identical; rejected as the cheaper long-term choice.
- **Provenance**: research.

## D003 — Where the behaviour is pinned

- **Decision**: a Playwright E2E test in `tests/e2e/`, run through Django's
  `StaticLiveServerTestCase`, with explicit `Song.modified` stamps set by a queryset `update` so
  server order and alphabetical order differ deterministically.
- **Rationale**: the fault is visible only in the DOM after a fetch-driven refresh; the existing
  adjacent test `tests/e2e/test_reading.py::test_song_sort_toggles_between_last_modified_and_alphabetical`
  is the prior art and already drives `#songSort`. The probe was run red on `b46f7efe` and green
  with the one-line change.
- **Alternatives considered**: a unit test of the comparator — rejected because it would pass on
  base code, where the bug lives in the call site rather than the comparator; a screenshot diff —
  rejected because no geometry changes.
- **Provenance**: research (red/green evidence above).

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
