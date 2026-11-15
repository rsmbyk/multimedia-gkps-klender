# Requirements Checklist: the runner keeps its live entry in view

**Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Created**: 2026-11-15 · **Depth**: Standard

- [ ] CHK001 Does FR-001 name both halves of the top snap — the row flush at the top edge and the block open beneath it — so an implementation cannot deliver one without the other? [Completeness, Spec FR-001]
- [ ] CHK002 Is "entirely out of the scroll area" measurable — does the spec name the box measured (`entryli`), the thing measured against (`clientHeight`), and the layout trick that keeps a pinned row's `offsetTop` from being mistaken for its position? [Clarity, Spec §Key Entities, §Assumptions]
- [ ] CHK003 Do US1 and US2 cover both exits the owner's screenshots show — far off the top and far off the bottom — with the same rule, not two behaviours? [Coverage, Spec §User Scenarios]
- [ ] CHK004 Is the partial-exit case decided (today's centring kept) rather than left to the implementer? [Ambiguity, Spec US3, FR-004]
- [x] CHK005 Does the spec state what a hand on the list still wins — mid-gesture and pending glide — and where that rule came from (`cancelPendingCenter`)? [Consistency, Spec US4, FR-006]
- [ ] CHK006 Is the bottom target pinned against the NEXT band's own rules, so the band's show/hide (`updateBand`) and the snap cannot disagree about where the entry's foot sits? [Consistency, Spec FR-002, FR-008]
- [ ] CHK007 Does the last-entry case (no band drawn) have its own target, or would FR-002's band-based arithmetic divide by nothing? [Coverage, Spec FR-003, Edge Cases]
- [x] CHK008 Are the trigger moments enumerated — every state notice, the morph's finish, the first paint — and is the one open moment (off-screen only) marked rather than smuggled in? [Completeness, Spec FR-005]
- [ ] CHK009 Does every requirement name its capability, including the new `dock/R14`, and does the fold note say spec 119's un-folded centring line is superseded? [Traceability, Spec §Requirements, §What the runner does today]
- [ ] CHK010 Does the go-to-on-air case have its own rule (or its own marker), rather than quietly inheriting the service entry's? [Clarity, Spec Edge Cases, FR-009]
- [ ] CHK011 Are the success criteria observable in a browser without naming code — row rect vs scroller rect, foot vs band top — and is each measured to a tolerance? [Measurability, Spec §Success Criteria]
- [ ] CHK012 Is every `## UI/UX` state reachable by hand in the preview, including the two snapped states and the reduced-motion instant? [Coverage, Spec §UI/UX]
- [ ] CHK013 Does any requirement change what a crossing morph does, or does the slice leave the 230 ms curve and `finishMorph`'s re-centre untouched? [Consistency, Spec Assumptions]
