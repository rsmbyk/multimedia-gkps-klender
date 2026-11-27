# Plan Checklist: Media Library filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is every story scenario in §US1–US2 traced to a component and a verification method? [Coverage, `plan.md` §Traceability]
- [ ] CHK002 Is the declared `bump: patch` justified by a user-visible change and re-checkable against `develop`? [Consistency, `plan.md` header, VER-10]
- [ ] CHK003 Is the one-rule design stated without a hidden template, script or endpoint change? [Clarity, `plan.md` §Phase 1, `data-model.md`]
- [ ] CHK004 Is "hover feedback" measurable as computed border/background values, not a visual adjective? [Measurability, `plan.md` rows US1/AC1–AC3, SC-001]
- [ ] CHK005 Is the verification split counted from the traceability table (9 test · 5 inspection · 0 manual)? [Consistency, `plan.md` §Verification split]
- [ ] CHK006 Are the 5 inspection rows each assigned a concrete observable rather than left implied? [Clarity, rows US2/AC3, FR-003, FR-004, SC-003, SC-004]
- [ ] CHK007 Is the selector's specificity and pressed-pill guard provenance recorded, not just asserted? [Completeness, `research.md` D001]
- [ ] CHK008 Is the live preview's shape justified by server-rendered markup and real pointer hover? [Completeness, `research.md` D005, `preview/README.md`]
- [ ] CHK009 Does every test row have a red and a green task in `tasks.md`, including removal of the gate-1 CSS edit for the red run? [Coverage, `tasks.md` §US1–US2]
- [ ] CHK010 Is the full browser suite explicitly deferred to the push step instead of silently omitted? [Completeness, `quickstart.md` §Verify]
- [ ] CHK011 [Gap] Can the focus-visible outline be asserted without fabricating a keyboard gesture in Playwright? [Ambiguity, `plan.md` row US2/AC2]
- [ ] CHK012 Are card, capability ID and patch level re-checks present for a repo with parallel slices? [Consistency, `tasks.md` Polish, BRD-04/VER-04]
