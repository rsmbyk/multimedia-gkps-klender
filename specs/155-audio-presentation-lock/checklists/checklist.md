# Requirements Checklist: a playing recording owns the projector screen until it pauses

**Spec**: `specs/155-audio-presentation-lock/spec.md` · **Created**: 2026-10-29 · **Depth**: Standard

- [x] CHK001 Does every requirement name an observable outcome rather than a mechanism? [Clarity, Spec §Requirements]
- [x] CHK002 Is "navigation" enumerated for both input families — keys, pointer, cue controls — rather than left as a category? [Completeness, Spec §FR-001–FR-003]
- [x] CHK003 Is each of the three ways back (pause, browser exit, end of recording) stated with its resulting screen state? [Coverage, Spec §FR-005–FR-007]
- [x] CHK004 Is the refused-fullscreen fallback stated as a requirement rather than left to the browser? [Coverage, Spec §FR-008]
- [x] CHK005 Does the spec say what must NOT change — the video path, the preview dialog, the dock channel? [Boundary, Spec §Edge Cases, Assumptions]
- [x] CHK006 Are the takeover's dimensions, colours and centring given as measured values? [Measurability, Spec §UI/UX]
- [x] CHK007 Does every requirement carry a capability reference that exists or is declared new? [Traceability, Spec §Requirements]
- [x] CHK008 Is each success criterion measurable from the page itself (`data-current-screen`, `data-playing`, `fullscreenElement`)? [Measurability, Spec §Success Criteria]
- [x] CHK009 Does each requirement reach a traceability row with a verification kind? [Traceability, Plan §Traceability]
- [x] CHK010 Is the lock's lifetime stated for every way the audio screen can be released? [Completeness, Spec §Edge Cases, Data Model §State transitions]
- [x] CHK011 Is the accepted "no visible play control" decision recorded with its consequence for a mouse-only operator? [Clarity, Spec §Assumptions, Research §D005]
- [x] CHK012 Do the two audio states at rest and playing differ only by the cue and the viewport, with no invented chrome? [Consistency, Spec §UI/UX]

**Gate 1**: the spec was accepted by the owner on 2026-10-29, with "no visible play/pause control in
the fullscreen state" accepted as drafted.

**Gate 2**: ticked by the owner on 2026-10-29 — this list, the plan with its traceability table, the
task list and `analysis.md` were presented together, and the same answer authorised implementation.
