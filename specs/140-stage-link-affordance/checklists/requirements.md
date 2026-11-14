# Reading Checklist: The stage's entry links read as text until hovered

**Spec**: `specs/140-stage-link-affordance/spec.md` · **Created**: 2026-10-27 · **Depth**: Lite

- [ ] CHK001 Is "normal color" quantified as a token with its two measured values, rather than left as an adjective? [Clarity, Spec §FR-001, §SC-001]
- [ ] CHK002 Does the spec say what the underline looks like — offset, thickness, whether it animates — so "underlined if being hovered" is checkable? [Measurability, Spec §FR-002, §SC-003, §UI/UX]
- [ ] CHK003 Is the scope stated as a named selector, so "the link texts" cannot be read as every anchor in the app? [Clarity, Spec §Assumptions, §FR-004]
- [ ] CHK004 Is keyboard focus covered, given a rest state with no colour would otherwise leave keyboard users no affordance? [Coverage, Spec §FR-003, §US1 scenario 3]
- [ ] CHK005 Does the spec say what happens to the `--link` token and its contrast test, so retiring the colour does not orphan either? [Consistency, Spec §FR-004, §Assumptions]
- [ ] CHK006 Are the surfaces deliberately left alone enumerated — search results, media library, sidebar rows, editor? [Coverage, Spec §US2, §Assumptions]
- [ ] CHK007 Is the saved reading copy covered, so the rule is not assumed to apply only to a freshly served page? [Coverage, Spec §Edge Cases]
- [ ] CHK008 Does the spec say what a wrapped title's underline does, rather than leaving multi-line links to be discovered? [Completeness, Spec §US1 scenario 5, §UI/UX]
- [ ] CHK009 Is the touch pointer's lack of hover recorded as a stated outcome instead of an omission? [Ambiguity, Spec §Edge Cases]
- [ ] CHK010 Is the AA claim a measurement with values, not an assertion? [Measurability, Spec §SC-004]
