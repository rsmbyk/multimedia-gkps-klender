# Reading Checklist: the overlay's text wraps inside the box that owns it

**Spec**: `specs/183-overlay-text-wrap/spec.md` · **Created**: 2026-11-02 · **Depth**: Lite

- [ ] CHK001 Is the defect stated with develop's own numbers per state and frame (710.45px, 722.08px, 433.95px, …) rather than as "text overflows"? [Measurability, Spec §What the surfaces do today]
- [ ] CHK002 Is the cause pinned to the absence of one property — checked on the stage, plate, row, caption and their children — so no second cause can explain the spill? [Clarity, Spec §What the surfaces do today]
- [ ] CHK003 Does the spec say why a run has to *exceed the 90 % cap* before anything overflows, so a reader does not expect every long word to reproduce? [Precision, Spec §What the surfaces do today, §research D006]
- [ ] CHK004 Is the owner's first scope answer kept as **superseded** beside the widened one, with both dates, so the reversal is visible rather than silently rewritten? [Consistency, Spec §Clarifications]
- [ ] CHK005 Are the numbers for the elements the widening added — the caption's 2,035.20 / 1,336.81 / 1,017.61px and the verse title's 207.39 / 178.59 / 104.69px — carried through the spec, the plan and the review page, now as values the fix must bring to zero? [Coverage, Spec §UI/UX, §SC-001]
- [ ] CHK006 Does the spec define what "inside the panel" means — the ink's right edge against the plate's content edge, not its border edge — so padding cannot hide a spill? [Precision, Spec §SC-001, §research D004]
- [ ] CHK007 Is "unchanged" made measurable for a body that fits, rather than asserted (the rule removed on the live page, then the same box re-read)? [Measurability, Spec §US2, §research D005]
- [ ] CHK008 Are the mark's own declarations protected by name (nowrap, max-content column) so a wrap rule cannot silently unclip a labelled row? [Consistency, Spec §FR-004, §US1 scenario 4]
- [ ] CHK009 Is the absence of a height limit stated as a decision with its reason, so a reviewer does not read it as an omission? [Clarity, Spec §Assumptions, §research D003]
- [ ] CHK010 Does the spec name the preview by path and say it is built from the captured DOM of the real page over the church's frame, so the reviewer can tell it is not a mock? [Traceability, Spec §UI/UX]
- [ ] CHK011 Are the acceptance tests named by file and behaviour, at three frame sizes, with the red-on-1.26.0 claim re-runnable? [Traceability, Spec §SC-001, §SC-003, §quickstart]
- [ ] CHK012 Is the owner's reversal recorded as a superseded answer with both dates, and do FR-001 / FR-006 / SC-001 / SC-006 read as one scope rather than a patch over the narrow one? [Consistency, Spec §Clarifications, §Assumptions]
- [ ] CHK013 Does the spec say why a 64-character kicker measures the same before and after, so a reviewer does not read that state as an unfinished fix? [Clarity, Spec §US1 scenario 6, §research D007]
- [ ] CHK014 Is the caption's own look stated as a requirement (weight, centring, balance, outline) rather than assumed to survive a text-flow change? [Coverage, Spec §FR-006, §SC-006]

**Gate 1**: presented unticked on 2026-11-02 — the tick list stays the owner's; the agent never ticks it.
**Gate 2**: presented unticked on 2026-11-02, after the scope was widened and the pack revised.
