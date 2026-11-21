# Requirements checklist — spec 217 (the runtime entrypoint survives the bind mount)

Reviewer-owned: the agent generates and never ticks. Each item asks about the requirements, never
about whether the code works.

## Completeness

- [ ] CHK001 Does the spec state the measured evidence for both services, rather than one cause for both? [Completeness, Spec §US1, §Assumptions]
- [ ] CHK002 Is the case with no bind mount covered, so `media` is not silently left out? [Completeness, Spec §Edge Cases, §FR-004]
- [ ] CHK003 Is "no file inside the mounted tree is required to start" stated as a requirement, or only implied by the path? [Completeness, Spec §FR-003]

## Clarity

- [ ] CHK004 Is "outside `/app`" measurable — does the spec say how a reviewer checks the path? [Clarity, Spec §SC-002]
- [ ] CHK005 Does the spec say whether the entrypoint's contents change, or could a reader rewrite it while "moving" it? [Clarity, Spec §FR-002, §Assumptions]

## Consistency

- [ ] CHK006 Does FR-002 (strip the copy) still make sense for a file now outside the build context's mounted path, or is it redundant with the `.gitattributes` pin from spec 216? [Consistency, Spec §FR-002]
- [ ] CHK007 Is the deferral to ITEM-233 consistent with `local-stack/R4`'s claim that a checkout that predates a change still starts? [Consistency, Spec §Assumptions, docs/spec/local-stack.md]

## Measurability

- [ ] CHK008 Can SC-001 be run without a Windows machine? [Measurability, Spec §SC-001]
- [ ] CHK009 Does SC-003 name the command sequence and the observable state? [Measurability, Spec §SC-003]