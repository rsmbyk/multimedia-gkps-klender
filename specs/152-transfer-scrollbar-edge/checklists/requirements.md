# Media library Checklist: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` · **Created**: 2026-10-29 · **Depth**: Standard
**Revision 2** (2026-10-29, after gate 1): CHK003 and CHK006 restated for the bottom edge; CHK009 and
CHK010 appended.

- [x] CHK001 Is the outcome stated as a measured distance (0px of canvas between the bar and the border), rather than as "at the edge"? [Clarity, Spec §FR-002, §SC-001]
- [x] CHK002 Does the spec fix both ends of the bar in every state that can show it — library-opened, rail-opened, narrow, dark? [Coverage, Spec §US1/AC4, §SC-005]
- [x] CHK003 Is "nothing else moves" written as named distances for the row, the title, an age heading, the list's top and the scroll's end? [Measurability, Spec §US2, §FR-003, §FR-004]
- [x] CHK004 Does the spec say what happens when the list does not overflow, so the fix cannot leave a reserved lane? [Completeness, Spec §FR-005, §Assumptions]
- [x] CHK005 Is the bar's own drawing (5px, token colours, no buttons) kept out of the change rather than restated as new? [Consistency, Spec §FR-006]
- [x] CHK006 Does the spec say which of the dialog's edges are in scope — right and bottom — and which is not, with the reason? [Clarity, Spec §Assumptions]
- [x] CHK007 Are the surfaces that are *not* this dialog named as out of scope? [Coverage, Spec §Assumptions]
- [x] CHK008 Is the measuring instrument recorded, given that headless Chromium draws no bar? [Measurability, Spec §UI/UX, §SC-001]
- [x] CHK009 Is the corner stated as an outcome (nothing paints outside the radius) rather than as a rule ("apply overflow"), with what it costs if left alone? [Clarity, Spec §FR-007, §SC-006]
- [x] CHK010 Is the 22px at the end of the scroll accounted for now that the list reaches the bottom border — named as a requirement, not left to be discovered? [Completeness, Spec §FR-004, §Assumptions]
