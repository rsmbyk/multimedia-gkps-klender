# Reading Checklist: Remove the offline library; the projector fetches on selection

**Spec**: `specs/136-remove-offline-library/spec.md` · **Created**: 2026-10-26 · **Depth**: Standard

- [x] CHK001 Does every surface of the removed feature have a requirement — the browser store, the service worker, the rail control and panel, the saved-copy paint, the routes, and the capability's own saved-copy rules? [Completeness, Spec §Requirements]
- [x] CHK002 Is "no local copy" measurable by naming the storage the reader inspects, and what counts as empty? [Measurability, Spec §SC-001]
- [x] CHK003 Is the index's content bounded so it cannot become a copy of the corpus — and does the spec say what it may *not* carry? [Consistency, Spec §FR-006]
- [x] CHK004 Is the loading mode's lock enumerated rather than described as "no interaction" — keys, clicks, Escape, the dismiss overlay, the field? [Clarity, Spec §FR-010]
- [x] CHK005 Does the spec say what the operator sees when the lock ends — on success and on failure? [Coverage, Spec §US3.3, §Edge Cases]
- [x] CHK006 Is a failed index fetch given an outcome that does not invent a control the request never asked for? [Coverage, Spec §Edge Cases]
- [x] CHK007 Is "chapter" bounded — both editions, and what happens when one edition lacks the verse? [Clarity, Spec §FR-009, §Edge Cases]
- [x] CHK008 Is the detour's step path complete, with each step marked local or fetching? [Completeness, Spec §US4, §FR-011]
- [x] CHK009 Is the index's freshness rule stated, rather than implying a search that follows edits? [Consistency, Spec §US2.5, §Assumptions]
- [x] CHK010 Are the capability effects stated for both halves — the requirements removed and the capability opened? [Traceability, Spec §FR-001, §FR-013, §Assumptions]
- [x] CHK011 Does the spec say that nothing replaces the removed offline fallback, so no reader expects one? [Clarity, Spec §Assumptions]
- [x] CHK012 Do the loading indicators' numbers in `## UI/UX` come from the preview, and does each state in the preview correspond to a requirement? [Measurability, Spec §UI/UX]
