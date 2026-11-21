# Requirements Checklist: the song entry's pickers

**Spec**: `specs/210-song-verse-picker/spec.md` · **Created**: 2026-11-21 · **Depth**: Standard

- [ ] CHK001 Are the two pickers' own behaviors separated so each can be verified on its own? [Completeness, Spec §User Scenarios]
- [ ] CHK002 Is every owner decision from the preview review carried into a numbered requirement? [Completeness, Spec §Requirements]
- [ ] CHK003 Is the difference from `reading/R30` stated instead of silently replacing the old disabled-field rule? [Consistency, Capability]
- [ ] CHK004 Is the difference from `reading/R43` stated instead of silently replacing the comma-list summary? [Consistency, Capability]
- [ ] CHK005 Is "preview until release" measurable without relying on a screenshot? [Measurability, Spec §Success Criteria]
- [ ] CHK006 Are the no-song, no-verses, one-verse and saved-verses states each covered by a scenario? [Coverage, Spec §Edge Cases]
- [ ] CHK007 Are the dialog width, tile size, column count, gap, separator and overlay offsets given as numbers? [Clarity, Spec §UI/UX]
- [ ] CHK008 Is the 200 ms motion stated as one curve with a reduced-motion outcome? [Clarity, Spec §UI/UX]
- [ ] CHK009 Are the unchanged backend grammar, ordering, labels and 200-result cap explicit as non-goals? [Coverage, Spec §Assumptions]
- [ ] CHK010 Does every functional requirement name its capability, new or existing? [Traceability, Spec §Requirements]
- [ ] CHK011 Are keyboard and touch paths both stated for the song results and the verse grid? [Coverage, Spec §User Scenarios]
- [ ] CHK012 Are all Clarifications answers reflected in the requirements with nothing left open? [Completeness, Spec §Clarifications]
