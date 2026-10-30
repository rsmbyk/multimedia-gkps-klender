# Requirements Checklist: a Tata Ibadah is a service or a template

**Spec**: `specs/167-tata-ibadah-templates/spec.md` · **Created**: 2026-10-30 · **Depth**: Standard

- [ ] CHK001 Is the type stated as a value chosen once and never changed, with the exact writer that could change it named, rather than "templates behave differently"? [Clarity, Spec §FR-001, §FR-002]
- [ ] CHK002 Does the spec say what happens to the *existing* date-less services — which list they appear in and that no entry is converted — so the migration cannot be read as a re-typing of content? [Completeness, Spec §FR-006, §A11]
- [ ] CHK003 Is "Normal" defined by what it owns (a date, the projector) as well as by what a Template lacks, so a reviewer can tell the two apart from the page alone? [Precision, Spec §US1, §US5]
- [ ] CHK004 Is a fill-in's "no content of its own" stated as a rule a save can be refused against, not only as a shape the preview draws? [Measurability, Spec §FR-008]
- [ ] CHK005 Are a choice's options defined as complete entries of one kind — same validation, same preview — rather than as labels? [Clarity, Spec §FR-009, §US2/AC5]
- [ ] CHK006 Does the spec say a template may be *unfinished* and that the block is at generation, with the option-less choice named as the case? [Consistency, Spec §US2/AC6, §FR-015]
- [ ] CHK007 Is the generate flow's two-step order explicit — settle, **Next**, then the normal form — with **Next**'s disabled rule tied to a count the operator can read? [Completeness, Spec §FR-016, §FR-017]
- [ ] CHK008 Is the abandonment case stated separately from the create case, so "nothing was stored" is checkable after a cancel at either step? [Coverage, Spec §FR-019, §US3/AC10]
- [ ] CHK009 Does the spec say what a copy does to entries (nothing) and to the date (none), so "copy as template" cannot be read as a conversion? [Clarity, Spec §FR-021, §US4/AC3]
- [ ] CHK010 Is the media rule split into its two directions — kept as a use, never auto-downloaded — with the criterion named (today or later)? [Precision, Spec §FR-023, §FR-024]
- [ ] CHK011 Does `## UI/UX` carry numbers for every surface this slice draws (frame, header, footer, body, chooser, add bar, slot rows, badges), or a named preview where a number would be stale? [Measurability, Spec §UI/UX]
- [ ] CHK012 Is every state the preview claims reachable by hand — hover, disabled, empty choice, 420 wide, dark — named in the preview README rather than implied? [Coverage, Spec §Preview]
- [ ] CHK013 Are the capability numbers claimed (R34–R38) recorded with the base they were read against, so a sibling slice can detect the collision? [Traceability, Spec §A12]
- [ ] CHK014 Does the spec name the surfaces it deliberately does *not* touch — search, the API's shape, media retention — so scope creep reads as a change request? [Consistency, Spec §A9, §A10, §FR-023]

**Gate 1**: presented unticked on 2026-10-30 — the tick list stays the owner's; the agent never ticks it.
