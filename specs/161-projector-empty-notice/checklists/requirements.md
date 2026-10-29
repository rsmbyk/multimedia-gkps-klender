# Requirements Checklist: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md` · **Created**: 2026-10-29 · **Depth**: Standard

- [x] CHK001 Is "hidden" defined as taking no box in the layout, not merely invisible, so the stage's gained band is verifiable? [Clarity, Spec §Assumptions]
- [x] CHK002 Does every acceptance scenario name an observable outcome (the notice painted or not, the stage's room) rather than the mechanism that produces it? [Measurability, Spec §User Scenarios]
- [x] CHK003 Is the re-read case stated as in scope with its own trigger, and is the service-emptied-while-open case recorded out of scope with its reason? [Completeness, Spec §Edge Cases]
- [x] CHK004 Are the notice's copy, 28px size, colour and centred position explicitly frozen, so "nothing else changes" is checkable? [Consistency, Spec §FR-007]
- [x] CHK005 Is the released-display state decided rather than left ambiguous, and does it agree with the rule that the notice follows what the stage holds? [Ambiguity, Spec §Edge Cases]
- [x] CHK006 Is the detour's own fitting, cue and words declared unchanged, so the slice cannot drift into redesigning the passage screen? [Regression, Spec §FR-007]
- [x] CHK007 Do the §UI/UX numbers come from the rendered page at both stated viewports rather than from a CSS rule? [Measurability, Spec §UI/UX]
- [x] CHK008 Is the one-decision-point rule verifiable by inspection — a named function, its two callers, and no other writer? [Coverage, Spec §FR-005]
- [x] CHK009 Does the pack say what is not modelled (no server data, no persisted state, no client-created notice)? [Completeness, Spec §Assumptions]
- [x] CHK010 Is the service-adoption path covered as a state the rule must keep correct, with its own edge case? [Coverage, Spec §Edge Cases]
- [x] CHK011 Are the four E2E cases enough to prove both stories, including the side where the notice must stay? [Coverage, Spec §FR-006]
- [x] CHK012 Is every requirement mapped to a capability operation — `projector/R2` modified — so the fold has a destination? [Traceability, Spec §Requirements]

**Ticked by the owner, 2026-10-29 — gate 2.**
