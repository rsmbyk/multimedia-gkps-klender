# Requirements Checklist: a newly created service opens on the reading stage

**Spec**: `specs/209-open-created-service/spec.md` · **Created**: 2026-11-21 · **Depth**: Standard

## Completeness
- [x] CHK001 Is the reported gap — save succeeds, new row appears, stage and URL stay put — a scenario with an independent test? [Completeness, Spec US1]
- [x] CHK002 Is the target state stated as measurable values (URL, heading, current row, child pane, marker) rather than "opened"? [Completeness, Spec US1/SC-001]
- [x] CHK003 Are the boundaries — Template, edit, other record kinds, generate, copy-as-template — each given a requirement and a scenario? [Completeness, Spec US2/FR-004/FR-006]
- [x] CHK004 Is the refused-create path covered so a failed save can never move the stage? [Completeness, Spec US3/FR-005]

## Clarity
- [x] CHK005 Is "service" pinned to a dated Normal Tata Ibadah, with Templates explicitly out? [Clarity, Spec Assumptions]
- [x] CHK006 Is "immediately" pinned to the successful save response, not the form submit? [Clarity, Spec Assumptions]
- [x] CHK007 Is "in place" defined measurably (marker, `performance.timeOrigin`, `data-nav` unchanged)? [Clarity, Spec SC-002]
- [x] CHK008 Does the UI/UX section say plainly that this slice adds no new look, and name the live defect as its gate material? [Clarity, Spec UI/UX]

## Coverage
- [x] CHK009 Are both the empty stage and the stage already showing another service covered by scenarios? [Coverage, Spec US1 scenarios 1-2]
- [x] CHK010 Are create from home and create from `/tatib/` both covered? [Coverage, Spec Edge Cases]
- [x] CHK011 Is the no-reload requirement covered without relying on a headless hover or focus quirk? [Coverage, Spec SC-002]
- [x] CHK012 Are validation, permission and failed-request refusals all covered? [Coverage, Spec US3/FR-005]

## Consistency
- [x] CHK013 Do the capability citations name the new block and the two blocks this slice does not change (`reading/R36`, `reading/R37`)? [Consistency, Spec Requirements]
- [x] CHK014 Do the success criteria cover every functional requirement with a declared measurement? [Consistency, Spec SC-001..004]
- [x] CHK015 Does the planned patch-level bump match a user-visible fix under the repo's scheme? [Consistency, Plan Bump]

**Gate 2**: accepted 2026-11-21 — all 15 items ticked by the owner; plan, tasks and analysis presented together. Implementation authorised.
