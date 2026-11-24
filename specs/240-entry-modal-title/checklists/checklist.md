# Plan Checklist: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md` · **Plan**: `plan.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is every story scenario and FR/SC in `plan.md` §Traceability with a declared verification method? [Coverage, §Traceability]
- [ ] CHK002 Is the `bump: patch` justified by a user-visible regression fix and re-checkable against unmerged branches? [Consistency, plan header, VER-03]
- [ ] CHK003 Is the design stated as one scoped CSS rule plus a narrow override, with no hidden template or script edit? [Clarity, `research.md` D001, `data-model.md`]
- [ ] CHK004 Is the band measurable as text offset, band height and border width rather than a visual adjective? [Measurability, rows US1/AC1, US3/AC1]
- [ ] CHK005 Does every test row name a file and a function, including the existing guard modules? [Traceability, §Traceability]
- [ ] CHK006 Are the 4 inspection rows each assigned a concrete observable (frame numbers, compact forms, probe, CSS diff, scrollbar)? [Clarity, rows US1/AC2, US2/AC2, US3/AC2, FR-004]
- [ ] CHK007 Is the verification split counted from the table as 10 test · 4 inspection · 0 manual in plan, tasks and quickstart? [Consistency, §Traceability]
- [ ] CHK008 Does every test row have a red and a green task, with the base red run recorded for the existing frame guard? [Coverage, `tasks.md`]
- [ ] CHK009 Are card ID, spec number, `reading/R10` and patch level re-checked before delivery against parallel slices? [Consistency, `tasks.md` Polish]
- [ ] CHK010 Is the full browser suite explicitly deferred to the push step instead of silently omitted? [Completeness, `quickstart.md` §Verify]
- [ ] CHK011 [Gap] Is the "before" readout an honest control when it injects an override into the live page rather than serving a second build? [Ambiguity, `research.md` D003, §UI/UX]
