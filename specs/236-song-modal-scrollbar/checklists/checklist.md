# Plan Checklist: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is every scenario in §US1–US3 traced to a component and a verification method? [Coverage, `plan.md` §Traceability]
- [ ] CHK002 Is the declared `bump: patch` justified by a user-visible fix and re-checkable against `develop`? [Consistency, `plan.md` header, VER-10]
- [ ] CHK003 Is the one-declaration design stated without a hidden template/JS/endpoint change? [Clarity, `plan.md` §Phase 1, `data-model.md`]
- [ ] CHK004 Are "no scrollbar" and "still scrolls inside content" both measurable, not adjectives? [Measurability, `plan.md` §Traceability rows FR-001/FR-003]
- [ ] CHK005 Is the verification split counted from the traceability table (12 test · 4 inspection · 0 manual)? [Consistency, `plan.md` §Verification split]
- [ ] CHK006 Are the 4 inspection rows assigned a concrete observable rather than left implied? [Clarity, rows FR-002, FR-004, SC-004, US3/AC3]
- [ ] CHK007 Is the preview's self-contained shape explained by the frame's opaque origin? [Completeness, `research.md` D004, `preview/README.md`]
- [ ] CHK008 Does every test row have a red and a green task in `tasks.md`? [Coverage, `tasks.md` §US1–US3]
- [ ] CHK009 Is the heavy suite explicitly deferred to the push step instead of silently omitted? [Completeness, `quickstart.md` §Verify]
- [ ] CHK010 Are card, capability ID and version re-checks present for a repo with parallel slices? [Consistency, `tasks.md` Polish, BRD-04/VER-04]
- [ ] CHK011 [Gap] Are the tall-form and short-viewport fixtures named concretely enough to write without a second research pass? [Ambiguity, `plan.md` rows US3/AC1–AC2]
