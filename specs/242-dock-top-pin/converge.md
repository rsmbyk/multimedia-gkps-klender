# Convergence — spec 242

**Pass 1 — 2026-11-25.** Code compared against Plan's traceability table, each row by the method
it declared. Evidence: `tests.e2e.test_dock_top_pin` **5/5 green** (red on unmodified `develop`
at `56b3dcbf`: 4 failures and 1 error, all because `.topband-slot` does not exist);
`tests.e2e.test_obs_dock`, `test_dock_stuck_corner`, `test_dock_open_reset` **39/39 green**;
`preview/probe_top.py` before/after at 420×860 dark 1×.

| Row | Type | Result | Evidence |
| --- | --- | --- | --- |
| FR-001 | test | checked | `test_the_top_pin_stands_when_the_live_block_is_above`: clone visible, 0 px from edge, 0/9 px radius, exact label copy, one header-height |
| FR-002 | test | checked | `test_the_top_pin_tracks_the_block_per_frame` (0 mismatched of 51 frames), instant reduced-motion pin; resize path shares `updatePins()` |
| FR-003 | inspection | checked by inspection | diff of `obs-dock.js`/`obs-dock.css` against base: native sticky header, corner class and bottom slot rules untouched; clone is zero-height and overlays |
| FR-004 | test | checked | `test_clicking_the_top_pin_performs_the_centre_act`: byte-identical display state, row centred, following true |
| FR-005 | inspection + test | checked | diff shows no change to NEXT band, bottom pin, `.offstrip` or header wash; 39/39 regression tests green |
| SC-001 / US1 AC1–3 | test | checked | stand pin, no double, no bottom-pin competition |
| SC-002 / US2 AC1 | test + probe | checked | 0/51 per-frame mismatches; probe 0/25 |
| SC-003 / US2 AC2–3 | test | checked | hand scroll returns the native header; liveness change hides the pin |
| SC-004 / US3 AC1 | test | checked | centre act, state unchanged, following |
| SC-005 | test + inspection | checked | reduced motion instant; go to branch hides the slot |
| SC-006 | test | checked | three regression modules, 39/39 green on the slice |

**Outcome: Converged.** No `missing`, `partial`, `contradicts` or `unrequested` gaps.
The unchecked requirement checklist is reviewer-owned and is not an agent finding.

### Phase 1: Convergence (mechanism notes)

- The first E2E run had three failures: a hardcoded 38 px header height (test fault — song headers
  with subtitles are 56 px), a clamped centre assertion on a fixture whose live row sat too near
  the list head (fixture fault), and one stale pin frame. The first two were corrected in the test
  (compare against the measured header height; place long blocks above and below the live entry).
- The stale frame and the subsequent feedback loop were product faults: the glide could move the
  list before its first rAF, and an in-flow slot changed the list's height when shown/hidden. Fixed
  by `updatePins()` at the head of `glideRow()` and a zero-height slot with an absolutely
  positioned clone (research D005/D006). The new E2E was red before each fix and green after.
