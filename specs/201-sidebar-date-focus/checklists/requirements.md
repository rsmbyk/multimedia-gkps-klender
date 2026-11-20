# Requirements Checklist: a clicked service keeps its date

**Spec**: `specs/201-sidebar-date-focus/spec.md` · **Created**: 2026-11-19 · **Depth**: Standard

## Completeness
- [x] CHK001 Is the reported state (click leaves the link focused, pointer leaves, date stays hidden) a scenario with an independent test? [Completeness, Spec US1]
- [x] CHK002 Are both trailing-edge marks — the date and the Today badge — covered by a requirement? [Completeness, Spec FR-001/FR-002]
- [x] CHK003 Are the four painted states (rest, hover, clicked with pointer away, click elsewhere) named with their computed values? [Completeness, Spec UI/UX]
- [x] CHK004 Is the unchanged boundary named — media guard, touch rules, accessible label, geometry? [Completeness, Spec FR-003/FR-004]

## Clarity
- [x] CHK005 Is "focused for action reveal" pinned to the pencil/trash buttons rather than the row link? [Clarity, Spec Assumptions]
- [x] CHK006 Is the clicked-state testable without depending on headless Chromium's hover media? [Clarity, Plan D003]
- [x] CHK007 Does the spec say what the static preview simulates instead of implying it drives navigation? [Clarity, Spec UI/UX + preview README]

## Coverage
- [x] CHK008 Are keyboard link focus and keyboard action-button focus both covered? [Coverage, Spec US1 scenarios 5-6]
- [x] CHK009 Is the touch / `hover: none` path covered so the fix cannot regress it? [Coverage, Spec Edge Cases]
- [x] CHK010 Is the today-badge reveal covered in the same states as the date? [Coverage, Spec US2]

## Consistency
- [x] CHK011 Do the capability citations name the exact blocks the Fold will modify (`reading/R41`, `reading/R9`)? [Consistency, Spec Requirements]
- [x] CHK012 Is the preview's measured geometry consistent with the spec's UI/UX numbers? [Consistency, Spec UI/UX]
- [x] CHK013 Does the bump match a user-visible fix under the repo's scheme? [Consistency, Plan Bump]
