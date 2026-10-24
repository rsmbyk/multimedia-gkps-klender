# Behaviour Checklist: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md` · **Created**: 2026-10-24 · **Depth**: Lite

- [ ] CHK001 Is the trigger stated as a property of the data (both translations share the book name), not as the one book in the screenshot? [Clarity, Spec §US1]
- [ ] CHK002 Does every acceptance scenario name an observable the reader sees, rather than the mechanism that produces it? [Testability, Spec §User Scenarios]
- [ ] CHK003 Are the unchanged surfaces enumerated — distinct-name books, direct load, reload, saved copy? [Coverage, Spec §FR-004]
- [ ] CHK004 Is each success criterion stated so that it fails if the old behaviour returns? [Testability, Spec §Success Criteria]
- [ ] CHK005 Is the saved copy's coverage stated as inheritance with the mechanism named, rather than claimed as tested? [Completeness, Spec §Assumptions, §US2/AC3]
- [ ] CHK006 Are the edge cases decided — one translation with text, SIM selected before the move? [Completeness, Spec §Edge Cases]
- [ ] CHK007 Is `UI/UX` recorded as n/a with its reason instead of omitted? [Coverage, Spec §UI/UX]
- [ ] CHK008 Does the plan map every FR, SC and acceptance criterion to a file and a verification kind? [Traceability, Plan §Traceability]
- [ ] CHK009 Is the root cause recorded as reproduced evidence (running page), not as code reading alone? [Grounding, Plan §Phase 0, `research.md` D001]
- [ ] CHK010 Are the verification kinds honest — is nothing claimed as a test that no test exercises? [Honesty, Plan §Traceability split]

**Ticked at gate 2** (owner), together with the plan pack's acceptance.
