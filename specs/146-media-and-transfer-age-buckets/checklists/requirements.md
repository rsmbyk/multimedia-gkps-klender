# Reading Checklist: the Media Library and the transfer history group by age

**Spec**: `specs/146-media-and-transfer-age-buckets/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [ ] CHK001 Does the spec say what the today-existing heading is and what replaces it, with the row count that proves the current shape is wrong (eight files, five headings)? [Clarity, Spec §What the two surfaces do today]
- [ ] CHK002 Are the Media Library's three buckets given with the same edges as `reading/R9`'s — thirty days, then the calendar year — so a reader can tell they are the same rule and not a lookalike? [Consistency, Spec §FR-001, §FR-002, §Assumptions]
- [ ] CHK003 Does the spec say where the present day comes from, and why the server's UTC clock is not it? [Completeness, Spec §FR-003]
- [ ] CHK004 Is the missing `Upcoming` bucket on the Media Library stated with its reason, rather than left as an omission a reviewer has to notice? [Coverage, Spec §Assumptions]
- [ ] CHK005 Are the transfer ladder's rungs given as windows with both an upper and a lower edge, so no gap and no overlap is left between them? [Measurability, Spec §FR-009]
- [ ] CHK006 Does the spec name which instant dates a transfer, and does it say what that means for a row that is still running? [Clarity, Spec §FR-010, §FR-011, §Edge Cases]
- [ ] CHK007 Is the sort interaction decided both ways — size sorts drawing no headings, ascending date reversing the bucket order — instead of left to implementation? [Completeness, Spec §FR-005, §Edge Cases]
- [ ] CHK008 Are the heading's numbers given as measurements (12px, `.07em`, `--head-ink`, the two margin pairs), and is it said which of them are unchanged from the existing heading? [Measurability, Spec §FR-006, §FR-013, §UI/UX]
- [ ] CHK009 Does the spec say the rail's flyout keeps its shape, so a reader does not assume the ladder appears in a 360px popover? [Scope, Spec §FR-014]
- [ ] CHK010 Is the reason for one shared bucket rule stated as a drift risk, with the earlier sibling defect (the dock and the panel disagreeing, spec 132) named? [Traceability, Spec §FR-016, §US3]
- [ ] CHK011 Do the success criteria say how each is measured — browser reading, unit test on a pinned day or clock, string comparison — rather than asserting the outcome? [Measurability, Spec §SC-001 … §SC-007]
- [ ] CHK012 Is the open label question recorded as asked-and-unanswered with the recommendation and the offer to reopen, rather than silently decided? [Ambiguity, Spec §Clarifications]
- [ ] CHK013 Does the preview say what it cannot show (the companion fetch), so nobody reads the fixture set as the real library? [Traceability, `preview/README.md`]
- [ ] CHK014 Does the spec keep the Tata Ibadah list, the search ordering, the entry editor's picker and the companion's timestamps out of scope by name? [Scope, Spec §Assumptions]
