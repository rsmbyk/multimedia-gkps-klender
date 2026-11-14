# Dialog Checklist: a text entry's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md` · **Created**: 2026-10-25 · **Depth**: Lite

- [x] CHK001 Does every acceptance scenario name the viewport and the measured value it expects, rather than a comparative adjective? [Clarity, Spec §User Scenarios]
- [x] CHK002 Is "the same large modal" defined by the six values in `## UI/UX`, so a second reading of the request cannot produce a different box? [Ambiguity, Spec §UI/UX]
- [x] CHK003 Do FR-001 to FR-007 cover create, edit and every form that must *not* change? [Completeness, Spec §Requirements]
- [x] CHK004 Is each "unchanged" claim — switch, Save guard, 400 re-render, focus — paired with the scenario that would catch a regression? [Coverage, Spec §US1, US2]
- [x] CHK005 Is the scroll-placement requirement (FR-007) justified by a measured defect rather than by a preference, and does it name the other dialogs it touches? [Consistency, Spec §US3]
- [x] CHK006 Are the responsive values given as numbers at each named width, with the breakpoint where the gutters change? [Clarity, Spec §UI/UX, Responsive]
- [x] CHK007 Does the spec state what happens to the Text box at a short window (1280×600), where the frame, not the content, sets the size? [Coverage, Gap]
- [x] CHK008 Are the motion and the wide-line-length decisions recorded as assumptions the owner can veto, rather than left silent? [Completeness, Spec §Assumptions]
