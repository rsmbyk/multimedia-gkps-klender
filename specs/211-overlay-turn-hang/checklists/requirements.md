# Requirements Checklist: A speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md` · **Created**: 2026-11-21 · **Depth**: Standard

## Completeness
- [ ] CHK001 Does the spec distinguish the voice (already carried) from the layout (the defect)? [Completeness, Spec Intent]
- [ ] CHK002 Is the continuation's data shape defined exactly — no mark, non-empty voice? [Completeness, Spec Domain rules / Key Entities]
- [ ] CHK003 Are both sides of the rule stated: a screen with a mark, and a screen without one? [Completeness, Spec FR-001/FR-003]
- [ ] CHK004 Is the empty-voice case (ordinary line, cue, body with no speaker) stated as unchanged? [Completeness, Spec FR-004]
- [ ] CHK005 Are the out-of-scope surfaces named — projector, reading stage, entry preview? [Completeness, Spec Scope]

## Clarity
- [ ] CHK006 Is the anchor named as the screen's one words column, sized by the widest mark? [Clarity, Spec Domain rules]
- [ ] CHK007 Is "hang" quantified as an x position, not an adjective? [Ambiguity, Spec UI/UX / SC-001]
- [ ] CHK008 Is the no-mark screen's behaviour explained rather than left as a silent gap? [Clarity, Spec Assumptions]
- [ ] CHK009 Is the token-alone shape explicitly excluded, with a pointer to its own card? [Clarity, Spec Out of scope / Clarifications]

## Coverage
- [ ] CHK010 Does a test cover a leader continuation at 1280×720 with a 1 px tolerance? [Coverage, Spec SC-001]
- [ ] CHK011 Does a test cover a continuation that wraps, including the plate's right edge? [Coverage, Spec SC-002]
- [ ] CHK012 Does a test cover a no-mark screen and prove no indent is added? [Coverage, Spec SC-003]
- [ ] CHK013 Are the marked lines and the existing voice/overlay suites kept as no-change coverage? [Coverage, Spec SC-004]

## Consistency
- [ ] CHK014 Does the spec modify `overlay/R5` rather than create a duplicate rule? [Consistency, Spec FR table]
- [ ] CHK015 Does the spec avoid changing the voice colours or the mark-column width? [Consistency, Spec FR-005 / UI/UX]
- [ ] CHK016 Is the layout mechanism consistent with the marked row's grid and gap? [Consistency, Spec FR-002]
