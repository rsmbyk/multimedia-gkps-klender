# Overlay Checklist: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md` · **Created**: 2026-10-30 · **Depth**: Standard

- [ ] CHK001 Is the entry→style mapping total — does every `type`, including `break`, `media` and an unknown entry,
      have a stated outcome? [Completeness, Spec §FR-001]
- [ ] CHK002 Is "the caption it paints today" measurable from the spec alone, or does it rest on a reader who saw the
      old page? [Measurability, Spec §SC-001]
- [ ] CHK003 Does every number in `## UI/UX` carry a unit and the frame width it was measured at?
      [Clarity, Spec §UI/UX]
- [ ] CHK004 Is the heading's empty case stated on both sides — no kicker, and no orphan hairline either?
      [Coverage, Spec §FR-003]
- [ ] CHK005 Does the speaker-mark requirement cover a mark wider than its column, and two marks of different widths
      on one screen? [Coverage, Spec §FR-010]
- [ ] CHK006 Do the motion requirements give duration, displacement and easing for arrival *and* departure?
      [Measurability, Spec §FR-011, §FR-012]
- [ ] CHK007 Is a screen step inside one entry distinguished from a change of kind everywhere it changes the outcome?
      [Consistency, Spec §FR-013]
- [ ] CHK008 Does the spec say what a machine asking for reduced motion gets? [Coverage, Spec §FR-011]
- [ ] CHK009 Is the ink hierarchy stated as a measured contrast as well as an alpha? [Measurability, Spec §UI/UX]
- [ ] CHK010 Is "listen-only" testable as written — does it name what must be absent rather than "no chrome"?
      [Measurability, Spec §FR-009]
- [ ] CHK011 Is the fallback stated for a payload with no entry island, and for a screen index beyond it?
      [Coverage, Spec §Edge Cases, Gap]
- [ ] CHK012 Does the spec avoid board, branch and commit vocabulary? [Consistency, Spec §whole]
- [ ] CHK013 Is the longest realistic content bounded — which verse was measured, and what did it produce?
      [Coverage, Spec §Edge Cases]
- [ ] CHK014 Is the edition flip clear about what changes — the heading, the words, or both? [Clarity, Spec §FR-007]
- [ ] CHK015 Does every state in `## UI/UX` name how a reviewer reaches it by hand, including hover, focus and empty?
      [Coverage, Spec §UI/UX]
