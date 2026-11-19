# Requirements Checklist: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md` · **Created**: 2026-11-19 · **Depth**: Standard

## Completeness
- [ ] CHK001 Does the spec name every box the defect reaches — title, entry header, screen row — with its own measured spill, rather than "the text overflows"? [Completeness, Spec US1 / UI/UX]
- [ ] CHK002 Is the body's horizontal scrollbar a requirement of its own, so fixing the two named boxes alone cannot pass? [Completeness, Spec FR-004 / SC-002]
- [ ] CHK003 Is the unchanged boundary listed with values — number column, chevron offset and centre, date box, row heights? [Completeness, Spec FR-005 / SC-004]
- [ ] CHK004 Are the two labels that declare their own cut named, so the rule cannot silently wrap them? [Completeness, Spec FR-006 / US3]

## Clarity
- [ ] CHK005 Is "wraps" measurable — a spill number a probe returns, not "looks contained"? [Clarity, Spec SC-001]
- [ ] CHK006 Is the choice of `anywhere` over `break-word` justified against spec 137's recorded reason for choosing `break-word` on the reading page? [Clarity, Spec Assumptions]
- [ ] CHK007 Does the spec say why the hyphenated filename already wraps, so a reader does not read the fix as "make long names wrap"? [Clarity, Spec Input / US2 scenario 2]
- [ ] CHK008 Is the preview honest about what it is — the live route with one rule injected, not a second server or a hand-built page? [Clarity, Spec UI/UX + preview README]

## Coverage
- [ ] CHK009 Are the three entry-header shapes covered — a media filename, an untitled entry's quiet lines, a song's reference and title? [Coverage, Spec FR-002]
- [ ] CHK010 Is a width where everything already fits covered as a no-change claim, not only the narrow panel? [Coverage, Spec US2 scenario 4 / Edge Cases]
- [ ] CHK011 Is the picker covered as a no-change claim, since it shares the panel and already wraps? [Coverage, Spec FR-007 / US3 scenario 2]
- [ ] CHK012 Are the live row's sticky pin and the open block's morph covered at the taller height the wrap produces? [Coverage, Spec Edge Cases / UI/UX States]
- [ ] CHK013 Is the widest value each column can actually hold named, so the fixture is not an arbitrary string? [Coverage, Spec Key Entities]

## Consistency
- [ ] CHK014 Does the mechanism match the dock's own picker rule and the reading page's wrap requirement, rather than inventing a third approach? [Consistency, Spec Assumptions / FR-007]
- [ ] CHK015 Does the spec leave the reading page, projector and overlay alone, with the measurement that says they are already clean? [Consistency, Spec Assumptions]
- [ ] CHK016 Is the scope decision — three surfaces rather than the two named — recorded as an assumption with its evidence rather than folded in silently? [Consistency, Spec Assumptions]
