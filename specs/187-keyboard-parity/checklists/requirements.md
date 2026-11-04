# Requirements Checklist: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md` · **Created**: 2026-11-04 · **Depth**: Standard

- [x] CHK001 Does every requirement name its surface — dock runner, dock picker, projector or overlay — so no chord is left to "wherever it fits"? [Completeness, Spec §Requirements]
- [x] CHK002 Is the hold's timing and every way it is cancelled stated, so "held" is one number rather than a feel? [Clarity, Spec FR-001, §Assumptions]
- [x] CHK003 Does the spec say what `Home`/`End` act on without the word "unit" being the only answer — is the bait/entry rule written out? [Clarity, Spec FR-012, US8]
- [x] CHK004 Is "the projector's own wording" pinned to one source, and is the dock-only set named exhaustively? [Consistency, Spec FR-008]
- [x] CHK005 Do the scenarios cover the go to started from the picker on every surface that paints it — dock, projector, overlay — including `Back` leaving all three idle? [Coverage, Spec FR-004, FR-011]
- [x] CHK006 Is the picker's narrowed key set exhaustive, and does it say what the band's own field keeps? [Completeness, Spec FR-006]
- [x] CHK007 Is the in-flight guard's scope stated for keys and for pointer acts, and does it say when it ends? [Clarity, Spec FR-009]
- [x] CHK008 Does the spec say what happens to a go to's words when it stands with no service, and what `Space` does there? [Consistency, Spec §Edge Cases]
- [x] CHK009 Are the two sheets' groupings stated as observable lists — group names and row order — rather than as "like the projector"? [Measurability, Spec FR-013, FR-014]
- [x] CHK010 Is the projector's sheet frame stated as a measured outcome, with the 720p behaviour named? [Clarity, Spec FR-014, §UI/UX]
- [x] CHK011 Does the spec state the delta to spec 185's contract (a go to may now name no service) rather than quietly extending it? [Consistency, Spec FR-003, contracts/display-state.md]
- [x] CHK012 Does the spec state its delta to projector/R9's fixed frame and R12's grouping? [Consistency, Spec FR-013, FR-014]
- [x] CHK013 Is the band's focus behaviour stated as a rule — every way the focus can be lost and where it lands — rather than one event? [Coverage, Spec FR-015, US11]
- [x] CHK014 Are the sheet's numbers measurable without naming an implementation — rows, groups, widths, heights, scroll? [Measurability, Spec §UI/UX]
- [x] CHK015 Is every state in `## UI/UX` reachable by hand in the preview? [Coverage, Spec §UI/UX]
- [x] CHK016 Does any requirement contradict "one dock, one source" (spec 119), the overlay's listen-only rule (`overlay/R1`) or the session boundary (spec 184)? [Consistency, Spec FR-003, FR-011]
- [x] CHK017 Do the success criteria each carry a measurement a command can read? [Measurability, Spec §Success Criteria]
- [x] CHK018 Does every requirement name its capability, including the new `dock` ones and the modified `projector` ones? [Traceability, Spec §Requirements]
- [x] CHK019 Are the failure cases covered — a chapter fetch that fails, a go to at the first or last book, a sheet opened with the picker showing? [Coverage, Spec §Edge Cases]
- [x] CHK020 Does the spec keep names of people out, and does it call the two surfaces by the repo's vocabulary? [Consistency, Spec §Glossary]

**Ticked**: 2026-11-05 — all 20 items, against the spec as accepted at gate 1 (FR-001…FR-015,
SC-001…SC-012, US1…US11). Three items earned a fix while reading: CHK009 (the sheet's rows were stated
as a count, not a list — the group and row order was written into FR-013/FR-014), CHK011 (the contract
now states the `service: null` allowance) and CHK014 (the frame's 835.5 px and the 720p scroll were
measured and written down, not implied).
