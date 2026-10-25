# Behaviour Checklist: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md` · **Created**: 2026-10-25 · **Depth**: Lite

- [x] CHK001 Is "retired" defined as three separate surfaces and an endpoint, so a reviewer can tell which one is missing? [Completeness, Spec §FR-001–FR-004]
- [x] CHK002 Is the empty service's tile row covered, given it is a creation surface and a five-track grid? [Coverage, Spec §FR-001, §UI/UX, Research D003]
- [x] CHK003 Is the refusal specified for both a stale page and a direct request? [Coverage, Spec §US1/AC5, §FR-004, §Edge Cases]
- [x] CHK004 Is editing refused for an existing break even though no Edit control has been drawn since spec 057? [Completeness, Spec §FR-005, §Assumptions]
- [x] CHK005 Is the stored kind's survival stated as a requirement rather than left to the reader? [Clarity, Spec §FR-010, §data-model]
- [x] CHK006 Is the legacy `END_OF_SECTION` row explicitly excluded, so a reviewer does not read it as an omission? [Consistency, Spec §FR-011, §Edge Cases]
- [x] CHK007 Is the delete path given an acceptance scenario, and does the record say the owner's report was environmental rather than a defect? [Clarity, Spec §US3, §Clarifications]
- [x] CHK008 Is reorder covered, so a break does not become an immovable row? [Coverage, Spec §FR-008]
- [x] CHK009 Is the saved page held to the same four kinds and the same divider? [Coverage, Spec §FR-003, §FR-009, Spec 122's parity rule]
- [x] CHK010 Are the numbers that could move given as measurements (400px row, 28px buttons, 6px gaps; 52px tiles, 10px gaps, 300→238px)? [Testability, Spec §SC-004, §UI/UX]
- [x] CHK011 Is the grid track count named as part of the change, with the off-centre result of leaving it? [Clarity, Spec §FR-001, §UI/UX, Research D003]
- [x] CHK012 Does the plan map every requirement and success criterion to a file and an honest verification kind? [Traceability, Plan §Traceability]
- [x] CHK013 Does the plan say which tests are replaced and which are deleted because their behaviour is gone? [Traceability, Research D006, Plan §Project Structure]

*(Items are ticked by the owner at gate 2; the agent does not tick them.)*

**Ticked at gate 2** (owner, 2026-10-25), together with the plan pack's acceptance.
