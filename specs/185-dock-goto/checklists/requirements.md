# Requirements Checklist: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md` · **Created**: 2026-11-03 · **Depth**: Standard

- [ ] CHK001 Does FR-001 name every part of what is on air and of what is returned to, so a goto cannot be half-defined? [Completeness, Spec §Requirements]
- [ ] CHK002 Is "it stays a pointer" measurable — does the spec say exactly what must not appear in the stored state? [Clarity, Spec FR-001, SC-005]
- [ ] CHK003 Do US1–US4 cover every surface that can start, follow or end a goto, including the reading page's project control? [Coverage, Spec §User Scenarios]
- [ ] CHK004 Is the words state across a return decided rather than left to implementation — hidden during a goto, then Back? [Ambiguity, Spec §Edge Cases]
- [ ] CHK005 Does the spec say what happens to a playing recording when a goto arrives, and does that agree with projector/R5 as it stands? [Consistency, Spec FR-012]
- [ ] CHK006 Does any open item survive into gate 1 — is every marker answered or recorded as an assumption with its reason? [Completeness, Spec §Clarifications]
- [ ] CHK007 Are the success criteria observable without naming an implementation, and does each carry a measurement? [Measurability, Spec §Success Criteria]
- [ ] CHK008 Does every requirement name its capability, including the new `dock` one? [Traceability, Spec §Requirements]
- [ ] CHK009 Is "the projector's grammar and labels" pinned to one source of truth, or could the two surfaces drift? [Consistency, Spec FR-005, SC-006]
- [ ] CHK010 Are the failing-content cases covered — no lyric, a failed chapter, a corrupt goto — with what stays on air in each? [Coverage, Spec §Edge Cases]
- [ ] CHK011 Is the Go To's placement in the dock stated as a design assumption for the preview, not asserted as settled? [Clarity, Spec §UI/UX, §Assumptions]
- [ ] CHK012 Does the spec state its delta to spec 119's pinned state shape and to spec 184's lifecycle, rather than quietly extending both? [Consistency, Spec §The Go To after this slice]
- [ ] CHK013 Is the off-service state named for every control it changes — transport, bait strip, edition chip, list, head? [Completeness, Spec FR-007, FR-009]
- [ ] CHK014 Is every state in `## UI/UX` reachable by hand in the preview? [Coverage, Spec §UI/UX]
- [ ] CHK015 Does any requirement conflict with "one dock, one source" (spec 119) or the overlay's listen-only rule (overlay/R1)? [Consistency, Spec FR-011]
- [ ] CHK016 Does FR-018 name every way the layer closes, what it protects, and what closing restores? [Completeness, Spec FR-018]
- [ ] CHK017 Are the dock's own transport keys accounted for while the layer is up, so no covered control acts? [Consistency, Spec FR-018]
- [ ] CHK018 Does FR-019 say which of disabled or hidden, what the head keeps, and what restores it? [Clarity, Spec FR-019]
- [ ] CHK019 Does the state contract state every verb's behaviour with and without a goto, so no transition is left to the reader? [Completeness, contracts/display-state.md]
- [ ] CHK020 Is the return place's single home — the state's `screen` and `translation`, not a copy inside `goto` — findable from FR-001's wording? [Ambiguity, plan D001]
