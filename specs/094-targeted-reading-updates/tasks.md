# Tasks 094: Targeted reading updates

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

## Checklist

- [x] Owner accepts this Draft before product code changes.
- [x] Add focused browser tests in `tests/e2e/test_targeted_reading_updates.py` for delete POST/read separation, duplicate activation, failed POST, failed readback, and targeted DOM preservation.
- [x] Make the reading shell expose completion of the affected view update and reject stale refresh responses.
- [x] Keep current/legacy delete confirmation busy through the completed view update; settle the single toast only afterward and preserve truthful recovery on readback failure.
- [x] Reconcile changed stage, sidebar rows, and dependent controls without replacing unchanged nodes; retain existing navigation, offline, focus, filters, scroll, and reorder behavior.
- [x] Run targeted browser tests and relevant endpoint tests; update traceability and release metadata.
- [x] Commit and push on the owner-selected branch, link the spec in its review PR, and mark ITEM-097 In review.
- [x] Before merge, verify required CI at the pushed head and mark the ITEM Done in the same PR.

## Done when

- [x] All Spec 094 acceptance scenarios pass.
- [x] An accepted deletion is never left as a clickable stale view, and unchanged reading components remain mounted during updates.
- [x] Board, tasks, changelog, and version metadata are complete in the review PR.
