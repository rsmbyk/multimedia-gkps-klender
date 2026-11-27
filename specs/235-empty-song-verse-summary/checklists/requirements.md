# Requirements Checklist: An empty song names itself in the Verses section

Items are reviewer-owned. The agent generates them and never ticks them. Each carries a
quality dimension and a traceability marker to the spec section it questions.

- [ ] CHK001 Is the reversal from spec 210 stated as a deliberate change, with the old answer kept visible rather than silently rewritten? [Consistency, Spec §What the product does today]
- [ ] CHK002 Are Add and Edit modals, including an Add form returned by a refused save, named as the same state with one rule? [Completeness, Spec §FR-001, §FR-003]
- [ ] CHK003 Is "only the summary row part" defined as exactly which elements stay and which go? [Clarity, Spec §FR-001, §FR-002]
- [ ] CHK004 Is the visible state measurable — label, panel border/padding, one line, no bottom rule — rather than described as a feeling? [Measurability, Spec §UI/UX]
- [ ] CHK005 Is the no-song state explicitly kept at 0 px so the change cannot leak into it? [Coverage, Spec §FR-004]
- [ ] CHK006 Is the full-picker state, including first-verse tick, drag, All/Clear and the 200 ms reveal, pinned as unchanged? [Coverage, Spec §FR-004, §US2]
- [ ] CHK007 Are both save refusals preserved with their exact wording? [Completeness, Spec §FR-005]
- [ ] CHK008 Is the motion decision unambiguous — no new phase for the empty ↔ populated swap — and stated in numbers where relevant? [Clarity, Spec §UI/UX, §Assumptions]
- [ ] CHK009 Are the two capability requirements named with the right operation (modified, not added), and is superseded text kept as a note? [Traceability, Spec §Capability, §Assumptions]
- [ ] CHK010 Are the untouched surfaces named so a reader can tell this slice from spec 189's empty song stage? [Coverage, Spec §FR-006]
- [ ] CHK011 Is the failed-fetch edge distinguishable from a real empty song? [Robustness, Spec §Edge Cases]
- [ ] CHK012 Does every acceptance scenario map to a functional requirement or an explicit assumption? [Traceability, Spec §User Scenarios & Testing, §Requirements]
- [ ] CHK013 Is the claim about the server-rendered first paint verifiable without JavaScript? [Measurability, Spec §FR-003]
- [ ] CHK014 Is there an `[Gap]` for any question a reviewer could still ask about dark/light theme parity? [Gap, Spec §UI/UX]
