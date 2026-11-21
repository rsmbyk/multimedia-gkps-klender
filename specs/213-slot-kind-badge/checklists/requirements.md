# Requirements Checklist: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md` · **Created**: 2026-11-21 · **Depth**: Lite

- [ ] CHK001 Does FR-001 name *which* surface draws the badge, given the same row renders on the template page, in the Use template dialog and in the sidebar? [Clarity, Spec §Edge Cases]
- [ ] CHK002 Is FR-002's "drawn in the mark's own stroke language" quantified anywhere a reader can check it — stroke width, grid, colour — rather than left to judgment? [Measurability, Spec §UI/UX]
- [ ] CHK003 Can FR-003 be verified without reading CSS — is the "unchanged frame and inner glyph" stated as something a test can compare? [Measurability, Spec §FR-003]
- [ ] CHK004 Does every requirement state an outcome rather than a technique, so the badge could be re-drawn and still satisfy the spec? [Completeness, Spec §Requirements]
- [ ] CHK005 Is the `fill_kind`-missing case (a legacy slot) covered by a requirement and not only by an edge case? [Coverage, Spec §Edge Cases]
- [ ] CHK006 Is FR-006's "the stage's own meta-text contrast" tied to a number, or does it ask the reader to invent one? [Ambiguity, Spec §UI/UX]
- [ ] CHK007 Do the acceptance scenarios cover all four kinds — song, passage, media, text — including the one kind the product has no glyph for? [Coverage, Spec §US1]
- [ ] CHK008 Is the text kind's mark a stated decision with its reasoning, rather than an inherited consequence of the other three? [Completeness, Spec §Assumptions]
- [ ] CHK009 Does SC-004 name every measurement that must not move, so "nothing moves" is checkable rather than assertable? [Measurability, Spec §SC-004]
- [ ] CHK010 Is the pointer/focus behaviour of the badge stated, so it cannot silently become an interactive target? [Clarity, Spec §FR-004]
- [ ] CHK011 Are the two surfaces the badge is deliberately *absent* from recorded as decisions with evidence, not as omissions? [Consistency, Spec §Clarifications]
- [ ] CHK012 Does the spec say what a reader loses if the badge is never drawn — i.e. is the problem statement's cost stated in the page's own words? [Completeness, Spec §What the page does today]
- [ ] CHK013 Is the badge's relationship to the existing `slot__kind` words defined — replacement, or repetition? [Consistency, Spec §Assumptions]
- [ ] CHK014 Does the spec avoid prescribing a class name or file path, so implementation stays free while the behaviour is fixed? [Completeness, Spec §Requirements]
