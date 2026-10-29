# Projector Checklist: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Is the request kept in the owner's own words, including the follow-up that names the two group headings? [Clarity, Spec §Input]
- [ ] CHK002 Does the spec state the sheet as it ships with its measured box and column heights, rather than as "the row is in the wrong place"? [Measurability, Spec §What the sheet does today]
- [ ] CHK003 Is the column decided by a stated constraint — the sheet's box must not grow — with the rejected placement and its cost named? [Consistency, Spec §FR-004, §Assumptions]
- [ ] CHK004 Are the two groups' contents enumerated down to the label and the chord, so neither is left to the implementer? [Completeness, Spec §FR-001, §FR-002]
- [ ] CHK005 Does the spec name what may not move — `Display`'s other three rows, the row pitch, the heading box, the group gap, the sheet's motion — so a wider tidy-up is excluded by name? [Coverage, Spec §FR-003, §FR-005]
- [ ] CHK006 Is the key's behaviour guarded by its own story, so the regrouping cannot pass while Space's meaning changed? [Coverage, Spec §US2]
- [ ] CHK007 Are the states that already exist (a window shorter than the sheet, the narrow column, reduced motion) recorded as unchanged rather than left unstated? [Coverage, Spec §Edge Cases]
- [ ] CHK008 Does the spec say how the two states are reached in the preview, rather than describing the difference in adjectives? [Measurability, Spec §UI/UX]
- [ ] CHK009 Is the capability target named as `projector/R3`, with the reason the existing two requirements are not reused? [Consistency, Spec §Requirements]
