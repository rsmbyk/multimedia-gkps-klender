# Requirements Checklist: Sidebar Delete Buttons

**Spec**: `specs/190-sidebar-delete/spec.md` · **Created**: 2026-11-13 · **Depth**: Standard

## Completeness
- [x] CHK001 Are all three sidebar surfaces covered (non-hymn songbooks, non-hymn songs, Tata Ibadah services/templates)? [Completeness, Spec FR-001/US1–US3]
- [x] CHK002 Is the delete confirmation flow specified before any destructive request? [Completeness, Spec FR-005/SC-002]
- [x] CHK003 Are server endpoints specified for both confirm context and delete action with POST+CSRF? [Completeness, Spec FR-008/FR-009]
- [x] CHK004 Is post-delete UI behavior specified (row removal target, stage/history handling)? [Completeness, Spec FR-010/FR-011]

## Clarity
- [x] CHK005 Is the noun/labeling for template vs dated service deletes unambiguous? [Clarity, Spec FR-006/FR-007/US3]
- [x] CHK006 Is the “hide date on hover/focus” behavior scoped to dated Tata Ibadah rows with displayed dates? [Clarity, Spec FR-004/UI/UX]

## Coverage
- [x] CHK007 Are hymn/restricted/non-editor cases explicitly excluded from rendering controls? [Coverage, Spec FR-002/Edge Cases]
- [x] CHK008 Are hover, focus, cancel, success, and touch/responsive states addressed? [Coverage, Spec UI/UX/Edge Cases]
- [x] CHK009 Is the on-stage delete case covered with history replacement (not append)? [Coverage, Spec FR-011/Edge Cases]

## Consistency
- [x] CHK010 Does the spec align with existing editor modal patterns and row-edit affordances? [Consistency, Spec FR-003/FR-012]
- [x] CHK011 Does preview demonstrate the required dated-service hover state with date hidden? [Consistency, Spec UI/UX/Preview]