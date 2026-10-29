# Projector Checklist: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md` · **Created**: 2026-10-29 · **Depth**: Standard

Fit / coverage
- [x] CHK001 Does the spec state the control's size, position and the distance to the bar as numbers, so
      "above the seek bar" cannot be satisfied by any spacing? [Measurability, Spec §UI/UX, §SC-001]
- [x] CHK002 Are the two click layers — the pointer zones and the windowed fullscreen reservation — stated
      as requirements rather than left to the implementation? [Coverage, Spec §FR-005]
- [x] CHK003 Is "hidden" written as a measured state (`opacity: 0`, `pointer-events: none`, box unchanged)
      instead of "disappears", so the no-jump guarantee is checkable? [Clarity, Spec §FR-003, §US1 AC3]
- [x] CHK004 Does the spec agree with itself on idle behaviour — the control hiding while the bar and times
      dim — everywhere it is mentioned? [Consistency, Spec §FR-003, §UI/UX, §Assumptions]
- [x] CHK005 Is every state named with its expected mark or visibility: paused, playing, idle, returned,
      ended, missing file, reduced motion? [Completeness, Spec §UI/UX, §Edge Cases]

Shape / risk
- [x] CHK006 Does each FR name the capability it changes, including the new `projector/R3`? [Traceability,
      Spec §Requirements]
- [x] CHK007 Is "the same mark the app's audio player uses" pinned to a named source, so the port is
      checkable rather than interpretive? [Clarity, Spec §FR-002, §Assumptions]
- [x] CHK008 Is the blast radius bounded by a testable statement — no other screen, no preview player, no
      seek-bar geometry — rather than by a promise to be careful? [Coverage, Spec §FR-006]
- [x] CHK009 Is the seek bar's unchanged clickability recorded as an out-of-scope decision, so its absence
      is not later read as an omission? [Consistency, Spec §Assumptions]
