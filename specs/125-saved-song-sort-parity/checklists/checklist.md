# Behaviour Checklist: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md` · **Created**: 2026-10-24 · **Depth**: Lite

- [x] CHK001 Is the trigger stated as a class (any song of any hymn book, opened from the sidebar) rather than as the one song in the report? [Clarity, Spec §US1]
- [x] CHK002 Does every acceptance scenario name what the operator sees — the control's presence or absence and the field's width — rather than the argument that produces it? [Testability, Spec §User Scenarios]
- [x] CHK003 Are the unchanged surfaces enumerated — ordinary songbooks, the book routes, offline, and the other fields on these pages? [Coverage, Spec §FR-003, §FR-005]
- [x] CHK004 Is each success criterion stated so that it fails if the old behaviour returns, including the transient, not only the settled state? [Testability, Spec §Success Criteria]
- [x] CHK005 Is the server page's rule stated with its source (spec 011 and the view), so the fix cannot drift into changing the server instead? [Clarity, Spec §Assumptions, `research.md` D002]
- [x] CHK006 Is the measured evidence recorded as numbers from the running page, not as an adjective? [Grounding, Spec §UI/UX, `research.md` D001]
- [x] CHK007 Are the edge cases decided — an unnumbered hymn, a route with no saved book, the offline final frame? [Completeness, Spec §Edge Cases]
- [x] CHK008 Is `UI/UX` justified rather than waved through, and does it name the existing reference instead of inventing a new design? [Coverage, Spec §UI/UX]
- [x] CHK009 Does the plan map every FR, SC and acceptance criterion to a file and a verification kind? [Traceability, Plan §Traceability]
- [x] CHK010 Are the verification kinds honest — is nothing claimed as a test that no test exercises (the book routes are `inspection`)? [Honesty, Plan §Traceability split]
- [x] CHK011 Is the second difference found during research recorded and kept out of scope, rather than silently fixed or silently dropped? [Scope, `research.md` D004]

**Ticked at gate 2** (owner, 2026-10-24), together with the plan pack's acceptance.
