# Requirements Checklist: a passage and a song carry their own kind mark

**Spec**: `specs/144-passage-song-icons/spec.md` · **Created**: 2026-10-28 · **Depth**: Lite

- [ ] CHK001 Does the spec state the mark as a property of a kind (passage, song), rather than naming a colour or a pixel size that could pass for a different shape? [Clarity, Spec §What the page does today, §US1]
- [ ] CHK002 Is "different from the media chip" measurable — size plus one of fill, colour or container — rather than "looks different"? [Measurability, Spec §FR-003, §SC-002]
- [ ] CHK003 Does the spec name the column the mark and the title take, in numbers, so the shared left rail with media rows is checkable? [Measurability, Spec §UI/UX]
- [ ] CHK004 Is the height claim honest — no height of its own, and the wraps the narrower column causes declared with their pixel cost? [Consistency, Spec §FR-005, §US3.2]
- [ ] CHK005 Are the four fixture songs' measured widths stated, so a reader can see why they wrap and at which pane they stop? [Traceability, Spec §UI/UX]
- [ ] CHK006 Does the spec say what a text entry, a section break, a legacy row and a media row each render, so "only passage and song" is exhaustive? [Completeness, Spec §FR-004, §FR-008]
- [ ] CHK007 Is the deleted-target case decided rather than left to chance (a mark states the kind, not the availability)? [Coverage, Spec §Edge Cases]
- [ ] CHK008 Does the spec state the mark's accessibility contract — decorative, no focus stop, the row's name unchanged — given it sits inside a heading? [Completeness, Spec §FR-006, §SC-005]
- [ ] CHK009 Is the reason the mark cannot hang outside the row recorded, so the indent is not re-litigated as a stylistic choice? [Ambiguity, Spec §UI/UX, research D3]
- [ ] CHK010 Does the spec keep the sidebar's service list and the OBS dock out of scope in words, not by silence? [Scope, Spec §FR-008, §Assumptions]
- [ ] CHK011 Is the "text entries are unmarked" decision recorded as an assumption the owner may reopen, rather than as a settled requirement? [Traceability, Spec §FR-004, §Clarifications]
- [ ] CHK012 Does the spec avoid claiming the faster reading it promises can be measured by a test, leaving that to a manual check? [Measurability, Spec §US1.3, plan §Traceability]
- [ ] CHK013 Are both themes' contrast stated as ratios, so the darkness claim is checkable without a screenshot? [Measurability, Spec §UI/UX]
- [ ] CHK014 Does the spec account for the coupling that made a first-child mark give the heading its 30px margin back? [Consistency, Spec §UI/UX, research D1]
