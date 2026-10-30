# Requirements checklist — spec 166

Reviewer-owned. The agent generated these and does not tick them.

## Scope and completeness (US1)

- CHK001 Is every family the reported deck names accounted for in FR-001, including the one that
  reaches the deck through its theme (`Calibri Light`) rather than through a run? [Completeness] [Spec §What happens today]
- CHK002 Does FR-001 state what happens to a family the table does not list, so a future deck cannot
  fall back to a monospaced face by omission? [Coverage] [Spec §Edge Cases]
- CHK003 Is the LibreOffice version in FR-002 stated as a floor with a reason, rather than a
  recommendation? [Measurability] [Spec §What happens today, item 2]
- CHK004 Does the spec state that the conversion command, its limits and its profile are unchanged, so
  the slice cannot drift into rewriting the converter? [Consistency] [Spec §Edge Cases, FR-002]
- CHK005 Is the caching defect (US2) written as a user-visible consequence — the operator keeps seeing
  the old render — rather than as a cache-key detail? [Clarity] [Spec §What happens today, item 3]

## Measurability

- CHK006 Can SC-001 be measured without a person judging it — word boxes from a tool, page by page?
  [Measurability] [Spec §Success Criteria]
- CHK007 Is the reference render named precisely enough to be re-created by someone else (version,
  font mapping, dpi)? [Clarity] [Spec §Assumptions]
- CHK008 Does SC-002 give a box and a tolerance, rather than "the title looks right"? [Measurability] [Spec §Success Criteria]
- CHK009 Is SC-004 a check that can fail the build, rather than an instruction to look carefully?
  [Measurability] [Spec §Success Criteria]
- CHK010 Does the spec say what "converted once" means for two requests arriving together, so US2's
  third scenario cannot be read as a regression of the existing sharing test? [Consistency] [Spec §US2]

## Contradictions and gaps

- CHK011 Does US3 conflict with FR-001's "no proportional family answers a monospaced face" when the
  operator supplies a face that shadows a mapped one? [Conflict] [Gap]
- CHK012 Is the behaviour of an old derivative after the change specified, or is it silently assumed
  to disappear? [Gap] [Spec §Edge Cases]
- CHK013 Does the spec state that the library's identity and deadlines are untouched, so a reviewer can
  see the slice cannot orphan a deck? [Consistency] [Spec §FR-006, §US2 AC4]
- CHK014 Is the two-page residual (the Office-only faces) recorded as the operator's step, with what it
  costs if nobody takes it? [Completeness] [Spec §US3]

## Vocabulary and traceability

- CHK015 Do the requirements use the vocabulary of the capability file (`media-library`, projector/R7)
  rather than inventing a new one? [Consistency] [Spec §Requirements]
- CHK016 Does every functional requirement name a capability anchor — `media-library/R<n>` or `new:
  media-library` — so Fold can place it? [Traceability] [Spec §Requirements]
- CHK017 Do the scenarios avoid board words and spec words crossing (no `Ready`, no `In review`)?
  [Consistency] [Spec §US1–US3]
- CHK018 Is every number in §UI/UX traceable to a measurement recorded in the spec, not to an
  impression? [Traceability] [Spec §UI/UX]
