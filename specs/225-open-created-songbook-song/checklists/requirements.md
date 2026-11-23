# Requirements Checklist: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md` · **Created**: 2026-11-23 · **Depth**: Standard

## Completeness
- [x] CHK001 Is the gap stated with measured before/after values rather than "nothing happens"? [Completeness, Spec introduction]
- [x] CHK002 Is "opened" pinned to the click-through state for each record kind? [Completeness, Spec US1/US2, Clarifications]
- [x] CHK003 Are edits, other kinds and the spec-209 service path bounded? [Completeness, Spec US3/FR-004]
- [x] CHK004 Is a refused create covered so no selection can move without a saved row? [Completeness, Spec US3/FR-005]

## Clarity
- [x] CHK005 Are the destinations named as concrete routes and state fields (`lists` + `data-ch`, `/songs/<id>/` + `data-read`)? [Clarity, Spec FR-001/FR-002]
- [x] CHK006 Is "after created" pinned to the successful save response? [Clarity, Spec Assumptions]
- [x] CHK007 Is "in place" measurable (marker, `performance.timeOrigin`, `data-nav`)? [Clarity, Spec SC-003]
- [x] CHK008 Does UI/UX say plainly that no new look is added? [Clarity, Spec UI/UX]

## Coverage
- [x] CHK009 Are first-in-list and replacement of an already-open record covered? [Coverage, Spec US1/US2 scenarios]
- [x] CHK010 Are mini/collapsed panel and hymn book covered as edge cases? [Coverage, Spec Edge Cases]
- [x] CHK011 Is the no-reload requirement covered without a headless hover quirk? [Coverage, Spec SC-003]
- [x] CHK012 Are validation and failed saves both covered? [Coverage, Spec US3/FR-005]

## Consistency
- [x] CHK013 Does the capability cite one new `reading/R53` and the untouched `R46`/`R40`? [Consistency, Spec Requirements]
- [x] CHK014 Do the success criteria cover every functional requirement? [Consistency, Spec SC-001..004]
- [x] CHK015 Does the patch-level bump match a user-visible fix? [Consistency, Plan Bump]

**Gate 2**: accepted 2026-11-23 — all 15 items ticked; plan, tasks and analysis presented with the spec.
