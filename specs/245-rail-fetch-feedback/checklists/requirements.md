# Reading Checklist: rail fetch feedback for Search and Media Library

**Spec**: `specs/245-rail-fetch-feedback/spec.md` · **Created**: 2026-11-26 · **Depth**: Standard

- [ ] CHK001 Does the spec name all three requested pieces — rail lock, reading-page bar, real-layout placeholder? [Completeness, Spec §Input]
- [ ] CHK002 Does each placeholder carry the destination's real classes and row anatomy — Search results, Search home, Media Library — with bars only for unknown content, and no library group headings or seeded file data? [Clarity, Spec §Assumptions]
- [ ] CHK003 Are locked, pending, settled, reduced-motion and quick-response states all reachable in the preview? [Coverage, Spec §UI/UX]
- [ ] CHK004 Are the tile opacity, bar height/offset and placeholder origin given as measured numbers? [Measurability, Spec §UI/UX]
- [ ] CHK005 Does every functional requirement name the capability requirement it extends? [Traceability, Spec §Requirements]
- [ ] CHK006 Are Supersede, failure and full-page fallback defined for both destinations? [Coverage, Spec §Edge Cases]
- [ ] CHK007 Are Search's last-results destination and Media Library's route declared unchanged? [Consistency, Spec §Requirements]
- [ ] CHK008 Are the four verification measurements tied to a probe run rather than an assertion? [Measurability, Spec §Success Criteria]
- [ ] CHK009 Is the direct-load loading line distinguished from the in-place placeholder and tied to one render? [Coverage, Spec §Requirements]
- [ ] CHK010 Is the old stage content required to be hidden, not just covered, while a shorter destination placeholder is shown? [Coverage, Spec §Requirements]
- [ ] CHK011 Is the direct-load spinner an 18px ring centred above the text, with an 800ms sweep, reduced-motion stillness, and cleared on render? [Measurability, Spec §Requirements]
