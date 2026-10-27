# Reading Checklist: The landing search field sits on the window's middle

**Spec**: `specs/139-home-search-center/spec.md` · **Created**: 2026-10-27 · **Depth**: Standard

- [ ] CHK001 Is "centred vertically" stated as a measurable outcome — a box centre against the window's middle, with the tolerance — rather than as an intention? [Clarity, Spec §FR-001, §SC-001]
- [ ] CHK002 Does the spec distinguish the field from the logo-and-field block, and say why the block's own centring is not the report? [Clarity, Spec §Assumptions, §Clarifications]
- [ ] CHK003 Is every width and height in the acceptance set named, so "at every width" is not left to the reader? [Measurability, Spec §SC-001]
- [ ] CHK004 Is the phone layout covered by a requirement of its own, given it pads differently and today mis-measures the section by 36px? [Coverage, Spec §FR-004, §US1 scenario 2]
- [ ] CHK005 Is the results view's compact bar excluded with its own numbers, so a regression there is detectable rather than a matter of taste? [Consistency, Spec §FR-005, §SC-004]
- [ ] CHK006 Does the spec say the page must not gain a scrollbar, rather than only that the field must move? [Completeness, Spec §FR-003, §SC-002]
- [ ] CHK007 Are the numbers in `## UI/UX` reproducible — a named page, engine and command — instead of described? [Measurability, Spec §UI/UX, `preview/probe_preview.py`]
- [ ] CHK008 Is the logo's 26px gap stated as a kept value, so the fix cannot quietly change the cluster's spacing? [Clarity, Spec §FR-002, §SC-003]
- [ ] CHK009 Is motion addressed, so "no animation" is a decision on record rather than an omission? [Completeness, Spec §FR-006, §UI/UX §Motion]
- [ ] CHK010 Is the slice's scope limited to CSS, with markup, scripts and assets named as untouched? [Consistency, Spec §Assumptions]
