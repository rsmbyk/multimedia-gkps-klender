# Reading Checklist: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [x] CHK001 Is the failure stated with what the page did (two draws 190ms apart, 8 placeholder rows at 800px, then 868px) rather than as "the fix didn't work"? [Measurability, Spec §What the page does today]
- [x] CHK002 Does the spec name the mechanism — the token is assigned inside `setStatus`, which the refresh now runs last — so no other explanation fits the 403? [Clarity, Spec §What the page does today]
- [x] CHK003 Is the suite's blind spot named as part of the defect, with the stub that caused it? [Completeness, Spec §What the page does today, §FR-003]
- [x] CHK004 Does the spec say what must NOT move — one draw, the head controls applied once — so the obvious fix (call `setStatus` earlier) is excluded by name? [Consistency, Spec §FR-002, §Assumptions]
- [x] CHK005 Is the new verification more than "the six go green", pinning the request header itself? [Coverage, Spec §SC-002, `research.md` D003]
- [x] CHK006 Is the degraded path still stated as surviving — a failed references write with a valid token? [Coverage, Spec §Edge Cases]
- [x] CHK007 Is it clear why the live readout is a post-merge step, rather than a missing test? [Clarity, Spec §SC-001, `research.md` D004]
- [x] CHK008 Does the spec keep the six spec-148 assertions unchanged, so a failure points at the fix and not at rewritten tests? [Consistency, Spec §FR-004, §US2]

**Gate 2**: ticked by the owner on 2026-10-28 — this list, the plan with its traceability table, the
task list and `analysis.md` were presented together, and the same answer authorised implementation.
