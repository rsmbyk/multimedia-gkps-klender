# Reading Checklist: the add bar opens over the seam

**Spec**: `specs/143-add-bar/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [ ] CHK001 Is the defect stated as measured movement with the mechanism named (the row's 43.6px taken from the flow), rather than as "it feels jumpy"? [Measurability, Spec §What the page does today]
- [ ] CHK002 Does the spec state "nothing moves" as a property of every entry, not only the hovered one, and give the sweep that proves it? [Clarity, Spec §US1, §SC-001]
- [ ] CHK003 Is the start bar's behaviour stated separately from the between-entries rows, so a reader can tell that the first entry's case is included? [Completeness, Spec §US1.3, §FR-005]
- [ ] CHK004 Does the spec pin the geometry both ways — the 20px slot in the flow and the 34px bar over it — so the two cannot drift apart? [Measurability, Spec §FR-002, §UI/UX]
- [ ] CHK005 Is the bar's hit area bounded, and its reason given (the entry's own controls sit exactly where a full-width overlay would land)? [Completeness, Spec §US2.1, §FR-004]
- [ ] CHK006 Does the spec cover the keyboard, given a floating bar could become mouse-only? [Coverage, Spec §US2.2, §FR-005]
- [ ] CHK007 Are the line's two states given as colours and opacities, not adjectives ("muted", "soft")? [Ambiguity, Spec §FR-003, §UI/UX]
- [ ] CHK008 Does the spec say what the resting button style is *and* what hover changes, distinguishing them? [Consistency, Spec §FR-006]
- [ ] CHK009 Are the gaps given as the measurements the eye compares — 53px of white either side of the first seam — rather than box values? [Measurability, Spec §FR-007, §SC-006]
- [ ] CHK010 Does the spec account for the eight tests that still assert the replaced mechanism, and say who changes them and when? [Traceability, Spec §Assumptions]
- [ ] CHK011 Is the touch case covered, where nothing hovers and the rows are drawn open? [Coverage, Spec §US2.4, §Edge Cases]
- [ ] CHK012 Does the spec avoid claiming behaviour beyond the stage — the dock, the projector, the editors and the sidebars are untouched? [Scope, Spec §Assumptions]
