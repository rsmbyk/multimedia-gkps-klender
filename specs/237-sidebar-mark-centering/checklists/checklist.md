# Plan Checklist: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is every scenario in §US1–US3 traced to a component and a verification method? [Coverage, `plan.md` §Traceability]
- [ ] CHK002 Is the declared `bump: patch` justified by a user-visible fix and re-checkable against `develop`? [Consistency, `plan.md` header, VER-10]
- [ ] CHK003 Is the two-selector design stated without a hidden template, script or endpoint change? [Clarity, `plan.md` §Phase 1, `data-model.md`]
- [ ] CHK004 Is "centred" measurable as box-centre minus row-centre within ±1px, not as a visual adjective? [Measurability, `plan.md` rows US1/AC1, SC-001]
- [ ] CHK005 Is the verification split counted from the traceability table (8 test · 6 inspection · 0 manual)? [Consistency, `plan.md` §Verification split]
- [ ] CHK006 Are the 6 inspection rows each assigned a concrete observable rather than left implied? [Clarity, rows US1/AC2, US3/AC2, FR-003, FR-004, SC-003, SC-004]
- [ ] CHK007 Is the live preview's shape justified by the server-rendered rows and the control-only probe? [Completeness, `research.md` D005, `preview/README.md`]
- [ ] CHK008 Does every test row have a red and a green task in `tasks.md`, including the temporarily removed CSS edit? [Coverage, `tasks.md` §US1–US3]
- [ ] CHK009 Is the heavy suite explicitly deferred to the push step instead of silently omitted? [Completeness, `quickstart.md` §Verify]
- [ ] CHK010 Are card, capability ID and version re-checks present for a repo with parallel slices? [Consistency, `tasks.md` Polish, BRD-04/VER-04]
- [ ] CHK011 [Gap] Is the drag-copy inspection concrete enough without writing a flaky drag gesture? [Ambiguity, `plan.md` rows US3/AC2, FR-003, SC-003]
