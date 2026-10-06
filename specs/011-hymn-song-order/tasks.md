# Tasks 011: Sort hymn book songs by number and sub-number

- **Status:** Accepted (owner, 2026-10-06)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner (2026-10-06)
- [x] Branch from the current base (`fix/011-hymn-song-order`)
- [x] Red — add a Django reading-view test in `multimedia/web/tests.py` for numeric number order, sub-number order, blank suffix, and null-number placement; ran it and observed the prior modification-time order
- [x] Green — apply hymn-only ordering in `multimedia/web/reading/views.py`; focused view and non-hymn sort tests pass
- [x] Add a browser acceptance test in `tests/e2e/test_reading.py` that opens the hymn book from the public home/index flow and asserts visible row order
- [x] Green — focused E2E passes with `DJANGO_ALLOW_ASYNC_UNSAFE=true`; see the verification note below for the normal-run harness failure
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on ITEM-012 and this spec
- [x] Set `VERSION` to `0.11.3`, add the changelog section, and set ITEM release version for the same PR
- [x] With PR #270 open, move ITEM-012 and the board to In review and record the PR link; move to Done before merge
- [x] Create the Conventional Commit and draft PR #270 linking `./spec.md` (same PR; extra commits fine)

## Verification note

The focused browser test passes with `DJANGO_ALLOW_ASYNC_UNSAFE=true`. Without that local override, the E2E runner errors in `ReadingE2ETests.setUp` with `SynchronousOnlyOperation` before the test body; the unchanged `test_reader_can_browse_and_read_a_song` reproduces the same failure. The browser assertion itself passes with the override. Full normal-run browser coverage remains unverified; the shared E2E harness is outside this spec's scope.

## Done when

- [x] Hymn song lists sort by numeric number and sub-number, including specified legacy-row behavior
- [x] Non-hymn last-modified and alphabetical sorting are unchanged
- [ ] Focused Django and normal E2E test commands are green
- [ ] Board, tasks, and version records are complete in the same PR
