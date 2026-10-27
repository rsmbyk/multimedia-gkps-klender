# Reading Checklist: the sidebars are a drawer stack

**Spec**: `specs/138-sidebar-overlay-stack/spec.md` · **Created**: 2026-10-27 · **Depth**: Standard

- [ ] CHK001 Is "the stage's width does not change" stated as a measurement with the widths in it, rather than as an intention? [Measurability, Spec §FR-001, §SC-001, §UI/UX]
- [ ] CHK002 Does every level of the stack have a requirement — the menu, the section list, the contents list — including the phone's fourth state? [Completeness, Spec §FR-002, §FR-007, §FR-010]
- [ ] CHK003 Is the toolbar's control's behaviour stated as three states and one gesture each, so an implementer cannot invent a fourth? [Clarity, Spec §FR-008, §FR-009]
- [ ] CHK004 Is the exception — no contents drawer on a phone — stated with its reason, so it is not "fixed" later as a bug? [Clarity, Spec §FR-018, §FR-020]
- [ ] CHK005 Are the two breakpoints named with their values, and does every requirement that depends on them say which one? [Consistency, Spec §FR-001, §FR-007]
- [ ] CHK006 Does the spec say what happens above the breakpoint, so the desktop's push layout is a requirement and not a hope? [Coverage, Spec §FR-014, §US1.4]
- [ ] CHK007 Is the always-visible edit control traced to the touch exemption the product already has, rather than presented as a new idea? [Consistency, Spec §FR-021]
- [ ] CHK008 Is the row's stacking tied to the edit control's presence, so the date's clipping is a cause and not a coincidence? [Clarity, Spec §FR-023]
- [ ] CHK009 Are the retractions kept visible — the logo, the offset, the inset, the back glyph? [Consistency, Spec §Clarifications]
- [ ] CHK010 Is every success criterion measurable by a rectangle, a computed style or a state attribute? [Measurability, Spec §Success Criteria]
