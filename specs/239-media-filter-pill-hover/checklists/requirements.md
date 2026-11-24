# Media Library Checklist: filter-pill hover

**Spec**: `specs/239-media-filter-pill-hover/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is the reported surface — the six Media Library filter pills — named in a testable scenario? [Completeness, Spec §US1]
- [ ] CHK002 Is the chosen hover pair (`--focus` border, `--icon-hover-bg` fill) tied to the existing neighbouring controls rather than stated as a new colour? [Clarity, Spec §Introduction]
- [ ] CHK003 Is "hover effect" measurable as computed border/background values, not as a visual adjective? [Clarity, Spec §UI/UX, §SC-001]
- [ ] CHK004 Are before/after numbers given for both light and dark themes? [Completeness, Spec §UI/UX]
- [ ] CHK005 Is the selected-pill case covered so hover cannot override the pressed fill? [Coverage, Spec §US2, §FR-002]
- [ ] CHK006 Are geometry, label, focus-visible outline, separator dot and filter behaviour explicitly protected? [Consistency, Spec §US2, §FR-003]
- [ ] CHK007 Is the plain `:hover` selector (no `@media (hover: hover)` wrapper) explained against the Playwright hover-media finding? [Completeness, Spec §Edge Cases]
- [ ] CHK008 Is the no-motion decision stated, given the app's reduced-motion rule? [Consistency, Spec §Edge Cases]
- [ ] CHK009 Are all six pill states reachable by hand on the live preview? [Coverage, Spec §UI/UX, Preview README]
- [ ] CHK010 Is the patch bump recorded as an expectation rather than a gate-1 decision? [Ambiguity, Spec §Assumptions]
- [ ] CHK011 Is every functional requirement traced to at least one scenario? [Coverage, Spec §Requirements]
