# Requirements Checklist: Project Button on the Song and Bible Pages

**Spec**: `specs/193-reading-project-button/spec.md` · **Created**: 2026-11-14 · **Depth**: Standard

## Completeness

- [ ] CHK001 Are both target surfaces covered with their exact routes (`/songs/<id>/` and `/bible/<book>/<chapter>/`), and the no-chapter book page excluded? [Completeness, Spec FR-001/FR-002/FR-007]
- [ ] CHK002 Is the Go To pointer shape specified for both kinds, matching the display state's own parser? [Completeness, Spec FR-003/FR-004]
- [ ] CHK003 Is the projector-window act specified for all three cases (closed, open, popup blocked)? [Completeness, Spec FR-005/US1 AC2–AC3/Edge Cases]
- [ ] CHK004 Is the ending of the detour specified without inventing a new control? [Completeness, Spec A1/FR-006]

## Clarity

- [ ] CHK005 Is "goto detour" defined in the spec's own vocabulary (the Go To pointer of spec 185) rather than left as the request's shorthand? [Clarity, Spec FR-003/FR-004]
- [ ] CHK006 Is the start position of each detour stated as a number or an explicit open question? [Clarity, Spec US2 AC1/A7]
- [ ] CHK007 Is "opens projector window if none open" stated as named-window reuse, not a new window per click? [Clarity, Spec FR-005/US1 AC2]

## Consistency

- [ ] CHK008 Does the control reuse the Tata Ibadah project group's anatomy and tokens instead of introducing new ones? [Consistency, Spec FR-001/UI/UX]
- [ ] CHK009 Does the spec leave the dock's Go To rules untouched and cite them where they already govern? [Consistency, Spec FR-006/SC-005]
- [ ] CHK010 Does the narrow-width rule match the existing Tata Ibadah rule's terms rather than inventing a new breakpoint? [Consistency, Spec FR-007/UI/UX]

## Coverage

- [ ] CHK011 Are the verse-less song, saved page, detour-already-on-air, and service-on-air edges each covered? [Coverage, Spec Edge Cases/FR-007]
- [ ] CHK012 Is in-page navigation (the stage swap) covered so the control cannot go dead? [Coverage, Spec US1 AC4/SC-004]
- [ ] CHK013 Are both editions (TB/SIM) covered for the passage detour, including the projector's flip reaching the other? [Coverage, Spec US2 AC2/A3]
- [ ] CHK014 Is hymn vs ordinary song citation handled by keying the detour on the song id? [Coverage, Spec Edge Cases/FR-003]
