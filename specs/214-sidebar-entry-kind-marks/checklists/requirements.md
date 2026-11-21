# Requirements Checklist: a contents row marks its entry's kind

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md` · **Created**: 2026-11-21 · **Depth**: Lite

- [ ] CHK001 Does FR-001 name the single surface the mark belongs to, given that rows of the same
  service render on the stage, in the dock and in the projector's entry list? [Clarity, Spec §FR-001]
- [ ] CHK002 Does FR-002 enumerate every kind, including the two slot kinds and the legacy row, rather
  than leaving "every entry" to the reader's guesswork? [Coverage, Spec §FR-002]
- [ ] CHK003 Is "the product's existing stroke language" quantified with a viewBox, stroke width and
  colour, so it can be checked? [Measurability, Spec §UI/UX]
- [ ] CHK004 Does FR-005 name the three geometry contracts the mark must not break — centring, the
  three-line clamp and wrapping — instead of a generic "nothing moves"? [Measurability, Spec §FR-005]
- [ ] CHK005 Is the 26px label-column cost declared with its measurement and a named risk, rather than
  hidden behind "the column is small"? [Measurability, Spec §UI/UX]
- [ ] CHK006 Is the section-break row's missing order number treated as a question, not silently
  resolved by an assumption? [Clarity, Spec §Edge Cases]
- [ ] CHK007 Does the spec state that spec 144 FR-008 is reversed for `#chList` only and that the dock
  stays excluded, with the evidence (the test and the class name)? [Consistency, Spec §What the page does today]
- [ ] CHK008 Can FR-003 be verified without reading the model — is "no new field or migration" stated
  as an observable fact about the row payload? [Measurability, Spec §FR-003]
- [ ] CHK009 Is the in-place rebuild after a save or delete covered by a requirement, not only an edge
  case? [Coverage, Spec §Edge Cases]
- [ ] CHK010 Does FR-004 fix pointer and focus behaviour, so the mark cannot silently become a second
  tab stop? [Clarity, Spec §FR-004]
- [ ] CHK011 Is the deleted-target case covered for the mark as well as the label (spec 144's lesson)?
  [Coverage, Spec §FR-006]
- [ ] CHK012 Are both themes' contrast figures tied to the product tokens and actual numbers?
  [Measurability, Spec §SC-006]
- [ ] CHK013 Does every FR state an outcome rather than a file path or class name, leaving the
  implementation free? [Completeness, Spec §Requirements]
- [ ] CHK014 Does the spec say what the reader loses today — the cost of the problem — in the page's
  own terms? [Completeness, Spec §What the page does today]
- [ ] CHK015 Is the choice between the two measured layouts left as a marker to Clarify, with a
  recommendation, rather than silently made? [Clarity, Spec §Clarifications]
- [ ] CHK016 Does FR-002 keep the slot's corner kind modifier from spec 213, rather than reducing a
  fill-in or choice to a bare dashed mark? [Coverage, Spec §FR-002]
- [ ] CHK017 Is the three-digit limit of B's 24px number box stated where an implementer will see it?
  [Measurability, Spec §UI/UX]
