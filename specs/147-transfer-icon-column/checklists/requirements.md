# Reading Checklist: the transfer row's icon column

**Spec**: `specs/147-transfer-icon-column/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [ ] CHK001 Is the defect stated with the shipped numbers (mark 32 → 21 / 22.75, text x 741 → 730.0 / 731.8) rather than as "misaligned"? [Measurability, Spec §What the page does today]
- [ ] CHK002 Does the spec name the mechanism — a shrinkable flex item whose automatic minimum is its 21px glyph — so the fix cannot be replaced by another that looks similar? [Clarity, Spec §What the page does today]
- [ ] CHK003 Is "aligned" bounded by two x values (the glyph's and the text's) rather than by "the rows line up"? [Measurability, Spec §FR-001, §FR-003, §SC-001, §SC-002]
- [ ] CHK004 Does the spec say what must *not* move — the glyph's 21px size and its centring — so the obvious alternative (pin the box at 21px) is excluded by name? [Completeness, Spec §Assumptions]
- [ ] CHK005 Is the truncation stated as still working, with its own criterion (`scrollWidth > clientWidth`, row stays 72px), so a fix that stops ellipsizing fails? [Coverage, Spec §FR-002, §SC-003]
- [ ] CHK006 Does the spec cover the narrow window where the text column is smallest, and the 200% zoom case? [Coverage, Spec §US2, §Edge Cases, §UI/UX]
- [ ] CHK007 Is the list's other geometry declared out of scope — row count, order, height, divider, rail — so review can tell "unchanged" from "unnoticed"? [Completeness, Spec §FR-005, §Assumptions]
- [ ] CHK008 Does the spec name the second stacked list (service media, grid, 38px) and say why it is untouched? [Consistency, Spec §Assumptions]
- [ ] CHK009 Is the preview reachable in both states by hand, with the readout that produces the numbers? [Coverage, Spec §UI/UX]
