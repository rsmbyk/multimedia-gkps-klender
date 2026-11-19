# Plan: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md` · **Bump**: `patch` (presentation constraint,
no new capability; declared here for gate 2).

## Technical context

- Python 3.12, Django 4.0, static CSS/JS served by WhiteNoise.
- The overlay's stage is a size container, so `cqh` resolves against the browser-source viewport.
- No new dependency, no migration, no endpoint.

## Constitution check

No `CONSTITUTION.md` in the repo (SDD-01); nothing to check.

## Decisions

Recorded in [research.md](./research.md): height-only rest, JS-derived floor, no 80px ceiling.
The fit remains a 6 %-per-step decrement with a 60-iteration guard; 5 % → 2 % takes 15 steps.

## Traceability

| Requirement | Component | Verified by |
| --- | --- | --- |
| FR-001 rest is `5cqh` | `obs-overlay.css:52` | `test` — `tests/e2e/test_obs_caption_height.py::test_the_rest_is_five_percent_of_the_stage_height` |
| FR-002 floor is 2 % of stage height | `obs-overlay.js` `captionFloor()` / `fitCaption()` | `test` — `::test_the_fit_stops_at_two_percent_when_two_lines_cannot_fit` |
| FR-003 no fit carried over | `fitCaption()` clears inline size | `test` — `::test_the_rest_is_five_percent_of_the_stage_height` (two viewports, fresh paints) |
| FR-004 only font-size changes | shrink loop | `test` — `test_obs_overlay_wrap.py::test_a_song_caption_wraps_its_long_run` |
| SC-001 numbers | same as FR-001 | `test` — same |
| SC-002 shrink band | same as FR-002 | `test` — `::test_a_wrapping_lyric_shrinks_but_stays_above_the_floor` |
| SC-003 floor edge | same as FR-002 | `test` — same as FR-002 |
| SC-004 plates unchanged | `obs-overlay.css` plate rule | `test` — existing overlay suites |
| `overlay/R2` delta | `docs/spec/overlay.md` | `inspection` — R2 names 5cqh rest, 2cqh floor, the two-line target and the accepted edge |

## Exit gate

All requirements have a component and a verification method; zero unknowns; no constitution to
violate; `quickstart.md` runs.
