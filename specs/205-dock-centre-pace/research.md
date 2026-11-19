# Research — spec 205 (dock centre pace)

Decision / Rationale / Alternatives / Provenance. Unknowns remaining: 0.

## D1 — The pace: 200 ms

- **Decision**: halve spec 200's 400 ms re-centring to 200 ms, on one shared constant `CENTRE_MS`.
- **Rationale**: the reported defect is advancing *faster than the glide completes*. Each advance
  cancels the running glide and restarts from `t = 0`; at 400 ms a 120–300 ms cadence always retargets
  mid-flight, so the list never catches up. At 200 ms a 200–300 ms cadence lets the glide finish
  between steps, and even at 120 ms it is ~85% done when retargeted instead of ~26%. Measured: mean
  live-row offset under rapid advancing falls 16.0→13.7 px (120 ms), 14.6→9.4 (200 ms), 11.9→6.6
  (300 ms); max frame-step 148→100 px (120 ms).
- **Alternatives**: 160 ms (snappier, but a single move starts to read as a snap — the owner rejected
  snapped switches in spec 196); keep 400 ms and only change the curve (does not fix the lag — duration
  is the knob that sets how fast a move feels, see the motion-verification reference). 200 ms is the
  minimal halving that keeps a single move smooth.
- **Provenance**: owner decision (gate 1 Accept, 2026-11-19) on the measured candidate; live probe
  `preview/probe.py` before/after.

## D2 — The curve: plain sine in-out, drop the smootherstep half

- **Decision**: `ease(t) = ½ − cos(πt)/2`, replacing spec 200's `½(sine + smootherstep)`.
- **Rationale**: "less easen" = remove the extra end-flattening. The blend's flatter ends are exactly
  what stalls each retargeted glide at near-zero velocity. Plain sine keeps the in-out character the
  owner approved in spec 200 (the E2E deceleration guard still passes: first/last step < 0.35 × peak)
  while starting quicker (first sampled step 16 px vs 8 px on a ~940 px move).
- **Alternatives**: ease-out (fastest restart, but the first step becomes the peak — fails the
  deceleration guard and reads as a leap); near-linear (abrupt stop reads as a snap). Plain sine is the
  smallest curve delta that satisfies "less eased" without a snap.
- **Provenance**: owner decision (gate 1 Accept); measured single-move steps; the existing guard
  `test_the_centring_decelerates_into_its_target`.

## D3 — One shared pace and curve across all three re-centre paths

- **Decision**: `glideScroll`, `glideRow` and the crossing morph's carried scroll all read `CENTRE_MS`
  and `ease`. The hand block-toggle keeps its own 230 ms `easeInOut`.
- **Rationale**: R14/R15 require expand, collapse and scroll to read as one motion; a different pace on
  the morph would reintroduce a phase boundary (the spec-196 "jaggy" failure). The hand toggle is a
  different gesture the owner did not name.
- **Alternatives**: tune only the glide (leaves crossings slow — inconsistent). Rejected.
- **Provenance**: repo capability `dock/R14`, `dock/R15`; motion-verification reference ("put the
  carried crossing morph on the SAME curve and duration as the glide").

## D4 — The per-crossing collapse clamp is out of scope

- **Decision**: do not change the crossing morph's clamp behaviour in this slice.
- **Rationale**: the 9 direction reversals under fast advancing come from the departing block shrinking
  the scroll range and the browser clamping `scrollTop` mid-morph (scroll up ~105 px, clamp back ~65 px),
  not from the glide ease. They are unchanged by the pace (9→9 measured). Removing them is a separate
  mechanism change; if the owner's "up and down" is that jerk, it is a follow-up card.
- **Provenance**: live probe scroll-segment analysis (`preview/shots/*-120.json`); recorded in spec
  Assumptions and the card.

## D5 — Verification: a new pace test plus existing regression guards

- **Decision**: add `test_the_centring_glide_runs_at_the_shared_pace` (single-move duration ≤ 280 ms,
  red on develop's 400 ms); keep the deceleration guard, the reduced-motion test and the header-toggle
  test as regression. The rapid-advance improvement is verified by the live probe (manual).
- **Rationale**: the deceleration guard passes on both curves (both decelerate), so it cannot anchor the
  pace change; a duration assertion is the behavioural anchor that distinguishes 200 from 400 ms.
- **Provenance**: TDD classicist (a unit is a behaviour); the existing tests in
  `tests/e2e/test_obs_dock_follow.py` and `test_obs_dock.py`.