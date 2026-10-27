# Reading Checklist: the entry surface

**Spec**: `specs/142-entry-surface/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [ ] CHK001 Is the removed surface stated as a value a reader can check — the fill's 3-of-255 step and the ring's 1.166 : 1 — rather than as "too subtle"? [Measurability, Spec §What the page does today]
- [ ] CHK002 Does the spec state the resting state as a state ("at rest, in this theme, nothing painted") rather than as a transition from the old box? [Clarity, Spec §FR-001]
- [ ] CHK003 Is "bare" bounded — does the spec say what is *not* removed (the box's padding and minimum height, the controls' column, the break's rule), so a reader cannot read it as "strip the row"? [Completeness, Spec §FR-003, §FR-004]
- [ ] CHK004 Does the spec account for the tokens being read by tests as well as by CSS, and say they are deleted rather than zeroed? [Completeness, Spec §FR-005, §Assumptions]
- [ ] CHK005 Are the five entry kinds each given their own acceptance scenario, with media's own numbers, rather than one sentence covering all of them? [Coverage, Spec §US3, §FR-004]
- [ ] CHK006 Does the spec name the touch case, where nothing hovers, and say what an entry looks like there? [Coverage, Spec §Edge Cases]
- [ ] CHK007 Is the vertical rhythm stated as a measurement with its parts (32px = 4 + 8 + 6 + 6 + 8), and declared out of scope if it is not changing? [Ambiguity, Spec §UI/UX, §Assumptions]
- [ ] CHK008 Does the spec give the hover fill's exact values for both themes, so it cannot be re-invented during implementation? [Measurability, Spec §FR-002, §UI/UX]
- [ ] CHK009 Is quiet focus restoration distinguished from deliberate focus, given the two now differ only by a fill? [Consistency, Spec §US2.3]
- [ ] CHK010 Does the spec say what happens to spec 068's record — superseded, not rewritten — and where that is marked? [Consistency, Spec §Assumptions]
- [ ] CHK011 Are the success criteria measurable without reading the implementation — computed values, entry counts on a named service, a named test file? [Measurability, Spec §Success Criteria]
- [ ] CHK012 Does the spec avoid promising a rhythm change, a new outline or a media-only surface that the owner did not ask for? [Scope, Spec §Assumptions, §Clarifications]
