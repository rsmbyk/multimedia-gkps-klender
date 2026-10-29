# Reading Checklist: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

## Requirements quality

- [ ] CHK001 Is the defect stated as what the browser and the page each did — focus lands on the body, the first key press flips `:focus-visible`, the body *is* the dialog's box — so that a fix aimed at the shortcut alone is excluded by name? [Clarity, Spec §What the page does today]
- [ ] CHK002 Is the measurement table reproducible: route, viewport, entries, and the four steps in order? [Measurability, Spec §What the page does today]
- [ ] CHK003 Does the spec say what must NOT be lost — the body's ring when reached by Tab, and arrow-key scrolling — so "delete the rule" is not a passing answer? [Consistency, Spec §US2, §FR-002, §FR-003]
- [ ] CHK004 Is the ring's purpose named (spec 071's scroll region) rather than described as unwanted chrome? [Clarity, Spec §US2]
- [ ] CHK005 Does FR-001 name the key's *effect* ("a key that operates the player") rather than the space bar, so the audio and video listeners are both covered without a second requirement? [Completeness, Spec §FR-001]
- [ ] CHK006 Is the fix's one forbidden shortcut spelled out — moving focus to the play button — with why it fails? [Ambiguity, Spec §Assumptions]
- [ ] CHK007 Is the untouched surface enumerated — image and PDF previews, the seek bar, the pointer click, Escape, the header tabs? [Coverage, Spec §FR-004, §Edge Cases]
- [ ] CHK008 Is every state of the ring accounted for, including the one left open? [Coverage, Spec §UI/UX, §Clarifications]

## Success criteria

- [ ] CHK009 Does each criterion name the thing measured (`:focus-visible`, the computed outline, the player's paused state) rather than "the ring is gone"? [Measurability, Spec §Success Criteria]
- [ ] CHK010 Does SC-003 pin the ring's numbers, so a fix that also changes its geometry fails here? [Measurability, Spec §SC-003]

## Scope

- [ ] CHK011 Is the boundary stated where the spec could have grown: not narrowing the ring to bodies that scroll, not touching previews without a space shortcut? [Scope, Spec §Assumptions]

## Plan-quality questions (added at the Checklist stage, after `plan.md`)

- [ ] CHK012 Does the plan's mechanism follow from the requirement, or is it a preference dressed as one — is "a state class" argued against moving focus and against reusing `.focus-restore-quiet`? [Clarity, Spec §FR-001, `research.md` D001]
- [ ] CHK013 Is the state's lifetime stated, given that one body element serves every preview? [Completeness, `research.md` D002, `data-model.md`]
- [ ] CHK014 Is the discrepancy between SC-001's measurement cell and what any correct fix can produce recorded as a finding rather than quietly written around? [Consistency, `research.md` D003]
- [ ] CHK015 Does every `test` row in the traceability table name a module and a function that the task list then creates? [Coverage, Spec §Success Criteria, `plan.md` §Traceability]
- [ ] CHK016 Are the two `manual` rows post-merge steps with a command and an expected reading, rather than "check it looks right"? [Measurability, `quickstart.md`, `plan.md` §Traceability]
- [ ] CHK017 Is the untouched surface named in the plan, so a reviewer can see what the diff may not contain? [Scope, `plan.md` §What is deliberately not done]

**Gate 2**: ticked by the owner — this list, the plan with its traceability table, the task list and
`analysis.md` are presented together, and one answer authorises implementation.
