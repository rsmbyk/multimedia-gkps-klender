# Specification Quality Checklist: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is the broken surface named per dialog (text Create/Edit, media Create) rather than one vague "modal title"? [Clarity, §Input, §US1]
- [ ] CHK002 Is the regression's mechanism stated — a headerless entry form after spec 226 — without prescribing a particular CSS selector? [Clarity, §Overview]
- [ ] CHK003 Is the title band measurable as text offsets, band height and border width, not as "looks right"? [Measurability, §UI/UX, SC-001/SC-003]
- [ ] CHK004 Is the compact media Edit form explicitly scoped out and its numbers recorded? [Coverage, §Edge Cases, §UI/UX]
- [ ] CHK005 Does every FR and SC trace to a requirement (`reading/R10`) already in the capability tree? [Traceability, §Requirements]
- [ ] CHK006 Are both theme and loading/screen-reader cases accounted for without new rules? [Coverage, §Edge Cases, FR-004]
- [ ] CHK007 Is the narrow-window override required by FR-002 and covered by a scenario? [Consistency, US3/AC1, SC-003]
- [ ] CHK008 Are the untouched verse-header and other compact frames guarded with an independent test? [Coverage, US2, SC-002/SC-004]
- [ ] CHK009 Is the live preview path and click route from `/` concrete, with a restart command? [Completeness, header, `preview/README.md`]
- [ ] CHK010 Are card ID, spec number and patch level marked as re-checkable because parallel slices are open? [Consistency, §Assumptions]
- [ ] CHK011 Is the differential evidence (before/after numbers, not a screenshot) declared as the preview's proof? [Measurability, §UI/UX]
