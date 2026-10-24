# Behaviour Checklist: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md` · **Created**: 2026-10-24 · **Depth**: Lite

- [x] CHK001 Is the change stated as what the header *shows*, rather than as which field the view reads? [Clarity, Spec §US1, §FR-001]
- [x] CHK002 Does the spec say why the short name is the right citation — the evidence that other surfaces already use it, including the sidebar row on the same page? [Grounding, Spec §US1]
- [x] CHK003 Are the four reference shapes decided — short name plus number, sub-number, blank short name, and an unnumbered hymn song? [Completeness, Spec §US1/AC1–AC4, §Edge Cases]
- [x] CHK004 Is the ordinary songbook decided for both of its states — blank short name and a short name set? [Completeness, Spec §FR-003, §FR-006]
- [x] CHK005 Is the tab title decided rather than left to be discovered during implementation? [Clarity, Spec §FR-005, §Clarifications]
- [x] CHK006 Are the untouched surfaces enumerated, so a later reviewer can tell an omission from a decision? [Coverage, Spec §FR-007, §US2/AC2]
- [x] CHK007 Is the saved renderer covered by a requirement with a measurable criterion, not only named in prose? [Coverage, Spec §FR-004, §SC-004]
- [x] CHK008 Does each success criterion fail if today's behaviour returns — including the header text itself, not only its agreement between renderers? [Testability, Spec §Success Criteria]
- [x] CHK009 Is the visual consequence of the shorter text recorded as numbers, including the width at which the old header wrapped? [Grounding, Spec §UI/UX]
- [x] CHK010 Are the states that do not apply (hover, focus, motion) named as not applying, rather than left blank? [Completeness, Spec §UI/UX]
- [x] CHK011 Is every assumption labelled with what the request was silent about, and every answered question written into `## Clarifications`? [Consistency, Spec §Assumptions, §Clarifications]
- [x] CHK012 Does the plan map every requirement, success criterion and acceptance scenario to a file and an honest verification kind? [Traceability, Plan §Traceability]

*(Items are ticked by the owner at gate 2; the agent does not tick them.)*

**Ticked at gate 2** (owner, 2026-10-24), together with the plan pack's acceptance.
