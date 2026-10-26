# Reading Checklist: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md` · **Created**: 2026-10-26 · **Depth**: Lite

- [ ] CHK001 Does every editor kind named in scope have a scenario for its visible stage and sidebar representations? [Coverage, Spec §US1]
- [ ] CHK002 Are the reading-shell routes included by “all pages” explicit, with separate surfaces scoped by evidence? [Clarity, Spec §Assumptions]
- [ ] CHK003 Does search cover both a result that still matches and one that stops matching after an edit? [Coverage, Spec §US2]
- [ ] CHK004 Is “without a reload” measurable in the independent test and success criterion? [Measurability, Spec §US1, §Success Criteria]
- [ ] CHK005 Are shell state, failed saves, and existing entry saves covered as boundary behavior? [Completeness, Spec §Edge Cases]
- [ ] CHK006 Does the spec distinguish an unrelated stage from a stage that represents the edited record? [Consistency, Spec §FR-002]
- [ ] CHK007 Does the UI/UX section name the visible content change while keeping the unchanged layout and styles explicit? [Clarity, Spec §UI/UX]
