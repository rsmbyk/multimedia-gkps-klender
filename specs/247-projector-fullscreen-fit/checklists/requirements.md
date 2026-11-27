# Projector Checklist: fullscreen refit of the words

**Spec**: `specs/247-projector-fullscreen-fit/spec.md` · **Created**: 2026-11-27 · **Depth**: Standard

- [ ] CHK001 Does the spec name all three operator paths — F key, mouse zone and F11 — as the ones that leave the words unchanged? [Completeness, Spec §Clarifications]
- [ ] CHK002 Does every functional requirement name the capability requirement it modifies rather than claiming a new `R<n>`? [Traceability, Spec §Requirements]
- [ ] CHK003 Are the fitted words and the heading distinguished from the cue, HUD and media-player sizes that stay unchanged? [Clarity, Spec §Scope]
- [ ] CHK004 Are entering, leaving, no-change, Go To detour and both-signals-in-one-transition states all reached by the scenarios or marked manual? [Coverage, Spec §User Scenarios]
- [ ] CHK005 Are the stage boxes and font sizes given as measured before/after numbers rather than adjectives? [Measurability, Spec §UI/UX]
- [ ] CHK006 Is the browser signal for F11 stated separately from the page's own `fullscreenchange`, with the Safari limit recorded? [Coverage, Spec §Assumptions]
- [ ] CHK007 Is the re-fit pinned to the next frame after the signal, with no polling or timer added? [Clarity, Spec §Research D004]
- [ ] CHK008 Does the plan's traceability table carry every FR, SC and story scenario with a `Verified by` method? [Traceability, Plan §Traceability]
- [ ] CHK009 Is the verification split stated as `10 test · 6 inspection · 1 manual`, with the full browser suite deferred to the push step? [Measurability, Plan §Traceability]
- [ ] CHK010 Are the no-change guarantees — fit walk, CSS, controls, endpoints and the frozen resize answer — written as inspection rows? [Coverage, Spec §Out of scope]
- [ ] CHK011 Is the headless harness's inability to produce an OS-level fullscreen disclosed with the substituted public-signal seam? [Clarity, Quickstart §Not yet runnable]
- [ ] CHK012 Is the patch bump declared at Plan but applied in the pre-merge delivery commit, and the card opened at delivery? [Consistency, Plan header + Spec §Assumptions]
