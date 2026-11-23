# Reading Checklist: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md` · **Created**: 2026-11-23 · **Depth**: Lite

- [ ] CHK001 Does the spec state which of the two identical buttons survives and why, without naming an alternative not in the page? [Clarity, Spec §Assumptions]
- [ ] CHK002 Is "no verses" defined against live verses rather than all verse rows? [Completeness, Spec §Edge Cases]
- [ ] CHK003 Are empty, with-verses, soft-deleted-only, hymn and restricted states each covered? [Coverage, Gap]
- [ ] CHK004 Is the button count in each state a number a probe can read, not an adjective? [Measurability, Spec §UI/UX]
- [ ] CHK005 Does the spec say which boxes must not move and which box legitimately moves? [Ambiguity, Spec §UI/UX]
- [ ] CHK006 Are the unchanged invitation copy, write endpoints and permission guards named as out of scope? [Coverage, Spec §Requirements]
- [ ] CHK007 Is the new placement claim tied to a reference page, two measured viewports and a declared mobile tolerance? [Measurability, Spec §US2, §UI/UX]
