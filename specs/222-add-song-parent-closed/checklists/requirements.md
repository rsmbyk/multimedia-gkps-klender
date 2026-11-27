# Reading Checklist: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md` · **Created**: 2026-11-22 · **Depth**: Lite

- [ ] CHK001 Does US1 name the exact path — close only the first sidebar with the songs list open — and an independent browser check? [Coverage, Spec §US1]
- [ ] CHK002 Is the CSS boundary stated explicitly: hide only `.panel .editor-add`, never `.ch__add .editor-add`? [Clarity, Spec §FR-001]
- [ ] CHK003 Does the spec require the first sidebar's own add control to stay hidden in mini and closed states? [Consistency, Spec §FR-003]
- [ ] CHK004 Are mini parent, hymn book, no-songbook disabled state and closed songs list covered as edge cases? [Coverage, Spec §Edge Cases, §FR-004]
- [ ] CHK005 Are the before/after computed values and box measurements stated as numbers? [Measurability, Spec §UI/UX]
- [ ] CHK006 Is the non-visible surface (search landing, other section add controls) explicitly out of scope? [Scope, Spec §Assumptions]
- [ ] CHK007 Can every criterion be observed in a browser without reaching into CSS internals or mocking the DOM? [Measurability, Spec §Success Criteria]
- [ ] CHK008 Is the unchanged editor/form/hymn behaviour stated so the slice cannot silently widen? [Scope, Spec §FR-005]
