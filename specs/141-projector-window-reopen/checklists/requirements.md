# Reading Checklist: reopening the projector window

**Spec**: `specs/141-projector-window-reopen/spec.md` · **Created**: 2026-10-27 · **Depth**: Lite

- [ ] CHK001 Is the control's condition stated as a state ("this page's service is the live service and on is true") rather than as a transition? [Clarity, Spec §FR-001]
- [ ] CHK002 Is "opens at the screen that is on air" measurable without reading the implementation — does the spec say what screen 0, a hidden display and a released display do? [Measurability, Spec §US1]
- [ ] CHK003 Does the spec say what happens when the window is already open, and distinguish that from opening a second window? [Completeness, Spec §FR-003, §Edge Cases]
- [ ] CHK004 Is the no-write rule stated for the reopen act, so a reader can tell it apart from Project's `show`? [Clarity, Spec §FR-002, §SC-002]
- [ ] CHK005 Are the width figures given as measurements with the pane they were taken in (400 px at 1440, 240 px at 1280), rather than as adjectives? [Ambiguity, Spec §UI/UX]
- [ ] CHK006 Does the spec name the widths where the control must not be drawn, and tie them to the existing rule it extends? [Coverage, Spec §FR-005, §US2.4]
- [ ] CHK007 Is every state the group can be in covered — off air, on air, hidden, released, another service live? [Coverage, Spec §US1.4, §UI/UX]
- [ ] CHK008 Does the spec say what a blocked popup does, so the control cannot silently release instead? [Completeness, Spec §Edge Cases]
- [ ] CHK009 Are the two buttons' existing treatments (primary Project, danger Stop projecting) declared unchanged, so this slice cannot quietly restyle them? [Consistency, Spec §UI/UX]
- [ ] CHK010 Is the new control's accessible name specified, given the face carries no words? [Completeness, Spec §FR-005, §UI/UX]
- [ ] CHK011 Does the spec keep spec 119's hide/release model intact rather than re-introducing a closing-window stopper? [Consistency, Spec §FR-004, §Assumptions]
- [ ] CHK012 Is the layout consequence at the narrowest desktop width stated as a number (69 → 111 px) instead of "may wrap"? [Measurability, Spec §US2.3]
- [ ] CHK013 Does the spec avoid promising per-window position memory or cross-machine behaviour? [Scope, Spec §Assumptions]
