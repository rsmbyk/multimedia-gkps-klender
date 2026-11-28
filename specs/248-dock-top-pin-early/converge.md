# Convergence: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`
**Plan**: `specs/248-dock-top-pin-early/plan.md`
**Tasks**: `specs/248-dock-top-pin-early/tasks.md`

## Phase 1: Convergence

Every row below was re-assessed from the present code and test output, not from task checkboxes.
Gap types: `missing` · `partial` · `contradicts` · `unrequested`.

| Requirement | Declared method | Evidence read | Gap |
| --- | --- | --- | --- |
| FR-001 | test | `test_the_top_pin_takes_over_when_the_header_is_clipped` passes on the slice; red on unmodified develop (pin absent at `blockTop = -2`) | none |
| FR-001 (one header) | test | `test_only_one_header_is_painted_while_the_pin_owns_the_edge` passes: source `visibility: hidden`, clone visible, boxes equal within 0.6 px | none |
| FR-002 | test | `test_the_top_pin_tracks_the_block_per_frame` now samples `bt` and reports 0 mismatches; 490 stepped frames in `after-boundary.json`, 0 boundary mismatches | none |
| FR-002 (reduced motion) | test | `test_the_top_pin_lands_instantly_under_reduced_motion` passes | none |
| FR-003 | test | `test_clicking_the_top_pin_performs_the_centre_act` passes; display state byte-identical, following true | none |
| FR-004 | inspection | diff touches only `updateTopBand()`, the `.is-covered` rule/comments and the E2E module; `updateLiveBand()`, `updateBand()`, `.offstrip`, header wash and entry anatomy are unchanged; 23 regression tests green | none |
| SC-001 | inspection | frozen gate-1 numbers: first pin 1164 → 1056, blockTop -110 → -2, pin 0/38 px, radius 0/9 px, label `26Entri 26` exact | none |
| SC-002 | test + inspection | per-frame sampler passes; 490-frame probe has 0 mismatches to the new boundary | none |
| SC-003 | test | `tests.e2e.test_dock_top_pin` 7/7; `test_dock_stuck_corner` + `test_dock_open_reset` 23/23, throwaway DB `gkps248` | none |
| US1/AC1 | test | shared with FR-001 case | none |
| US1/AC2 | test | shared with one-header case | none |
| US1/AC3 | manual | `preview/check_goto.py` on both builds: `goto: true`, offstrip shown, 21 rows; service pin present on both — pre-existing (D006), removed claim kept as retraction | none for this slice |
| US2/AC1 | inspection | probe frames past `blockBottom <= 0.5` keep the pin at 0 px, one header-height | none |
| US2/AC2 | inspection | bottom-pin and NEXT-band functions byte-identical in `git diff` | none |

**Outcome**: Converged in one pass — zero `missing`, `partial`, `contradicts` or `unrequested`.
A1 (stale frame sampler) was resolved by task T009 before this pass; A2 (a false carried-over Go To
claim) was recorded as a retraction rather than silently rewritten, and does not change this slice's
behaviour. The full browser matrix remains deferred to the push step by repo preference; the named
modules were actually executed and reported above.
