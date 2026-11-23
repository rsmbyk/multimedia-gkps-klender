# Reading Checklist: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is the reported surface (new/edit song entry modal) named in a testable scenario? [Completeness, Spec §US1, §US2]
- [ ] CHK002 Is the root cause — the dialog's own UA `overflow:auto`, not the content wrapper — stated before the fix? [Clarity, Spec §Introduction]
- [ ] CHK003 Is "no scrollbar" measurable without a visual adjective (gutter, computed overflow, wheel result)? [Clarity, Spec §UI/UX, §SC-001]
- [ ] CHK004 Is the collapsed verse panel's 10px overflow given with the measured before numbers? [Completeness, Spec §UI/UX]
- [ ] CHK005 Are both entry modes covered, including the collapsed and settled verse-panel states? [Coverage, Spec §US1, §US2]
- [ ] CHK006 Is the requirement that tall forms still scroll in `.editor__content` covered? [Coverage, Spec §US3, §FR-003]
- [ ] CHK007 Is the picker-menu escape (`reading/R48`) protected by a scenario? [Consistency, Spec §US1]
- [ ] CHK008 Is keeping the verse-panel animation stated, so a hide-with-`display:none` shortcut cannot pass? [Consistency, Spec §FR-004, §Assumptions]
- [ ] CHK009 Are light theme and narrow/tall window states reachable in the preview? [Coverage, Spec §UI/UX, Preview README]
- [ ] CHK010 Is the overlap with in-flight spec 235 recorded as an assumption rather than an unrequested change? [Ambiguity, Spec §Assumptions]
- [ ] CHK011 Is every functional requirement traced to at least one scenario? [Coverage, Spec §Requirements]
