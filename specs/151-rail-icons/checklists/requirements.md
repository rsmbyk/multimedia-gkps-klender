# Reading Checklist: the rail's marks and the song's note

**Spec**: `specs/151-rail-icons/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Is each of the three collisions stated as two named glyphs with their sources, rather than as "confusing"? [Clarity, Spec §What the page does today]
- [ ] CHK002 Does the spec keep the rail's geometry (80px rail, 44px button, 24px glyph) in every requirement that changes a mark, so a "better icon" cannot cost a box? [Measurability, Spec §FR-006, §SC-003]
- [ ] CHK003 Is "a song is one mark" bounded by three places — rail, kind mark, Add Song tile — rather than by "consistent"? [Measurability, Spec §FR-003, §SC-002]
- [ ] CHK004 Does the spec say what must not change (Search, Media Library, the other four media families, the `missing` fallback) so review can tell "unchanged" from "unnoticed"? [Completeness, Spec §FR-005, §FR-008, §Assumptions]
- [ ] CHK005 Is the audio mark's reach enumerated — stage chip, Media Library, service-media dialog, upload preview — with the one function that draws them all? [Coverage, Spec §FR-004, §Assumptions]
- [ ] CHK006 Does the spec declare the cross's proportions (4-unit bar, 6.4-unit stem) so "a cross, not a plus" is checkable and not an opinion? [Measurability, Spec §UI/UX, §Assumptions]
- [ ] CHK007 Is the alternate candidate for each slot named and left in the preview, so the owner's choice is a choice and not a correction? [Coverage, Spec §Clarifications, §UI/UX]
- [ ] CHK008 Are the narrow rail (64px / 40px buttons) and the phone menu drawer covered, where the same marks are drawn at 20px? [Coverage, Spec §Edge Cases, §UI/UX]
- [ ] CHK009 Does the spec avoid claiming a repaint or colour change where `currentColor` already carries the theme, and state the ink for each mark instead? [Consistency, Spec §FR-007, §SC-005]
