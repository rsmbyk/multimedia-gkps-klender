# Convergence — spec 205 (dock centre pace)

## Pass 1 — 2026-11-19

Checked the code against the Plan traceability table, each row by its declared method.

| Row | Method | Evidence | Result |
| --- | --- | --- | --- |
| FR-001 pace | test | `test_the_centring_glide_runs_at_the_shared_pace` — red on base (383 ms > 280), green on slice | converged |
| FR-001 curve | test | `test_the_centring_decelerates_into_its_target` — green (sine shape) | converged |
| FR-002 | inspection | diff leaves `startToggleMorph` (230 ms `easeInOut`) untouched; toggle tests green | converged |
| FR-003 reduced | test | `test_reduced_motion_jumps_instead_of_gliding` — green | converged |
| FR-003 clamp/cancel | inspection | diff leaves `glideScroll` end-clamp and wheel/pointerdown cancel untouched | converged |
| US1/AC4 | inspection | `startMorph` `duration = CENTRE_MS`, same `ease` — one motion | converged |
| SC-001 | manual | probe single-move: landing 0 px, 0 reversals, ~12 moving frames | converged |
| SC-002 | manual | probe rapid: mean_off 13.7/9.4/6.6 vs 16.0/14.6/11.9; max_step 100/82/80 vs 148/99/88 | converged |
| SC-003 | test | deceleration guard green | converged |

Targeted lanes run: `test_obs_dock_follow` (pace, deceleration, reduced-motion) and `test_obs_dock`
(header toggle, toggle reduced-motion) — 5 tests, all green, throwaway DB `gkps205`. The full dock
suites and the rest of the E2E are deferred to the push step (owner's standing preference).

**Findings**: none. No `missing`, `partial`, `contradicts` or `unrequested` work. The per-crossing
collapse clamp is unchanged and was declared out of scope (research D4), not a gap.

**Outcome**: Converged (pass 1).