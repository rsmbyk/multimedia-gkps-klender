# Requirements Checklist: an ordinary song's verses, edited on its page

**Spec**: `specs/189-song-verse-editing/spec.md` · **Created**: 2026-11-05 · **Depth**: Standard

- [ ] CHK001 Does every one of the four verbs name its control, its result and where the result shows, so none is left to be inferred from another? [Completeness, Spec FR-002–FR-011]
- [ ] CHK002 Is "the number is the position" stated once and used everywhere — add, delete, reorder — rather than restated differently in three requirements? [Consistency, Spec FR-003/FR-007/FR-012, §Assumptions]
- [ ] CHK003 Is the reference model measurable — which field changes type, what the label reads, and what "the same lyric" means after a reorder? [Clarity, Spec FR-008, SC-003]
- [ ] CHK004 Does FR-013 name every rule the endpoints enforce, so a bypassed modal cannot write something the page would refuse? [Completeness, Spec FR-013]
- [ ] CHK005 Is the read-only rule for hymn songs stated as a server rule and a page rule, and does it agree with spec 005? [Consistency, Spec FR-001, SC-004]
- [ ] CHK006 Is the migration's scope exact — which rows convert, what a number with no live verse does, and what must not be touched? [Clarity, Spec FR-009, FR-015, SC-007]
- [ ] CHK007 Does the spec say what a person sees when the delete is disabled, and does that agree with the owner's rule that a referenced verse cannot be deleted? [Coverage, Spec FR-010/US4]
- [ ] CHK008 Are concurrent writes covered — a stale verse save, a stale reorder list, a stale entry form — with what the page does after each refusal? [Coverage, Spec §Edge Cases]
- [ ] CHK009 Is every state in `## UI/UX` reachable by hand in the preview, including the restricted reader and the empty song? [Coverage, Spec §UI/UX]
- [ ] CHK010 Are the success criteria observable without naming an implementation, and does each carry a measurement? [Measurability, Spec §Success Criteria]
- [ ] CHK011 Does every requirement name its capability, and is `reading/R40` still free in `docs/spec/reading.md`? [Traceability, Spec §Requirements]
- [ ] CHK012 Does the spec state its delta to spec 005 (the editor modal and the hymn rule) and to spec 162 (a song with no verses), rather than quietly extending either? [Consistency, Spec §What the song page does today, §Assumptions]
- [ ] CHK013 Is the friction of the reorder write — no Save, one write per drop, no keyboard — stated as a decision, including what it costs a keyboard user? [Consistency, Spec FR-006, §Assumptions]
- [ ] CHK014 Does the spec say what the song page does when the write fails, not only when it succeeds? [Coverage, Spec §Edge Cases, §UI/UX States]
- [ ] CHK015 Is the dead management screen named as out of scope, so a reader does not assume it is repaired? [Clarity, Spec §Assumptions]
- [ ] CHK016 Is the display's freshness after a verse edit decided rather than assumed — does an on-air service keep the old lyric, and is that stated with its evidence? [Ambiguity, Spec §Assumptions, §Edge Cases]
- [ ] CHK017 Does the spec say how the setlist's accepted drift is bounded — no write, no migration, no API change? [Completeness, Spec FR-015]
- [ ] CHK018 Is the verse picker's new payload shape stated, so the entry form, the summary line and the stage label cannot each read `verses` differently? [Consistency, Spec FR-008]
