# Song form Checklist: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md` · **Created**: 2026-10-29 · **Depth**: Standard

- [ ] CHK001 Is the new line stated verbatim, so the reviewer reads the sentence rather than a description of it? [Clarity, Spec §US1 AC1, §FR-001]
- [ ] CHK002 Is the difference between "no song picked" and "a song with no verses" written as two distinct states with their own outcomes? [Completeness, Spec §FR-001, §FR-005]
- [ ] CHK003 Does first paint appear as its own requirement, so a script-only fix cannot pass? [Coverage, Spec §FR-002, §US1 AC4]
- [ ] CHK004 Is the disabled trigger stated as an outcome with its reason, not just as a style? [Measurability, Spec §FR-003]
- [ ] CHK005 Are both save refusals distinguished — a verse-less song and a cleared checklist — with the message each keeps? [Consistency, Spec §FR-004, §US2]
- [ ] CHK006 Does the spec name the geometry that must not move, with the measured numbers? [Measurability, Spec §SC-003, §UI/UX]
- [ ] CHK007 Are the four unchanged lines enumerated, so the change cannot leak into them? [Coverage, Spec §FR-005, §Edge Cases]
- [ ] CHK008 Is the stored-verses-but-cleared-song edge case given a direction (the entry stays saveable)? [Edge case, Spec §Edge Cases]
- [ ] CHK009 Does the spec avoid prescribing the implementation — no function named, no property, no condition — while staying testable? [Consistency, Spec §Requirements]
- [ ] CHK010 Is the failed-fetch state covered, so a broken request cannot read as "this song has no verses"? [Robustness, Spec §Edge Cases]
