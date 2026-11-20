# Requirements Checklist: The dock's bucket head pins flush to the picker's top

**Spec**: `specs/197-dock-bucket-head-pin/spec.md` · **Created**: 2026-11-16 · **Depth**: Standard

## Completeness
- [ ] CHK001 Does the spec name the exact band the defect is about, and its size, rather than "a small gap"? [Completeness, Spec US1 / UI/UX]
- [ ] CHK002 Is the label's own invariant named as a requirement — the same offset under the divider at rest and pinned — so the fix cannot move it? [Completeness, Spec FR-002 / SC-003]
- [ ] CHK003 Is the reserve's fixed point covered (the head's foot does not move), so the keyboard path cannot regress? [Completeness, Spec FR-003 / US2]
- [ ] CHK004 Are the boxes that must not move listed with their values (head height, padding, body padding, runner entry, next band)? [Completeness, Spec FR-004 / UI/UX]

## Clarity
- [ ] CHK005 Is "pinned" measurable — is the offset where a head counts as pinned stated, and the group-boundary case excluded? [Clarity, Spec SC-001 / Edge Cases]
- [ ] CHK006 Is the success criterion a number a probe returns, not "looks flush"? [Clarity, Spec SC-001/SC-002]
- [ ] CHK007 Does the spec say why the defect is invisible at some offsets, so a reader does not read the fix as sniffing for glyphs? [Clarity, Spec Assumptions / Edge Cases]

## Coverage
- [ ] CHK008 Are both the pixel evidence and the hit-test evidence required, so a same-coloured leak cannot pass? [Coverage, Spec SC-001/SC-002]
- [ ] CHK009 Is the keyboard path covered by its own success criterion? [Coverage, Spec US2 / SC-003]
- [ ] CHK010 Is the runner — the other scroller that shares `.dock__body` — covered as a no-change claim? [Coverage, Spec US1 scenario 4 / FR-004]
- [ ] CHK011 Are widths other than the reported 449px and both themes covered, so the fix cannot be width- or theme-specific? [Coverage, Spec Edge Cases / UI/UX States]

## Consistency
- [ ] CHK012 Does the chosen mechanism match the two sticky elements already in the same file, rather than a new one? [Consistency, Spec Assumptions]
- [ ] CHK013 Does the spec refrain from changing the dock body's padding, which the other sticky elements depend on? [Consistency, Spec Assumptions]
- [ ] CHK014 Is the preview honest about what it is — the real markup and stylesheet, differing in one declaration? [Consistency, Spec UI/UX preview reference]