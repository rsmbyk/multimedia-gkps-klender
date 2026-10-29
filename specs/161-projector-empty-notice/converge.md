# Convergence: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-29

Checked every row of `plan.md`'s traceability table against the code:

| Row | Checked by | Result |
| --- | --- | --- |
| FR-001 | running `test_an_empty_service_shows_its_empty_state` | met — the notice is visible and carries no `hidden` |
| FR-002 | `test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | met — `display: none`, `bounding_box()` `None`, the stage gains exactly the notice's height |
| FR-003 | `test_closing_the_detour_brings_the_empty_notice_back` | met |
| FR-004 | `test_a_reread_with_screens_hides_the_empty_notice`, `test_a_reread_without_screens_keeps_the_empty_notice` | met |
| FR-005 | `grep -rn "projector__empty" static/web multimedia/web/templates`; `grep -n "syncEmptyNotice" static/web/projector.js` | met — one writer at `projector.js:313`, called from `render()` `:414`, `renderDetour()` `:1177` and `adoptService()` `:1443`; the only other reference (`:1485`) writes the copy, not `hidden` |
| FR-006 | the four cases in `tests/e2e/test_projector.py` | met |
| FR-007 | `git diff --stat` | met — `static/web/projector.js` (+17/−2), `tests/e2e/test_projector.py` (+94), the pack and the board row; no route, template copy, stylesheet or fitting change |
| SC-001 | `test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | met |
| SC-002 | live readout on `127.0.0.1:8765/projector?service=147`, 1920×1080 | met after G1 — stage 984, fitted lines 107px, lines box y 279.3 h 736.7, centre 647.6 |
| SC-003 | `test_closing_the_detour_brings_the_empty_notice_back` | met |
| SC-004 | the two re-read cases | met |
| US1/AC4 | the class run below, which includes `test_a_verse_step_inside_a_chapter_makes_no_request` | met — stepping still paints inside the detour and the notice stays hidden |

Two gaps were found while the slice was being built, both fixed in the slice:

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The first implementation synced the notice *after* `fit()`, so the detour was fitted to the 945.6px stage and painted at 103px instead of the 107px the spec's SC-002 names. | `contradicts` | SC-002 | live readout, 1920×1080, before the fix: `display: none`, stage 984, **fitted lines 103px**. Fixed by moving `syncEmptyNotice()` before the fit in `render()` and `renderDetour()`. |
| The first E2E case counted `#projectorScreens .screen`, which includes the always-appended (inactive) `.projector-detour` node, so "one screen" never matched and an empty service read as one screen. | `contradicts` | FR-006 | `test_a_reread_without_screens_keeps_the_empty_notice` failed `1 != 0` on an emptied service. Fixed to `.screen[data-screen]`, the same selector `screens()` uses. |

**Outcome**: 2 findings, both fixed in the slice; no convergence tasks were appended — each was
corrected where it was found, before the closing pass.

## Pass 2 — 2026-10-29

**Outcome**: Converged — nothing remains.

- `tests.e2e.test_projector.ProjectorE2ETests` — **66 tests, OK** (227.2s) against the final code.
- The five notice cases specifically — **5 tests, OK** (19.2s).
- Live readout on the worktree's dev server, `develop` base + this slice, `/projector?service=147`,
  1920×1080: at rest notice `block` / stage 945.6; detour notice `none` / stage 984 / fitted lines
  107px / lines box y 279.3 h 736.7; `Escape` notice `block` / stage 945.6.
- The static preview's probe reads the same numbers off its two boards (notice `none`, no box, stage
  1856×984, fitted lines 107px), so the approved look and the running page agree.

## Accepted gaps

None — nothing was left for the owner to accept.

## Cap reached

Not reached: 2 of 3 passes.
