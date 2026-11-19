# Convergence: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`
**Plan**: `specs/203-dock-long-word-wrap/plan.md`

## Phase 1: Convergence

**Date**: 2026-11-19 · **Base**: `85319b73` (`origin/develop`, spec 202 merged) · **Pass**: 1 of 3

### What was checked

Every row of Plan's traceability table, by the method that row declares. The suite was re-run at this
pass rather than trusted from the Implement run; the diff was read against `origin/develop`; the live
page was re-measured in both states.

| Row | Method | Evidence | Result |
| --- | --- | --- | --- |
| FR-001 | test | `test_an_unbroken_service_name_wraps_inside_its_column` — spill ≤ 1 at 320/456/900, 3 lines at 456 | pass |
| FR-002 | test | `test_an_unbroken_entry_header_wraps_inside_its_row` — every header ≤ 1px at 320/456, incl. the 200-char filename and the ordinary-songbook title | pass |
| FR-003 | test | `test_a_screen_row_wraps_inside_the_open_block` — the open block's lines ≤ 1px at 320/456 | pass |
| FR-004 | test | `test_the_runner_body_does_not_scroll_sideways` — body overflow 0 and document overflow 0 at 320/456/900 | pass |
| FR-005 | test | `test_text_that_fits_is_unchanged`, `test_a_short_service_is_unchanged`, `test_a_wide_panel_renders_as_it_does_today` — rule shipped vs restored to `normal`, every fitting box equal | pass |
| FR-005 (geometry) | test | `test_the_row_keeps_its_number_and_chevron` — numbers `[33.6 ×5]`, chevrons `offRight 10 / offCentre 0` in both reads | pass |
| FR-006 | test | `test_a_truncating_label_still_truncates` — `nowrap`, `ellipsis`, 1 line, still clipped, label starts `https://` | pass |
| FR-007 | test | `test_the_picker_name_still_wraps` — `anywhere`, spill ≤ 1, 2 lines | pass |
| US1/AC1–4, US2/AC1–4, US3/AC1–2 | test | the same ten functions, mapped row by row in Plan | pass |
| SC-001…SC-005 | test | the same ten functions | pass |
| the diff itself | inspection | `git diff origin/develop -- static/styles/design/obs-dock.css`: 20 insertions, 1 deletion; three `overflow-wrap: anywhere` declarations (`.serviceline`, `.entryrow__t`, `.screenerow`) and their comments. No picker, transport, find-band or truncator rule touched | checked by inspection |
| the live page | manual | `probe.py --restore` → title spill 328px / body 135px; `probe.py` → 0 / 0, title 3 lines, `overflow-wrap: anywhere` computed. The owner's own click-through on `:8767` remains his to make | checked by inspection |

**Suite at this pass**: `tests.e2e.test_dock_text_wrap` — 10 tests, OK (`gkps203-converge.log`).
**Neighbours**: `test_obs_dock`, `test_obs_dock_follow`, `test_dock_bucket_head`, `test_dock_goto`,
`test_dock_keys` — 66 tests, OK (`gkps203-neighbours.log`).

### Findings

| Type | Finding | Evidence | Action |
| --- | --- | --- | --- |
| — | `missing` — none | every FR/SC row has a passing test or a read diff | — |
| — | `partial` — none | the three declarations cover all three surfaces; no fourth text box in the runner overflows (the probe reads every header, screen line and the title) | — |
| — | `contradicts` — none | the code does what the spec says, including the corrected wide-panel claim | — |
| — | `unrequested` — none | the diff is three declarations; no clamp, no token, no script, no other rule | — |
| note | **The base moved during the slice.** `origin/develop` advanced to `85319b73` (spec 202, PR #539) while this slice waited at gate 2. The branch had no commits, so it was re-pointed at the new develop with the working tree carried across (`git stash -u` → `reset --hard` → `stash pop`, clean). | `git log`, `VERSION` 1.34.1 → 1.34.2 on develop | the bump is re-stamped **1.34.3**, not the 1.34.2 the plan named |
| note | **Card ID collision, renumbered.** Spec 202's merged card is also `ITEM-212` (`ITEM-212-overlay-caption-height-cap.md`). This slice's card was uncommitted, so it renumbered to **ITEM-213** — file renamed, frontmatter and board row re-pointed. Anchor issue **#540 kept** (BRD-10: nothing is ever read back from it), its title still reading ITEM-212. | `git ls-tree -r origin/develop backlog/items/` | recorded here and in the closing report |

### Outcome

**Converged.** Zero gaps of any type; the two notes are delivery facts, not behaviour gaps. The run
proceeds to Fold.
