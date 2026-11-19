# Converge: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md`
**Pass**: 1 · **Checked**: every row of plan.md's traceability table by its declared method
**Outcome**: converged

## Pass 1

| Row | Method | Evidence |
| --- | --- | --- |
| FR-001 | test | `test_the_rest_is_five_percent_of_the_stage_height` — 54px at 1080p, 36px at 720p, ±0.5. Red on the old stylesheet (72/48). |
| FR-002 | test | `test_the_fit_stops_at_two_percent_when_two_lines_cannot_fit` — 21.6px at 1080p, rows > 2. Red on the old script (11px). |
| FR-003 | test | the rest test measures fresh paints at two viewports; no fit carries over. |
| FR-004 | test | `test_obs_overlay_wrap.py::test_a_song_caption_wraps_its_long_run` — weight 800, outline, centre, balance, 1728px box all unchanged. |
| SC-001/002/003 | test | the three cases in `tests/e2e/test_obs_caption_height.py`, all green. |
| SC-004 | test | `test_obs_overlay.py` and `test_obs_overlay_wrap.py` — plate scale and look unchanged. |
| `overlay/R2` | inspection | `docs/spec/overlay.md:57-96` now names `5cqh` rest, 2 % floor, the 4 %-of-rest step (15 steps), the two-line target, the accepted edge, and the remeasured 66-character-run numbers. |

## Verification runs

- Red (old CSS/JS stashed): 3 new tests, 4 failures — 72≠54, 48≠36, 11≠21.6, and the old floor.
- Green: the 3 new tests pass; a later run of the new + two overlay suites + dock suite passed 37/37
  after one flaky 30s timeout in an existing dock test on the first attempt.
- Static: `node --check static/web/obs-overlay.js` clean; a 4 %-of-rest step covers the 60 % of rest
  between 5 % and 2 % in exactly 15 steps, inside the 60-iteration guard. The ladder is pinned by
  `::test_the_shrink_step_is_four_percent_of_the_rest_size` (red at 29.0852px under the old
  multiplicative step, green at the linear value).

## Findings

None material. The flaky dock timeout and the post-acceptance pack are recorded in analysis.md.
