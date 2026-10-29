# Reading Checklist: the Media Library list holds still

**Spec**: `specs/148-media-library-refresh-flicker/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [x] CHK001 Is the defect stated with the shipped numbers (rows 119/101/123 → 97px, list 1024 → 956px, row 2 top 377 → 355) rather than as "it flickers"? [Measurability, Spec §What the page does today]
- [x] CHK002 Does the spec name the mechanism — a refresh that draws twice, the first pass with `uses = null` — so the fix cannot be satisfied by a different change that looks similar? [Clarity, Spec §What the page does today]
- [x] CHK003 Is "the list holds still" bounded by a measurable statement (each row's top has one value across every sampled frame) rather than "it doesn't jump"? [Measurability, Spec §FR-002, §SC-001]
- [x] CHK004 Does the spec enumerate every action that triggers a refresh, so a fix that leaves one of them jolting is caught? [Completeness, Spec §What the page does today, §US1]
- [x] CHK005 Does the spec say what the placeholder is still for, so a fix that deletes it outright fails? [Coverage, Spec §FR-003, §US2 AC2, §Assumptions]
- [x] CHK006 Is the cost of the chosen reading stated — the first paint arriving one round trip later, with its measured 16–31 ms — so the owner can veto it knowingly? [Clarity, Spec §Assumptions, `research.md` D001]
- [x] CHK007 Is the 2s poll declared out of scope with the reason it was excluded, so "unchanged" is distinguishable from "unnoticed"? [Completeness, Spec §FR-004, §Assumptions]
- [x] CHK008 Does the spec name the surfaces this page shares with in-flight work (slices 145/146/147), so this slice's boundary is reviewable against theirs? [Consistency, Spec §Assumptions]
- [x] CHK009 Is the verification seam justified — why a settled-DOM assertion cannot catch this — rather than assumed? [Coverage, Spec §Assumptions, §SC-001]
- [x] CHK010 Is the preview reachable by hand in every state it names, and does the pack say the sampler is what reads it? [Coverage, Spec §UI/UX, `preview/README.md`]

**Gate 2**: ticked by the owner on 2026-10-28 — this list, the plan with its traceability table, the task list and `analysis.md` were presented together, and the same answer authorised implementation.
