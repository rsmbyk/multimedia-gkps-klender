# Requirements Checklist: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md` · **Created**: 2026-11-19 · **Depth**: Standard

## Completeness
- [ ] CHK001 Does the spec say the bound is on the font size, not the block height? [Completeness, Spec Intent / Assumptions]
- [ ] CHK002 Are both ends of the range named as percentages of the stage height? [Completeness, Spec FR-001/FR-002]
- [ ] CHK003 Is the behaviour at the floor stated — the block may exceed two rows? [Completeness, Spec Scenario 3]
- [ ] CHK004 Are the numbers at both reference viewports written down? [Completeness, Spec UI/UX]

## Clarity
- [ ] CHK005 Is the floor's measurement basis named (stage height per paint, matching `2cqh`)? [Clarity, Spec FR-002]
- [ ] CHK006 Is "two visual rows" the fit's target rather than a promise, given the floor? [Clarity, Spec Domain rules]

## Coverage
- [ ] CHK007 Does a test prove the rest at two different heights, so a width-based formula fails? [Coverage, Spec SC-001]
- [ ] CHK008 Does a test prove the floor with a lyric that cannot fit two rows? [Coverage, Spec SC-003]
- [ ] CHK009 Are the passage and liturgy plates covered as no-change rows? [Coverage, Spec SC-004]

## Consistency
- [ ] CHK010 Does the spec state the step as 4 % of rest — exactly 15 steps from 5 % to 2 % — and leave the look properties unchanged? [Consistency, Spec FR-004 / UI/UX]
- [ ] CHK011 Is the accepted edge expressed the same way in the capability file and the spec? [Consistency, Spec Domain rules]
