# Requirements Checklist: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [ ] CHK001 Is "never reads as zero" quantified for every magnitude, not just the reported one? [Completeness, Spec §Success Criteria]
- [ ] CHK002 Is the rounding rule stated as a rule rather than as an example? [Clarity, Spec §FR-002]
- [ ] CHK003 Is the unit base (decimal vs binary) stated and justified? [Consistency, Spec §Assumptions]
- [ ] CHK004 Is every surface that prints a size named, including the one that prints none? [Coverage, Spec §US2, Gap]
- [ ] CHK005 Is the `1000`-in-one-unit case handled and measurable? [Edge Cases, Spec §Edge Cases]
- [ ] CHK006 Does the spec say what stays unchanged about the line — typography, spacing — so the slice cannot drift into a redesign? [Clarity, Spec §UI/UX]
- [ ] CHK007 Is the derivation of the label from the stored byte count stated, so no migration is implied? [Consistency, Spec §Key Entities]
- [ ] CHK008 Is the chosen label style traceable to the owner's answer rather than to the agent's taste? [Traceability, Spec §Clarifications]
