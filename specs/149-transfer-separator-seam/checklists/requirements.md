# Media library Checklist: The Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md` · **Created**: 2026-10-28 · **Depth**: Standard

- [x] CHK001 Is "one line" stated as a count of painted lines at the seam, rather than as "not doubled"? [Clarity, Spec §FR-001]
- [x] CHK002 Does every seam scenario say where the line sits relative to the text above and below it? [Measurability, Spec §UI/UX]
- [x] CHK003 Is the scroll container requirement stated for both the fits and the overflows case? [Completeness, Spec §FR-004–FR-006]
- [x] CHK004 Are the states that carry no divider enumerated, so the change cannot leak into them? [Coverage, Spec §US1 AC4]
- [x] CHK005 Does the spec name the token and the weight of each line, so a 2px seam and a 1px row border can be told apart? [Clarity, Spec §UI/UX]
- [x] CHK006 Is the padding guarantee written as a measured distance rather than as "the padding is preserved"? [Measurability, Spec §FR-005, §SC-002]
- [x] CHK007 Are the empty list, the single row and the over-long name covered? [Coverage, Spec §Edge Cases]
- [x] CHK008 Does the spec leave the divider's own appearance rule (when it appears) out of scope, rather than restating it? [Consistency, Spec §Assumptions]
