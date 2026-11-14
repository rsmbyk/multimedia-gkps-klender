# Reading Checklist: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Is the gap shown as a difference between code paths a reader can open — the media branch beside the four that append a rest — rather than as a claim about behaviour? [Measurability, Spec §What the page does today]
- [ ] CHK002 Are the before-numbers taken from real services and named (149, 144), so the ten screens and the four missing rests can be re-measured rather than trusted? [Measurability, Spec §What the page does today, §Success Criteria]
- [ ] CHK003 Is "rest" defined once — the built-in blank of spec 058, not a section break, not a row — so no reader can take it for a stored entry? [Clarity, Spec §Key Entities, §FR-003]
- [ ] CHK004 Does the spec state that the rest goes *after* the media screen and inside the entry, with the alternatives and why they were refused? [Completeness, Spec §Assumptions 2]
- [ ] CHK005 Is the no-file case decided rather than left to the implementer — one rest, not two — and is the reason given? [Ambiguity, Spec §US1.4, §FR-002]
- [ ] CHK006 Is every one of the five families named, so a PDF or a slide deck cannot be read as out of scope? [Coverage, Spec §FR-001, §US1.2]
- [ ] CHK007 Does the spec keep the media screens' payloads, the fit and pan rules and the audio/video lock explicitly unchanged, with their requirement IDs? [Consistency, Spec §US3, §FR-006]
- [ ] CHK008 Is the dock's side of the change stated — the inner row, its treatment, the step list — so the slice cannot land on the projector page alone? [Completeness, Spec §FR-005, §US2]
- [ ] CHK009 Is the display-state shift stated as a consequence with its reason and no invented migration? [Consistency, Spec §Edge Cases, §Assumptions 5]
- [ ] CHK010 Are the tests that pin today's shape named, with why they are rewritten instead of deleted? [Coverage, Spec §What the page does today, §Assumptions 7]
- [ ] CHK011 Can every success criterion be checked from the preview, the running route or one call, without reading the diff? [Measurability, Spec §Success Criteria]

**Gate 2**: accepted by the owner on 2026-10-29 — this list (presented unticked, as gate 2 requires),
`plan.md` with its traceability table (13 test · 1 inspection · 0 manual), `tasks.md` and `analysis.md`
were shown together, and the same answer authorised implementation. The boxes above stay unticked: they
are the reviewer's, and the owner's accept is the gate.
