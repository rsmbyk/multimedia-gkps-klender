# Dock Checklist: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md` · **Created**: 2026-11-28 · **Depth**: Lite

- [ ] CHK001 Does the spec state that the takeover happens at the live header's own top edge rather than the block's bottom edge? [Completeness, Spec §Clarifications]
- [ ] CHK002 Is the "off-screen" boundary given as a measurable condition (`li.top <= box.top + 0.5`) rather than an adjective? [Measurability, Spec §Requirements]
- [ ] CHK003 Does every functional requirement name the `dock/R19` block it modifies rather than claiming a new number? [Traceability, Spec §Requirements]
- [ ] CHK004 Are the takeover, straddle, fully-above, yield, crossing and go-to states all reached by a scenario or recorded as manual? [Coverage, Spec §User Scenarios]
- [ ] CHK005 Are the before/after boundary numbers, pin offsets and radius written as measured values in `## UI/UX`? [Measurability, Spec §UI/UX]
- [ ] CHK006 Is the one-visible-header rule stated for the straddle range, where the native header is still at the edge? [Completeness, Spec §Assumptions]
- [ ] CHK007 Is the clone's 0 px position justified against the rejected -4 px build and its measured hop? [Clarity, Research D002]
- [ ] CHK008 Are the unchanged bottom pin, NEXT band, go-to strip and click act written as explicit inspection or test rows? [Coverage, Plan §Traceability]
- [ ] CHK009 Is the verification split stated as `9 test · 4 inspection · 1 manual`, with the full browser suite deferred to the push step? [Measurability, Plan §Traceability]
- [ ] CHK010 Is the patch bump declared at Plan and applied in the pre-merge delivery commit, with the card checked against siblings before writing it? [Consistency, Plan header + Research D005]
- [ ] CHK011 Does the quickstart name a throwaway database and state which checks are not yet runnable? [Clarity, Quickstart]
- [ ] CHK012 Is the live-preview chronology recorded, including the code edit made before gate 1 and the absence of a pre-Fold commit? [Consistency, Spec §Assumptions]
