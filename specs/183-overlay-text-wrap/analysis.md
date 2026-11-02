# Analyze: the overlay's text wraps inside the box that owns it

**Date**: 2026-11-02 · **Slice**: `specs/183-overlay-text-wrap` · **Run**: 2 (run 1 was the narrow
scope, superseded at gate 2)

**Artifacts read** (SHA-1, first 12): `spec.md` `0172f293bbc4` · `plan.md` `fa1fa38394d1` ·
`tasks.md` `6975425bc484` · `research.md` `ed72fb78a565` · `quickstart.md` · `data-model.md` ·
`contracts/none.md` · `checklists/requirements.md` · the working tree's `.obs-overlay__stage` rule and
`tests/e2e/test_obs_overlay_wrap.py`.

**Metrics**: 7 functional requirements · 6 success criteria · 12 story scenarios · 18 tasks (17 done,
T013 waits for gate 2) · plan traceability rows 18 → coverage **100 %** · critical **0** · high 0 ·
medium 0 · low 1 (F1; F2 closed before delivery).

## Findings

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | LOW | The review page still carries a `scope` field on every state, now constant `'in'` after the widening; the readout would say "out of scope" for nothing. | Reported and accepted: it is preview tooling, not the product, and the branch would only fire if a later slice re-marked a state. Cost of leaving: one dead conditional in a static page. |
| F2 | LOW | ~~The fixture lives in `scratch/` (gitignored)~~ — **closed before delivery**: the seed moved into the slice as `preview/seed.py`, so `quickstart.md` §2 runs from a clean clone. | Fixed. |

Run 1's two findings are closed by this run: the "two speaker turns" scenario it flagged was rewritten
as US1.2 and is covered by the marked-row test, and the fixture finding is F2 above, unchanged.

No CRITICAL: no requirement without a task, no task without a requirement, no verification method
missing. Terminology matches `docs/spec/overlay.md` (overlay, stage, plate, kicker, title, caption, body
row, speaker mark). No same-statement duplicate across FR/SC. Stale paths: none — every path in the
plan and the quickstart exists, and both test names and the preview are the ones on disk.

## History

- **2026-11-02 — run 1**: the narrow scope (the plate's body). 7 requirements, 6 criteria, 13 tasks;
  0 critical, 1 medium, 1 low; coverage 100 %. Gate 2 opened.
- **2026-11-02 — run 2**: after the owner widened the scope to the caption and the heading. The pack
  was revised rather than patched — spec clarified with the reversal recorded, plan re-derived, three
  cases added and one deleted, the declaration moved from the row to the stage. 7 requirements, 6
  criteria, 12 scenarios, 18 tasks; 0 critical, 0 medium, 2 low; coverage 100 %. Gate 2 may open.
