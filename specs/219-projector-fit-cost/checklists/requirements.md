# Requirements Checklist: a text screen arrives as fast as the entries beside it

**Spec**: `specs/219-projector-fit-cost/spec.md`
**Generated**: 2026-11-22 · reviewer-owned: the agent writes these and never ticks them (SDD-15)

## Completeness

- [ ] CHK001 Is every path that fits a screen covered by a requirement — an advance, a jump, a resize, the bundled faces arriving, a header rewritten by the translation, a Go To detour, and a single-screen cut? [Completeness, Spec §Requirements]
- [ ] CHK002 Does the spec say what a screen shows when the idle work has not run — the first press after a load, a rapid advance, a jump — rather than leaving it to the reader? [Completeness, Spec §US1/AC2, §Edge Cases]
- [ ] CHK003 Is the visible change (a screen may be one to eight pixels larger) stated with its cause, so a reviewer can tell a correction from a regression? [Completeness, Spec §UI/UX]

## Clarity

- [ ] CHK004 Is "fitted at rest" defined by what it excludes — the arrival morph's transform — rather than by the word "rest"? [Clarity, Spec §FR-001]
- [ ] CHK005 Is the remembered-fit key stated in full (stage size, header, row count, text length), so its invalidation can be checked? [Clarity, Spec §FR-003, Assumptions]
- [ ] CHK006 Does the spec say which of the two measured cadences is the operator's and which is the floor, instead of presenting one number as "the" number? [Clarity, Spec §Assumptions]

## Consistency

- [ ] CHK007 Does the spec's account of why the search stays a one-pixel walk agree with `research.md` D001, including the screen that is refused at 101–105 px? [Consistency, Spec §FR-004, research D001]
- [ ] CHK008 Do the numbers in `## UI/UX` match the ones in the success criteria, and does each say which build and which cadence it came from? [Consistency, Spec §SC-001–006, §UI/UX]
- [ ] CHK009 Is the "largest size that fits" promise kept everywhere, including for a screen fitted ahead of time? [Consistency, Spec §FR-004, §US1/AC3]

## Measurability

- [ ] CHK010 Can every success criterion be checked by a command in `quickstart.md`, and does each name the fixture (service, viewport) it was measured on? [Measurability, Spec §SC-001–006]
- [ ] CHK011 Is the test that guards the fix stated as a bound (one layout read) rather than a duration, so it cannot pass on a fast machine and fail on a slow one? [Measurability, Spec §SC-001]
- [ ] CHK012 Does the spec name what is *not* changed — the morph, the cue, the media fits — so a reviewer knows what to compare? [Measurability, Spec §UI/UX]

## Coverage

- [ ] CHK013 Does every functional requirement trace to a component and a verification in `plan.md`, with no row left as "manual" that a test could carry? [Coverage, Plan §Traceability]
- [ ] CHK014 Does the capability tree gain the requirement this slice establishes (`projector/R14`), including the behaviour that was true before this slice (the largest fitting size)? [Coverage, Fold]
- [ ] CHK015 Is the failure the owner reported — a text entry slower than the entries beside it — stated in a way that would be recognisable in the numbers if it came back? [Coverage, Spec §Input, §SC-002]
