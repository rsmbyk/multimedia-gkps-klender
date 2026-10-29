# Requirements Checklist: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md` · **Created**: 2026-10-29 · **Depth**: Standard

- [ ] CHK001 Does every requirement name an observable outcome rather than a mechanism? [Clarity, Spec §Requirements]
- [ ] CHK002 Is "navigation" enumerated for both input families — keys, pointer, cue controls — rather than left as a category? [Completeness, Spec §FR-001–FR-003]
- [ ] CHK003 Is each of the three ways back (pause, browser exit, end of recording) stated with its resulting screen state? [Coverage, Spec §FR-005–FR-007]
- [ ] CHK004 Is the refused-fullscreen fallback stated as a requirement rather than left to the browser? [Coverage, Spec §FR-008]
- [ ] CHK005 Does the spec say what must NOT change — the video path, the preview dialog, the dock channel? [Boundary, Spec §Edge Cases, Assumptions]
- [ ] CHK006 Are the takeover's dimensions, colours and centring given as measured values? [Measurability, Spec §UI/UX]
- [ ] CHK007 Does every requirement carry a capability reference that exists or is declared new? [Traceability, Spec §Requirements]
- [ ] CHK008 Is each success criterion measurable from the page itself (`data-current-screen`, `data-playing`, `fullscreenElement`)? [Measurability, Spec §Success Criteria]
- [ ] CHK009 Does each requirement reach a traceability row with a verification kind? [Traceability, Plan §Traceability]
- [ ] CHK010 Is the lock's lifetime stated for every way the audio screen can be released? [Completeness, Spec §Edge Cases, Data Model §State transitions]
- [ ] CHK011 Is the accepted "no visible play control" decision recorded with its consequence for a mouse-only operator? [Clarity, Spec §Assumptions, Research §D005]
- [ ] CHK012 Do the two audio states at rest and playing differ only by the cue and the viewport, with no invented chrome? [Consistency, Spec §UI/UX]
