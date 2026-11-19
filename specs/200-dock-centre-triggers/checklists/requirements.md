# Dock Checklist: the dock centres its live entry only when asked

**Spec**: `specs/200-dock-centre-triggers/spec.md` · **Created**: 2026-11-18 · **Depth**: Standard

- [ ] CHK001 Does every requirement name its trigger explicitly enough that a reader can tell which event centres the list and which does not? [Clarity, Spec §Requirements]
- [ ] CHK002 Is "an item inside an entry" resolved for every candidate — screen row, Next band, entry header, go to row, bait chip? [Completeness, Spec §Assumptions]
- [ ] CHK003 Are all six idle conditions testable independently, each with a state where it alone is false? [Coverage, Spec §US3]
- [ ] CHK004 Is "idle" quantified — which events restart the count, and whether a still pointer counts? [Ambiguity, Spec §US3]
- [ ] CHK005 Is the list left where the operator put it for every event that no longer centres? [Coverage, Spec §US4]
- [ ] CHK006 Does the slice say what happens when the idle centring and a crossing land at the same moment? [Consistency, Spec §Edge Cases]
- [ ] CHK007 Is the disabled state of the new control tied to a state the dock can read, not to a guess? [Measurability, Spec §FR-003]
- [ ] CHK008 Is the reduced-motion behaviour stated for each of the three triggers, not only for the control? [Coverage, Spec §US1, §SC-005]
- [ ] CHK009 Does the spec keep spec 198's rule that a header click never scrolls the list? [Consistency, Spec §FR-005]
- [ ] CHK010 Is the centring target named precisely (live screen row, or the label row when the screen has none)? [Clarity, Spec §Key Entities]
- [ ] CHK011 Is the removal stated as the acceptance that this slice exists for? [Completeness, Spec §US4]
- [ ] CHK012 Is the superseded assumption about a key-driven crossing kept visible as a retraction, with the owner's later follow-mode answer beside it? [Consistency, Spec §Clarifications]
- [ ] CHK013 Does `## UI/UX` carry the preview's measured numbers rather than adjectives? [Measurability, Spec §UI/UX]
- [ ] CHK014 Does every success criterion name an observation a probe can make? [Measurability, Spec §Success Criteria]
- [ ] CHK015 Is the state the dock starts in named, and is it the state today's behaviour gives? [Completeness, Spec §FR-011]
- [ ] CHK016 Are the three ways back into following distinct from the two ways out, and is the transport's Next/Back pair explicitly mode-neutral? [Consistency, Spec §FR-002, §FR-004, §FR-006, §FR-007, §FR-012]
- [ ] CHK017 Is the service-on-air guard stated for following, including the go to case? [Coverage, Spec §FR-013]
