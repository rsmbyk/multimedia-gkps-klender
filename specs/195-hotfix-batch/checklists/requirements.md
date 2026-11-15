# Requirements Checklist: Production hotfixes — 2026-11-15

**Spec**: `specs/195-hotfix-batch/spec.md` · **Created**: 2026-11-15 · **Depth**: Standard

## Completeness
- [ ] CHK001 Are all six reported defects covered by a user story with an independent test? [Completeness, Spec US1–US6]
- [ ] CHK002 Is the stored contract for `ServiceEntry.verses` (verse IDs) named explicitly, so the fix cannot regress spec 189's storage? [Completeness, Spec FR-004/Edge Cases]
- [ ] CHK003 Is the re-read requirement scoped to every painted surface (overlay, dock, projector's existing behaviour named)? [Completeness, Spec FR-008/US6]
- [ ] CHK004 Are the accepted numbers the fixes must not disturb written down (badge CSS block, caption 1728×202 at 72px, checklist row anatomy)? [Completeness, Spec UI/UX]

## Clarity
- [ ] CHK005 Is "two visual lines" measurable (what counts as a line, where the floor is)? [Clarity, Spec FR-007/US5 scenario 4]
- [ ] CHK006 Is the reveal set that hides the badge the same one that hides the date (hover + focus reveal, hover-capable pointers)? [Clarity, Spec FR-001/UI/UX]
- [ ] CHK007 Does US6 state what repaints and what must not (same words → no repaint)? [Clarity, Spec FR-008/US6 scenario 4]

## Coverage
- [ ] CHK008 Are the deep-link and stage-swap paths both covered for the date picker? [Coverage, Spec US3 scenarios 1, 3]
- [ ] CHK009 Are the fresh-pick and re-rendered-checklist paths both covered for the verses summary? [Coverage, Spec US4 scenarios 1–4]
- [ ] CHK010 Are the keyboard/touch reveal cases covered for the badge hide? [Coverage, Spec US1 scenarios 4–5]
- [ ] CHK011 Is the already-fits lyric case covered so the fit cannot shrink screens that paint as accepted? [Coverage, Spec US5 scenario 1]

## Consistency
- [ ] CHK012 Does US2's styling come from the accepted preview rather than a new design? [Consistency, Spec UI/UX/Assumptions]
- [ ] CHK013 Do the preserved behaviours (no-verses named state, empty-verses refusal, projector re-read) appear as named constraints? [Consistency, Spec FR-006/US6 scenario 3]
- [ ] CHK014 Is the preview split honest about what a static page can show (fetch-dependent fixes named live)? [Consistency, Spec UI/UX preview reference]
