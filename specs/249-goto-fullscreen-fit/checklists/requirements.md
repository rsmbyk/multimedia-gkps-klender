# Projector Checklist: Go To detour fit on resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md` · **Created**: 2026-11-27 · **Depth**: Lite

- [ ] CHK001 Does the spec name the Go To detour's words as the failing surface, following the owner's retest? [Completeness, Spec §Input]
- [ ] CHK002 Is the missing path stated as `resize` fitting service screens only while `fitNeighbours()` skips the detour? [Clarity, Spec §Overview]
- [ ] CHK003 Are resize-only and fullscreen-signal-before-resize both covered? [Coverage, Spec §Acceptance scenarios]
- [ ] CHK004 Are the stage sizes and font sizes given as measured numbers rather than adjectives? [Measurability, Spec §UI/UX]
- [ ] CHK005 Is the fonts-ready detour gap recorded as a known, unaddressed case? [Coverage, Spec §Assumptions]
- [ ] CHK006 Does every functional requirement name the `projector/R14` block it modifies, with no new `R<n>`? [Traceability, Spec §Requirements]
- [ ] CHK007 Is the no-detour guard written so service screens and their neighbour fits stay unchanged? [Coverage, Spec §Requirements]
- [ ] CHK008 Does the plan carry every FR, SC and story scenario with a `Verified by` method and a `8 test · 4 inspection · 0 manual` split? [Traceability, Plan §Traceability]
